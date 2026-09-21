# Plan C Recovery Evidence — Tasks 1–13 (recovery branch)

Ledger home: `D:/Project/tahamohammadi-platform/Docs/05-delivery/knowledge-atlas/plans/`
(plan files live in the coordination root, not in public-site).

- Incident: destructive `reset` on `feat/knowledge-atlas-public` removed Tasks 7–13
  from ancestry; a parallel agent/Cursor kept mutating that ref
  (`fc7f91e` → `db1de76` → `93f70a3` → `8738d5b` observed, including an
  unreviewed Task-9 rewrite `stateAttr()/exists({kind,key})/collision-throw`
  and a scope-creeping Task-6 restyle).
- Response: branch quarantined read-only; merge object `09b1ae2`
  (parents `[fc7f91e, 23d946a]`) anchored as `backup/reconcile-09b1ae2`;
  single-writer recovery branch `feat/knowledge-atlas-public-recovery`
  created at `09b1ae2` in worktree
  `D:/Project/.atlas-worktrees/public-site-plan-c-recovery`.
- Merge `09b1ae2` verified blob-by-blob: Task-7/8 paths == parent 1
  (`fc7f91e`); Tasks 9–13 paths == reviewed backup tip `23d946a`;
  `selection.ts` is the reviewed variant (`6cb4592`), not the Cursor
  rewrite (`1edcb19`).

## Task → SHA map (recovery branch HEAD `063333e`)

| Task | Title | Accepted SHA | Origin | Verdict |
|------|-------|--------------|--------|---------|
| 1 | Contract types and key grammar | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 2 | Runtime payload validator | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 3 | Build-time snapshot loader | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 4 | Fixtures and hermetic fixture server | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 5 | Routes and route registrations | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 6 | Region, semantic index and content states | (via `09b1ae2` ancestry) | reviewed | PASS retained |
| 7 | Runtime refresh | current variant (`ff2ded1` impl) + fix `10ce312` | fresh review | SPEC PASS / QUALITY APPROVED |
| 8 | Draft-preview shell | `afc9f1a` + `fc7f91e` + fixes `4dac758`, `10ce312` | fresh security review | SPEC PASS / QUALITY APPROVED* |
| 9 | Selection state and URL codec | `23d946a` blobs, byte-identical at HEAD | reviewed | PASS retained |
| 10 | Search, filters and neighbourhood | `0cb7a95` + prettier-only `063333e` | reviewed | PASS retained |
| 11 | Inspector projection | `bd9aa6f` blobs, byte-identical at HEAD | reviewed | PASS retained |
| 12 | Layout consumption | `3ba05cf` blobs, byte-identical at HEAD | reviewed | PASS retained |
| 13 | 2D SVG projection engine | algorithm `c9ecbfbc` identical + shared-renderer repair `df7712d` | scoped re-review | SPEC PASS / QUALITY APPROVED |

`*` Task-8 quality APPROVED pending the two landed test-only fixes
(`as unknown as History` casts, fragment-capture-before-strip + live-location
test); no production-type weakening.

## Gate evidence (recovery HEAD)

- Focused Atlas + route/SEO/component: 18 files / 84 passed.
- Full suite: 112 files / 671 passed, 4 skipped.
- eslint: 0 errors (1 warning = `.py` generator ignored, no matching config).
- prettier --check over the full Plan-C path set: clean.
- `npm run build`: 46 pages; `validate:seo` PASS (16 routes x 2 locales, 44 pages).
- tsc: total 141; plan-C-introduced errors = 0 (only the known
  `AstroContainer` `.astro` TS2307 pattern, identical in pre-existing about
  tests; one real TS2459 found in `presentation.ts` and fixed in `ecb1258`).
- dist: `/en/atlas/` + `/fa/atlas/` honest `unavailable` (no API at build),
  correct `lang`, locale copy, canonical/alternate; `/en|fa/atlas/preview/`
  shells with `preview=false`, `noindex, nofollow`, no token, absent from
  sitemap.
- Scope: Hero/Home/About/ResearchUniverse diff = 0; backend + admin untouched
  (only pre-existing unrelated dirt in those checkouts); fixture source
  `backend-plan-b` clean at `bdb546f`.

## Remaining risk

- The quarantined branch is still being mutated by the parallel agent; any
  future reconcile must re-verify its tip and never build on it.
- `AtlasProjection2d.astro` is currently unreferenced by the shared-string
  path (kept as the thin-wrapper consumer for Task 15+); Task 15 should
  confirm or remove it rather than leave two consumers drifting.
