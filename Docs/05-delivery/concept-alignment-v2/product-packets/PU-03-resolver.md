> Current review: ../reviews/PU-03-resolver-R1.md. Revision required before dependency acceptance.

# PU-03-resolver — Resolve published graph record IDs to canonical record descriptors without private-record enumeration.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **ACCEPTED_LOCAL**.

Dependencies: PU-02. Family: F02/F03.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I04. Current generated schema and named source files are evidence, not proposed support.

Additional read-only source paths in this repository: `apps/api/admin_common.py`, `apps/api/api.py`.

## Exact write allowlist

- `apps/api/api.py`
- `apps/api/record_resolver.py` — NEW/PROPOSED
- `tests/test_product_record_resolver.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/ACCEPTANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-03-resolver-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

Coordinator note (2026-09-06, provenance/acceptance split): acceptance pins the stable `docs/contracts/openapi/current/ACCEPTANCE.json` record instead of timestamped `docs/contracts/openapi/current/PROVENANCE.json`, because every export regenerates PROVENANCE (fresh timestamp), which made identical-snapshot acceptance ambiguous and broke the drift gate. PROVENANCE remains writable here and via other packets' allowlists as generation evidence. Prior PROVENANCE pin history is preserved in reviews/ACCEPTANCE-VERIFICATION-2026-09-06.md.

## Acceptance and verification

- uv run pytest tests/test_product_record_resolver.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-03-resolver-HANDOFF.md`.

Stop: **PU-03-resolver_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
