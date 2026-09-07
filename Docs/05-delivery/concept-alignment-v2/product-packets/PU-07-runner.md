# PU-07-runner — Implement atomic static rebuild, edge revocation manifest and authenticated job completion using standalone staging topology.

Owner: **ROOT** (`D:/Project/tahamohammadi-platform`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-07-jobs, PU-23-invalidation. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `Infra/staging/docker-compose.stage.yml`
- `Infra/staging/Caddyfile.staging.fragment`
- `Infra/staging/nginx-public.conf`
- `Infra/staging/rebuild-product.py` — NEW/PROPOSED
- `Infra/staging/test_rebuild_product.py` — NEW/PROPOSED
- `Docs/08-operations/PRODUCT-PUBLISHING-RUNBOOK.md` — NEW/PROPOSED
- `Docs/10-tracking/product-v2/PU-07-runner-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- python -m unittest discover -s Infra/staging -p test_rebuild_product.py

- Exercise a local fake callback/build: duplicate requests, failure, atomic rollback, revoke-before-rebuild and index removal.

- Validate Compose/Caddy/Nginx config against installed runtime without contacting production.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `Docs/10-tracking/product-v2/PU-07-runner-HANDOFF.md`.

Stop: **PU-07-runner_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
