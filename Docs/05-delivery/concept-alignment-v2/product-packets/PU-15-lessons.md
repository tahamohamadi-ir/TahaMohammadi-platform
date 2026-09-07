# PU-15-lessons — Render complete lesson pages, parent course links, resources and published-only ordered neighbors.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **REVISE**.

Dependencies: PU-13-routes, PU-13-story, PU-15-courses. Family: F07.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I05. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/lib/lessons-content.ts` — NEW/PROPOSED
- `src/components/teaching/LessonDetailContent.astro` — NEW/PROPOSED
- `src/pages/fa/education/[courseSlug]/lessons/[lessonSlug].astro` — NEW/PROPOSED
- `src/pages/en/education/[courseSlug]/lessons/[lessonSlug].astro` — NEW/PROPOSED
- `src/components/teaching/product-lessons.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-15-lessons-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/components/teaching/product-lessons.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-15-lessons-HANDOFF.md`.

Stop: **PU-15-lessons_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

## Content completion amendment — 2026-09-07

Authorized by owner implementation plan; preserve previous source and tests.

- `src/lib/lessons-content.test.ts`
