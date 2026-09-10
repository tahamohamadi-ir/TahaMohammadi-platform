# REVISE re-verification — 2026-09-10

Independent read-only re-verification of the three repaired `REVISE` packets
against the original findings in `CONTENT-MANAGEMENT-REVIEW-2026-09-07.md`.
`PU-25-admin-journey` (the fourth `REVISE`) is owner-deferred to R9 and was not
reviewed (`OWNER-DECISION-2026-09-10.md`).

**Method caveat:** the verifier environment had no shell/git execution, so all
runtime numbers (pytest/vitest counts, lint, build) remain handoff/R8 claims. The
verdicts below are static verification: source, tests, and generated contract
inspection with exact file references. No file, queue state, or database was
modified.

## PU-15-lessons (PUBLIC, CM-04) — PASS (static)

- `published_at` gate removed: `src/lib/lessons-content.ts:45-67` no longer
  calls `assertPublishedOnly`; the real schema has no such field
  (`Back-End/apps/api/api.py:1517-1531`, publication enforced at
  `api.py:2084-2109`). Regression: `src/lib/lessons-content.test.ts:37-43`
  returns `status: 'ready'` for a schema-typed fixture without `published_at`.
- Resources/neighbors are `WorkRefOut` with real hrefs through `workRefToHref`
  (`LessonDetailContent.astro:89-108`), no `#` fallback.
- Course enumeration paginates until `count`
  (`lessons-content.ts:84-120`; 101-course/two-page regression at
  `lessons-content.test.ts:56-79`).
- Alternates use explicit translation identity, not same-slug guessing
  (`lessons-content.ts:132-145`).
- Remaining gap: runtime commands not re-executed here.

## PU-03-settings (BACKEND, CM-02-adjacent) — PASS for backend scope (static)

- `LocalizedSiteSettings` model with draft/published snapshot split, managed
  copy, featured records, brand media, journey (`apps/siteconfig/models.py:94-134`;
  migrations `0005`, `0006`, `0007`).
- Real-client tests: draft-only/exact-locale 404s
  (`tests/test_product_localized_settings.py:106-223`), If-Match 409 + CSRF +
  validation (249-557), publish snapshot isolation (438-477), managed copy
  (18-64), featured/brand bounds and revocation (603-717).
- Contract artifacts: `brandMedia`/`contentCopy`/`featuredRecords` in
  `public-openapi.json:2363-2384`; `/api/v1/site/{locale}`, `/journey` at
  :6528/:6568.
- **Ownership finding:** the consumer-side CM-02 defect (public Header/Footer/nav
  rendering localized published settings) is **not** in this packet's scope; it
  belongs to CA-08 (accepted, `packets/CA-08.md`), PU-17-home and
  PU-08-settings (both `IMPLEMENTED_UNREVIEWED`). Residual items to close CM-02
  fully: brand **mark image** still comes from the local promoted registry
  (`Header.astro:13,70`), and Header falls back to the approved route registry
  when published `navLinks` is empty (`Header.astro:41-51`, documented in
  `CA-08-HANDOFF.md:220-266`).

## PU-09-editor (ADMIN, CM-08) — PARTIAL

- CM-08 defects repaired with regression tests: table-style `RowListField`
  (`StoryEditor.tsx:151-230`), media/related library controls with paging,
  stale-response guard and preserved selections
  (`story-library-fields.tsx:237-332`), no raw-JSON fallback
  (`StoryEditor.tsx:530-536`), save blocked by
  `validateStoryDraft` (`story-validation.ts:17-130`,
  `StoryEditor.tsx:918-928`), contract match with real catalog
  (`Back-End/apps/composition/blocks.py:288-291,584-589,683-706,829-836`).
- Open acceptance items: browser RTL/keyboard/focus/responsive review, published
  status copy, CSRF/session-expiry exercise, and relevant 409 conflicts remain
  unproven (`PU-09-editor-HANDOFF.md:45-47`). Local blocking is bypassed when the
  schema is unavailable (`story-validation.ts:21`), disclosed in the UI
  (`StoryEditor.tsx:717-722`).

## Disposition recommendation

| Packet           | Verification      | Suggested queue action                                                |
| ---------------- | ----------------- | --------------------------------------------------------------------- |
| PU-15-lessons    | PASS (static)     | coordinator may move `REVISE` → `IMPLEMENTED_UNREVIEWED`/acceptance review |
| PU-03-settings   | PASS (backend)    | coordinator may clear backend `REVISE`; CM-02 consumer items stay with CA-08/PU-17-home/PU-08-settings |
| PU-09-editor     | PARTIAL           | remaining admin visual/keyboard/RTL + CSRF/session evidence required before clearing |
| PU-25-admin-journey | owner-deferred | move toward R9 credential-gated disposition                            |

Queue status changes remain coordinator/owner actions; this document records
verification evidence only.
