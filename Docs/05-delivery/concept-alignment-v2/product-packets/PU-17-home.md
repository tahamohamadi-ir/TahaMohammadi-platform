# PU-17-home — Integrate research-first home, two audience paths, three selected works and CMS settings; inherit CA-09 editorial rhythm.

Owner: **PUBLIC** (`D:/Project/tahamohammadi-platform/Front-End/public-site`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-13-routes, PU-13-story, CA-06, PU-03-settings, CA-03. Family: F02.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I04. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/components/home/HomeResearchInterests.astro`
- `src/components/home/HomeJourney.astro`
- `src/components/home/HomeFeaturedProjects.astro`
- `src/components/home/HomeFeaturedPublications.astro`
- `src/components/home/HomeExploreRails.astro`
- `src/components/home/HomeCollaborationCta.astro`
- `src/styles/home.css`
- `src/components/home/wp40-home.behavior.test.ts`
- `tests/e2e/wp40-home.e2e.ts`
- `src/lib/site-settings-content.ts`
- `src/lib/home-content.ts`
- `src/components/home/product-home.test.ts` — NEW/PROPOSED
- `docs/quality/product-v2/PU-17-home-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

Visual criteria source (read-only): packets/CA-09.md. Transfer its Done when / visual checks; do not execute its retired allowlist.

## Acceptance and verification

- npm.cmd test -- src/components/home/product-home.test.ts

- npm.cmd run lint

- npm.cmd run build

- npm.cmd run validate:design

- For UI: FA/EN + light/dark, 320/390/768/1024/1280/1440, keyboard, 200% zoom, no-JS and empty/unavailable/ready evidence.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-17-home-HANDOFF.md`.

Stop: **PU-17-home_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
