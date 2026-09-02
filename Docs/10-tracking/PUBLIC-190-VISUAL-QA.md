# PUBLIC-190 Visual and Accessibility QA Report

**Packet:** WP-50 (re-run after PUBLIC-180; updated after PUBLIC-270/280)  
**Tool:** Cursor  
**Public-site commit:** `cc4b851` (viewport-aware home visual compare pairing)
**Coordination commit:** `af24876`
**Run date:** 2026-09-02  
**Result:** `REVISE`

---

## PF-01..PF-08 structural empty-state (`7c6efc3`)

Prep owner review flagged PF-01..PF-08 index routes as bare `ContentState` vs page-family concepts (hero, filter/section shells, list/grid placeholders). Public-site now renders **structural empty chrome** on index routes when published API content is absent:

| PF | Family | Empty chrome |
|---|---|---|
| PF-01 | Creative | Hero, disabled filter shell, grid placeholder (`07f876f`) |
| PF-03 | Writing | Hero, disabled filter tabs + search shell, list placeholders |
| PF-04 | Projects | Hero, disabled filter chips + search shell, row placeholders |
| PF-05 | Research | Hero, disabled section tabs, graph placeholder, focus-area shell |
| PF-05 | Publications | Hero, disabled filter chips + search shell, row placeholders |
| PF-06 | Teaching | Hero, disabled filter tabs + search shell, list placeholders |
| PF-07 | About | Hero, intro/education/experience section shells |
| PF-07 | CV | Hero, downloads section placeholders |
| PF-08 | Contact | Hero, topic chips, details + disabled form shell |

All families keep honest `ContentState` `empty` copy — no invented records, titles, dates, or images. `template-base.css` uses `box-sizing: border-box` on `tm-template__main` for PUBLIC-280 @320 overflow.

PF-01..PF-08 captures regenerated (PUBLIC-270 ×36, PUBLIC-280 ×216, WP-40 home ×8). Compare report **39 / 48** pairs ready (viewport-aware home pairing @ `cc4b851`). Visual alignment improved; owner manual compare and sign-off still required — **does not change verdict to PASS**.

---

## PF-01 structural empty-state (`07f876f`) — superseded by table above

---

## Owner visual review artifacts (`3a54130`)

Captures regenerated 2026-09-01 in one Playwright session (avoids `test-results/` wipe between runs).

| Artifact | Value |
|---|---|
| PNG capture count | **44** (`test-results/visual/*.png`) — 36 PUBLIC-270 index + 8 WP-40 home/gateway |
| Compare report | `Front-End/public-site/test-results/visual/compare-report.html` |
| Pairs ready | **39 / 48** (PF-02 detail ×4 optional; EN 768/200% and FA dark 768 are capture-only — no width-matched concept) |
| Regenerate | `cd Front-End/public-site && npm run build && npx playwright test --grep "PUBLIC-270\|WP-40 home captures\|WP-40 home and gateway capture" --workers=1 && npm run report:visual-compare` |

Open `compare-report.html` locally for side-by-side concept comparison. Does **not** change verdict to PASS.

### One-sitting quick start (owner)

Captures and `compare-report.html` are **gitignored** — they exist only on the machine that ran the Playwright session above. If missing, run the **Regenerate** command in the artifacts table first.

1. Open `Front-End/public-site/test-results/visual/compare-report.html` in a browser (double-click or `file://` URL).
2. Review each side-by-side pair (39 with concept references; EN 768/200% and FA dark @768 capture-only). Note deviations inline or below.
3. Complete **§3 Manual accessibility checks** on a running `npm run preview` build (or `dist/` static server).
4. Paste accepted capture SHA-256 hashes into **§4 Sign-off evidence** (hashes shown in compare-report).
5. Check manual compare columns in `Front-End/public-site/docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`.
6. Change **Result** at top of this report from `REVISE` to `PASS` only after explicit owner approval.

---

## Automated gate summary (`cc4b851`)

Full local gate sweep @ `cc4b851` (2026-09-02). Playwright suites run with `--workers=1` after clean `dist/` rebuild between commands.

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **228 passed** — includes `public-270-visual-compare.test.ts` viewport-aware home pairing |
| `npm run lint` | 0 | ESLint flat config |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run validate:seo` | 0 | sitemap, canonical/hreflang, Pagefind bundles |
| `npm run build` | 0 | 23 static pages |
| `npm run test:foundation` | 0 | **6 passed** |
| `npm run test:performance` | 0 | **6 passed** |
| `npm run test:nojs` | 0 | **23 passed** |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** — PF-02 detail open |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **216 passed** |
| `npm run test:visual -- --grep "PUBLIC-270\|WP-40 home"` | 0 | **38 passed, 1 skipped** — WP-40 home ×8 |
| `npm run report:visual-compare` | 0 | **39 / 48** honest pairs (home viewport-aware pairing @ `cc4b851`) |
| GitHub Actions CI @ `cc4b851` | pass | [run 33576370767](https://github.com/tahamohammadi-ir/TahaMohammadi-platform-FrontEnd-publicSite/actions/runs/33576370767) — `main`; [run 33576373403](https://github.com/tahamohammadi-ir/TahaMohammadi-platform-FrontEnd-publicSite/actions/runs/33576373403) — `cx/public-recovery-integration` |

### Prior gate summary (`7c6efc3`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **228 passed** — PF-03..PF-08 structural empty-state behavior tests |
| `npm run lint` | 0 | ESLint flat config |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run validate:seo` | 0 | sitemap, canonical/hreflang, Pagefind bundles |
| `npm run build` | 0 | 23 static pages |
| `npm run test:nojs` | 0 | **23 passed** |
| `npm run test:visual -- --grep "PUBLIC-270\|WP-40 home"` | 0 | **38 passed, 1 skipped** — PF-02 detail open; WP-40 home ×8 |
| `npm run report:visual-compare` | 0 | **39 / 48** pairs ready (44 PNGs; home pairing fixed @ `cc4b851`) |
| GitHub Actions CI @ `7c6efc3` | pass | [run 33575027666](https://github.com/tahamohammadi-ir/TahaMohammadi-platform-FrontEnd-publicSite/actions/runs/33575027666) — `main`; [run 33575042389](https://github.com/tahamohammadi-ir/TahaMohammadi-platform-FrontEnd-publicSite/actions/runs/33575042389) — `cx/public-recovery-integration` |

### Prior gate summary (`3a54130`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **228 passed** — includes `public-270-visual-compare.test.ts` harness |
| `npm run lint` | 0 | ESLint flat config (Astro + TypeScript + Prettier disable) |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro`; byte-pinned paths excluded via `.prettierignore` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang, per-locale Pagefind bundles |
| `npm run build` | 0 | 23 static pages |
| `npm run test:foundation` | 0 | **6 passed** — WP-10 theme + PUBLIC-060 locale font computed styles |
| `npm run test:performance` | 0 | **6 passed** — home EN/FA + creative EN LCP/CLS, font preloads, font-display swap, theme-toggle INP (1 flaky retry on first run) |
| `npm run test:nojs` | 0 | **23 passed** — gateway, home, PF index routes, search with JS disabled |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** — PF-02 creative detail open |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **216 passed** — 6 widths × 2 locales × 2 themes on PF-01, PF-03..PF-08 index routes |
| `npm run test:smoke` | 0 | **1 skipped** — `PUBLIC_STAGING_SITE_URL` unset (expected until BACKEND-180 staging) |
| `npm run report:visual-compare` | 0 | **43 / 48** pairs ready from 44 PNG captures (see Owner visual review artifacts) |
| GitHub Actions CI @ `3a54130` | pass | [run 33569434903](https://github.com/tahamohamadi-ir/TahaMohammadi-platform-FrontEnd-publicSite/actions/runs/33569434903) — lint, format check, unit, design, SEO, build |

### Prior gate summary (`faafdac`)

Full local gate sweep @ `faafdac` / coordination `a07b49f` (2026-09-01). Playwright suites run with clean `dist/` between commands to avoid Windows concurrent-build corruption.

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **223 passed** — home published-link gating, PUBLIC-212 parent-family coverage |
| `npm run lint` | 0 | ESLint flat config (Astro + TypeScript + Prettier disable) |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro`; byte-pinned paths excluded via `.prettierignore` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang, per-locale Pagefind bundles |
| `npm run test:foundation` | 0 | **6 passed** — WP-10 theme + PUBLIC-060 locale font computed styles |
| `npm run test:performance` | 0 | **6 passed** — home EN/FA + creative EN LCP/CLS, font preloads, font-display swap, theme-toggle INP |
| `npm run test:nojs` | 0 | **23 passed** — gateway, home, PF index routes, search with JS disabled |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** — PF-02 creative detail open |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **216 passed** — 6 widths × 2 locales × 2 themes on PF-01, PF-03..PF-08 index routes |
| `npm run test:smoke` | 0 | **1 skipped** — `PUBLIC_STAGING_SITE_URL` unset (expected until BACKEND-180 staging) |
| CI workflow | present | `.github/workflows/ci.yml` — lint, format check, unit, design, SEO, build on push/PR |
| Atlas leak check | pass | no `/_design` in production build |

### Prior gate summary (`fad71e0`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **223 passed** — includes home published-link gating, PUBLIC-212 parent-family coverage |
| `npm run lint` | 0 | ESLint flat config (Astro + TypeScript + Prettier disable) |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro`; byte-pinned paths excluded via `.prettierignore` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang, per-locale Pagefind bundles |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** — re-run 2026-09-01 @ `fad71e0`; PF-02 detail open |
| `npm run test:visual -- --grep PUBLIC-280` | not re-run | Last green on `f3acb24` (216 passed) |
| `npm run test:nojs` | not re-run | Last green on `f3acb24` (23 passed) |
| `npm run test:foundation` | not re-run | Last green on `f3acb24` (6 passed) |
| `npm run test:performance` | not re-run | Last green on `f3acb24` (6 passed) |
| `npm run test:smoke` | not re-run | Last run on `95df072` (1 skipped) |
| CI workflow | present | `.github/workflows/ci.yml` — lint, format check, unit, design, SEO, build on push/PR |
| Atlas leak check | pass | no `/_design` in production build |

### Prior gate summary (`f3acb24`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **205 passed** — includes `public-011.toolchain.test.ts`; contract fixtures re-synced with backend authoritative copies |
| `npm run lint` | 0 | ESLint flat config (Astro + TypeScript + Prettier disable) |
| `npm run format:check` | 0 | Prettier + `prettier-plugin-astro`; byte-pinned paths excluded via `.prettierignore` |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang, per-locale Pagefind bundles |
| `npm run test:foundation -- --grep PUBLIC-060` | not re-run | Last green on `95df072` (4 passed) |
| `npm run test:performance` | not re-run | Last green on `95df072` (6 passed) |
| `npm run test:visual -- --grep PUBLIC-270` | not re-run | Last green on `95df072` (36 passed, 1 skipped) |
| `npm run test:visual -- --grep PUBLIC-280` | not re-run | Last green on `95df072` (216 passed) |
| `npm run test:nojs` | not re-run | Last green on `95df072` (23 passed) |
| `npm run test:smoke` | not re-run | Last run on `95df072` (1 skipped) |
| CI workflow | present | `.github/workflows/ci.yml` — lint, format check, unit, design, SEO, build on push/PR |
| Atlas leak check | pass | no `/_design` in production build |

### Prior gate summary (`95df072`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **201 passed** — unit + PUBLIC-060 font tokens, PUBLIC-260/261 asset promotion, PUBLIC-270/280 visual scaffolds, PUBLIC-290 performance budget scaffold, PUBLIC-300 no-JS audit scaffold, PUBLIC-310 contract fixture validation, PUBLIC-320 staging smoke scaffold, PUBLIC-230–250 routes |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages; promoted preview/rail/brand masters via Astro image pipeline |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang on sample pages, per-locale Pagefind bundles |
| `npm run test:foundation -- --grep PUBLIC-060` | 0 | **4 passed** — home EN/FA body/display computed `font-family`, locale CSS vars, 200% zoom |
| `npm run test:performance` | 0 | **6 passed** - home EN/FA + creative EN LCP/CLS probes, theme-toggle INP on EN home, locale font preloads, font-display swap |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** (PF-02 detail — no published creative detail route) |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **216 passed** (36 locale-route-theme combos × 6 widths; PF-01..PF-08 dual-theme index matrix minus PF-02 detail) |
| `npm run test:nojs` | 0 | **23 passed** — gateway + home + PF index + search crawl with `javaScriptEnabled: false` (PF-02 detail excluded) |
| `npm run test:smoke` | 0 | **1 skipped** — Playwright `@smoke` probes skip until `PUBLIC_STAGING_SITE_URL` + `BACKEND-180` staging |
| CI workflow | present | `.github/workflows/ci.yml` — unit, design, SEO, build on push/PR |
| Atlas leak check | pass | no `/_design` in production build |

---

## Findings

### F-01 — PUBLIC-180 ✅ cleared (2026-09-01)

Dedicated `ContentState` components with matrix tests landed in `f1e57a6`. Re-verified on subsequent commit with 118 Vitest tests.

### F-02 — Manual visual acceptance (blocking)

Owner/concept comparison matrix and screenshot SHA-256 evidence still required per `VISUAL-QA-CONTRACT.md`. PUBLIC-270 automated index captures at 1440/390 are green (36 passed); manual owner compare columns remain open.

### F-03 — Page-family utility routes expanded

`PUBLIC-230` Contact/CV and `PUBLIC-240` Search routes are built with API-only/unavailable honesty. `PUBLIC-250` adds sitemap, robots, and `validate:seo` gate. Header links for contact, cv, and search resolve to built pages.

### F-04 — Asset promotion Group A/B staged (not visual acceptance)

`PUBLIC-260` (decorative atmosphere) and `PUBLIC-261` (project previews, rail decorative, brand shell) promote masters to `src/assets/media`, wire Header/Footer to `PromotedPicture brand.mark`, and remove legacy `public/media` copies. Runtime contract staged per ledger; manual concept comparison and owner sign-off still required.

### F-05 — PUBLIC-270 visual capture scaffold (not acceptance)

Playwright `@visual` stubs capture PF-01..PF-08 index routes at 1440 and 390 CSS px. Evidence checklist: `Front-End/public-site/docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`. PF-02 detail remains skipped until a published creative detail route exists in the static build.

### F-06 — PUBLIC-280 responsive matrix expanded (not acceptance)

Six-width dual-theme capture harness (320–1440 CSS px, light + dark) now covers PF-01 and PF-03..PF-08 index routes (216 captures). **320px horizontal overflow** on EN creative index cleared via narrow shell utility tightening; overflow gate applies at all matrix widths. PF-02 detail remains open.

### F-07 — PUBLIC-012 Phase 1 CI (not acceptance)

`.github/workflows/ci.yml` added on `main` @ `4931455`: `npm ci`, unit tests, `validate:design`, `validate:seo`, `build` on push/PR. Playwright visual gates remain local-only.

### F-08 — PUBLIC-290 performance budget scaffold (not acceptance)

`cx/public-page-families-290` merged to `main` @ `e65b1ec`: local LCP/CLS probes on home EN/FA and creative EN, locale font-preload contract, and `font-display: swap` CSS gate. Evidence: `docs/quality/PUBLIC-290-PERFORMANCE-BUDGET.md`. Production 75th-percentile telemetry and font CLS/preload budget closure remain open (`PUBLIC-290` stays `[~]`).

### F-09 — PUBLIC-060 locale font computed-style probes (not acceptance)

`cx/public-page-families-060` merged to `main` @ `56658c4`: Playwright `@foundation` computed-style checks on home EN/FA for `--font-display` / `--font-body` locale wiring, body + h1 `font-family`, and 200% root font-size stability. Evidence: `docs/quality/PUBLIC-060-FONT-COMPUTED-EVIDENCE.md`. FONT-ACQUISITION-PLAN subset/coverage fixtures remain open.

### F-10 — PUBLIC-300 no-JS crawl audit (not acceptance)

`cx/public-page-families-300` merged to `main` @ `2b52b6e`: Playwright `@nojs` crawl of all 23 static build routes with JavaScript disabled — gateway, home EN/FA, PF-01 and PF-03..PF-08 index routes, and search utility. Evidence: `docs/quality/PUBLIC-300-NO-JS-AUDIT.md`. PF-02 creative detail excluded until a published detail route exists; search results with `?q=` remain a progressive-enhancement surface.

### F-11 — PUBLIC-310 contract fixture tests (not acceptance)

`main` @ `111a96e`: consumer fixtures under `tests/fixtures/contracts/` byte-aligned with backend authoritative copies; Vitest validates OpenAPI component shapes, error matrix rows, and LF-canonical hash pinning. Evidence: `docs/quality/PUBLIC-310-CONTRACT-FIXTURES.md`.

### F-12 — PUBLIC-320 integrated staging smoke scaffold (not acceptance)

`main` @ `95df072`: staging harness (`src/test-harness/staging-smoke.ts`), Vitest env-contract tests, and Playwright `@smoke` probes via `npm run test:smoke` / `playwright.staging.config.ts`. Live probes skip honestly when `PUBLIC_STAGING_SITE_URL` is unset (requires `BACKEND-180` staging deployment). Evidence: `docs/quality/PUBLIC-320-STAGING-SMOKE.md`. Does **not** close `PUBLIC-190` or claim production readiness.

### F-13 — PUBLIC-011 ESLint + Prettier toolchain (not acceptance)

`main` @ `b12b017`: `eslint.config.js`, `.prettierrc` + `prettier-plugin-astro`, `npm run lint` / `format:check`, CI lint/format steps, and `public-011.toolchain.test.ts`. Initial Prettier pass excludes byte-pinned design authority and contract fixture paths. Consumer contract fixtures re-synced with current backend authoritative copies for green `PUBLIC-310` gate. Does **not** close `PUBLIC-190`.

### F-14 — PUBLIC-013 architecture decision records (not acceptance)

`main` @ `3652fc6`: repository-local ADRs in `docs/architecture/` for npm, Astro static `fa`/`en` routing, static `dist/` deployment, Vitest + Playwright tag matrix, and Chromium/WCAG 2.2 AA browser targets; `src/public-013.adr.test.ts` guard. Does **not** close `PUBLIC-190`.

### F-15 — PUBLIC-350 release evidence scaffold (not acceptance)

Gate sweep on `f3acb24` re-ran Playwright foundation (6), performance (6), PUBLIC-280 visual (216), and no-JS (23) — all green after clean `dist/` rebuild. `PUBLIC-350` ships `docs/quality/PUBLIC-350-RELEASE-EVIDENCE.md`, `src/test-harness/release-evidence.ts`, and `public-350.release-evidence.test.ts` with honest `ready: false` until owner acceptance, staging smoke, and frozen page-family routes close. Does **not** close `PUBLIC-190` or mark R4/R8 complete.

### F-16 — Home featured cards link to seed slugs without API-backed detail routes ✅ cleared (code)

Home featured projects and publications still render from `src/lib/home-content.ts` seed copy with draft notes. At build time, `fetchPublishedHomeLinkSlugs` queries published API slug sets; `HomeFeaturedProjects` and `HomeFeaturedPublications` omit detail `href` values unless the seed slug exists in the published set. Cards remain visible as draft previews; links appear automatically when owner publishes matching API records. Evidence: `home-published-links.ts`, `home-published-links.test.ts`, updated `wp40-home.behavior.test.ts`.

### F-17 — Page-family routes implemented but frozen (not acceptance)

`PUBLIC-201` through `PUBLIC-221` and `PUBLIC-212` (books/talks/downloads embedded in parent families per `ROUTE-REGISTRY.md`) have routes, loaders, and behavior tests on `main`. TASK-LIST updated — implemented; frozen pending visual acceptance. Does **not** unfreeze recovery or close `PUBLIC-190`.

### F-18 — Owner visual compare assist (not acceptance)

`scripts/page-family-visual-compare.mjs` maps PUBLIC-270 captures to concept references; `npm run report:visual-compare` generates HTML side-by-side report from existing PNGs with SHA-256 hashes for owner sign-off. Evidence checklist updated in `docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`. Does **not** close `PUBLIC-190` or change verdict to PASS.

### F-19 — CI standalone repo fixes (not acceptance)

Vitest spawn uses cross-platform `npm` (not `npm.cmd` on Linux). PUBLIC-310/PUBLIC-350 skip workspace-sibling checks when Back-End/coordination repos are absent in standalone GitHub CI. Does **not** close `PUBLIC-190`.

### F-20 — CI green @ `3a54130` + visual-compare formatting (not acceptance)

`main` @ `3a54130`: removes unused `scriptDir` in CI-related scripts; Prettier pass on visual-compare tooling. GitHub Actions green on standalone repo. Does **not** close `PUBLIC-190` or change verdict to PASS.

---

## Owner action required (blocking `PUBLIC-190` PASS)

Complete these steps manually; agents cannot claim visual acceptance.

### 1. Concept comparison matrix

Compare each implementation screenshot against the matching concept at the same viewport, locale, theme, and content state per `Docs/04-design/VISUAL-QA-CONTRACT.md`.

| PF | Concept reference | Capture paths (1440 / 390) |
|---|---|---|
| PF-01 | `concepts/page-families/creative-index-light.png` | `Front-End/public-site/test-results/visual/public-270-pf01-{en\|fa}-{1440\|390}-light.png` |
| PF-03 | `writing-index-light.png` | `public-270-pf03-{en\|fa}-{1440\|390}-light.png` |
| PF-04 | `projects-index-dark.png` | `public-270-pf04-{en\|fa}-{1440\|390}-dark.png` |
| PF-05 | `research-publications-index-light.png` | `public-270-pf05-research-{en\|fa}-{1440\|390}-light.png`, `public-270-pf05-publications-{en\|fa}-{1440\|390}-light.png` |
| PF-06 | `teaching-index-dark.png` | `public-270-pf06-{en\|fa}-{1440\|390}-dark.png` |
| PF-07 | `about-cv-light.png` | `public-270-pf07-about-{en\|fa}-{1440\|390}-light.png`, `public-270-pf07-cv-{en\|fa}-{1440\|390}-light.png` |
| PF-08 | `contact-dark.png` | `public-270-pf08-{en\|fa}-{1440\|390}-dark.png` |
| Home | `concepts/home-*.png` (see mapping table in `PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`) | Run `npm run test:visual -- --grep "WP-40 home captures"` then `npm run report:visual-compare` |

**Owner compare assist:** `npm run report:visual-compare` generates `test-results/visual/compare-report.html` — side-by-side pairs from existing PNGs. Does **not** change verdict to PASS.

**Regenerate captures:** `cd Front-End/public-site && npm run build && npm run test:visual -- --grep PUBLIC-270`

### 2. Home page review

WP-40 visual captures use **768px reflow** and **200% zoom** evidence (not 1440/390 — those widths apply to PF index routes in PUBLIC-270). See compare-report **Home** section and `scripts/page-family-visual-compare.mjs` `HOME_VISUAL_ENTRIES`.

**Agent audit @ `7c6efc3` (2026-09-02):** Home structure matches WP-40 authority (orbit hero + tokenized scrim, semantic graph list, section slots). FA 768 pairs against `home-mobile-fa-light-concept-v1.png` (narrow reference); overlay-hero vs side-by-side concept layout reflects WP-40 implementation direction, not missing chrome. **No home code changes warranted.**

**Compare mapping fix @ `cc4b851` (2026-09-02):** `resolveHomeConceptReference()` stops pairing 768px/720px EN captures with 1440 desktop composition concepts. FA light @768/200% keeps `home-mobile-fa-light-concept-v1.png` (390 mobile authority). Gateway 200% now pairs with `language-gateway-dark-concept-v1.png` (layout/affordance only — capture is light). Pairs **43 → 39** (removed 5 misleading home pairs; added 1 gateway pair). EN 768/200% and FA dark @768 show capture-only in compare-report.

- [ ] Compare home FA **768px light** and **200% zoom** captures against mobile concept in compare-report.
- [ ] Review home EN **768px** and **200% zoom** captures (capture-only — no EN tablet concept in authority).
- [ ] Review **gateway 200% zoom** vs dark gateway concept (theme differs; compare language-choice affordance only).
- [x] Verify draft notes on featured projects/publications are acceptable for owner preview.
- [x] Home card link strategy (F-16): link only when slug exists in published API at build; otherwise non-link cards.

### 3. Manual accessibility checks

- [ ] Keyboard-only navigation on gateway, home, PF-01..PF-08, search.
- [ ] Real 200% browser zoom on home EN/FA.
- [ ] Screen-reader landmarks and contact form feedback.
- [ ] Reduced-motion review.

### 4. Sign-off

- [ ] Record SHA-256 hashes of accepted screenshots in the table below (copy from compare-report).
- [ ] Mark manual compare columns in `docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`.
- [ ] Explicit owner approval to change verdict from `REVISE` to `PASS`.

#### Sign-off evidence (owner fills)

| Capture file | SHA-256 (from compare-report) | Accepted |
|---|---|:---:|
| _(e.g. `public-270-pf01-en-1440-light.png`)_ | | [ ] |
| _(add rows for each accepted pair)_ | | |

---

## Verdict

**`REVISE`** — Home compare mappings fixed @ `cc4b851` (`resolveHomeConceptReference`; 39/48 honest pairs); PF-01..PF-08 structural empty-state @ `7c6efc3`; GitHub CI green; manual owner visual acceptance and a11y still open before `PUBLIC-190` may close.

**Goal complete:** NO — owner visual compare, manual a11y, and explicit sign-off still required.
