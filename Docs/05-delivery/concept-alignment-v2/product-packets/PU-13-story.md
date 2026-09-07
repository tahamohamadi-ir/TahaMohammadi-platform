# PU-13-story — Render typed story blocks once with readable no-JS/print content, TOC, code/table/math/file/relations.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **NOT_STARTED**.

Dependencies: PU-SYNC-public, CA-08. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I03. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/components/story/StoryDocument.astro` — NEW/PROPOSED
- `src/components/story/StoryBlock.astro` — NEW/PROPOSED
- `src/styles/story.css` — NEW/PROPOSED
- `src/lib/story-content.ts` — NEW/PROPOSED
- `src/lib/story-content.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-13-story-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/lib/story-content.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-13-story-HANDOFF.md`.

Stop: **PU-13-story_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
