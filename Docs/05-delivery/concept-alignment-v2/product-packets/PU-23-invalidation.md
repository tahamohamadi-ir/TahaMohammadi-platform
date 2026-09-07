# PU-23-invalidation — Enqueue all publish/archive/restore/schedule/graph/settings changes with affected paths and removal status; no backend search engine.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-07-jobs, PU-07-preview, PU-03-settings. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06/I07. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/rebuild/services.py`
- `apps/content/services/lifecycle.py`
- `apps/api/admin_content.py`
- `apps/api/admin_graph.py`
- `apps/api/admin_siteconfig.py`
- `tests/test_product_publication_invalidation.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-23-invalidation-HANDOFF.md` — NEW/PROPOSED
- `apps/content/management/commands/publish_scheduled_content.py`
- `apps/api/admin_home.py`

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- uv run pytest tests/test_product_publication_invalidation.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-23-invalidation-HANDOFF.md`.

Stop: **PU-23-invalidation_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
