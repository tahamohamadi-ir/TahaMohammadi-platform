# PUBLIC-190 Visual and Accessibility QA Report

**Packet:** WP-50 (re-run after PUBLIC-180; updated after PUBLIC-270/280)  
**Tool:** Cursor  
**Public-site commit:** `ddb7ae0` (+ overflow fix follow-up on integration branch)  
**Coordination commit:** `856ed5d`  
**Run date:** 2026-09-01  
**Result:** `REVISE`

---

## Automated gate summary (`ddb7ae0` + overflow fix)

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | 183 passed (PUBLIC-260/261 asset promotion, PUBLIC-270/280 visual scaffolds, PUBLIC-230–250 routes) |
| `npm run validate:design` | 0 | 24 components, 6 templates |
| `npm run build` | 0 | 23 static pages; promoted preview/rail/brand masters via Astro image pipeline |
| `npm run validate:seo` | 0 | sitemap-index.xml, robots.txt, canonical/hreflang on sample pages, per-locale Pagefind bundles |
| `npm run test:visual -- --grep PUBLIC-270` | 0 | **36 passed, 1 skipped** (PF-02 detail — no published creative detail route) |
| `npm run test:visual -- --grep PUBLIC-280` | 0 | **12 passed** (PF-01 six-width scaffold; 320px overflow gate green after shell fix) |
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

### F-06 — PUBLIC-280 responsive matrix scaffold (not acceptance)

PF-01 six-width capture harness (320–1440 CSS px) scaffolded. **320px horizontal overflow** on EN creative index cleared via narrow shell utility tightening; overflow gate now applies at all matrix widths.

---

## Verdict

**`REVISE`** — automated gates green including PUBLIC-270/280 visual capture scaffolds; manual owner visual acceptance remains open before `PUBLIC-190` may close.
