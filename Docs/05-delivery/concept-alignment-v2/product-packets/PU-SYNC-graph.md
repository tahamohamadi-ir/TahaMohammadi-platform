# PU-SYNC-graph — Generate public types and resolver fixture from the accepted resolver schema.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **ACCEPTED_LOCAL**.

Dependencies: PU-03-resolver. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I04. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/generated/public-api.ts`
- `tests/fixtures/contracts/product-record-resolver.json` — NEW/PROPOSED
- `src/lib/product-resolver.contract.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-SYNC-graph-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd run generate:api-types

- npm.cmd test -- src/lib/product-resolver.contract.test.ts

- Pin source OpenAPI SHA; fixture uses synthetic records only.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-SYNC-graph-HANDOFF.md`.

Stop: **PU-SYNC-graph_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
