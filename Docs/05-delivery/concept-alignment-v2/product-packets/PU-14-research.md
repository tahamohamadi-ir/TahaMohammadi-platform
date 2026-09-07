# PU-14-research — Implement complete F03 index/detail with CMS story and original CA-10 visual acceptance; remove placeholders, retain actual published facts.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-13-routes, PU-13-story. Family: F03.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I01/I03. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/lib/research-content.ts`
- `src/components/research/ResearchPageContent.astro`
- `src/components/research/ResearchTopicDetailContent.astro`
- `src/styles/product-research.css` — NEW/PROPOSED
- `src/pages/fa/research/index.astro`
- `src/pages/fa/research/[slug].astro`
- `src/pages/en/research/index.astro`
- `src/pages/en/research/[slug].astro`
- `src/components/page-family/PageFamilyConstellationShell.astro`
- `src/components/page-family/PageFamilySelectedPublicationsShell.astro`
- `src/styles/pf05-alignment.css` — NEW/PROPOSED
- `src/components/research/public-201.behavior.test.ts`
- `src/components/research/product-family.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-14-research-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

Visual criteria source (read-only): packets/CA-10.md. Transfer its Done when / visual checks; do not execute its retired allowlist.

## Acceptance and verification

- npm.cmd test -- src/components/research/product-family.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-14-research-HANDOFF.md`.

Stop: **PU-14-research_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
