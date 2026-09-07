# Product Publishing and Rebuild Runbook

**Contract**: `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06  
**Delivery**: `PU-07-runner` (Standalone Staging Topology)  
**Target Environment**: Staging (`staging.tahamohamadi.ir`) and Production  

---

## 1. Overview and Architecture

The platform uses an asynchronous, state-machine-backed publication and rebuild system:

```
+-------------------------------------------------------------------------+
|                               Back-End (Django)                         |
|  - Creates PublicationJob rows on publish/archive/schedule/graph/site   |
|  - Tracks state: queued -> running -> succeeded / failed                |
|  - Exposes admin inspection & idempotent retry endpoints                 |
|  - Exposes private authenticated machine callback endpoints              |
+------------------------------------+------------------------------------+
                                     |
                                     | Machine HMAC Auth
                                     v
+------------------------------------+------------------------------------+
|                         rebuild-product.py Runner                       |
|  - Reads job payload via GET /api/v1/internal/publication-jobs/{id}     |
|  - Transitions job to 'running'                                         |
|  - Revoke-Before-Rebuild: updates edge-deny manifest immediately         |
|  - Generates static site release (releases/<revision>)                  |
|  - Atomically swaps active symlink (current -> releases/<revision>)     |
|  - Reports success/failure via POST .../result                          |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                     Edge Ingress (Caddy + Nginx)                        |
|  - Caddy: Blocks public edge access to /api/v1/internal/* (returns 404) |
|  - Nginx: Checks edge-deny.map; returns 404 for revoked paths           |
|  - Nginx: Serves active release static assets from /usr/share/nginx/html|
+-------------------------------------------------------------------------+
```

---

## 2. Machine Authentication & Security Boundary

Internal publication job endpoints (`/api/v1/internal/publication-jobs/*`) are strictly isolated from anonymous public edge traffic:

1. **Edge Protection**: `Caddyfile.staging.fragment` explicitly intercepts `/api/v1/internal/*` requests at edge ingress and answers `404 Not Found`.
2. **Internal Network**: The build runner connects directly over the internal Docker network (`stage_internal`) to `http://cms:8000`.
3. **HMAC-SHA256 Request Signing**:
   - `X-Publication-Timestamp`: Integer Unix epoch seconds. Must be within 300 seconds of current server time (`abs(now - ts) <= 300`).
   - `X-Publication-Nonce`: Unique UUID string. Recorded in database; duplicates are rejected constant-time to prevent replay attacks.
   - `X-Publication-Signature`: Hex digest of HMAC-SHA256 calculated over:
     ```
     <METHOD>\n<PATH>\n<TIMESTAMP>\n<NONCE>\n<SHA256_OF_EXACT_BODY_BYTES>
     ```
   - Shared Secret: Configured via `PUBLICATION_MACHINE_SECRET` (fallback to `REBUILD_TRIGGER_SECRET`). Fails closed if missing or empty.

---

## 3. Publication Job Lifecycle

### Trigger Events
A `PublicationJob` row is created in the database by the request transaction and the
build dispatch fires only **after transaction commit**, carrying the job UUID
(`enqueue_publication_job`, A03). A rolled-back transaction dispatches nothing.
Dispatch prefers the standalone runner command configured in
`PUBLICATION_RUNNER_ARGV` (job UUID appended); with an empty argv and
`REBUILD_TRIGGER_ENABLED=false` (staging default) the job stays queued for an
explicit operator invocation (see below) — no background build is implied.

Enqueue events:
- Content publish or bulk publish.
- Content unpublish / archive or bulk archive.
- Scheduled content transitions executed by `publish_scheduled_content`.
- Knowledge Graph version activation (`apps/api/admin_graph.py`).
- Localized site settings publication (`apps/api/admin_siteconfig.py`).
- Home module composition updates (`apps/api/admin_home.py`).
- Admin retry of a job (enqueues a fresh job; the failed job is kept as evidence).

Restore-as-draft explicitly enqueues **no** job: the published snapshot keeps
serving, so there is nothing to rebuild or revoke (A04).

### Claim Discipline (A03)
- `queued → running` is an exclusive atomic claim. The first runner wins (200);
  any concurrent/second claim gets 409 and the losing runner **stops
  immediately** — no build, no swap, no further callbacks.
- Terminal results require the claim: `queued → succeeded/failed` is rejected
  with 409. Repeated identical terminal callbacks stay idempotent (200);
  conflicting terminal transitions return 409.
- `succeeded` requires a non-empty `artifactRevision` equal to the job's
  `requestedRevision` (every job carries a server-issued opaque revision when
  the caller passes none). `removalState: effective|failed` is accepted only
  for jobs whose removal is `pending`.
- Recovery after a worker cut: if a job is `running` but its artifact is
  already active, the next runner run **resumes** (re-verifies deny state,
  re-reports completion) instead of rebuilding. Any other orphaned `running`
  job is left to its holder — recover via admin retry (fresh job), never by
  running two builders concurrently.

### Job Wire Shape
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "queued",
  "locale": "en",
  "requestedRevision": "rev-20260906-01",
  "deployedRevision": null,
  "affectedPaths": ["/en/", "/en/blog/", "/en/blog/quantum-computing/"],
  "revokedPaths": ["/en/blog/quantum-computing/"],
  "removalState": "pending",
  "errorCode": null,
  "createdAt": "2026-09-06T00:00:00Z",
  "startedAt": null,
  "finishedAt": null,
  "updatedAt": "2026-09-06T00:00:00Z"
}
```
`affectedPaths` is the rebuild set (own URLs plus shared pages so fresh
indexes/search drop references). `revokedPaths` is the deny set (own
detail/file URLs only, never home or list pages). The runner denies only
`revokedPaths` (A01).

---

## 4. Revocation & Edge Deny Manifest (§I06)

> [!IMPORTANT]
> **Unpublish/archive operations must NOT wait for static site regeneration to hide content.**

1. **Immediate Revocation**: When `removalState == "pending"`, the runner updates the edge deny manifest (`/etc/nginx/conf.d/edge-deny.map`) *before* initiating static site compilation.
2. **Manifest Format**:
   ```nginx
   # Edge deny manifest generated by rebuild-product.py
   "/en/blog/quantum-computing/" 1;
   "/en/blog/quantum-computing" 1;
   ```
3. **Ingress Evaluation**: `nginx-public.conf` evaluates `$edge_denied` via Nginx `map`:
   ```nginx
   map $uri $edge_denied {
     default 0;
     include /etc/nginx/conf.d/edge-deny*.map;
   }
   server {
     if ($edge_denied) {
       return 404;
     }
     ...
   }
   ```
4. **Effectiveness Verification (A02)**: effectiveness is staged and fail-closed —
   writing the file never counts as proof:
   1. `write_manifest`: merge paths into the manifest (atomic replace).
   2. `verify_effective`: the file itself lists every path (write check only).
   3. `apply_configuration`: run `EDGE_VALIDATE_CMD` (e.g. `nginx -t`), then
      `EDGE_RELOAD_CMD` (e.g. `nginx -s reload`). Any configured failure aborts.
   4. `probe_paths_blocked`: GET every revoked path (plus slash twin) against
      `EDGE_PROBE_BASE_URL` and require HTTP 404 for each; any non-404,
      timeout or connection error aborts.
   
   If any configured stage fails, the build is halted immediately, and the job reports `state: "failed"`, `errorCode: "EDGE_DENY_FAILED"`, and `removalState: "failed"` — never `effective`.
   
   Production wiring: the runner accepts `--edge-validate-cmd`,
   `--edge-reload-cmd`, `--edge-probe-base-url`, `--edge-probe-timeout`
   (or the `EDGE_*` environment equivalents). Without a configured probe, the
   report is file-local only: do not treat it as operational edge acceptance.
   The real-ingress integration check stays an explicit open gate until it runs
   against the deployed Caddy/Nginx topology (A02).

---

## 5. Atomic Build, Swap, and Rollback

1. **Releases Directory Structure**:
   ```
   /var/www/releases/
     ├── rev-20260905-01/
     ├── rev-20260906-01/
     └── current -> /var/www/releases/rev-20260906-01/
   ```
2. **Build Isolation**: Build generates static HTML, sitemaps, and Pagefind search indexes into the isolated directory `releases/<requestedRevision>`. The revision must be a non-empty opaque token without path parts, and the release target must stay inside the releases root — anything else fails closed with `VALIDATION_FAILED` before anything is written.
3. **Pre-Swap Artifact Verification (A03)**: before swapping, the runner requires the full artifact set in the new release — `index.html`, `sitemap.xml`, `pagefind/pagefind.js` (override via `--require-artifacts` / `REQUIRED_RELEASE_ARTIFACTS`). A gap reports `SITEMAP_FAILED` / `PAGEFIND_FAILED` / `BUILD_FAILED` and keeps the previous release active. `index.html` alone never proves a deployment.
3. **Atomic Swap**: Once compilation and validation succeed, the active link (`current`) is atomically swapped to the new release directory using `os.replace` on a temporary symlink.
4. **Automatic Rollback**: If compilation, asset bundling, sitemap generation, or Pagefind index creation fails:
   - The runner preserves the previously active release directory.
   - The active symlink remains pointing to the previous successful release.
   - The failure callback is sent:
     ```json
     {
       "state": "failed",
       "errorCode": "BUILD_FAILED"
     }
     ```
   - Deployed site remains functional and intact; no partial or broken build is served to visitors.
5. **Publish cleanup is fail-closed (2026-09-06)**: after a successful swap for
   `removalState == "not_requested"`, the runner clears restored URLs via
   `remove_revocations` (revokedPaths if present, else affectedPaths). A `False`
   return reports `state: "failed"`, `errorCode: "REMOVAL_FAILED"` instead of
   `succeeded`, in both normal and resume paths, so stale deny entries can never
   masquerade as a successful publish. The same holds for resume cleanup.

---

## 6. Operations & Troubleshooting

### Running the Rebuild Runner Manually
To process a publication job from the CLI (the only supported trigger while
`REBUILD_TRIGGER_ENABLED=false`; staging Compose keeps the legacy loopback off):
```bash
python Infra/staging/rebuild-product.py <JOB_UUID> \
  --backend-url http://cms:8000 \
  --secret "$PUBLICATION_MACHINE_SECRET" \
  --manifest-path /etc/nginx/conf.d/edge-deny.map \
  --releases-dir /var/www/releases \
  --current-link /usr/share/nginx/html
```
For automatic post-commit dispatch, set `REBUILD_TRIGGER_ENABLED=true` and either
`PUBLICATION_RUNNER_ARGV` (preferred, e.g. `python /opt/staging/rebuild-product.py
--backend-url http://cms:8000` — the job UUID is appended) or the legacy
`REBUILD_SCRIPT_PATH`. Without either, jobs stay queued for explicit invocation.

### Inspecting Publication Jobs
Administrators can check publication status via the Admin API:
```http
GET /api/v1/admin/publication-jobs?state=failed
```
Requires staff session + OTP authentication.

### Retrying a Failed Publication Job
To retry a failed or queued job:
```http
POST /api/v1/admin/publication-jobs/{id}/retry
If-Match: "2026-09-06T00:00:00Z"
Idempotency-Key: "retry-550e8400-01"
```
- Precondition: `If-Match` must match the job's `updatedAt` timestamp. Mismatches return HTTP 412.
- Idempotency: Repeating the request with the same `Idempotency-Key` returns the existing retry job without triggering duplicate deployments.

### Registered Safe Error Codes
- `BUILD_FAILED`: Static site build command (`npm run build` / Astro) failed.
- `PAGEFIND_FAILED`: Pagefind search index generation failed.
- `SITEMAP_FAILED`: Sitemap generation failed.
- `EDGE_DENY_FAILED`: Edge deny manifest could not be written or verified.
- `REMOVAL_FAILED`: Revocation manifest ineffective or path unresolvable.
- `TIMEOUT`: Build or callback exceeded configured timeout threshold.
- `VALIDATION_FAILED`: Job payload or parameters failed contract validation.
