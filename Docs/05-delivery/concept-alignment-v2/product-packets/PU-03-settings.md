# PU-03-settings — Add localized draft/published site settings alongside the legacy operational settings.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **ACCEPTED_LOCAL**.

Dependencies: PU-02, PU-03-resolver. Family: F01/F02.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I04. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/siteconfig/models.py`
- `apps/siteconfig/migrations/0005_localized_product_settings.py` — NEW/PROPOSED
- `apps/api/api.py`
- `apps/api/admin_api.py`
- `apps/api/admin_siteconfig.py`
- `tests/test_product_localized_settings.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/ACCEPTANCE.json` — NEW/PROPOSED
- `scripts/verify_openapi_export.py`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-03-settings-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

Coordinator note (2026-09-06, provenance/acceptance split): `docs/contracts/openapi/current/PROVENANCE.json` stays writable here for schema-export runs, but it is generation evidence (the export regenerates it with a fresh timestamp on every run) and is therefore excluded from acceptance pins; acceptance pins the stable `docs/contracts/openapi/current/ACCEPTANCE.json` record instead. `scripts/verify_openapi_export.py` is retargeted to gate against that stable record. `tests/test_openapi_hash_drift.py` is edited under its existing PU-20-events ownership (single writer, no allowlist duplication) to assert acceptance from the stable record plus PROVENANCE-to-ACCEPTANCE linkage. See reviews/ACCEPTANCE-VERIFICATION-2026-09-06.md.

## Acceptance and verification

- uv run pytest tests/test_product_localized_settings.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-03-settings-HANDOFF.md`.

Stop: **PU-03-settings_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
