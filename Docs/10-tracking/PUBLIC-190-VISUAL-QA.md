# PUBLIC-190 Visual and Accessibility QA Report

**Packet:** WP-50 (re-run after PUBLIC-180; updated after PUBLIC-270/280)  
**Tool:** Cursor  
**Public-site commit:** `4931455` (`main` after merge of `cx/public-page-families-280`)  
**Coordination commit:** `f3c367d`  
**Run date:** 2026-09-01  
**Result:** `REVISE`

---

## Automated gate summary (`4931455`)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | unit + PUBLIC-260/261 asset promotion, PUBLIC-270/280 visual scaffolds, PUBLIC-230–250 routes |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages; promoted preview/rail/brand masters via Astro image pipeline |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang on sample pages, per-locale Pagefind bundles |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** (PF-02 detail — no published creative detail route) |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **108 passed** (18 routes × 6 widths; PF-01..PF-08 index matrix minus PF-02 detail) |
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

Six-width capture harness (320–1440 CSS px) now covers PF-01 and PF-03..PF-08 index routes (108 captures). **320px horizontal overflow** on EN creative index cleared via narrow shell utility tightening; overflow gate applies at all matrix widths. PF-02 detail and dual-theme matrix remain open.

### F-07 — PUBLIC-012 Phase 1 CI (not acceptance)

`.github/workflows/ci.yml` added on `main` @ `4931455`: `npm ci`, unit tests, `validate:design`, `validate:seo`, `build` on push/PR. Playwright visual gates remain local-only.

---

## Verdict

**`REVISE`** — automated gates green including PUBLIC-270/280 visual capture scaffolds; manual owner visual acceptance remains open before `PUBLIC-190` may close.
