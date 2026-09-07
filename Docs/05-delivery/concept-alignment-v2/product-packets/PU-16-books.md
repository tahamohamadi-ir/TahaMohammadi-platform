# PU-16-books — Build canonical books pages from accepted projections, full body and real file/member links; no duplicate content records.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **NOT_STARTED**.

Dependencies: PU-13-routes, PU-13-story. Family: F09.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I01/I02/I05. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/lib/books-content.ts` — NEW/PROPOSED
- `src/components/books/CollectionPage.astro` — NEW/PROPOSED
- `src/components/books/DetailPage.astro` — NEW/PROPOSED
- `src/styles/product-books.css` — NEW/PROPOSED
- `src/pages/fa/books/index.astro` — NEW/PROPOSED
- `src/pages/fa/books/[slug].astro` — NEW/PROPOSED
- `src/pages/en/books/index.astro` — NEW/PROPOSED
- `src/pages/en/books/[slug].astro` — NEW/PROPOSED
- `src/lib/books-content.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-16-books-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/lib/books-content.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-16-books-HANDOFF.md`.

Stop: **PU-16-books_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
