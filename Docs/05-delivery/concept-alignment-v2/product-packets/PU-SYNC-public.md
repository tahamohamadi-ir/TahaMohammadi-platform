# PU-SYNC-public — Generate final public schema consumer types before family implementation.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-03-resolver, PU-03-settings, PU-04-catalog, PU-04-metadata, PU-04-publication, PU-04-course, PU-04-creative, PU-05-lessons, PU-06-book, PU-06-talk, PU-06-resource, PU-06-collection, PU-06-series, PU-04-project-evidence, PU-07-revisions, PU-07-preview, PU-07-jobs, PU-23-invalidation, PU-20-events, CA-08, PU-SYNC-graph. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I08. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/generated/public-api.ts`
- `src/lib/product-api.contract.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-SYNC-public-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd run generate:api-types

- npm.cmd test -- src/lib/product-api.contract.test.ts

- Record source schema SHA and additive compatibility checks.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-SYNC-public-HANDOFF.md`.

Stop: **PU-SYNC-public_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

Coordinator audit ownership extension (2026-09-06): `contracts/openapi.public.sha256`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `src/generated/openapi-hash.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `src/lib/hero-graph-resolve.test.ts`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `src/test-harness/contract-fixtures.ts`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/responses/articles-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/responses/project-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.

Coordinator audit ownership extension (2026-09-06): `tests/fixtures/contracts/responses/publication-detail.get.200.json`. See `../reviews/COORDINATOR-REVIEW-2026-09-06.md`.
