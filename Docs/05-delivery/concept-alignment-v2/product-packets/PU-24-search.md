# PU-24-search — Extend existing Pagefind metadata/query normalization to all published families, with no-JS collection links and honest error states.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-14-research, PU-14-publications, PU-14-projects, PU-15-articles, PU-15-courses, PU-15-creative, PU-14-statements, PU-15-lessons, PU-16-books, PU-16-talks, PU-16-resources, PU-16-collections, PU-16-series, PU-17-home, PU-18-about, PU-18-cv, PU-18-contact, PU-23-invalidation. Family: F15.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I07. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/integrations/pagefind.mjs`
- `src/lib/search-content.ts`
- `src/components/search/SearchPageContent.astro`
- `src/styles/product-search.css` — NEW/PROPOSED
- `src/components/search/public-240.behavior.test.ts`
- `docs/quality/product-v2/PU-24-search-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/components/search/public-240.behavior.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-24-search-HANDOFF.md`.

Stop: **PU-24-search_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
