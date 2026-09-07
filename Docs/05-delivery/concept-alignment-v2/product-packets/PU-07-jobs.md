# PU-07-jobs — Persist idempotent publication jobs and expose admin status/retry plus authenticated build-result callback.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-07-revisions, PU-03-settings, PU-04-project-evidence, PU-07-preview. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/rebuild/models.py` — NEW/PROPOSED
- `apps/rebuild/migrations/__init__.py` — NEW/PROPOSED
- `apps/rebuild/migrations/0001_publication_jobs.py` — NEW/PROPOSED
- `apps/rebuild/services.py`
- `apps/rebuild/views.py`
- `apps/api/admin_api.py`
- `apps/api/admin_publication_jobs.py` — NEW/PROPOSED
- `config/urls.py`
- `tests/test_product_publication_jobs.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-07-jobs-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- uv run pytest tests/test_product_publication_jobs.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-07-jobs-HANDOFF.md`.

Stop: **PU-07-jobs_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

Coordinator audit ownership extension (2026-09-06): `config/settings/production.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_product_publication_lifecycle_a03.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.
