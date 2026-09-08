# Acceptance drift note — 2026-09-07 (implementation session)

`validate-plan.py` currently fails at the accepted-head assertion for every
packet. This predates this session: merges `06d26d6` (admin), `368d243`
(backend) and ROOT `2b6934f` moved HEADs past the `ACCEPTED-LOCAL-2026-09-06`
baseline, and previously committed concurrent work already drifted most
accepted file snapshots (backend OpenAPI churn, migrations, home/shell
rewiring).

This session's verified fixes add drift to 9 accepted packets — all with
green tests/builds recorded in their handoffs, all needing coordinator
re-review (NOT silent re-baselining by the implementer):

- `PU-13-story` — `StoryBlock.astro`, `story-content.ts`, test (media-shape
  normalization; 6/6 + build 42 pages)
- `PU-09-editor` — `StoryEditor.test.tsx` only (type fix; 17/17 + build green)
- `PU-14-research`, `PU-14-publications`, `PU-14-projects`,
  `PU-14-statements`, `PU-15-lessons`, `PU-16-books`, `PU-16-talks` —
  detail-page SEO forwarding (en/fa); `PU-16-resources` pages changed too
  (resources evidence entry covers old paths)
- `PU-25-admin-journey` — `product-journey.spec.ts` MISSING (deleted
  misleading scaffold in committed `fbb61d5`); journey evidence file itself
  drifted via handoff updates

Machine-readable detail:
`ACCEPTANCE-DRIFT-2026-09-07.json` (same directory).

No status in `execution-tasks.json` was flipped by this session; acceptance
decisions stay with the coordinator. No commit, push, deployment or live
database mutation beyond the `cx/content-completion-2026-09-07` branches was
performed by this note.
