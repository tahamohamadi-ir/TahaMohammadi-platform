# PUBLIC-190 Visual and Accessibility QA Report

**Packet:** WP-50 (re-run after PUBLIC-180; updated after PUBLIC-270/280)  
**Tool:** Cursor  
**Public-site commit:** `2b52b6e` (`main` after PUBLIC-300 no-JS crawl audit)
**Coordination commit:** `283578e`  
**Run date:** 2026-09-01  
**Result:** `REVISE`

---

## Automated gate summary (`2b52b6e`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | **191 passed** — unit + PUBLIC-060 font tokens, PUBLIC-260/261 asset promotion, PUBLIC-270/280 visual scaffolds, PUBLIC-290 performance budget scaffold, PUBLIC-300 no-JS audit scaffold, PUBLIC-230–250 routes |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages; promoted preview/rail/brand masters via Astro image pipeline |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang on sample pages, per-locale Pagefind bundles |
| `npm run test:foundation -- --grep PUBLIC-060` | 0 | **4 passed** — home EN/FA body/display computed `font-family`, locale CSS vars, 200% zoom |
| `npm run test:performance` | 0 | **6 passed** - home EN/FA + creative EN LCP/CLS probes, theme-toggle INP on EN home, locale font preloads, font-display swap |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** (PF-02 detail — no published creative detail route) |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **216 passed** (36 locale-route-theme combos × 6 widths; PF-01..PF-08 dual-theme index matrix minus PF-02 detail) |
| `npm run test:nojs` | 0 | **23 passed** — gateway + home + PF index + search crawl with `javaScriptEnabled: false` (PF-02 detail excluded) |
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

---

## Verdict

**`REVISE`** — automated gates green including PUBLIC-060 font computed probes, PUBLIC-270/280 dual-theme visual capture scaffolds, PUBLIC-290 local performance probes, and PUBLIC-300 no-JS crawl audit; manual owner visual acceptance remains open before `PUBLIC-190` may close.
