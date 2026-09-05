# COORD-080 — R8 Sign-Off Package (Evidence Template)

Task: COORD-080 — "Visual/public + admin quality matrix sign-off package".
Board deliverable: "`R8` evidence template filled".
Created: 2026-09-02.

**Status: TEMPLATE COMPLETE — R8 NOT PASSED.** Sections are prefilled **only**
with evidence that already exists in the repositories; staging- and
owner-dependent results are marked `[TODO]` blocks. No gate below may be claimed
from local or scaffold evidence alone.

R8 gate (`Docs/05-delivery/RELEASE-GATES.md`):
"Accessibility, visual, browser, performance, and security gates pass. Every
deferral is named, owned, and non-blocking."

## Gate rollup

| R8 criterion                         | Section | State @ 2026-09-02                                         |
| ------------------------------------ | ------- | ---------------------------------------------------------- |
| Visual                               | §1      | Automated captures green; owner compare open               |
| Accessibility                        | §2      | Automated 29/29 green; manual §3 items open                |
| Browser                              | §6      | Blocked on staging (`PUBLIC-320` skip / `ADMIN-300` open)  |
| Performance                          | §3      | Local probes green; production field data open             |
| Security                             | §5      | Scan requirement defined; per-commit scan results `[TODO]` |
| Deferrals named, owned, non-blocking | §7      | Register drafted; owners unassigned                        |

---

## §1 Public visual matrix (PUBLIC-270 / PUBLIC-280)

**Existing evidence** (cited, not re-verified here):

- `Front-End/public-site/docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`
  — automated gate @ `27fc859` (2026-09-01): build PASS (23 static pages),
  Vitest 214 PASS, visual capture **36 passed, 1 skipped** (PF-02 detail skipped —
  no published detail route). All manual owner-compare cells `[ ]`.
- `Front-End/public-site/docs/quality/PUBLIC-280-RESPONSIVE-MATRIX-EVIDENCE.md`
  — six-width (320/390/768/1024/1280/1440) dual-theme captures **216 passed**;
  overflow gate at all widths. All manual owner-compare cells `[ ]`; PF-02
  detail open.
- `Docs/10-tracking/PUBLIC-190-VISUAL-QA.md` — verdict **`REVISE`**: manual
  owner visual compare, accepted capture hashes, and explicit sign-off still
  open.

`[TODO]` before sign-off:

- [ ] Owner compare completed per PF row (both files' manual columns marked).
- [ ] PF-02 detail evidence or documented deferral.
- [ ] PUBLIC-190 verdict moved `REVISE` → `PASS` with owner evidence.

## §2 Accessibility — zoom / keyboard / screen-reader (PUBLIC-190 §3 items)

**Existing evidence:**

- `Front-End/public-site/docs/quality/PUBLIC-080-A11Y-AUDIT.md` — automated
  crawl **29 passed** (23 route WCAG 2.2 AA scans + 6 foundation probes) @
  `2f35e6e`; axe tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`.
  Manual keyboard, screen-reader, and zoom matrix explicitly open.
- Required evidence contract: `Front-End/public-site/docs/quality/ACCESSIBILITY.md`
  (keyboard-only use, focus order/visibility, landmarks, labels/errors,
  screen-reader spot checks, 200%/400% zoom, reflow, contrast, RTL, reduced
  motion, non-color cues; "automated scans are necessary but not sufficient").

Manual items from `Docs/10-tracking/PUBLIC-190-VISUAL-QA.md` §3 (all `[TODO]`):

- [ ] Keyboard-only navigation on gateway, home, PF-01..PF-08, search.
- [ ] Real 200% browser zoom on home EN/FA.
- [ ] Screen-reader landmarks and contact form feedback.
- [ ] Reduced-motion review.

## §3 Performance budgets (PUBLIC-290)

**Existing evidence** — `Front-End/public-site/docs/quality/PUBLIC-290-PERFORMANCE-BUDGET.md`:

- Local probes **6 passed** (2026-09-01, loopback static preview): `/en/` LCP
  124 ms / CLS 0.000; `/fa/` LCP 68 ms / CLS 0.000; `/en/creative/` LCP 60 ms /
  CLS 0.000; local INP theme-toggle probe. Font preload verified per locale.
- Budget authority: `Docs/06-quality/PERFORMANCE-BUDGET.md` (LCP ≤ 2500 ms 75th
  percentile production; CLS ≤ 0.1; INP ≤ 200 ms).
- The file itself states: local probes are **scaffold evidence**, not a
  production claim.

`[TODO]` before sign-off:

- [ ] Production 75th-percentile LCP / CLS / INP field data (requires deployed origin).
- [ ] Full route-family probe matrix beyond home + one index.
- [ ] PUBLIC-060 font subset/coverage fixtures (open per PUBLIC-290 deferral table).

## 4 Admin browser + form-error matrix (ADMIN-290)

**Existing state (refreshed 2026-09-04):**

- `ADMIN-290` is now **closed**: `tests/e2e/admin-matrix.e2e.ts` (Playwright,
  mocked admin API boundary, real Chromium) covers signed-out redirect, MFA
  challenge -> dashboard, honest forbidden state, validation blocking create
  before any POST, and stale-revision reload escape; CI runs it
  (`npm run test:e2e`, 5/5 green at `86341e6`). Server-side guard
  _enforcement_ is proven by `Back-End/tests/test_admin_permission_matrix.py`
  (BACKEND-190, closed).
- Form-error expectation: `AdminError {code, message, fields?}` normalized per
  `Docs/03-contracts/ERROR-COMPATIBILITY-MATRIX.md` — preserve `code`, map
  optional `fields`, never assume `request_id`.

`[TODO]` before sign-off (live-staging variant still open):

- [ ] Signed-out redirect — result: automated 5/5 green (mocked boundary); live-staging capture: ____
- [ ] MFA challenge — result: automated green; live-staging capture: ____
- [ ] Forbidden route shows honest state — result: automated green; live-staging capture: ____
- [ ] Validation errors surface (`code/message/fields`) — result: automated green; live-staging capture: ____
- [ ] Stale revision / conflict — result: automated green; live-staging capture: ____
- [ ] ADMIN-290 CI workflow green — result: automated local 5/5; CI run: ____

## §5 Dependency + secret scans

**Existing state:**

- Required check names include "secret/dependency scan" for all three repos —
  `Docs/06-quality/CI-REQUIRED-CHECKS.md`; baseline rule "Dependency and secret
  scanning in CI" — `Docs/06-quality/SECURITY-BASELINE.md`.
- `Docs/06-quality/CI-ROLLOUT-PLAN.md` Phase 2 places dependency/secret scanning
  before release-gating. Workflow files exist in all three repos, but scan
  results against the release commits are not recorded here.

`[TODO]` before sign-off:

- [ ] Back-End: scan tool + run + result on release commit — ____
- [ ] Front-End/public-site: scan tool + run + result — ____
- [ ] Front-End/admin-panel: scan tool + run + result — ____

## §6 Browser / integrated gates feeding R8

R8's "browser" criterion cannot pass on local evidence. Current honest state:

- BACKEND-180 disposable-env smoke: 3/3 pass (server-side only; does not
  substitute for browser acceptance — `Back-End/docs/quality/INTEGRATION-TEST-PLAN.md`).
- PUBLIC-320 live staging smoke: **skip** while `PUBLIC_STAGING_SITE_URL` unset.
- ADMIN-300 integrated staging smoke: open (not scaffolded).
- Staging browser evidence: planned only — see `COORD-060-STAGING-TOPOLOGY-CHECKLIST.md`
  and `COORD-070-STAGING-EVIDENCE-PLAN.md`.

`[TODO]`: attach the COORD-070 evidence set once it exists.

## §7 Finding / deferral register

Rule: at R8 close every remaining row must be **named, owned, and
non-blocking**. Owner assignments are owner actions — `Owner: ____` placeholders
are not fillable by agents.

| ID      | Finding / deferral                                                                                                                 | Blocking gate | Blocking?                                           | Owner       |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------- | ----------- |
| DEF-005 | Staging restore drill not executed (`Docs/10-tracking/DEFERRED-VALIDATION.md`)                                                     | R7            | blocking until drilled                              | Owner: ____ |
| F-01    | PUBLIC-190 visual acceptance `REVISE` — independent QA PASS + owner sign-off required (`Docs/10-tracking/PUBLIC-190-VISUAL-QA.md`) | R8            | blocking                                            | Owner: ____ |
| F-02    | PF-02 creative detail captures/route open (PUBLIC-270/280)                                                                         | R8            | blocking until evidence or deferral accepted        | Owner: ____ |
| F-03    | Production performance telemetry open (PUBLIC-290)                                                                                 | R8            | non-blocking if accepted as post-launch measurement | Owner: ____ |
| F-04    | PUBLIC-320 live staging smoke blocked on staging URL                                                                               | R7→R8         | blocking until staging exists                       | Owner: ____ |
| F-05    | ADMIN-290 browser matrix not started                                                                                               | R8            | blocking                                            | Owner: ____ |
| F-06    | Dependency/secret scan results not recorded per release commit                                                                     | R8            | blocking until recorded                             | Owner: ____ |

`[TODO]`: resolve or accept every row as non-blocking before owner sign-off.

## §8 Owner acceptance block (fill at sign-off — do not prefill)

| Item                               | Value |
| ---------------------------------- | ----- |
| Sections reviewed (§1–§7)          | ____  |
| Deferrals accepted as non-blocking | ____  |
| Owner name                         | ____  |
| Owner signature                    | ____  |
| Date signed                        | ____  |

**Bottom line:** template complete as a coordination deliverable. R8 remains
**not passed**; this package may only be signed after §1–§7 `[TODO]` items
close and every register row is owned and non-blocking.
