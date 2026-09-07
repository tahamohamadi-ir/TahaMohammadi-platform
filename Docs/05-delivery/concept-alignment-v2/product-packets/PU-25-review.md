# PU-25-review — Record independent cross-repository acceptance on exact commits and owner review; return fixes to owning packets.

Owner: **ROOT** (`D:/Project/tahamohammadi-platform`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: CA-17, PU-25-admin-journey, PU-25-public-journey, PU-22-analytics. Family: all.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules and the assigned family; CMS-SPEC relevant editor section; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I08. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `Docs/10-tracking/product-v2/FINAL-ACCEPTANCE.md` — NEW/PROPOSED
- `Docs/10-tracking/product-v2/PU-25-review-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only. Migration names are reserved against SOURCE-INVENTORY; if the base moved, coordinator updates the exact name/dependency before work. Never apply migrations to production in this packet.

## Acceptance and verification

- All 15 families and admin-to-public flows have evidence; implementation, publication and visual acceptance stay distinct.

- No failed or unrun gate is labelled PASS.

- Before behavior changes, add a focused failing case for the stated defect/gap. Missing implementation may be demonstrated by an import/route/schema test; record actual output, not a predicted failure.

- Preserve private/draft exclusion, exact-locale semantics, accessibility and existing interface compatibility.

- For fixture evidence, use explicit synthetic records; never publish illustrative profile claims.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `Docs/10-tracking/product-v2/PU-25-review-HANDOFF.md`.

Stop: **PU-25-review_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.
