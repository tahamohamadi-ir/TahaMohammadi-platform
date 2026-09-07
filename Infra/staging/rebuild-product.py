#!/usr/bin/env python3
"""Standalone product rebuild runner (§I06).

Contract: Docs/03-contracts/PRODUCT-INTERFACES-V2.md §I06
Packet: Docs/05-delivery/concept-alignment-v2/product-packets/PU-07-runner.md

Responsibilities:
- Authenticates internal API calls via HMAC-SHA256 headers:
  X-Publication-Timestamp, X-Publication-Nonce, X-Publication-Signature.
- Reads publication job details from GET /api/v1/internal/publication-jobs/<job_id>.
- Transitions job to "running".
- Pushes affected paths to edge-deny manifest BEFORE rebuild for unpublish/archive,
  and independently verifies edge-deny effectiveness before proceeding.
- Builds static site into revisioned directory under releases/.
- Atomically swaps the active release symlink to point to the new build.
- On build or swap failure, retains the last successful active release (rollback).
- Submits final result callback to POST /api/v1/internal/publication-jobs/<job_id>/result.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_TIMEOUT = 300
SAFE_ERROR_CODES = {
    "BUILD_FAILED",
    "PAGEFIND_FAILED",
    "SITEMAP_FAILED",
    "EDGE_DENY_FAILED",
    "REMOVAL_FAILED",
    "TIMEOUT",
    "VALIDATION_FAILED",
}

TERMINAL_JOB_STATES = {"succeeded", "failed"}

# A03: every release directory name must be a plain opaque revision token —
# never empty, never a path. The release target is additionally contained
# inside the configured releases root before anything is written.
REVISION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,128}\Z")

# A03: pre-swap contract checks. The deployed release must contain the site
# entry point, the sitemap and the Pagefind search index — index.html alone
# never proves a successful deployment.
REQUIRED_RELEASE_ARTIFACTS = ("index.html", "sitemap.xml", "pagefind/pagefind.js")


def is_valid_revision(revision: str) -> bool:
    """Return True for a non-empty opaque revision token without path parts."""
    if not revision or not isinstance(revision, str):
        return False
    if "/" in revision or "\\" in revision or revision in (".", ".."):
        return False
    return REVISION_RE.match(revision) is not None


def release_target_for_revision(releases_dir: Path, revision: str) -> Path | None:
    """Resolve releases/<revision>, contained inside releases_dir, or None."""
    if not is_valid_revision(revision):
        return None
    try:
        root = Path(releases_dir).resolve()
        target = (root / revision).resolve()
    except Exception:
        return None
    try:
        if target != root and root in target.parents:
            return target
    except Exception:
        return None
    return None


def verify_release_artifacts(
    release_target: Path,
    require_artifacts: tuple[str, ...] = REQUIRED_RELEASE_ARTIFACTS,
) -> tuple[bool, str | None]:
    """Check required deploy artifacts; map the first gap to a safe error code."""
    missing = [
        name
        for name in require_artifacts
        if not (Path(release_target) / name).is_file()
    ]
    if not missing:
        return True, None
    if any(name == "sitemap.xml" or name.endswith("/sitemap.xml") for name in missing):
        return False, "SITEMAP_FAILED"
    if any(name == "pagefind" or name.startswith("pagefind/") for name in missing):
        return False, "PAGEFIND_FAILED"
    return False, "BUILD_FAILED"


def sign_machine_request(
    secret: str,
    method: str,
    path: str,
    timestamp: int,
    nonce: str,
    body_bytes: bytes,
) -> str:
    """Compute hex HMAC-SHA256 signature for machine runner requests (§I06).

    Signed text joins uppercase method, path, timestamp, nonce, and hex SHA-256
    digest of exact body bytes with newline separators.
    """
    body_sha256 = hashlib.sha256(body_bytes).hexdigest()
    signed_text = f"{method.upper()}\n{path}\n{timestamp}\n{nonce}\n{body_sha256}"
    return hmac.new(secret.encode("utf-8"), signed_text.encode("utf-8"), hashlib.sha256).hexdigest()


def make_authenticated_request(
    url: str,
    method: str,
    secret: str,
    body: bytes = b"",
    timeout: int = 30,
) -> tuple[int, dict]:
    """Perform HTTP request carrying machine authentication headers."""
    parsed = urlparse(url)
    path = parsed.path
    if parsed.query:
        path = f"{path}?{parsed.query}"

    timestamp = int(time.time())
    nonce = uuid.uuid4().hex
    signature = sign_machine_request(secret, method, path, timestamp, nonce, body)

    headers = {
        "X-Publication-Timestamp": str(timestamp),
        "X-Publication-Nonce": nonce,
        "X-Publication-Signature": signature,
        "Accept": "application/json",
    }
    if body:
        headers["Content-Type"] = "application/json"

    req = Request(url, data=body if body else None, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            data = resp.read()
            return status_code, json.loads(data.decode("utf-8")) if data else {}
    except HTTPError as e:
        status_code = e.code
        err_data = e.read()
        try:
            parsed_err = json.loads(err_data.decode("utf-8")) if err_data else {}
        except Exception:
            parsed_err = {"error": err_data.decode("utf-8", errors="replace")}
        return status_code, parsed_err


class EdgeDenyManager:
    """Manages the edge deny manifest for immediate path revocation (§I06).

    A02: writing the file, applying the edge configuration and verifying the
    HTTP effect are three separate stages. ``apply_revocations`` runs all
    configured stages and is fail-closed: any stage failure means the paths
    are NOT reported effective.
    """

    def __init__(
        self,
        manifest_path: Path,
        *,
        reload_cmd=None,
        validate_cmd=None,
        probe_base_url: str | None = None,
        probe_timeout: int = 5,
    ):
        self.manifest_path = Path(manifest_path)
        self.reload_cmd = reload_cmd
        self.validate_cmd = validate_cmd
        self.probe_base_url = (probe_base_url or "").rstrip("/") or None
        self.probe_timeout = probe_timeout

    def load_denied_paths(self) -> set[str]:
        """Read existing denied paths from manifest if it exists."""
        if not self.manifest_path.is_file():
            return set()
        paths = set()
        for line in self.manifest_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts and parts[-1].rstrip(";") == "1":
                paths.add(parts[0].strip('"').strip("'"))
        return paths

    @staticmethod
    def _normalize_variants(path: str) -> list[str]:
        """Return the path plus its trailing-slash twin (edge matches $uri)."""
        p = "/" + path.strip().lstrip("/")
        if p.endswith("/"):
            return [p, p.rstrip("/") or "/"]
        return [p, p + "/"]

    def write_manifest(self, paths: list[str]) -> bool:
        """Stage 1: merge paths into the deny manifest file (atomic replace)."""
        if not paths:
            return True
        try:
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
            denied = self.load_denied_paths()

            for path in paths:
                for variant in self._normalize_variants(path):
                    denied.add(variant)

            lines = [
                "# Edge deny manifest generated by rebuild-product.py (§I06)",
                "# Maps denied URI paths directly to 404 at edge ingress.",
            ]
            for p in sorted(denied):
                lines.append(f'"{p}" 1;')

            content = "\n".join(lines) + "\n"

            temp_file = self.manifest_path.with_suffix(f".tmp_{uuid.uuid4().hex}")
            temp_file.write_text(content, encoding="utf-8")
            os.replace(temp_file, self.manifest_path)
            return True
        except Exception:
            return False

    def apply_revocations(self, paths: list[str]) -> bool:
        """Push revoked paths and confirm effectiveness (fail-closed).

        Stages: write manifest file → verify file contents → apply edge
        configuration (validate + reload, when configured) → probe the HTTP
        effect at the ingress (when configured). The first failing stage
        aborts with False; True requires every configured stage to pass.
        """
        if not paths:
            return True
        if not self.write_manifest(paths):
            return False
        if not self.verify_effective(paths):
            return False
        if not self.apply_configuration():
            return False
        if not self.probe_paths_blocked(paths):
            return False
        return True

    def remove_revocations(self, restored_paths: list[str]) -> bool:
        """Remove paths from edge deny manifest (e.g. upon republish)."""
        if not self.manifest_path.is_file() or not restored_paths:
            return True

        try:
            denied = self.load_denied_paths()
            for path in restored_paths:
                p = "/" + path.strip().lstrip("/")
                denied.discard(p)
                denied.discard(p.rstrip("/"))
                denied.discard(p.rstrip("/") + "/")

            lines = [
                "# Edge deny manifest generated by rebuild-product.py (§I06)",
                "# Maps denied URI paths directly to 404 at edge ingress.",
            ]
            for p in sorted(denied):
                lines.append(f'"{p}" 1;')

            content = "\n".join(lines) + "\n"
            temp_file = self.manifest_path.with_suffix(f".tmp_{uuid.uuid4().hex}")
            temp_file.write_text(content, encoding="utf-8")
            os.replace(temp_file, self.manifest_path)
            return True
        except Exception:
            return False

    def verify_effective(self, paths: list[str]) -> bool:
        """Stage 2: verify the manifest file itself lists every path.

        This proves the file was written — never that the edge serves 404.
        Only :meth:`probe_paths_blocked` proves the HTTP effect.
        """
        try:
            if not self.manifest_path.is_file():
                return False

            content = self.manifest_path.read_text(encoding="utf-8")
            for path in paths:
                p = "/" + path.strip().lstrip("/")
                if f'"{p}" 1;' not in content and f'"{p.rstrip("/")}" 1;' not in content:
                    return False
            return True
        except Exception:
            return False

    @staticmethod
    def _run_cmd(cmd) -> bool:
        """Run a configured shell argv; an empty command is a no-op success."""
        if not cmd:
            return True
        argv = shlex.split(cmd) if isinstance(cmd, str) else [str(c) for c in cmd]
        if not argv:
            return True
        try:
            completed = subprocess.run(argv, capture_output=True, timeout=60)
            return completed.returncode == 0
        except Exception:
            return False

    def apply_configuration(self) -> bool:
        """Stage 3: validate then reload the edge configuration (when set).

        Unconfigured environments skip this stage (True). Any configured
        command failure is fail-closed (False): the revocation must not be
        reported effective when the edge may not have picked it up.
        """
        if not self._run_cmd(self.validate_cmd):
            return False
        if not self._run_cmd(self.reload_cmd):
            return False
        return True

    def _probe_single_path(self, url: str) -> bool:
        """Return True only when the ingress answers exactly 404 for url."""
        try:
            with urlopen(url, timeout=self.probe_timeout) as resp:
                return resp.getcode() == 404
        except HTTPError as e:
            return e.code == 404
        except (URLError, OSError, ValueError):
            return False

    def probe_paths_blocked(self, paths: list[str]) -> bool:
        """Stage 4: probe the real ingress HTTP effect (when configured).

        GETs every revoked path (plus its slash twin) against
        ``probe_base_url`` and requires 404 for each. Unconfigured
        environments skip this stage (True); any non-404, redirect sink,
        timeout or connection error fails closed (False).
        """
        if not paths:
            return True
        if not self.probe_base_url:
            return True
        for path in paths:
            for variant in self._normalize_variants(path):
                if not self._probe_single_path(f"{self.probe_base_url}{variant}"):
                    return False
        return True


class StaticSiteManager:
    """Manages revisioned release directories and atomic active symlink swapping."""

    def __init__(self, releases_dir: Path, current_link: Path, site_source_dir: Path | None = None):
        self.releases_dir = Path(releases_dir)
        self.current_link = Path(current_link)
        self.site_source_dir = Path(site_source_dir) if site_source_dir else None

    def get_active_revision(self) -> str | None:
        """Return the revision name currently pointed to by current_link, if any."""
        rev_marker = self.current_link / ".revision"
        if rev_marker.is_file():
            try:
                val = rev_marker.read_text(encoding="utf-8").strip()
                if val:
                    return val
            except Exception:
                pass

        side_marker = self.current_link.parent / ".current_revision"
        if side_marker.is_file():
            try:
                val = side_marker.read_text(encoding="utf-8").strip()
                if val:
                    return val
            except Exception:
                pass

        if self.current_link.is_symlink():
            try:
                target = self.current_link.resolve()
                return target.name
            except Exception:
                pass

        return None

    def build_site(
        self,
        revision: str,
        build_fn: callable | None = None,
        build_cmd: list[str] | None = None,
    ) -> bool:
        """Generate static site into releases/<revision> directory."""
        release_target = self.releases_dir / revision
        release_target.mkdir(parents=True, exist_ok=True)

        if build_fn is not None:
            try:
                return bool(build_fn(release_target, revision))
            except Exception:
                return False

        if build_cmd is not None:
            cmd = build_cmd
        else:
            cmd = ["npm", "run", "build"]

        cwd = self.site_source_dir if self.site_source_dir and self.site_source_dir.is_dir() else None
        try:
            res = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
                timeout=DEFAULT_TIMEOUT,
            )
            if res.returncode != 0:
                return False
        except Exception:
            return False

        # In production build, copy dist files to target release dir if needed
        if cwd and (cwd / "dist").is_dir():
            dist_dir = cwd / "dist"
            for item in dist_dir.iterdir():
                dest = release_target / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)

        return (release_target / "index.html").exists()

    def atomic_swap(self, revision: str) -> bool:
        """Atomically point current_link to releases/<revision>."""
        target_dir = (self.releases_dir / revision).resolve()
        if not target_dir.is_dir():
            return False

        try:
            (target_dir / ".revision").write_text(revision, encoding="utf-8")
        except Exception:
            pass

        self.current_link.parent.mkdir(parents=True, exist_ok=True)
        try:
            (self.current_link.parent / ".current_revision").write_text(revision, encoding="utf-8")
        except Exception:
            pass

        # On Windows or systems where symlinks may require privileges:
        # If symlink creation fails, use atomic directory rename/replace
        temp_link = self.current_link.parent / f".tmp_{uuid.uuid4().hex}"
        try:
            os.symlink(str(target_dir), str(temp_link), target_is_directory=True)
            os.replace(str(temp_link), str(self.current_link))
            return True
        except (OSError, NotImplementedError):
            # Fallback for Windows developer environments without symlink privileges:
            # Atomic directory copy/swap
            if temp_link.exists():
                if temp_link.is_dir() and not temp_link.is_symlink():
                    shutil.rmtree(temp_link)
                else:
                    temp_link.unlink()

            shutil.copytree(str(target_dir), str(temp_link), dirs_exist_ok=True)
            if self.current_link.exists():
                backup = self.current_link.parent / f".bak_{uuid.uuid4().hex}"
                os.replace(str(self.current_link), str(backup))
                os.replace(str(temp_link), str(self.current_link))
                if backup.is_dir() and not backup.is_symlink():
                    shutil.rmtree(backup)
                elif backup.exists():
                    backup.unlink()
            else:
                os.replace(str(temp_link), str(self.current_link))
            return True

    def rollback(self, previous_revision: str) -> bool:
        """Roll back current_link to previous_revision."""
        if not previous_revision:
            return False
        return self.atomic_swap(previous_revision)


def job_revoke_paths(job: dict) -> list[str]:
    """Return the edge-deny set for a job payload (A01, §I06).

    New payloads carry ``revokedPaths`` (own detail/file URLs only, never
    shared pages). Payloads enqueued before A01 lack the key and fall back to
    ``affectedPaths`` so legacy removals are still enforced.
    """
    affected = job.get("affectedPaths") or []
    if "revokedPaths" not in job or job.get("revokedPaths") is None:
        return list(affected)
    return list(job.get("revokedPaths") or [])


def run_publication_job(
    job_id: str,
    backend_url: str,
    secret: str,
    manifest_path: Path,
    releases_dir: Path,
    current_link: Path,
    site_source_dir: Path | None = None,
    build_fn: callable | None = None,
    http_client: callable = make_authenticated_request,
    require_artifacts: tuple[str, ...] = REQUIRED_RELEASE_ARTIFACTS,
    edge_reload_cmd=None,
    edge_validate_cmd=None,
    edge_probe_base_url: str | None = None,
    edge_probe_timeout: int = 5,
) -> bool:
    """Execute publication job lifecycle and return True on success (§I06).

    A03 guarantees:
    - Terminal jobs are a no-op success (never rebuilt, never re-reported).
    - The running claim is exclusive: a rejected claim stops the runner
      immediately — no build, no swap, no further callbacks.
    - A job left ``running`` whose artifact is already active is resumed
      (deny state re-verified, completion re-reported) instead of rebuilt,
      covering the worker-cut-after-swap case. Any other ``running`` job is
      left to its holder; recovery is a fresh admin retry job.
    - Empty/forged revisions and releases escaping the releases root fail
      closed with VALIDATION_FAILED before anything is written.
    - Swap requires the full artifact set (site, sitemap, Pagefind); gaps
      report PAGEFIND_FAILED/SITEMAP_FAILED/BUILD_FAILED and keep the last
      successful release active.
    """
    base_url = backend_url.rstrip("/")
    detail_url = f"{base_url}/api/v1/internal/publication-jobs/{job_id}"
    result_url = f"{base_url}/api/v1/internal/publication-jobs/{job_id}/result"

    edge_mgr = EdgeDenyManager(
        manifest_path,
        reload_cmd=edge_reload_cmd,
        validate_cmd=edge_validate_cmd,
        probe_base_url=edge_probe_base_url,
        probe_timeout=edge_probe_timeout,
    )
    site_mgr = StaticSiteManager(releases_dir, current_link, site_source_dir)

    def post_result(payload: dict) -> tuple[int, dict]:
        body = json.dumps(payload).encode("utf-8")
        return http_client(result_url, "POST", secret, body=body)

    def fail(error_code: str, removal_state: str | None = None) -> bool:
        payload = {"state": "failed", "errorCode": error_code}
        if removal_state:
            payload["removalState"] = removal_state
        post_result(payload)
        return False

    # 1. Fetch job payload
    status, job = http_client(detail_url, "GET", secret)
    if status != 200 or not job:
        return False

    fetched_state = job.get("state")
    if fetched_state in TERMINAL_JOB_STATES:
        # Already decided: never rebuild or re-report a terminal job.
        return True
    if fetched_state not in ("queued", "running"):
        return False

    requested_revision = job.get("requestedRevision") or ""
    removal_state = job.get("removalState") or "not_requested"
    affected_paths = job.get("affectedPaths") or []
    # A01: deny only the revoked detail/file URLs, never shared rebuild pages.
    revoke_paths = job_revoke_paths(job)

    # 2. Resume a worker-cut-after-swap job: the artifact is already active,
    # so re-verify the deny state and re-report completion without rebuilding.
    if fetched_state == "running":
        active_revision = site_mgr.get_active_revision()
        if active_revision and active_revision == requested_revision:
            if removal_state == "pending":
                if not edge_mgr.verify_effective(revoke_paths):
                    if not edge_mgr.apply_revocations(revoke_paths):
                        return fail("EDGE_DENY_FAILED", "failed")
                success_payload = {
                    "state": "succeeded",
                    "artifactRevision": requested_revision,
                    "removalState": "effective",
                }
            else:
                if revoke_paths or affected_paths:
                    if not edge_mgr.remove_revocations(
                        revoke_paths if revoke_paths else affected_paths
                    ):
                        return fail("REMOVAL_FAILED")
                success_payload = {
                    "state": "succeeded",
                    "artifactRevision": requested_revision,
                }
            status, _ = post_result(success_payload)
            return status in (200, 201)
        # Another worker holds this job (or it died mid-build): stop.
        # Recovery is a fresh admin retry job, never a concurrent build.
        return False

    # 3. Exclusive claim: queued -> running. Any rejection stops the runner.
    status, _ = post_result({"state": "running"})
    if status not in (200, 201):
        return False

    # 4. Revision and release-path validation before anything is written.
    release_target = release_target_for_revision(releases_dir, requested_revision)
    if release_target is None:
        return fail("VALIDATION_FAILED")

    # 5. Revoke before rebuild (§I06). A01: only revokedPaths enter the deny
    # manifest; shared pages in affectedPaths are rebuilt, never denied.
    if removal_state == "pending":
        deny_ok = edge_mgr.apply_revocations(revoke_paths)
        if not deny_ok:
            return fail("EDGE_DENY_FAILED", "failed")

    # 6. Record previous revision for rollback
    previous_revision = site_mgr.get_active_revision()

    # 7. Build static site
    build_ok = site_mgr.build_site(requested_revision, build_fn=build_fn)
    if not build_ok:
        if previous_revision:
            site_mgr.rollback(previous_revision)
        return fail("BUILD_FAILED")

    # 8. Pre-swap artifact verification (site entry + sitemap + Pagefind).
    artifacts_ok, artifact_error = verify_release_artifacts(
        release_target, require_artifacts
    )
    if not artifacts_ok:
        if previous_revision:
            site_mgr.rollback(previous_revision)
        return fail(artifact_error or "BUILD_FAILED")

    # 9. Atomic swap
    swap_ok = site_mgr.atomic_swap(requested_revision)
    if not swap_ok:
        if previous_revision:
            site_mgr.rollback(previous_revision)
        return fail("BUILD_FAILED")

    # If this was a publish/restore, clear the deny entries for the restored
    # URLs. Publish jobs carry an empty revokedPaths, so fall back to the
    # rebuild set (which still contains the detail URL) to lift older denies.
    # Fail-closed: a failed cleanup must not report succeeded with stale denies.
    if removal_state == "not_requested" and affected_paths:
        if not edge_mgr.remove_revocations(
            revoke_paths if revoke_paths else affected_paths
        ):
            return fail("REMOVAL_FAILED")

    # 10. Notify completion
    success_payload = {
        "state": "succeeded",
        "artifactRevision": requested_revision,
    }
    if removal_state == "pending":
        success_payload["removalState"] = "effective"

    status, _ = post_result(success_payload)
    return status in (200, 201)


def main():
    parser = argparse.ArgumentParser(description="Standalone product rebuild runner (§I06)")
    parser.add_argument("job_id", help="UUID of the publication job to process")
    parser.add_argument("--backend-url", default=os.environ.get("BACKEND_INTERNAL_URL", "http://cms:8000"))
    parser.add_argument("--secret", default=os.environ.get("PUBLICATION_MACHINE_SECRET", ""))
    parser.add_argument(
        "--manifest-path",
        default=os.environ.get("EDGE_DENY_MANIFEST_PATH", "/etc/nginx/conf.d/edge-deny.map"),
    )
    parser.add_argument(
        "--releases-dir",
        default=os.environ.get("RELEASES_DIR", "/var/www/releases"),
    )
    parser.add_argument(
        "--current-link",
        default=os.environ.get("CURRENT_LINK", "/usr/share/nginx/html"),
    )
    parser.add_argument(
        "--source-dir",
        default=os.environ.get("PUBLIC_SITE_SOURCE_DIR", ""),
    )
    parser.add_argument(
        "--require-artifacts",
        default=os.environ.get(
            "REQUIRED_RELEASE_ARTIFACTS", ",".join(REQUIRED_RELEASE_ARTIFACTS)
        ),
        help="Comma-separated release-relative artifacts required before swap.",
    )
    parser.add_argument(
        "--edge-validate-cmd",
        default=os.environ.get("EDGE_VALIDATE_CMD", ""),
        help="Edge config validation command (e.g. 'nginx -t'); empty skips.",
    )
    parser.add_argument(
        "--edge-reload-cmd",
        default=os.environ.get("EDGE_RELOAD_CMD", ""),
        help="Edge config reload command (e.g. 'nginx -s reload'); empty skips.",
    )
    parser.add_argument(
        "--edge-probe-base-url",
        default=os.environ.get("EDGE_PROBE_BASE_URL", ""),
        help="Ingress base URL for the HTTP 404 effect probe; empty skips.",
    )
    parser.add_argument(
        "--edge-probe-timeout",
        type=int,
        default=int(os.environ.get("EDGE_PROBE_TIMEOUT", "5")),
        help="Per-path probe timeout in seconds.",
    )

    args = parser.parse_args()

    if not args.secret:
        print("Error: PUBLICATION_MACHINE_SECRET must be provided via argument or environment", file=sys.stderr)
        sys.exit(1)

    ok = run_publication_job(
        job_id=args.job_id,
        backend_url=args.backend_url,
        secret=args.secret,
        manifest_path=Path(args.manifest_path),
        releases_dir=Path(args.releases_dir),
        current_link=Path(args.current_link),
        site_source_dir=Path(args.source_dir) if args.source_dir else None,
        require_artifacts=tuple(
            part.strip()
            for part in str(args.require_artifacts).split(",")
            if part.strip()
        )
        or REQUIRED_RELEASE_ARTIFACTS,
        edge_reload_cmd=args.edge_reload_cmd or None,
        edge_validate_cmd=args.edge_validate_cmd or None,
        edge_probe_base_url=args.edge_probe_base_url or None,
        edge_probe_timeout=args.edge_probe_timeout,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
