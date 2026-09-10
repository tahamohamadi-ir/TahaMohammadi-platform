# COORD-080 — R8 Sign-Off Package (Evidence)

Task: COORD-080 — "Visual/public + admin quality matrix sign-off package".
Board deliverable: "`R8` evidence template filled".
Created: 2026-09-02. Evidence refresh: 2026-09-10.

**Status: ALL AGENT-EXECUTABLE R8 GATES GREEN — F-01 OWNER REVIEW RETURNED REVISIONS — R8 NOT YET PASSED.**

Every result below is pinned to the release commit set **PUBLIC `f3e9032` /
ADMIN `f1cfa37` / BACKEND `9c2c704`** and staging release
**`stage-f3e90323-f1cfa37d-9c2c7045`** (2026-09-10). Owner-only cells remain
`____`; agents do not fill owner signatures or accept owner decisions.

R8 gate (`Docs/05-delivery/RELEASE-GATES.md`):
"Accessibility, visual, browser, performance, and security gates pass. Every
deferral is named, owned, and non-blocking."

## Gate rollup

| R8 criterion                         | Section | State @ 2026-09-10                                                              |
| ------------------------------------ | ------- | ------------------------------------------------------------------------------- |
| Visual                               | §1      | Automated captures 39/39 + responsive matrix green; owner review returned revisions (F-01) |
| Accessibility                        | §2      | Automated 31/31 green; keyboard/zoom/reduced-motion specs green; manual SR owner-accepted non-blocking |
| Browser                              | §6      | Live staging smoke 10/10; admin matrix 5/5 (mocked boundary); CI green           |
| Performance                          | §3      | Local budget probes 6/6 green; production field data owner-accepted post-launch  |
| Security                             | §5      | `npm audit` 0 / `pip-audit` 0; secret-scan candidates triaged; none live         |
| Deferrals named, owned, non-blocking | §7      | F-02/F-03/F-05 + manual SR owner-accepted 2026-09-10; only F-01 owner sign-off remains |

---

## §1 Public visual matrix (PUBLIC-270 / PUBLIC-280)

**Evidence on release set (2026-09-10):**

- `npm run review:visual` (build with staging CMS source + PUBLIC-270/WP-40
  capture set, `--workers=1`): **39/39 @visual captures PASS**; compare report
  **43/48 pairs ready** (39 index + 4 PF-02 empty-shell; 5 capture-only Home
  rows have no concept reference). Local artifact:
  `Front-End/public-site/test-results/visual/compare-report.html`.
- Full browser matrix on the CMS-backed build
  (`npx playwright test --workers=4`): **461 passed, 2 skipped, 0 failed**
  (skips: `@visual` atlas specimen requires `DESIGN_ATLAS=1`; staging smoke is
  run separately with the staging env).
- Six-width matrix (`public-280` 320/390/768/1024/1280/1440 × locales × themes)
  and PF-01..PF-08 index captures are inside the 39/39 set; overflow predicate
  green at all widths.
- Prior independent QA references remain: `PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`,
  `PUBLIC-280-RESPONSIVE-MATRIX-EVIDENCE.md`.

`[TODO]` before sign-off (owner actions):

- [x] Owner compare completed on the refreshed compare report (2026-09-10).
- [ ] Revision round: owner-requested fixes applied, captures regenerated, and
  the fixed rows re-reviewed.
- [ ] Accepted capture SHA-256 hashes recorded (`npm run report:signoff-hashes`).
- [ ] PUBLIC-190 verdict moved `REVISE` → `PASS` with owner evidence.

**Owner revision feedback (2026-09-10, verbatim scope):** icons are wrong; no
image should sit below the graphs; graph text is messy; node/child-node
hierarchy is unclear; the concepts are far more professional and beautiful
across the board. Scope: Home EN/FA, Gateway, page families, shared chrome.
Tracked in `PUBLIC-190-VISUAL-QA.md` and `reviews/OWNER-DECISION-2026-09-10.md`.

**Capture-only rows:** the 5 Home rows without a concept reference are accepted
as non-blocking capture-only evidence (owner decision 2026-09-10).

## §2 Accessibility — zoom / keyboard / screen-reader (PUBLIC-190 §3 items)

**Evidence on release set (2026-09-10):**

- `npm run test:a11y`: **31 passed** (route WCAG 2.2 AA scans + foundation
  probes + shell/chrome checks).
- `npm run test:nojs`: **23 passed** — every audited route readable without
  JavaScript, including Home EN/FA with the managed-content contract.
- Keyboard: `wp40-home` keyboard order with visible focus, `ca07` gateway
  keyboard reach, `public-150` shell controls — all green in the matrix run.
- Real 200% zoom: `ca07` gateway 200% spec and `wp40-home` 200%-zoom capture
  spec green in the matrix run.
- Reduced motion: `ca05`, `ca06`, `ca07`, and `scene-polish` live
  preference-change specs green (including the bounded gateway arrival that
  must stop rendering once settled/reduced).
- Empty-heading regression fixed: managed Home headings are omitted until
  published copy exists (PUBLIC `19c6ecd`).

`[TODO]` before sign-off (owner/manual):

- [x] Screen-reader scope decided by owner (2026-09-10): automated axe/landmark
  coverage accepted; manual spot check deferred as non-blocking.

## §3 Performance budgets (PUBLIC-290)

**Evidence on release set (2026-09-10):**

- `npm run test:performance`: **6 passed** — `/en/` and `/fa/` Home LCP/CLS
  within local budget, creative index LCP/CLS, font preloads per locale,
  `font-display: swap`, local INP theme-toggle probe.
- Budget authority: `Docs/06-quality/PERFORMANCE-BUDGET.md` (LCP ≤ 2500 ms p75
  production; CLS ≤ 0.1; INP ≤ 200 ms).
- `PUBLIC-290-PERFORMANCE-BUDGET.md` states local probes are scaffold evidence,
  not a production claim.

`[TODO]` before sign-off:

- [x] Owner decision (2026-09-10): production field measurement accepted as a
  post-launch deferral (non-blocking).

## §4 Admin browser + form-error matrix (ADMIN-290)

**Evidence on release set (2026-09-10):**

- `npm run test:e2e` (Playwright, mocked admin API boundary, real Chromium):
  **5 passed, 1 skipped** — signed-out redirect, MFA challenge → dashboard,
  honest forbidden state, validation blocked before any POST, stale-revision
  reload escape. The skipped spec is the PU-25 live publication journey, which
  requires admin credentials (owner input).
- CI green on `f1cfa37` (run 34506073779: build + unit + e2e).
- Server-side permission enforcement: `Back-End/tests/test_admin_permission_matrix.py`
  (BACKEND-190, closed).
- Form-error contract: `AdminError {code, message, fields?}` per
  `Docs/03-contracts/ERROR-COMPATIBILITY-MATRIX.md`.

`[TODO]` before sign-off (owner input):

- [x] Owner decision (2026-09-10): current scope accepted (mocked-boundary 5/5
  + CI); the live-staging admin journey is deferred as non-blocking.

## §5 Dependency + secret scans

**Evidence on release set (2026-09-10):**

| Repository          | Tool + command                                   | Result on release commit                     |
| ------------------- | ------------------------------------------------ | -------------------------------------------- |
| Public site         | `npm audit --json`                               | 0 vulnerabilities (all severities) @ `f3e9032` |
| Admin panel         | `npm audit --json`                               | 0 vulnerabilities (all severities) @ `f1cfa37` |
| Back-End            | `uv run --with pip-audit pip-audit`              | "No known vulnerabilities found" @ `9c2c704`  |
| All three           | `uvx --from detect-secrets detect-secrets scan`  | candidates triaged, no live secret           |

- Fixed during this cycle: `js-yaml` high advisory (PUBLIC `ddbcef6` / ADMIN
  `3d42995`), `@vitest/mocker` moderate via vitest 4.1.11 (PUBLIC `6f44298` /
  ADMIN `f1cfa37`), Django 5.2.9 → 5.2.17 and pytest 9.0.2 → 9.0.3 (BACKEND
  `9c2c704`).
- Secret-scan candidates are all classified: content hashes and checksums
  (design authority, OpenAPI provenance, font subset coverage, media authority
  checksums), documented local-only development credentials (`.env.example`,
  `docker-compose.dev.yml`, local-operations docs), and test fixtures. No
  production credential is present; production settings fail closed without
  `DJANGO_SECRET_KEY` (`config/settings/production.py`).
- **CI enforcement (2026-09-10):** dependency audit (`npm audit
  --audit-level=high` / `uv run --with pip-audit pip-audit`) and a
  detect-secrets baseline gate were added to all three workflows and are green
  on PUBLIC `da0faac`, ADMIN `58ec81c`, BACKEND `b7bfccb`.

## §6 Browser / integrated gates feeding R8

**Evidence on release set (2026-09-10):**

- Staging release `stage-f3e90323-f1cfa37d-9c2c7045` deployed by workflow run
  34506073682 (success), pinned to the three release SHAs.
- `PUBLIC-320` live staging smoke against
  `https://staging.tahamohamadi.ir`: **10/10 passed** (health, site settings,
  landings EN/FA, gateway, Home EN/FA, About EN/FA, same-origin `/api` proxy).
- Boundaries verified on staging: public routes/API 200; internal
  `/api/v1/internal/*` unavailable through the public edge; every staging
  response carries `X-Robots-Tag: noindex, nofollow, noarchive`.
- Home integration on staging: `data-home-state="ready"`, eight published
  modules per locale, graph 4 nodes / 3 edges / 4 published related records.
- R7 restore drill executed by the deploy workflow (run 34506073682): full
  `pg_dump` + media archive backup, isolated restore into
  `taha_stage_restore_probe`, table-count equality, `migrate --plan` reports no
  pending operations, `manage.py check` clean.
- Contact delivery (owner-approved live probe 2026-09-10): `POST /api/contact`
  → **200** `{"ok": true}`; foreign-origin POST → **400** rejected; owner inbox
  confirmation at the configured recipient (`taha.mohammadi@shahed.ac.ir` per the
  public payload unless `CONTACT_FORM_TO` overrides) pending
  (`R7-contact-delivery-EVIDENCE.md`).
- Live security boundary probes (2026-09-10, no credentials sent):
  `POST /api/v1/admin/auth/login` without CSRF → **403 `CSRF_FAILED`**;
  `/api/v1/admin/content/schema`, `/api/v1/admin/auth/me`,
  `/api/v1/admin/dashboard/summary` unauthenticated → **401**;
  `/api/v1/internal/*` → **404**; admin OpenAPI docs → **404** unless
  authenticated staff + OTP; public landing/home payloads contain **0** draft,
  unpublished, or archived markers.
- CI: PUBLIC run 34506073819, ADMIN run 34506073779, BACKEND run 34506073878 —
  all success.

## §7 Finding / deferral register

Rule: at R8 close every remaining row must be **named, owned, and
non-blocking**. Owner assignments are owner actions — `Owner: ____` placeholders
are not fillable by agents.

| ID      | Finding / deferral                                                                                                        | Blocking gate | State @ 2026-09-10                                                                                              | Owner       |
| ------- | ------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------- | ----------- |
| DEF-005 | Staging restore drill not executed                                                                                        | R7            | **CLOSED** — executed with backup + isolated restore verification on `stage-f3e90323-f1cfa37d-9c2c7045`          | —           |
| F-01    | PUBLIC-190 visual acceptance `REVISE` — owner compare + accepted hashes + sign-off                                        | R8            | **OWNER REVIEWED 2026-09-10 — REVISION REQUIRED**: icons wrong; no image below graphs; messy graph text; unclear node/child-node hierarchy; overall concept quality gap. Scope: Home EN/FA, Gateway, page families, shared chrome. Fix round then re-capture + hashes + sign-off | Owner: ____ |
| F-02    | PF-02 creative detail captures/route                                                                                      | R8            | **OWNER-ACCEPTED 2026-09-10 as non-blocking** — empty-shell captures accepted; published creative detail stays owner CMS content | Owner ✅ |
| F-03    | Production performance telemetry open                                                                                     | R8            | **OWNER-ACCEPTED 2026-09-10 as non-blocking** — post-launch field measurement                                                 | Owner ✅ |
| F-04    | PUBLIC-320 live staging smoke blocked on staging URL                                                                      | R7→R8         | **CLOSED** — 10/10 green on `stage-f3e90323-f1cfa37d-9c2c7045`                                                   | —           |
| F-05    | ADMIN-290 browser matrix not started                                                                                      | R8            | **CLOSED + OWNER-ACCEPTED 2026-09-10** — mocked-boundary 5/5 + CI accepted; live journey deferred as non-blocking              | Owner ✅ |
| F-06    | Dependency/secret scan results not recorded per release commit                                                            | R8            | **CLOSED** — §5 pinned to `f3e9032` / `f1cfa37` / `9c2c704`                                                       | —           |

Owner decisions recorded 2026-09-10 through the platform owner's answer round:
F-02, F-03, F-05, and the manual screen-reader scope are accepted as
non-blocking deferrals. Only F-01 (visual compare + accepted hashes + §8
signature) remains open.

## §8 Owner acceptance block (fill at sign-off — do not prefill)

| Item                               | Value |
| ---------------------------------- | ----- |
| Sections reviewed (§1–§7)          | ____  |
| Deferrals accepted as non-blocking | ____  |
| Owner name                         | ____  |
| Owner signature                    | ____  |
| Date signed                        | ____  |

**Bottom line:** every gate an agent can execute is green and pinned to the
release commit set; F-02/F-03/F-05 and the manual screen-reader scope are
owner-accepted non-blocking deferrals. The owner reviewed the visual evidence
and returned a revision round for F-01 (see §1). R8 passes when the revision
round is fixed, re-captured, and the owner completes §8 with the accepted
hashes. The owner pre-approved the signature as `Taha Mohammadi` /
`2026-09-10`; it is held until F-01 closes.
