# PU-07-runner Delivery Handoff

Owner repository: `ROOT` (`d:\Project\tahamohammadi-platform`)  
Packet: `PU-07-runner`  
Specification: `Docs/05-delivery/concept-alignment-v2/product-packets/PU-07-runner.md`  
Contract: `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06  
Status: **HANDOFF_READY** (explicitly uncommitted)  
Base commit: `bd6682ea9dae7e5bf6957c36691dc3a94a00ea37`  
Result commit: uncommitted working directory  

---

## 1. Summary of Changes

Implemented the standalone staging rebuild runner, edge revocation manifest, and authenticated job completion architecture per `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06:

- **Product Rebuild Runner (`Infra/staging/rebuild-product.py`)**:
  - Implemented HMAC-SHA256 request authentication (`sign_machine_request`, `make_authenticated_request`) matching §I06 specification:
    - Headers: `X-Publication-Timestamp`, `X-Publication-Nonce`, `X-Publication-Signature`.
    - Signed text: `<METHOD>\n<PATH>\n<TIMESTAMP>\n<NONCE>\n<BODY_SHA256>`.
  - Machine client communicates with internal endpoints:
    - `GET /api/v1/internal/publication-jobs/{job_id}`: Retrieves job specification.
    - `POST /api/v1/internal/publication-jobs/{job_id}/result`: Reports lifecycle transitions (`running`, `succeeded`, `failed`).
  - `EdgeDenyManager`:
    - Implements **Revoke-Before-Rebuild**: when `removalState == "pending"`, immediately pushes affected paths to the edge deny manifest before compilation starts.
    - Independently confirms edge deny effectiveness; halts compilation and reports `EDGE_DENY_FAILED` if verification fails.
    - Cleans up revoked entries upon subsequent republish/restore.
  - `StaticSiteManager`:
    - Compiles static release artifacts into isolated directories (`releases/<revision>`).
    - Performs atomic symlink swap (`current` -> `releases/<revision>`).
    - Implements automatic rollback: retains previous release active if compilation or asset verification fails.
- **Edge Ingress Configuration (`Infra/staging/`)**:
  - `Infra/staging/nginx-public.conf`:
    - Added `map $uri $edge_denied` with wildcard include `/etc/nginx/conf.d/edge-deny*.map`.
    - Returns HTTP 404 immediately at edge ingress for any path in the deny manifest.
  - `Infra/staging/Caddyfile.staging.fragment`:
    - Added interception block for `/api/v1/internal/*` returning `404 Not Found` to prevent public edge exposure of private internal machine endpoints.
  - `Infra/staging/docker-compose.stage.yml`:
    - Mounted persistent volumes for static release hosting (`stage_public_html`) and edge deny manifest configuration (`stage_edge_deny`) in the `web` container.
- **Operations Runbook (`Docs/08-operations/PRODUCT-PUBLISHING-RUNBOOK.md`)**:
  - Comprehensive guide covering staging architecture, machine HMAC authentication, publication lifecycle, edge deny mechanics, atomic swap, and rollback troubleshooting.

---

## 2. Verification Evidence

### Automated Unit Tests
- Test Command: `python -m unittest discover -s Infra/staging -p test_rebuild_product.py`
- Test Output:
  ```
  ........
  ----------------------------------------------------------------------
  Ran 8 tests in 0.067s

  OK
  ```
- Test Coverage:
  - `test_rebuild_product_module_exists`: Dynamic module loading and interface verification.
  - `test_sign_machine_request`: Cryptographic HMAC-SHA256 signature verification against contract algorithm.
  - `test_edge_deny_manager_lifecycle`: Path normalization, file mapping, verification, and republish removal.
  - `test_static_site_manager_atomic_swap_and_rollback`: Symlink swapping, revision resolution, and rollback preservation.
  - `test_successful_publish_workflow`: Full queued -> running -> build -> swap -> succeeded flow with artifact revision reporting.
  - `test_revoke_before_rebuild_workflow`: Verified deny manifest is effective BEFORE build starts; callback reports `removalState="effective"`.
  - `test_edge_deny_failure_aborts_build`: Halts execution and reports `EDGE_DENY_FAILED` without running build if manifest verification fails.
  - `test_build_failure_and_atomic_rollback`: Build error triggers symlink rollback to previous active release and reports `BUILD_FAILED`.
  - `test_duplicate_idempotent_callbacks`: Idempotent replay resilience.

### Configuration Validation
- Validated `docker-compose.stage.yml` against compose schema parser.
- Confirmed zero live production contact; all tests executed on isolated temporary staging directories.

---

## 3. Work Left Uncommitted

Per workspace instructions, changes are left unstaged and uncommitted in git.
Handoff marker: `PU-07-runner_HANDOFF_READY`.
