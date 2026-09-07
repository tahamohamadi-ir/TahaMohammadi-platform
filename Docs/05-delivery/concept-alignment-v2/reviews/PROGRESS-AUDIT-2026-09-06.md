# Implementation progress audit — 2026-09-06

## Decision and scope

Implementation has advanced beyond the dispatch queue. Existing handoffs are review inputs, not evidence that dependencies were accepted. Do not rebuild already implemented packets, and do not dispatch the remaining page families on the assumption that the shared editor/renderer is complete.

This pass inspected queue, handoffs and selected integration source, independently ran all three application test suites and both frontend builds, and produced this report plus `PROGRESS-AUDIT-2026-09-06.json` (all 82 leaf packets, dependency lists and handoff-file presence). It did not perform exhaustive line-by-line review of every packet, visual acceptance, deployment, or packet acceptance. Central statuses are unchanged. Handoff presence is explicitly not a completion count.

## Independently executed checks

| Check | Current result |
|---|---|
| BACKEND `uv run pytest -q` | 910 passed |
| PUBLIC `npm.cmd test` | 376 passed, 64 files |
| ADMIN `npm.cmd test` | 185 passed, 46 files |
| PUBLIC `npm.cmd run build` | PASS, 33 pages, FA/EN Pagefind and sitemap; chunk-size warning remains |
| ADMIN `npm.cmd run build` | PASS, TypeScript and Vite |
| ROOT `python Docs/05-delivery/concept-alignment-v2/validate-plan.py` | FAIL: PUBLIC `src/lib/routes.test.ts:93: new blank line at EOF` |

The earlier SettingsPage build failure is no longer reproducible in the current tree. The existing reconciliation JSON says PASS, but the fresh validator failed before completing; do not present that stored PASS as current verification. No browser journey or visual suite was run in this pass. Runner, lint and schema-export checks reported by other agents were not re-run here.

## Findings requiring work before broader acceptance

1. **P1 — PU-09-editor: structured values become strings.** `Front-End/admin-panel/src/components/editor/StoryEditor.tsx`, `FieldInput`, handles select/boolean/number/media/textarea and otherwise emits a text input with `String(value)`. The actual backend catalog in `Back-End/apps/composition/blocks.py` includes `columnList`, `rowList`, `referenceList`, `relatedList`, `mediaList` and item lists. Editing those controls cannot preserve the required arrays/objects. Implement real list/table/reference/media controls, preserving types, and test against actual catalog schemas and save/reload payloads.

2. **P1 — PU-13-story: actual API fields do not match the renderer.** `Front-End/public-site/src/components/story/StoryBlock.astro` reads quote `text/author/citation`; the catalog and projection deliver `body/source`. It converts heading `level` with `Number`, whereas the catalog supplies `h2/h3/h4`, making higher levels fall back to 2. Related projection intentionally returns only `{family,id}` (`Back-End/apps/composition/projection.py`); the renderer expects slug/title and produces `href="#"`. Resolve references through the real public resolver, use canonical routes, and render actual projected quote and heading shapes. Tests must render backend-shaped documents, not only helper fixtures.

3. **P1 — PU-13-story: incomplete catalog coverage.** The renderer has no branches for several accepted story types, including CTA, gallery, video, audio, timeline, counters, before_after and slider. Such blocks currently disappear. Add supported rendering or an explicit readable fallback consistent with the contract; verify no-JS/print output. Compare all 21 catalog types rather than inferring coverage from a successful build.

4. **P2 — PU-13-story: unavailable download still looks actionable.** File rendering uses `fileUrl || '#'` and always shows a download action. When the backend intentionally omits a restricted/unavailable file, render a non-actionable state or omit the block; never invent a download link.

5. **Product usability gap — ADMIN family editors.** For example, `collection-fields.tsx` exposes members as a raw JSON array and media as IDs. Field presence and passing shallow tests do not establish a usable owner-facing CMS. Review PU-10 family editors and PU-11-media for actual selectors, ordering, validation and save/reload journeys. Do not claim every family is fully editable merely because its keys match DETAIL_FIELD_MAPS.

6. **Reporting correction — autosave.** The editor handoff explicitly delegates timing policy to the host; ContentEditPage saves explicitly and reports dirty state. A status label is not working autosave. Verify the agreed requirement and implement/test it in PU-09-host if required; otherwise describe manual save accurately.

7. **Queue reconciliation gap.** ADMIN packets still marked BLOCKED/NOT_STARTED have implementation and handoffs. PUBLIC PU-13-routes, PU-13-story and PU-14-research also have handoffs despite NOT_STARTED. Record implementation separately from acceptance, after reading each latest handoff revision. A final schema export alone does not satisfy an ACCEPTED_LOCAL dependency.

## Observed work

- BACKEND: resolver/settings already accepted locally; catalog has revision handoff; metadata, extended families, evidence, revision/preview/jobs/invalidation and events have existing implementation evidence awaiting dependency-ordered review.
- PUBLIC: CA-01–08 and graph/public schema sync have existing evidence; routes, shared story and research family now also have handoffs/code. Research needs re-review after shared renderer corrections. A route helper is not a rendered detail page, and 33 empty/static build outputs do not establish all target content families.
- ADMIN: sync, transport, story editor/host, twelve family editors, settings/profile, media, home/graph/jobs and analytics have code/handoffs. Current full suite and build pass. These remain candidates for integration review, not an accepted CMS.
- ROOT: publishing runner and previous governance work remain in the working tree; runtime ingress and publication gates are still separate.

## Ordered next work

1. **Coordinator reconciliation:** review revised `PU-04-catalog` and `CA-02` against their previous findings and exact current files. Resolve the routes-test whitespace failure, then re-run the validator; it may reveal later failures hidden by the first assertion. Reconcile all observed handoffs into the queue/spec mirrors without granting unverified acceptance. Keep old review history and regenerate acceptance hashes only after justified review.
2. **Existing implementation review:** follow the backend dependency order: catalog → metadata → publication/course/creative → lessons → book/talk/resource/collection/series → project evidence → revisions → preview/jobs → invalidation/events and runner. Review CA-03 onward in its own dependency order. Then review schema sync against the accepted artifact. This is review/repair of existing code, not a new rebuild.
3. **Shared repair before new pages:** PU-09-editor and PU-09-host; PU-13-story and its source-shaped rendering tests. Review PU-13-routes and PU-14-research again with real published content. Run an isolated admin-create → save → publish → public-detail journey, including arrays, relations, media, locales and unavailable content.
4. **Remaining family implementations after prerequisites are accepted:** PU-14-publications, PU-14-projects, PU-14-statements; PU-15-articles, PU-15-courses, PU-15-lessons, PU-15-creative; PU-16-books, PU-16-talks, PU-16-resources, PU-16-collections, PU-16-series. Course precedes lesson; research precedes statements/publications as recorded in the queue. Reuse and extend existing legacy-compatible routes rather than assuming nothing exists.
5. **Remaining integration pages:** PU-17-home, PU-18-about, PU-18-cv, PU-18-contact; then PU-21-events, PU-24-search and PU-24-seo according to the DAG. Retain graph in home hero and portal only at language gateway.
6. **Acceptance journeys:** PU-25-admin-journey, PU-25-public-journey, CA-17, PU-25-review. Include real ingress, publication/restore/removal, multilingual content, responsive/keyboard/zoom/no-JS, visual and performance evidence. These gates cannot be closed by unit tests or handoff markers.

## Repository state

All four repositories remain on main with extensive pre-existing uncommitted changes. HEADs observed: ROOT `c69e339c8c26788467d29ad346fb7df99b1c2842`; BACKEND `bd6682ea9dae7e5bf6957c36691dc3a94a00ea37`; PUBLIC `b895b2cb9c6ad9519d55bd2663448461931c0a39`; ADMIN `ca4dd3d26484d4468465c756d302b8e3247a3cbe`. This audit changed no runtime code or central status and performed no commit/push/deploy. Its two new report files are the only intentional source writes; build/test output was generated by the checks.
