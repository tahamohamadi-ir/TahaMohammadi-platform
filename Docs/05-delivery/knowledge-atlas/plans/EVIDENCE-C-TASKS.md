# Plan C acceptance evidence (Tasks 1–24)

Branch: `feat/knowledge-atlas-public-recovery` (quarantine worktree
`D:/Project/.atlas-worktrees/public-site-plan-c-recovery`).
Base: `origin/main = 64dcbe8`. Backend fixtures: backend@`bdb546f`.
Machine: DESKTOP-K05IG1H (Windows, Node v22.23.2, npm 12.0.2).
Date (UTC): 2026-09-22.

Task 19 was **not executed**: Task 18 measured pick p95 ≈ 0.003 ms against
the 8 ms budget and recorded `broad-phase: not required` in
`docs/quality/KNOWLEDGE-ATLAS-PICK-BENCHMARK.md`.

## 1. Full frontend gates

```bash
npm run lint && npm run format:check && npm test && npm run validate:design && npm run build && npm run validate:seo
```

| Gate | Result |
|---|---|
| `lint` (eslint .) | clean |
| `format:check` (prettier --check .) | clean — `tests/fixtures/atlas/*` excluded via `.prettierignore` (source-derived, never hand-edited; generator `scripts/atlas-generate-fixtures.py`) |
| `test` (vitest run) | 119 files passed, 710 passed + 4 skipped |
| `validate:design` | PASS (24 components, 6 templates; V2 overlay 2.1.0) |
| `build` (plain, no API) | 46 pages; `/en/atlas/` + `/fa/atlas/` `unavailable` (honest: no API configured) |
| `build` (`PUBLIC_API_BASE_URL=http://127.0.0.1:4488` fixture server) | 52 pages; both Atlas routes `ready` (4 nodes / 3 relations each, contract `atlas01-1.0.0`, payload script embedded) |
| `validate:seo` on the plain 46-page build | PASS — 16 index routes × 2 locales; 44 locale HTML pages; per-locale Pagefind |

Known pre-existing failures (reproduced on clean HEAD via stash, not Atlas
regressions): `validate:seo` FAILs on the 52-page atlas-ready build
(`en/research/human-centered-ai` canonical `/404`); `public-300-nojs-crawl`
`home-en`/`home-fa` fail identically without our changes.

## 2. Browser gates (fixture-backed build)

```bash
PUBLIC_API_BASE_URL=http://127.0.0.1:4488 npx playwright test tests/e2e/product-atlas.e2e.ts tests/e2e/product-atlas-budgets.e2e.ts
```

Result: **18 passed** (13 hermetic product + 5 budgets), per-spec baselines:

- product-atlas: ready presentation EN+FA, node/relation/unknown deep links,
  Back/Forward, search, every filter, compact 2D, reduced motion, no-WebGL,
  no-JS semantics, representative scale.
- budgets: first frame ≤ 900 ms, payload ≤ 60 KB, snapshot ≤ 40 KB,
  chips ≤ 40, DOM ≤ 2,500, idle draws == 0.

```bash
npx playwright test tests/e2e/public-080-a11y-crawl.e2e.ts
```

Result: **23 passed**.

```bash
npx playwright test tests/e2e/public-300-nojs-crawl.e2e.ts
```

Result: **21 passed, 2 failed (`home-en`, `home-fa`)** — pre-existing (see
§1), unrelated to Atlas; Atlas no-JS semantics pass inside the hermetic
suite.

Live confirmation (`tests/knowledge-atlas/ka-live.e2e.ts`, config
`playwright.knowledge-atlas.config.ts`) skips honestly when the production
API has no active Atlas version; the fixture build remains the acceptance
surface until Plan D activates the migrated version.

## 3. Frozen surfaces untouched

```bash
git diff --stat origin/main...HEAD -- src/components/home src/components/hero src/styles/hero-sequence.css src/styles/hero-graph.css
```

Result: **empty**. Hero v2 and Home are byte-identical to the branch base.
`package.json` / `package-lock.json` diff is likewise empty — no new
dependency.

## 4. Budgets (spec §19.2; detail in `docs/quality/KNOWLEDGE-ATLAS-PERFORMANCE.md`)

| Metric | Budget | Measured | Verdict |
|---|---|---|---|
| First interactive frame | ≤ 900 ms | spec green (local Chromium) | PASS |
| Pick p95 (72/136) | ≤ 8 ms | 0.002–0.003 ms | PASS |
| Drag frame p95 | ≤ 16 ms | not instrumented at scale | OPEN (gap, not breach) |
| Runtime payload gzip | ≤ 60 KB | 782/844 B | PASS |
| Embedded snapshot gzip | ≤ 40 KB | 778 B | PASS |
| Label chips | ≤ 40 | 6 | PASS |
| DOM nodes | ≤ 2,500 | ~144 | PASS |
| Idle draws (1500 ms) | 0 | 0 | PASS |

No ceiling raised (§19.6).

## 5. Task log

| Task | Commit | Review |
|---|---|---|
| 1–4 model/validate/snapshot/fixtures | history before quarantine | PASS (recovery evidence) |
| 5–6 routes/shell | `443c703`, `c90ecc6` | PASS |
| 7–8 refresh/preview | `10ce312`, `4dac758` | PASS |
| 9–11 search/filters/neighbourhood/inspector | recovered blobs | PASS |
| 12–13 layout/projection-2d | recovered blobs + `df7712d` | PASS |
| 14 inspector + controls | `b497b74` | PASS + APPROVED |
| 15 orchestrator | `bc97a42` | PASS + APPROVED |
| 16 desktop 3D scene | `32a15c6` (rewritten after FAIL) | PASS + APPROVED |
| 17 interaction/framing/tiers | `b369bef` (amended after FAIL) | PASS + APPROVED |
| 18 pick benchmark | `37150fc` | measured, PASS |
| 19 broad-phase | — | NOT EXECUTED (evidence-gated) |
| 20 mobile 2D + neighbourhood | `4378ff4` | PASS + APPROVED |
| 21 parity/RTL/a11y | `50c82d8` | PASS + APPROVED |
| 22 performance budgets | `1bc451d` | PASS + APPROVED (5/5 green; evidence numbers independently verified) |
| 23 browser suites | `40d69f1` | 13/13 + 5/5 green |
| 24 acceptance | this file | — |

Plan C completion criterion: `/en/atlas/` and `/fa/atlas/` work against
Atlas API data — desktop 3D (capable), compact/fallback 2D, deep linking,
search, filters, accessible inspector, no-JS semantics, honest fallbacks,
measured budgets — with Hero v2 and Home untouched and no new dependency.
