"""Unit tests for PU-07-runner: Standalone staging rebuild runner and edge revocation manifest.

Contract: Docs/03-contracts/PRODUCT-INTERFACES-V2.md §I06
Packet: Docs/05-delivery/concept-alignment-v2/product-packets/PU-07-runner.md
"""

from __future__ import annotations

import hashlib
import hmac
import importlib.util
import json
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

# Dynamically import rebuild-product.py
RUNNER_PATH = Path(__file__).parent / "rebuild-product.py"
spec = importlib.util.spec_from_file_location("rebuild_product", RUNNER_PATH)
rebuild_product = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rebuild_product)


def write_release_artifacts(target_dir: Path, rev: str):
    """Emit the full A03 pre-swap artifact set into a release directory."""
    (target_dir / "index.html").write_text(f"<h1>{rev}</h1>", encoding="utf-8")
    (target_dir / "sitemap.xml").write_text(
        '<?xml version="1.0"?><urlset></urlset>', encoding="utf-8"
    )
    pagefind_dir = target_dir / "pagefind"
    pagefind_dir.mkdir(parents=True, exist_ok=True)
    (pagefind_dir / "pagefind.js").write_text("// search index", encoding="utf-8")
    return True


class TestRebuildProductRunner(unittest.TestCase):
    """Test suite covering the rebuild runner, machine HMAC auth, edge deny, and rollback."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_runner_"))
        self.releases_dir = self.test_dir / "releases"
        self.releases_dir.mkdir()
        self.current_link = self.test_dir / "current"
        self.manifest_path = self.test_dir / "edge-deny.map"
        self.secret = "test-secret-key-12345"
        self.job_id = "550e8400-e29b-41d4-a716-446655440000"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sign_machine_request(self):
        """Verify HMAC-SHA256 signature algorithm matches contract §I06 specification."""
        method = "POST"
        path = "/api/v1/internal/publication-jobs/123/result"
        timestamp = 1757000000
        nonce = "abc-123-nonce"
        body = b'{"state":"running"}'

        sig = rebuild_product.sign_machine_request(
            self.secret, method, path, timestamp, nonce, body
        )

        body_sha256 = hashlib.sha256(body).hexdigest()
        expected_text = f"{method}\n{path}\n{timestamp}\n{nonce}\n{body_sha256}"
        expected_sig = hmac.new(
            self.secret.encode("utf-8"),
            expected_text.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        self.assertEqual(sig, expected_sig)

    def test_edge_deny_manager_lifecycle(self):
        """Verify EdgeDenyManager adds, normalizes, verifies, and removes paths."""
        mgr = rebuild_product.EdgeDenyManager(self.manifest_path)

        paths = ["/en/blog/archived-post/", "fa/projects/old-project"]
        ok = mgr.apply_revocations(paths)
        self.assertTrue(ok)
        self.assertTrue(mgr.verify_effective(paths))

        content = self.manifest_path.read_text(encoding="utf-8")
        self.assertIn('"/en/blog/archived-post/" 1;', content)
        self.assertIn('"/en/blog/archived-post" 1;', content)
        self.assertIn('"/fa/projects/old-project" 1;', content)
        self.assertIn('"/fa/projects/old-project/" 1;', content)

        # Removal on republish
        mgr.remove_revocations(["/en/blog/archived-post/"])
        content_after = self.manifest_path.read_text(encoding="utf-8")
        self.assertNotIn('"/en/blog/archived-post/" 1;', content_after)
        self.assertIn('"/fa/projects/old-project" 1;', content_after)

    def test_static_site_manager_atomic_swap_and_rollback(self):
        """Verify StaticSiteManager swaps release symlink and rolls back cleanly."""
        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)

        # Create two releases
        def fake_builder(target_dir: Path, rev: str):
            (target_dir / "index.html").write_text(f"<h1>{rev}</h1>", encoding="utf-8")
            return True

        self.assertTrue(mgr.build_site("rev-1", build_fn=fake_builder))
        self.assertTrue(mgr.atomic_swap("rev-1"))
        self.assertEqual(mgr.get_active_revision(), "rev-1")
        self.assertEqual((self.current_link / "index.html").read_text(), "<h1>rev-1</h1>")

        # Swap to rev-2
        self.assertTrue(mgr.build_site("rev-2", build_fn=fake_builder))
        self.assertTrue(mgr.atomic_swap("rev-2"))
        self.assertEqual(mgr.get_active_revision(), "rev-2")
        self.assertEqual((self.current_link / "index.html").read_text(), "<h1>rev-2</h1>")

        # Rollback to rev-1
        self.assertTrue(mgr.rollback("rev-1"))
        self.assertEqual(mgr.get_active_revision(), "rev-1")
        self.assertEqual((self.current_link / "index.html").read_text(), "<h1>rev-1</h1>")

    def test_successful_publish_workflow(self):
        """Exercise full success build flow: queued -> running -> build -> swap -> succeeded."""
        callbacks: list[dict] = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                # Return queued publication job
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "en",
                    "requestedRevision": "rev-20260906-01",
                    "affectedPaths": ["/en/blog/new-post/"],
                    "removalState": "not_requested",
                }
            elif method == "POST":
                data = json.loads(body.decode("utf-8"))
                callbacks.append(data)
                return 200, {"status": "ok"}
            return 404, {}

        def mock_builder(target_dir: Path, rev: str):
            return write_release_artifacts(target_dir, f"Site {rev}")

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=mock_builder,
            http_client=fake_http_client,
        )

        self.assertTrue(ok)
        self.assertEqual(len(callbacks), 2)
        # 1. First callback: state="running"
        self.assertEqual(callbacks[0], {"state": "running"})
        # 2. Second callback: state="succeeded", artifactRevision="rev-20260906-01"
        self.assertEqual(callbacks[1]["state"], "succeeded")
        self.assertEqual(callbacks[1]["artifactRevision"], "rev-20260906-01")

        # Active symlink points to new build
        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)
        self.assertEqual(mgr.get_active_revision(), "rev-20260906-01")

    def test_revoke_before_rebuild_workflow(self):
        """Verify unpublish/archive pushes paths to edge deny manifest before build."""
        callbacks: list[dict] = []
        manifest_checked_during_build = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "fa",
                    "requestedRevision": "rev-archive-01",
                    "affectedPaths": ["/fa/blog/deprecated/"],
                    "removalState": "pending",
                }
            elif method == "POST":
                callbacks.append(json.loads(body.decode("utf-8")))
                return 200, {"status": "ok"}
            return 404, {}

        def mock_builder(target_dir: Path, rev: str):
            # Verify manifest was ALREADY populated when builder runs!
            content = self.manifest_path.read_text(encoding="utf-8")
            manifest_checked_during_build.append("/fa/blog/deprecated/" in content)
            return write_release_artifacts(target_dir, rev)

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=mock_builder,
            http_client=fake_http_client,
        )

        self.assertTrue(ok)
        self.assertTrue(manifest_checked_during_build[0], "Deny manifest must be updated before build")

        # Callback reports removalState="effective"
        final_cb = callbacks[-1]
        self.assertEqual(final_cb["state"], "succeeded")
        self.assertEqual(final_cb["removalState"], "effective")

    def test_edge_deny_failure_aborts_build(self):
        """When edge deny verification fails, build is aborted and EDGE_DENY_FAILED is reported."""
        callbacks: list[dict] = []
        builder_called = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "en",
                    "requestedRevision": "rev-fail-deny",
                    "affectedPaths": ["/en/secret/"],
                    "removalState": "pending",
                }
            elif method == "POST":
                callbacks.append(json.loads(body.decode("utf-8")))
                return 200, {"status": "ok"}
            return 404, {}

        def mock_builder(target_dir: Path, rev: str):
            builder_called.append(True)
            return True

        # Point manifest path to an un-writable path (child of a regular file)
        blocked_file = self.test_dir / "blocked_file"
        blocked_file.write_text("regular file", encoding="utf-8")
        bad_manifest_path = blocked_file / "unwritable.map"

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=bad_manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=mock_builder,
            http_client=fake_http_client,
        )

        self.assertFalse(ok)
        self.assertEqual(len(builder_called), 0, "Build must not execute if edge deny failed")

        final_cb = callbacks[-1]
        self.assertEqual(final_cb["state"], "failed")
        self.assertEqual(final_cb["errorCode"], "EDGE_DENY_FAILED")
        self.assertEqual(final_cb["removalState"], "failed")

    def test_build_failure_and_atomic_rollback(self):
        """When build fails, previous active release is preserved and BUILD_FAILED is reported."""
        # 1. Establish initial active release
        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)
        initial_dir = self.releases_dir / "rev-initial"
        initial_dir.mkdir()
        (initial_dir / "index.html").write_text("Initial Site", encoding="utf-8")
        mgr.atomic_swap("rev-initial")
        self.assertEqual(mgr.get_active_revision(), "rev-initial")

        callbacks: list[dict] = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "en",
                    "requestedRevision": "rev-broken",
                    "affectedPaths": ["/en/blog/broken/"],
                    "removalState": "not_requested",
                }
            elif method == "POST":
                callbacks.append(json.loads(body.decode("utf-8")))
                return 200, {"status": "ok"}
            return 404, {}

        def failing_builder(target_dir: Path, rev: str):
            # Simulates build / Pagefind failure
            return False

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=failing_builder,
            http_client=fake_http_client,
        )

        self.assertFalse(ok)
        final_cb = callbacks[-1]
        self.assertEqual(final_cb["state"], "failed")
        self.assertEqual(final_cb["errorCode"], "BUILD_FAILED")

        # Active revision rolled back / preserved at rev-initial
        self.assertEqual(mgr.get_active_revision(), "rev-initial")
        self.assertEqual((self.current_link / "index.html").read_text(), "Initial Site")

    def test_duplicate_idempotent_callbacks(self):
        """Idempotent callback replays are accepted without crashing the runner."""
        call_count = 0

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            nonlocal call_count
            call_count += 1
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "en",
                    "requestedRevision": "rev-idempotent",
                    "affectedPaths": [],
                    "removalState": "not_requested",
                }
            elif method == "POST":
                # Backend accepts idempotent replay
                return 200, {"status": "idempotent_ok"}
            return 404, {}

        def mock_builder(target_dir: Path, rev: str):
            return write_release_artifacts(target_dir, "Idempotent")

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=mock_builder,
            http_client=fake_http_client,
        )
        self.assertTrue(ok)

    def test_job_revoke_paths_helper_prefers_revoked(self):
        self.assertEqual(
            rebuild_product.job_revoke_paths({
                "affectedPaths": ["/en/", "/en/blog/x/"],
                "revokedPaths": ["/en/blog/x/"],
            }),
            ["/en/blog/x/"],
        )
        self.assertEqual(
            rebuild_product.job_revoke_paths({"affectedPaths": ["/en/blog/y/"]}),
            ["/en/blog/y/"],
        )
        self.assertEqual(rebuild_product.job_revoke_paths({}), [])

    def test_remove_revocations_failure_blocks_success_normal_path(self):
        """REPRO normal: remove_revocations False must prevent succeeded.

        Before fix: return value ignored, runner reported succeeded with
        stale deny entries. Must report failed/REMOVAL_FAILED instead.
        """
        from unittest import mock

        callbacks: list[dict] = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "queued",
                    "locale": "en",
                    "requestedRevision": "rev-remove-fail-normal",
                    "affectedPaths": ["/en/blog/republished-post/"],
                    "revokedPaths": [],
                    "removalState": "not_requested",
                }
            callbacks.append(json.loads(body.decode("utf-8")))
            return 200, {"status": "ok"}

        def mock_builder(target_dir: Path, rev: str):
            return write_release_artifacts(target_dir, rev)

        with mock.patch.object(
            rebuild_product.EdgeDenyManager, "remove_revocations", return_value=False
        ):
            ok = rebuild_product.run_publication_job(
                job_id=self.job_id,
                backend_url="http://cms:8000",
                secret=self.secret,
                manifest_path=self.manifest_path,
                releases_dir=self.releases_dir,
                current_link=self.current_link,
                build_fn=mock_builder,
                http_client=fake_http_client,
            )
        self.assertFalse(ok, "remove failure must not report success")
        final = callbacks[-1]
        self.assertEqual(final["state"], "failed")
        self.assertEqual(final.get("errorCode"), "REMOVAL_FAILED")

    def test_remove_revocations_failure_blocks_success_resume_path(self):
        """REPRO resume: running job with active artifact but failing cleanup.

        Before fix: resume ignored remove_revocations and reported succeeded.
        Must report failed/REMOVAL_FAILED and preserve truthful removal state.
        """
        from unittest import mock

        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)
        seed = self.releases_dir / "rev-resume-remove-fail"
        seed.mkdir()
        write_release_artifacts(seed, "rev-resume-remove-fail")
        mgr.atomic_swap("rev-resume-remove-fail")

        callbacks: list[dict] = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, {
                    "id": self.job_id,
                    "state": "running",
                    "locale": "en",
                    "requestedRevision": "rev-resume-remove-fail",
                    "affectedPaths": ["/en/blog/resumed-post/"],
                    "revokedPaths": [],
                    "removalState": "not_requested",
                }
            callbacks.append(json.loads(body.decode("utf-8")))
            return 200, {"status": "ok"}

        def mock_builder(target_dir: Path, rev: str):  # pragma: no cover
            raise AssertionError("resume must not rebuild")

        with mock.patch.object(
            rebuild_product.EdgeDenyManager, "remove_revocations", return_value=False
        ):
            ok = rebuild_product.run_publication_job(
                job_id=self.job_id,
                backend_url="http://cms:8000",
                secret=self.secret,
                manifest_path=self.manifest_path,
                releases_dir=self.releases_dir,
                current_link=self.current_link,
                build_fn=mock_builder,
                http_client=fake_http_client,
            )
        self.assertFalse(ok, "resume remove failure must not report success")
        final = callbacks[-1]
        self.assertEqual(final["state"], "failed")
        self.assertEqual(final.get("errorCode"), "REMOVAL_FAILED")


class TestRevokeSplitA01(unittest.TestCase):
    """A01: edge deny covers only revokedPaths; shared pages are rebuilt, never denied."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_runner_a01_"))
        self.releases_dir = self.test_dir / "releases"
        self.releases_dir.mkdir()
        self.current_link = self.test_dir / "current"
        self.manifest_path = self.test_dir / "edge-deny.map"
        self.secret = "test-secret-key-12345"
        self.job_id = "550e8400-e29b-41d4-a716-446655440001"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _run_job(self, payload):
        callbacks: list[dict] = []

        def fake_http_client(url, method, secret, body=b"", timeout=30):
            if method == "GET":
                return 200, payload
            callbacks.append(json.loads(body.decode("utf-8")))
            return 200, {"status": "ok"}

        def mock_builder(target_dir: Path, rev: str):
            return write_release_artifacts(target_dir, rev)

        ok = rebuild_product.run_publication_job(
            job_id=self.job_id,
            backend_url="http://cms:8000",
            secret=self.secret,
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=mock_builder,
            http_client=fake_http_client,
        )
        return ok, callbacks

    def test_archive_denies_only_revoked_detail(self):
        """Archive denies the detail URL while home/blog stay reachable."""
        ok, callbacks = self._run_job({
            "id": self.job_id,
            "state": "queued",
            "locale": "en",
            "requestedRevision": "rev-a01-01",
            "affectedPaths": ["/en/", "/en/blog/", "/en/blog/a01-article/"],
            "revokedPaths": ["/en/blog/a01-article/"],
            "removalState": "pending",
        })
        self.assertTrue(ok)
        content = self.manifest_path.read_text(encoding="utf-8")
        self.assertIn('"/en/blog/a01-article/" 1;', content)
        self.assertNotIn('"/en/" 1;', content)
        self.assertNotIn('"/en/blog/" 1;', content)
        self.assertEqual(callbacks[-1]["removalState"], "effective")

    def test_legacy_job_without_revoked_paths_falls_back(self):
        """Pre-A01 payloads without revokedPaths still deny affectedPaths."""
        ok, _ = self._run_job({
            "id": self.job_id,
            "state": "queued",
            "locale": "en",
            "requestedRevision": "rev-a01-legacy",
            "affectedPaths": ["/en/blog/legacy-post/"],
            "removalState": "pending",
        })
        self.assertTrue(ok)
        content = self.manifest_path.read_text(encoding="utf-8")
        self.assertIn('"/en/blog/legacy-post/" 1;', content)

    def test_publish_clears_detail_deny(self):
        """Republish lifts the detail deny via the rebuild set."""
        mgr = rebuild_product.EdgeDenyManager(self.manifest_path)
        self.assertTrue(mgr.apply_revocations(["/en/blog/a01-article/"]))
        ok, _ = self._run_job({
            "id": self.job_id,
            "state": "queued",
            "locale": "en",
            "requestedRevision": "rev-a01-republish",
            "affectedPaths": ["/en/", "/en/blog/", "/en/blog/a01-article/"],
            "revokedPaths": [],
            "removalState": "not_requested",
        })
        self.assertTrue(ok)
        content = self.manifest_path.read_text(encoding="utf-8")
        self.assertNotIn('"/en/blog/a01-article/" 1;', content)


class _ScriptedHttpClient:
    """Fake backend with scripted POST statuses and recorded callbacks."""

    def __init__(self, payload, post_statuses=None):
        self.payload = dict(payload)
        self.posts: list[dict] = []
        self.post_statuses = list(post_statuses or [])

    def __call__(self, url, method, secret, body=b"", timeout=30):
        if method == "GET":
            return 200, dict(self.payload)
        self.posts.append(json.loads(body.decode("utf-8")))
        if self.post_statuses:
            return self.post_statuses.pop(0), {"status": "ok"}
        return 200, {"status": "ok"}


class TestPublicationJobLifecycleA03(unittest.TestCase):
    """A03: exclusive claim, revision discipline, pre-swap checks, recovery."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_runner_a03_"))
        self.releases_dir = self.test_dir / "releases"
        self.releases_dir.mkdir()
        self.current_link = self.test_dir / "current"
        self.manifest_path = self.test_dir / "edge-deny.map"
        self.builder_called: list[bool] = []

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _builder(self, target_dir: Path, rev: str):
        self.builder_called.append(True)
        return write_release_artifacts(target_dir, rev)

    def _run(self, payload, post_statuses=None, **kwargs):
        client = _ScriptedHttpClient(payload, post_statuses)
        ok = rebuild_product.run_publication_job(
            job_id=payload.get("id", "job-a03"),
            backend_url="http://cms:8000",
            secret="test-secret",
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=self._builder,
            http_client=client,
            **kwargs,
        )
        return ok, client

    def _queued(self, **over):
        payload = {
            "id": "job-a03",
            "state": "queued",
            "locale": "en",
            "requestedRevision": "rev-a03-01",
            "affectedPaths": ["/en/blog/a03-post/"],
            "revokedPaths": [],
            "removalState": "not_requested",
        }
        payload.update(over)
        return payload

    def test_claim_rejection_stops_runner_without_build(self):
        """A rejected claim (409) stops the run: no build, no callbacks after."""
        ok, client = self._run(self._queued(), post_statuses=[409])
        self.assertFalse(ok)
        self.assertEqual(self.builder_called, [])
        self.assertEqual(len(client.posts), 1)
        self.assertEqual(client.posts[0], {"state": "running"})
        self.assertFalse(self.current_link.exists())

    def test_empty_revision_fails_closed(self):
        ok, client = self._run(self._queued(requestedRevision=""))
        self.assertFalse(ok)
        self.assertEqual(self.builder_called, [])
        final = client.posts[-1]
        self.assertEqual(final["state"], "failed")
        self.assertEqual(final["errorCode"], "VALIDATION_FAILED")

    def test_path_traversal_revision_fails_closed(self):
        for evil in ("../evil", "a/b", "..", ".", "rev with space"):
            builder_called: list[bool] = []
            client = _ScriptedHttpClient(self._queued(requestedRevision=evil))
            ok = rebuild_product.run_publication_job(
                job_id="job-a03",
                backend_url="http://cms:8000",
                secret="test-secret",
                manifest_path=self.manifest_path,
                releases_dir=self.releases_dir,
                current_link=self.current_link,
                build_fn=lambda t, r: builder_called.append(True) or False,
                http_client=client,
            )
            self.assertFalse(ok, evil)
            self.assertEqual(builder_called, [], evil)
            self.assertEqual(client.posts[-1]["errorCode"], "VALIDATION_FAILED")
        # Nothing escaped the releases root.
        self.assertEqual(
            [p.name for p in self.releases_dir.iterdir()], []
        )

    def test_missing_sitemap_reports_sitemap_failed_and_keeps_active(self):
        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)
        seed = self.releases_dir / "rev-good"
        seed.mkdir()
        write_release_artifacts(seed, "rev-good")
        mgr.atomic_swap("rev-good")

        def no_sitemap_builder(target_dir: Path, rev: str):
            self.builder_called.append(True)
            (target_dir / "index.html").write_text("x", encoding="utf-8")
            pf = target_dir / "pagefind"
            pf.mkdir(parents=True, exist_ok=True)
            (pf / "pagefind.js").write_text("// idx", encoding="utf-8")
            return True

        client = _ScriptedHttpClient(self._queued(requestedRevision="rev-a03-nosmap"))
        ok = rebuild_product.run_publication_job(
            job_id="job-a03",
            backend_url="http://cms:8000",
            secret="test-secret",
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=no_sitemap_builder,
            http_client=client,
        )
        self.assertFalse(ok)
        self.assertEqual(client.posts[-1]["errorCode"], "SITEMAP_FAILED")
        self.assertEqual(mgr.get_active_revision(), "rev-good")

    def test_missing_pagefind_reports_pagefind_failed(self):
        def no_pagefind_builder(target_dir: Path, rev: str):
            (target_dir / "index.html").write_text("x", encoding="utf-8")
            (target_dir / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
            return True

        client = _ScriptedHttpClient(self._queued(requestedRevision="rev-a03-nopf"))
        ok = rebuild_product.run_publication_job(
            job_id="job-a03",
            backend_url="http://cms:8000",
            secret="test-secret",
            manifest_path=self.manifest_path,
            releases_dir=self.releases_dir,
            current_link=self.current_link,
            build_fn=no_pagefind_builder,
            http_client=client,
        )
        self.assertFalse(ok)
        self.assertEqual(client.posts[-1]["errorCode"], "PAGEFIND_FAILED")
        self.assertFalse(self.current_link.exists())

    def test_terminal_job_is_noop_success(self):
        ok, client = self._run(self._queued(state="succeeded"))
        self.assertTrue(ok)
        self.assertEqual(client.posts, [])
        self.assertEqual(self.builder_called, [])

    def test_resume_after_worker_cut_recompletes(self):
        """Running job whose artifact is already active resumes without rebuild."""
        mgr = rebuild_product.StaticSiteManager(self.releases_dir, self.current_link)
        seed = self.releases_dir / "rev-a03-resume"
        seed.mkdir()
        write_release_artifacts(seed, "rev-a03-resume")
        mgr.atomic_swap("rev-a03-resume")

        payload = self._queued(
            state="running",
            requestedRevision="rev-a03-resume",
            revokedPaths=["/en/blog/a03-post/"],
            removalState="pending",
        )
        ok, client = self._run(payload)
        self.assertTrue(ok)
        self.assertEqual(self.builder_called, [])
        final = client.posts[-1]
        self.assertEqual(final["state"], "succeeded")
        self.assertEqual(final["artifactRevision"], "rev-a03-resume")
        self.assertEqual(final["removalState"], "effective")
        content = self.manifest_path.read_text(encoding="utf-8")
        self.assertIn('"/en/blog/a03-post/" 1;', content)

    def test_running_held_elsewhere_stops(self):
        ok, client = self._run(
            self._queued(state="running", requestedRevision="rev-a03-other")
        )
        self.assertFalse(ok)
        self.assertEqual(client.posts, [])
        self.assertEqual(self.builder_called, [])


class _ManifestEdgeHandler(BaseHTTPRequestHandler):
    """Isolated fake ingress: 404s exactly the manifest's denied paths.

    With ``live_reload`` it re-reads the manifest file per request (an edge
    that picked up the config); frozen it serves a stale snapshot (an edge
    that never reloaded) — the audit's failing scenario.
    """

    manifest_path = None
    live_reload = True
    frozen_denied = frozenset()

    def _denied(self):
        if type(self).live_reload:
            return rebuild_product.EdgeDenyManager(
                type(self).manifest_path
            ).load_denied_paths()
        return type(self).frozen_denied

    def do_GET(self):
        path = urlparse(self.path).path
        if path in self._denied():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


class TestEdgeEffectVerificationA02(unittest.TestCase):
    """A02: file presence never proves effect; staged apply + HTTP probe do."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_edge_a02_"))
        self.manifest_path = self.test_dir / "edge-deny.map"
        _ManifestEdgeHandler.manifest_path = self.manifest_path
        _ManifestEdgeHandler.live_reload = True
        _ManifestEdgeHandler.frozen_denied = frozenset()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _ManifestEdgeHandler)
        self.base_url = (
            f"http://127.0.0.1:{self.server.server_address[1]}"
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join(timeout=10)
        self.server.server_close()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _manager(self, **over):
        kwargs = {"probe_base_url": self.base_url, "probe_timeout": 5}
        kwargs.update(over)
        return rebuild_product.EdgeDenyManager(self.manifest_path, **kwargs)

    def test_full_chain_file_to_http_effect(self):
        """Live edge: written manifest drives real HTTP 404s; apply is True."""
        mgr = self._manager()
        self.assertTrue(mgr.apply_revocations(["/en/blog/a02-post/"]))
        self.assertTrue(mgr.probe_paths_blocked(["/en/blog/a02-post/"]))

    def test_stale_edge_fails_closed(self):
        """File present + edge unchanged => NOT effective (audit scenario)."""
        _ManifestEdgeHandler.live_reload = False
        _ManifestEdgeHandler.frozen_denied = frozenset()
        mgr = self._manager()
        self.assertFalse(mgr.apply_revocations(["/en/blog/a02-stale/"]))
        # The file DOES contain the path — proving file text is not effect.
        self.assertTrue(mgr.verify_effective(["/en/blog/a02-stale/"]))
        self.assertFalse(mgr.probe_paths_blocked(["/en/blog/a02-stale/"]))

    def test_reload_failure_fails_closed(self):
        """Configured reload that fails blocks the effective report."""
        mgr = self._manager(
            reload_cmd=[sys.executable, "-c", "import sys; sys.exit(1)"]
        )
        self.assertFalse(mgr.apply_revocations(["/en/blog/a02-noreload/"]))
        self.assertTrue(mgr.verify_effective(["/en/blog/a02-noreload/"]))

    def test_validate_failure_skips_reload(self):
        marker = self.test_dir / "reloaded.marker"
        mgr = self._manager(
            validate_cmd=[sys.executable, "-c", "import sys; sys.exit(3)"],
            reload_cmd=[
                sys.executable,
                "-c",
                f"import pathlib; pathlib.Path({str(marker)!r}).write_text('x')",
            ],
        )
        self.assertFalse(mgr.apply_configuration())
        self.assertFalse(marker.exists())

    def test_validate_and_reload_success(self):
        mgr = self._manager(
            validate_cmd=[sys.executable, "-c", "pass"],
            reload_cmd=[sys.executable, "-c", "pass"],
        )
        self.assertTrue(mgr.apply_revocations(["/en/blog/a02-ok/"]))

    def test_unreachable_probe_fails_closed(self):
        mgr = self._manager(probe_base_url="http://127.0.0.1:1")
        self.assertFalse(mgr.apply_revocations(["/en/blog/a02-down/"]))
        self.assertTrue(mgr.verify_effective(["/en/blog/a02-down/"]))

    def test_remove_revocation_unblocks(self):
        mgr = self._manager()
        self.assertTrue(mgr.apply_revocations(["/en/blog/a02-temp/"]))
        self.assertTrue(mgr.remove_revocations(["/en/blog/a02-temp/"]))
        self.assertFalse(mgr.probe_paths_blocked(["/en/blog/a02-temp/"]))


if __name__ == "__main__":
    unittest.main()
