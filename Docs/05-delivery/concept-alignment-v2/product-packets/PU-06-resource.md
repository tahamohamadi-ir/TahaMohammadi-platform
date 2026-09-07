# PU-06-resource — Extend existing download detail and generic editor map with story/metadata; reuse current list/detail endpoints. Preserve versioned file replacement history and gated download behavior.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-04-metadata, PU-06-talk. Family: F11.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I01/I03. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/content/models.py`
- `apps/content/migrations/0028_pu_resource_story.py` — NEW/PROPOSED
- `apps/api/api.py`
- `apps/api/admin_content.py`
- `apps/api/admin_media_ext.py`
- `tests/test_product_resource.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-06-resource-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- uv run pytest tests/test_product_resource.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-06-resource-HANDOFF.md`.

Stop: **PU-06-resource_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
