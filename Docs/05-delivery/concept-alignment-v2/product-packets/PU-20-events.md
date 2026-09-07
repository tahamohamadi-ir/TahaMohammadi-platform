# PU-20-events — Implement first-party aggregate analytics ingest/reporting and 13-month retention without visitor identifiers.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-19, PU-06-series, PU-07-jobs, PU-23-invalidation. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I07. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/analytics/__init__.py` — NEW/PROPOSED
- `apps/analytics/apps.py` — NEW/PROPOSED
- `apps/analytics/models.py` — NEW/PROPOSED
- `apps/analytics/migrations/__init__.py` — NEW/PROPOSED
- `apps/analytics/migrations/0001_aggregate_events.py` — NEW/PROPOSED
- `apps/analytics/api.py` — NEW/PROPOSED
- `apps/analytics/management/__init__.py` — NEW/PROPOSED
- `apps/analytics/management/commands/__init__.py` — NEW/PROPOSED
- `apps/analytics/management/commands/prune_analytics.py` — NEW/PROPOSED
- `apps/api/api.py`
- `apps/api/admin_api.py`
- `config/settings/base.py`
- `tests/test_product_analytics.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-20-events-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- uv run pytest tests/test_product_analytics.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-20-events-HANDOFF.md`.

Stop: **PU-20-events_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

Coordinator audit ownership extension (2026-09-06): `apps/rebuild/migrations/0002_publicationjob_revoked_paths.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/public/articles-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/public/project-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/public/publication-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_admin_content_write.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_admin_revisions_schedule.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_admin_workflow_api.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_api.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_content_lifecycle_e2e.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_openapi_hash_drift.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.
