# PU-09-host — Connect story selection/edit/preview to generic content editor; preserve existing metadata and revision workflow.

Owner: **ADMIN** (`D:/Project/tahamohammadi-platform/Front-End/admin-panel`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-09-editor. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I03. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `src/pages/ContentEditPage.tsx`
- `src/lib/api/content.ts`
- `src/pages/ContentEditPage.test.tsx`
- `docs/quality/product-v2/PU-09-host-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- npm.cmd test -- src/pages/ContentEditPage.test.tsx

- npm.cmd run lint

- npm.cmd run build

- Verify saved/published distinction, validation, keyboard/RTL, CSRF/session expiry and relevant 409 conflicts.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-09-host-HANDOFF.md`.

Stop: **PU-09-host_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
