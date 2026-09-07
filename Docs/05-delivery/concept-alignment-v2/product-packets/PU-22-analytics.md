# PU-22-analytics — Show authenticated date/locale event counts with metric definitions and empty/error/not-connected states.

Owner: **ADMIN** (`D:/Project/tahamohammadi-platform/Front-End/admin-panel`). Status: **NOT_STARTED**.

Dependencies: PU-SYNC-admin, PU-12-jobs. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I07. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/pages/AnalyticsPage.tsx` — NEW/PROPOSED
- `src/lib/api/analytics.ts` — NEW/PROPOSED
- `src/app/router.tsx`
- `src/components/Nav.tsx`
- `src/pages/AnalyticsPage.test.tsx` — NEW/PROPOSED
- `docs/quality/product-v2/PU-22-analytics-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/pages/AnalyticsPage.test.tsx

- npm.cmd run lint

- npm.cmd run build

- Verify saved/published distinction, validation, keyboard/RTL, CSRF/session expiry and relevant 409 conflicts.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-22-analytics-HANDOFF.md`.

Stop: **PU-22-analytics_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
