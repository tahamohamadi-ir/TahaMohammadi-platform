# PU-07-revisions — Snapshot and restore content, attached story and ordered relations atomically; preserve history and published snapshot.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **REVISE**.

Dependencies: PU-04-catalog, PU-04-metadata, PU-04-publication, PU-04-course, PU-04-creative, PU-05-lessons, PU-06-book, PU-06-talk, PU-06-resource, PU-06-collection, PU-06-series, PU-04-project-evidence. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I03. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/content/models.py`
- `apps/content/migrations/0031_pu_publication_snapshots.py` — NEW/PROPOSED
- `apps/api/admin_content.py`
- `apps/api/admin_composition.py`
- `apps/composition/projection.py`
- `tests/test_product_revision_snapshot.py` — NEW/PROPOSED
- `docs/contracts/openapi/current/public-openapi.json`
- `docs/contracts/openapi/current/admin-openapi.json`
- `docs/contracts/openapi/current/PROVENANCE.json`
- `docs/contracts/openapi/current/endpoint-inventory.md`
- `docs/quality/product-v2/PU-07-revisions-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- uv run pytest tests/test_product_revision_snapshot.py

- uv run ruff check .

- Source-export both APIs with scripts/export_openapi.py; validate schemas and record hashes.

- For model changes: migrate a disposable database forward/backward, preserve source records and test draft/locale exclusion.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-07-revisions-HANDOFF.md`.

Stop: **PU-07-revisions_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

Coordinator audit ownership extension (2026-09-06): `apps/content/published.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/test_product_draft_published_isolation.py`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Execution ownership extension (2026-09-06, mission four-packet review): `apps/api/api.py` — public `ProjectDetailOut` nested resolvers (`resolve_evidence`, `resolve_collaborators`, `resolve_funding`, `resolve_case_study`) currently read live reverse managers, so `materialize_published_item` scalar-only fix cannot satisfy "public reads serve the latest publication snapshot while the live row is a draft workspace". Limited to those four resolvers to prefer frozen snapshot relations when `_published_snapshot_data` is present; no route, schema shape, or other family change.
