# PUBLIC-190 Visual Remediation Plan

**Packet:** PUBLIC-190 gap analysis (analysis + plan only — does **not** set PASS)  
**Public-site base:** `0e6a552` (Phase 6 writing/creative chrome; prior evidence grid @ `cf81f6f`; Path A + shared footer/PF shells + home FA hero reflow @ `cfce6b4`; prior pagination @ `dd515a0`)  
**Compare pairing fix:** `c14508a` (`page-family-visual-compare.mjs` concept root)  
**Generated:** 2026-09-02 (gate tip stamped 2026-09-04)  
**Pairs analyzed:** **48 / 48** (39 ready + 5 capture-only + 4 blocked-route)  
**Asset prompts:** [`PUBLIC-190-asset-prompts/`](./PUBLIC-190-asset-prompts/) (sibling agent 65eccafb — stub IDs linked below; populate prompt files as delivered)  
**QA verdict:** remains `REVISE` — owner manual compare + sign-off still required

---

## Executive summary

Owner feedback (2026-09-02, Persian): **concepts read much weaker than implementation** in side-by-side compare — meaning promoted empty-state chrome exists but **visual density, asset diversity, section fidelity, and dark/light token application** still diverge materially from design authority. Path A @ `dd515a0` improved pagination/theme-explore shells and hero proportions but did not close the gap.

**Top P0 themes across families:**

1. **Missing sections** — Projects Evidence Available grid; Writing newsletter band; Research constellation graph fidelity.
2. **Asset monotony** — Hero/list thumbnails reuse `home.rail.preview` / single project preview across PF families.
3. **Row/card chrome** — Numbered project rows, sanitized badges, bibliography type chips, teaching level/duration columns.
4. **Footer upgrade** — 4-column EXPLORE/RESOURCES/CONNECT with social links and location (currently 3-col + placeholders).
5. **Nav label drift** — Creative/Writing/Teaching vs Gallery/Blog/Learning (Category D — owner decision).
6. **PF-02 detail blocked** — No static build route; 4 compare rows cannot capture.
7. **CMS Category A** — All record titles, excerpts, tags remain blocked; shells must not invent copy.

**Phased delivery (Phase 0–8):**

| Phase | Focus | Families / pairs |
|------:|-------|------------------|
| 0 | Shared foundations — footer 4-col, display serif tokens, CTA band, sub-nav active states | All |
| 1 | Header/nav label decision + active underline tokens | All ready pairs |
| 2 | About/CV profile hero, tri-CTA, timeline/skills fidelity | PF-07 ×8 |
| 3 | Contact portal hero, topic cards, form parity | PF-08 ×4 |
| 4 | Research constellation + publications bibliography | PF-05 ×8 |
| 5 | Projects evidence grid + row chrome; Teaching path/list | PF-04 ×4, PF-06 ×4 |
| 6 | Creative masonry + featured; Writing theme-explore + newsletter | PF-01 ×4, PF-03 ×4 |
| 7 | Creative detail template (when route unblocked) | PF-02 ×4 |
| 8 | Home FA mobile + gateway 200% affordance | HOME ×8 |

**Allowed libraries (per owner mandate):** GSAP, Motion, Three.js, Canvas, SVG — prefer CSS-first per `ADR-ANIMATION.md`; reach for islands only when concept fidelity requires it (constellation, gallery carousel).

---

## Executive summary table (48 pairs)

| Pair ID | Capture | Concept | Locale | Viewport | Theme | Compare status | Severity | Phase |
|---------|---------|---------|--------|----------|-------|----------------|----------|-------|
| PF-01-pf01-EN-1440-LIGHT | public-270-pf01-en-1440-light.png | creative-index-light.png | en | 1440 | light | ready | High | Phase 6 |
| PF-01-pf01-EN-390-LIGHT | public-270-pf01-en-390-light.png | creative-index-light.png | en | 390 | light | ready | High | Phase 6 |
| PF-01-pf01-FA-1440-LIGHT | public-270-pf01-fa-1440-light.png | creative-index-light.png | fa | 1440 | light | ready | High | Phase 6 |
| PF-01-pf01-FA-390-LIGHT | public-270-pf01-fa-390-light.png | creative-index-light.png | fa | 390 | light | ready | High | Phase 6 |
| PF-03-pf03-EN-1440-LIGHT | public-270-pf03-en-1440-light.png | writing-index-light.png | en | 1440 | light | ready | High | Phase 6 |
| PF-03-pf03-EN-390-LIGHT | public-270-pf03-en-390-light.png | writing-index-light.png | en | 390 | light | ready | High | Phase 6 |
| PF-03-pf03-FA-1440-LIGHT | public-270-pf03-fa-1440-light.png | writing-index-light.png | fa | 1440 | light | ready | High | Phase 6 |
| PF-03-pf03-FA-390-LIGHT | public-270-pf03-fa-390-light.png | writing-index-light.png | fa | 390 | light | ready | High | Phase 6 |
| PF-04-pf04-EN-1440-DARK | public-270-pf04-en-1440-dark.png | projects-index-dark.png | en | 1440 | dark | ready | Critical | Phase 5 |
| PF-04-pf04-EN-390-DARK | public-270-pf04-en-390-dark.png | projects-index-dark.png | en | 390 | dark | ready | Critical | Phase 5 |
| PF-04-pf04-FA-1440-DARK | public-270-pf04-fa-1440-dark.png | projects-index-dark.png | fa | 1440 | dark | ready | Critical | Phase 5 |
| PF-04-pf04-FA-390-DARK | public-270-pf04-fa-390-dark.png | projects-index-dark.png | fa | 390 | dark | ready | Critical | Phase 5 |
| PF-05-pf05-research-EN-1440-LIGHT | public-270-pf05-research-en-1440-light.png | research-publications-index-light.png | en | 1440 | light | ready | Critical | Phase 4 |
| PF-05-pf05-research-EN-390-LIGHT | public-270-pf05-research-en-390-light.png | research-publications-index-light.png | en | 390 | light | ready | Critical | Phase 4 |
| PF-05-pf05-research-FA-1440-LIGHT | public-270-pf05-research-fa-1440-light.png | research-publications-index-light.png | fa | 1440 | light | ready | Critical | Phase 4 |
| PF-05-pf05-research-FA-390-LIGHT | public-270-pf05-research-fa-390-light.png | research-publications-index-light.png | fa | 390 | light | ready | Critical | Phase 4 |
| PF-05-pf05-publications-EN-1440-LIGHT | public-270-pf05-publications-en-1440-light.png | research-publications-index-light.png | en | 1440 | light | ready | High | Phase 4 |
| PF-05-pf05-publications-EN-390-LIGHT | public-270-pf05-publications-en-390-light.png | research-publications-index-light.png | en | 390 | light | ready | High | Phase 4 |
| PF-05-pf05-publications-FA-1440-LIGHT | public-270-pf05-publications-fa-1440-light.png | research-publications-index-light.png | fa | 1440 | light | ready | High | Phase 4 |
| PF-05-pf05-publications-FA-390-LIGHT | public-270-pf05-publications-fa-390-light.png | research-publications-index-light.png | fa | 390 | light | ready | High | Phase 4 |
| PF-06-pf06-EN-1440-DARK | public-270-pf06-en-1440-dark.png | teaching-index-dark.png | en | 1440 | dark | ready | High | Phase 5 |
| PF-06-pf06-EN-390-DARK | public-270-pf06-en-390-dark.png | teaching-index-dark.png | en | 390 | dark | ready | High | Phase 5 |
| PF-06-pf06-FA-1440-DARK | public-270-pf06-fa-1440-dark.png | teaching-index-dark.png | fa | 1440 | dark | ready | High | Phase 5 |
| PF-06-pf06-FA-390-DARK | public-270-pf06-fa-390-dark.png | teaching-index-dark.png | fa | 390 | dark | ready | High | Phase 5 |
| PF-07-pf07-about-EN-1440-LIGHT | public-270-pf07-about-en-1440-light.png | about-cv-light.png | en | 1440 | light | ready | Critical | Phase 2 |
| PF-07-pf07-about-EN-390-LIGHT | public-270-pf07-about-en-390-light.png | about-cv-light.png | en | 390 | light | ready | Critical | Phase 2 |
| PF-07-pf07-about-FA-1440-LIGHT | public-270-pf07-about-fa-1440-light.png | about-cv-light.png | fa | 1440 | light | ready | Critical | Phase 2 |
| PF-07-pf07-about-FA-390-LIGHT | public-270-pf07-about-fa-390-light.png | about-cv-light.png | fa | 390 | light | ready | Critical | Phase 2 |
| PF-07-pf07-cv-EN-1440-LIGHT | public-270-pf07-cv-en-1440-light.png | about-cv-light.png | en | 1440 | light | ready | High | Phase 2 |
| PF-07-pf07-cv-EN-390-LIGHT | public-270-pf07-cv-en-390-light.png | about-cv-light.png | en | 390 | light | ready | High | Phase 2 |
| PF-07-pf07-cv-FA-1440-LIGHT | public-270-pf07-cv-fa-1440-light.png | about-cv-light.png | fa | 1440 | light | ready | High | Phase 2 |
| PF-07-pf07-cv-FA-390-LIGHT | public-270-pf07-cv-fa-390-light.png | about-cv-light.png | fa | 390 | light | ready | High | Phase 2 |
| PF-08-pf08-EN-1440-DARK | public-270-pf08-en-1440-dark.png | contact-dark.png | en | 1440 | dark | ready | Critical | Phase 3 |
| PF-08-pf08-EN-390-DARK | public-270-pf08-en-390-dark.png | contact-dark.png | en | 390 | dark | ready | Critical | Phase 3 |
| PF-08-pf08-FA-1440-DARK | public-270-pf08-fa-1440-dark.png | contact-dark.png | fa | 1440 | dark | ready | Critical | Phase 3 |
| PF-08-pf08-FA-390-DARK | public-270-pf08-fa-390-dark.png | contact-dark.png | fa | 390 | dark | ready | Critical | Phase 3 |
| PF-02-pf02-EN-1440-DARK | public-270-pf02-en-1440-dark.png | creative-detail-dark.png | en | 1440 | dark | blocked | Blocked | Phase 7 |
| PF-02-pf02-EN-390-DARK | public-270-pf02-en-390-dark.png | creative-detail-dark.png | en | 390 | dark | blocked | Blocked | Phase 7 |
| PF-02-pf02-FA-1440-DARK | public-270-pf02-fa-1440-dark.png | creative-detail-dark.png | fa | 1440 | dark | blocked | Blocked | Phase 7 |
| PF-02-pf02-FA-390-DARK | public-270-pf02-fa-390-dark.png | creative-detail-dark.png | fa | 390 | dark | blocked | Blocked | Phase 7 |
| HOME-HOME-EN-768-LIGHT | wp40-home-en-768-light.png | — | en | 768 | light | capture-only | Medium | Phase 8 |
| HOME-HOME-EN-768-DARK | wp40-home-en-768-dark.png | — | en | 768 | dark | capture-only | Medium | Phase 8 |
| HOME-HOME-FA-768-LIGHT | wp40-home-fa-768-light.png | home-mobile-fa-light-concept-v1.png | fa | 768 | light | ready | Medium | Phase 8 |
| HOME-HOME-FA-768-DARK | wp40-home-fa-768-dark.png | — | fa | 768 | dark | capture-only | Medium | Phase 8 |
| HOME-HOME-EN-200PCT-LIGHT | wp40-home-en-200pct-light.png | — | en | 720 | light | capture-only | Medium | Phase 8 |
| HOME-HOME-EN-200PCT-DARK | wp40-home-en-200pct-dark.png | — | en | 720 | dark | capture-only | Medium | Phase 8 |
| HOME-HOME-FA-200PCT-LIGHT | wp40-home-fa-200pct-light.png | home-mobile-fa-light-concept-v1.png | fa | 720 | light | ready | Medium | Phase 8 |
| HOME-GATEWAY-200PCT-LIGHT | wp40-gateway-200pct-light.png | language-gateway-dark-concept-v1.png | neutral | 720 | light | ready | Low | Phase 8 |

---

## Screenshot ↔ pair mapping (owner attachments)

| Screenshot timestamp | Pair ID(s) | Notes |
|---------------------|------------|-------|
| 061513 | PF-04-FA-1440-DARK | Projects FA desktop — hero + featured + filter gaps |
| 061523 | PF-04-FA-1440-DARK | Projects list rows + missing Evidence section |
| 061538 | PF-07-EN-1440-LIGHT | About profile hero + sections |
| 061544 | PF-05-EN-1440-LIGHT | Research constellation area |
| 061601 | PF-08-EN-1440-DARK | Contact collaboration hero |
| 061609 | PF-01-EN-1440-LIGHT | Creative/Gallery index |
| 061621 | PF-03-EN-1440-LIGHT | Writing/Blog index |
| 061628 | PF-06-EN-1440-DARK | Teaching/Learning index |
| 061639 | HOME-FA-768-LIGHT | Home mobile FA |
| 061646 | PF-05-PUBLICATIONS-EN-1440-LIGHT | Publications bibliography |
| 061701–061850 | PF-01/03/04/05/06/07/08 variants | Additional EN/FA viewport confirmations |

---

## Per-pair gap analysis (48 / 48)

### PF-01-pf01-EN-1440-LIGHT: public-270-pf01-en-1440-light.png ↔ creative-index-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-01
- **Implementation files:** `CreativePageContent.astro`, `PageFamilyIndexHero`, `PageFamilyFeaturedShell`, `PageFamilyMediaGridPlaceholder`, `PageFamilyPaginationShell`, `CollectionIndexTemplate`, `creative-page` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Nav label reads **Creative** / **آثار خلاقه** vs concept **Gallery** / **Blog** adjacent — Category D (route registry). Header chrome otherwise aligned: brand mark, role line, theme toggle, EN/FA switch present.

- **Hero:** Concept: two-column hero — serif **Gallery** title, descriptive paragraph, tall side media with arch/stair motif + geometric overlay. Implementation: `PageFamilyIndexHero` single-column on mobile; side media uses recycled `home.rail.preview` asset (`gallery-ivory-forms`) not concept-specific crop; hero media column ~42% @1440 but lacks concept depth/glow frame.

- **Navigation/tabs:** Concept filter bar: **All work** + Medium/Year/Role dropdown chips + Contact CTA on same row. Implementation: disabled filter shell with chip placeholders — correct empty-state honesty but missing dropdown chevrons, chip spacing rhythm, and right-aligned Contact link styling.

- **Main content sections:**
  - **Featured work:** Concept large landscape featured card with teal label, CMS placeholder title, **View work** CTA, distinct wide render. Implementation: `PageFamilyFeaturedShell` — structural shell only; card proportions and inner media aspect differ; per-family styling @ `dd515a0` partial.
  - **Masonry grid:** Concept 9+ varied aspect tiles (dense masonry, mixed portrait/landscape). Implementation: `PageFamilyMediaGridPlaceholder` uses uniform placeholders + `grid-auto-flow: dense` — lacks thumbnail diversity, hover states, and per-tile metadata.
  - **Pagination:** Concept numbered 1–4 with chevrons. Implementation: `PageFamilyPaginationShell` present — verify active state teal square matches concept.
  - **Collaborate band:** Concept full-width CTA before footer. Implementation: via `ContactCTA` in `Footer.astro` — similar copy but band surface/glow differs.

- **Footer:** Concept 4-column footer: EXPLORE, RESOURCES, CONNECT with CMS placeholders for email/location. Implementation: 3-column grid; GitHub/LinkedIn are non-link placeholders; CONNECT email works via contact route but lacks location line and concept column headers styling.

- **Typography/color/spacing:** Concept uses display serif for **Gallery** and teal eyebrow **Selected visual work**. Implementation: tokenized but eyebrow copy differs; FA locale needs verified display/body font pairing @390.

- **Imagery/assets:** Concept requires unique gallery hero side media, featured landscape, and 9+ distinct masonry thumbnails. Implementation reuses promoted rail/project assets — visual monotony vs concept. → Asset prompts: [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md), [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (grid thumbs)

- **Animation/interaction:** Concept implies subtle tile hover lift and filter affordance. Implementation: CSS-only per ADR-ANIMATION; no grid hover choreography.

- **CMS/admin dependency:** Featured title/body, grid records, footer CONNECT copy — **Category A** (blocked). Filter labels and empty-state chrome — **Category B/C** fixable.

- **Priority fixes:**
  - P0: Replace hero side media with PF-01-specific promoted asset — `page-family-empty-chrome.ts`, `PageFamilyIndexHero.astro`, new asset prompt ASSET-PF01-HERO-SIDE-ARCH
  - P0: Masonry placeholder diversity (mixed aspects) — `PageFamilyMediaGridPlaceholder.astro` + CSS grid template areas
  - P1: Featured card aspect ratio + inner media frame — `PageFamilyFeaturedShell.astro`, family CSS

### PF-01-pf01-EN-390-LIGHT: public-270-pf01-en-390-light.png ↔ creative-index-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-01
- **Implementation files:** `CreativePageContent.astro`, `PageFamilyIndexHero`, `PageFamilyFeaturedShell`, `PageFamilyMediaGridPlaceholder`, `PageFamilyPaginationShell`, `CollectionIndexTemplate`, `creative-page` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Nav label reads **Creative** / **آثار خلاقه** vs concept **Gallery** / **Blog** adjacent — Category D (route registry). Header chrome otherwise aligned: brand mark, role line, theme toggle, EN/FA switch present.

- **Hero:** Concept: two-column hero — serif **Gallery** title, descriptive paragraph, tall side media with arch/stair motif + geometric overlay. Implementation: `PageFamilyIndexHero` single-column on mobile; side media uses recycled `home.rail.preview` asset (`gallery-ivory-forms`) not concept-specific crop; hero media column ~42% @1440 but lacks concept depth/glow frame.

- **Navigation/tabs:** Concept filter bar: **All work** + Medium/Year/Role dropdown chips + Contact CTA on same row. Implementation: disabled filter shell with chip placeholders — correct empty-state honesty but missing dropdown chevrons, chip spacing rhythm, and right-aligned Contact link styling.

- **Main content sections:**
  - **Featured work:** Concept large landscape featured card with teal label, CMS placeholder title, **View work** CTA, distinct wide render. Implementation: `PageFamilyFeaturedShell` — structural shell only; card proportions and inner media aspect differ; per-family styling @ `dd515a0` partial.
  - **Masonry grid:** Concept 9+ varied aspect tiles (dense masonry, mixed portrait/landscape). Implementation: `PageFamilyMediaGridPlaceholder` uses uniform placeholders + `grid-auto-flow: dense` — lacks thumbnail diversity, hover states, and per-tile metadata.
  - **Pagination:** Concept numbered 1–4 with chevrons. Implementation: `PageFamilyPaginationShell` present — verify active state teal square matches concept.
  - **Collaborate band:** Concept full-width CTA before footer. Implementation: via `ContactCTA` in `Footer.astro` — similar copy but band surface/glow differs.

- **Footer:** Concept 4-column footer: EXPLORE, RESOURCES, CONNECT with CMS placeholders for email/location. Implementation: 3-column grid; GitHub/LinkedIn are non-link placeholders; CONNECT email works via contact route but lacks location line and concept column headers styling.

- **Typography/color/spacing:** Concept uses display serif for **Gallery** and teal eyebrow **Selected visual work**. Implementation: tokenized but eyebrow copy differs; FA locale needs verified display/body font pairing @390.

- **Imagery/assets:** Concept requires unique gallery hero side media, featured landscape, and 9+ distinct masonry thumbnails. Implementation reuses promoted rail/project assets — visual monotony vs concept. → Asset prompts: [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md), [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (grid thumbs)

- **Animation/interaction:** Concept implies subtle tile hover lift and filter affordance. Implementation: CSS-only per ADR-ANIMATION; no grid hover choreography.

- **CMS/admin dependency:** Featured title/body, grid records, footer CONNECT copy — **Category A** (blocked). Filter labels and empty-state chrome — **Category B/C** fixable.

- **Priority fixes:**
  - P0: Replace hero side media with PF-01-specific promoted asset — `page-family-empty-chrome.ts`, `PageFamilyIndexHero.astro`, new asset prompt ASSET-PF01-HERO-SIDE-ARCH
  - P0: Masonry placeholder diversity (mixed aspects) — `PageFamilyMediaGridPlaceholder.astro` + CSS grid template areas
  - P1: Featured card aspect ratio + inner media frame — `PageFamilyFeaturedShell.astro`, family CSS

### PF-01-pf01-FA-1440-LIGHT: public-270-pf01-fa-1440-light.png ↔ creative-index-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-01
- **Implementation files:** `CreativePageContent.astro`, `PageFamilyIndexHero`, `PageFamilyFeaturedShell`, `PageFamilyMediaGridPlaceholder`, `PageFamilyPaginationShell`, `CollectionIndexTemplate`, `creative-page` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Nav label reads **Creative** / **آثار خلاقه** vs concept **Gallery** / **Blog** adjacent — Category D (route registry). Header chrome otherwise aligned: brand mark, role line, theme toggle, EN/FA switch present.

- **Hero:** Concept: two-column hero — serif **Gallery** title, descriptive paragraph, tall side media with arch/stair motif + geometric overlay. Implementation: `PageFamilyIndexHero` single-column on mobile; side media uses recycled `home.rail.preview` asset (`gallery-ivory-forms`) not concept-specific crop; hero media column ~42% @1440 but lacks concept depth/glow frame.

- **Navigation/tabs:** Concept filter bar: **All work** + Medium/Year/Role dropdown chips + Contact CTA on same row. Implementation: disabled filter shell with chip placeholders — correct empty-state honesty but missing dropdown chevrons, chip spacing rhythm, and right-aligned Contact link styling.

- **Main content sections:**
  - **Featured work:** Concept large landscape featured card with teal label, CMS placeholder title, **View work** CTA, distinct wide render. Implementation: `PageFamilyFeaturedShell` — structural shell only; card proportions and inner media aspect differ; per-family styling @ `dd515a0` partial.
  - **Masonry grid:** Concept 9+ varied aspect tiles (dense masonry, mixed portrait/landscape). Implementation: `PageFamilyMediaGridPlaceholder` uses uniform placeholders + `grid-auto-flow: dense` — lacks thumbnail diversity, hover states, and per-tile metadata.
  - **Pagination:** Concept numbered 1–4 with chevrons. Implementation: `PageFamilyPaginationShell` present — verify active state teal square matches concept.
  - **Collaborate band:** Concept full-width CTA before footer. Implementation: via `ContactCTA` in `Footer.astro` — similar copy but band surface/glow differs.

- **Footer:** Concept 4-column footer: EXPLORE, RESOURCES, CONNECT with CMS placeholders for email/location. Implementation: 3-column grid; GitHub/LinkedIn are non-link placeholders; CONNECT email works via contact route but lacks location line and concept column headers styling.

- **Typography/color/spacing:** Concept uses display serif for **Gallery** and teal eyebrow **Selected visual work**. Implementation: tokenized but eyebrow copy differs; FA locale needs verified display/body font pairing @390.

- **Imagery/assets:** Concept requires unique gallery hero side media, featured landscape, and 9+ distinct masonry thumbnails. Implementation reuses promoted rail/project assets — visual monotony vs concept. → Asset prompts: [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md), [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (grid thumbs)

- **Animation/interaction:** Concept implies subtle tile hover lift and filter affordance. Implementation: CSS-only per ADR-ANIMATION; no grid hover choreography.

- **CMS/admin dependency:** Featured title/body, grid records, footer CONNECT copy — **Category A** (blocked). Filter labels and empty-state chrome — **Category B/C** fixable.

- **Priority fixes:**
  - P0: Replace hero side media with PF-01-specific promoted asset — `page-family-empty-chrome.ts`, `PageFamilyIndexHero.astro`, new asset prompt ASSET-PF01-HERO-SIDE-ARCH
  - P0: Masonry placeholder diversity (mixed aspects) — `PageFamilyMediaGridPlaceholder.astro` + CSS grid template areas
  - P1: Featured card aspect ratio + inner media frame — `PageFamilyFeaturedShell.astro`, family CSS

### PF-01-pf01-FA-390-LIGHT: public-270-pf01-fa-390-light.png ↔ creative-index-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-01
- **Implementation files:** `CreativePageContent.astro`, `PageFamilyIndexHero`, `PageFamilyFeaturedShell`, `PageFamilyMediaGridPlaceholder`, `PageFamilyPaginationShell`, `CollectionIndexTemplate`, `creative-page` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Nav label reads **Creative** / **آثار خلاقه** vs concept **Gallery** / **Blog** adjacent — Category D (route registry). Header chrome otherwise aligned: brand mark, role line, theme toggle, EN/FA switch present.

- **Hero:** Concept: two-column hero — serif **Gallery** title, descriptive paragraph, tall side media with arch/stair motif + geometric overlay. Implementation: `PageFamilyIndexHero` single-column on mobile; side media uses recycled `home.rail.preview` asset (`gallery-ivory-forms`) not concept-specific crop; hero media column ~42% @1440 but lacks concept depth/glow frame.

- **Navigation/tabs:** Concept filter bar: **All work** + Medium/Year/Role dropdown chips + Contact CTA on same row. Implementation: disabled filter shell with chip placeholders — correct empty-state honesty but missing dropdown chevrons, chip spacing rhythm, and right-aligned Contact link styling.

- **Main content sections:**
  - **Featured work:** Concept large landscape featured card with teal label, CMS placeholder title, **View work** CTA, distinct wide render. Implementation: `PageFamilyFeaturedShell` — structural shell only; card proportions and inner media aspect differ; per-family styling @ `dd515a0` partial.
  - **Masonry grid:** Concept 9+ varied aspect tiles (dense masonry, mixed portrait/landscape). Implementation: `PageFamilyMediaGridPlaceholder` uses uniform placeholders + `grid-auto-flow: dense` — lacks thumbnail diversity, hover states, and per-tile metadata.
  - **Pagination:** Concept numbered 1–4 with chevrons. Implementation: `PageFamilyPaginationShell` present — verify active state teal square matches concept.
  - **Collaborate band:** Concept full-width CTA before footer. Implementation: via `ContactCTA` in `Footer.astro` — similar copy but band surface/glow differs.

- **Footer:** Concept 4-column footer: EXPLORE, RESOURCES, CONNECT with CMS placeholders for email/location. Implementation: 3-column grid; GitHub/LinkedIn are non-link placeholders; CONNECT email works via contact route but lacks location line and concept column headers styling.

- **Typography/color/spacing:** Concept uses display serif for **Gallery** and teal eyebrow **Selected visual work**. Implementation: tokenized but eyebrow copy differs; FA locale needs verified display/body font pairing @390.

- **Imagery/assets:** Concept requires unique gallery hero side media, featured landscape, and 9+ distinct masonry thumbnails. Implementation reuses promoted rail/project assets — visual monotony vs concept. → Asset prompts: [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md), [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (grid thumbs)

- **Animation/interaction:** Concept implies subtle tile hover lift and filter affordance. Implementation: CSS-only per ADR-ANIMATION; no grid hover choreography.

- **CMS/admin dependency:** Featured title/body, grid records, footer CONNECT copy — **Category A** (blocked). Filter labels and empty-state chrome — **Category B/C** fixable.

- **Priority fixes:**
  - P0: Replace hero side media with PF-01-specific promoted asset — `page-family-empty-chrome.ts`, `PageFamilyIndexHero.astro`, new asset prompt ASSET-PF01-HERO-SIDE-ARCH
  - P0: Masonry placeholder diversity (mixed aspects) — `PageFamilyMediaGridPlaceholder.astro` + CSS grid template areas
  - P1: Featured card aspect ratio + inner media frame — `PageFamilyFeaturedShell.astro`, family CSS

### PF-03-pf03-EN-1440-LIGHT: public-270-pf03-en-1440-light.png ↔ writing-index-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-03
- **Implementation files:** `WritingPageContent.astro`, `EditorialIndexTemplate`, `PageFamilyFeaturedShell`, `PageFamilyThemeExploreShell`, row placeholders, `PageFamilyPaginationShell`
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Nav **Writing** vs concept **Blog** — Category D. Active state concept uses coral/orange underline; implementation uses brand teal/coral mix via `eyebrowTone="coral"`.

- **Hero:** Concept: **INDEPENDENT WRITING** eyebrow, serif **Blog**, paragraph, gold diamond ornament, large coral architectural hero image right. Implementation: hero copy localized; side media recycles writing rail asset; missing diamond ornament and coral-forward hero framing.

- **Navigation/tabs:** Concept tab row: All (red outline active), Essays, Notes, Memories, Society, Archive + search **Search writing…**. Implementation: disabled tabs + search shell — tab active styling differs (outline vs filled); `PageFamilyThemeExploreShell` added @ dd515a0 but icon cards not matching concept 5-up explore row.

- **Main content sections:**
  - **Featured post:** Concept boxed grey featured with image right. Implementation: `PageFamilyFeaturedShell` — layout inversion on RTL FA must mirror concept.
  - **Post list:** Concept 6 rows with thumbnail, category label (ESSAY/NOTE), title placeholder, excerpt, teal arrow. Implementation: row placeholders — missing category chroma, arrow affordance density.
  - **Explore by theme:** Concept 5 icon cards with red borders. Implementation: `PageFamilyThemeExploreShell` partial.
  - **Newsletter band:** Concept optional updates + Follow updates. Implementation: absent on writing index empty state.
  - **Collaboration + pagination:** Present in concept; pagination shell exists; collaborate via footer promo.

- **Footer:** Same shared footer gaps as PF-01.

- **Typography/color/spacing:** Coral accent for writing family — verify WCAG AA on empty shells (@ dd515a0 fix noted in QA). FA @390: line-length and RTL tab overflow.

- **Imagery/assets:** Concept coral architectural renders distinct from creative teal. Implementation reuses shared rail assets. → Asset prompts: [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (featured), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (list thumbs)

- **Animation/interaction:** Row hover slide optional; list is static.

- **CMS/admin dependency:** All post titles/excerpts — Category A. Tab labels structural — B.

- **Priority fixes:**
  - P0: Writing-specific hero + featured assets — asset prompts + `getPageFamilyHeroMedia(writing)`
  - P1: Theme explore 5-card row fidelity — `PageFamilyThemeExploreShell.astro`
  - P1: Newsletter/updates band shell — new `PageFamilyOptionalUpdatesShell.astro`

### PF-03-pf03-EN-390-LIGHT: public-270-pf03-en-390-light.png ↔ writing-index-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-03
- **Implementation files:** `WritingPageContent.astro`, `EditorialIndexTemplate`, `PageFamilyFeaturedShell`, `PageFamilyThemeExploreShell`, row placeholders, `PageFamilyPaginationShell`
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Nav **Writing** vs concept **Blog** — Category D. Active state concept uses coral/orange underline; implementation uses brand teal/coral mix via `eyebrowTone="coral"`.

- **Hero:** Concept: **INDEPENDENT WRITING** eyebrow, serif **Blog**, paragraph, gold diamond ornament, large coral architectural hero image right. Implementation: hero copy localized; side media recycles writing rail asset; missing diamond ornament and coral-forward hero framing.

- **Navigation/tabs:** Concept tab row: All (red outline active), Essays, Notes, Memories, Society, Archive + search **Search writing…**. Implementation: disabled tabs + search shell — tab active styling differs (outline vs filled); `PageFamilyThemeExploreShell` added @ dd515a0 but icon cards not matching concept 5-up explore row.

- **Main content sections:**
  - **Featured post:** Concept boxed grey featured with image right. Implementation: `PageFamilyFeaturedShell` — layout inversion on RTL FA must mirror concept.
  - **Post list:** Concept 6 rows with thumbnail, category label (ESSAY/NOTE), title placeholder, excerpt, teal arrow. Implementation: row placeholders — missing category chroma, arrow affordance density.
  - **Explore by theme:** Concept 5 icon cards with red borders. Implementation: `PageFamilyThemeExploreShell` partial.
  - **Newsletter band:** Concept optional updates + Follow updates. Implementation: absent on writing index empty state.
  - **Collaboration + pagination:** Present in concept; pagination shell exists; collaborate via footer promo.

- **Footer:** Same shared footer gaps as PF-01.

- **Typography/color/spacing:** Coral accent for writing family — verify WCAG AA on empty shells (@ dd515a0 fix noted in QA). FA @390: line-length and RTL tab overflow.

- **Imagery/assets:** Concept coral architectural renders distinct from creative teal. Implementation reuses shared rail assets. → Asset prompts: [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (featured), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (list thumbs)

- **Animation/interaction:** Row hover slide optional; list is static.

- **CMS/admin dependency:** All post titles/excerpts — Category A. Tab labels structural — B.

- **Priority fixes:**
  - P0: Writing-specific hero + featured assets — asset prompts + `getPageFamilyHeroMedia(writing)`
  - P1: Theme explore 5-card row fidelity — `PageFamilyThemeExploreShell.astro`
  - P1: Newsletter/updates band shell — new `PageFamilyOptionalUpdatesShell.astro`

### PF-03-pf03-FA-1440-LIGHT: public-270-pf03-fa-1440-light.png ↔ writing-index-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-03
- **Implementation files:** `WritingPageContent.astro`, `EditorialIndexTemplate`, `PageFamilyFeaturedShell`, `PageFamilyThemeExploreShell`, row placeholders, `PageFamilyPaginationShell`
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Nav **Writing** vs concept **Blog** — Category D. Active state concept uses coral/orange underline; implementation uses brand teal/coral mix via `eyebrowTone="coral"`.

- **Hero:** Concept: **INDEPENDENT WRITING** eyebrow, serif **Blog**, paragraph, gold diamond ornament, large coral architectural hero image right. Implementation: hero copy localized; side media recycles writing rail asset; missing diamond ornament and coral-forward hero framing.

- **Navigation/tabs:** Concept tab row: All (red outline active), Essays, Notes, Memories, Society, Archive + search **Search writing…**. Implementation: disabled tabs + search shell — tab active styling differs (outline vs filled); `PageFamilyThemeExploreShell` added @ dd515a0 but icon cards not matching concept 5-up explore row.

- **Main content sections:**
  - **Featured post:** Concept boxed grey featured with image right. Implementation: `PageFamilyFeaturedShell` — layout inversion on RTL FA must mirror concept.
  - **Post list:** Concept 6 rows with thumbnail, category label (ESSAY/NOTE), title placeholder, excerpt, teal arrow. Implementation: row placeholders — missing category chroma, arrow affordance density.
  - **Explore by theme:** Concept 5 icon cards with red borders. Implementation: `PageFamilyThemeExploreShell` partial.
  - **Newsletter band:** Concept optional updates + Follow updates. Implementation: absent on writing index empty state.
  - **Collaboration + pagination:** Present in concept; pagination shell exists; collaborate via footer promo.

- **Footer:** Same shared footer gaps as PF-01.

- **Typography/color/spacing:** Coral accent for writing family — verify WCAG AA on empty shells (@ dd515a0 fix noted in QA). FA @390: line-length and RTL tab overflow.

- **Imagery/assets:** Concept coral architectural renders distinct from creative teal. Implementation reuses shared rail assets. → Asset prompts: [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (featured), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (list thumbs)

- **Animation/interaction:** Row hover slide optional; list is static.

- **CMS/admin dependency:** All post titles/excerpts — Category A. Tab labels structural — B.

- **Priority fixes:**
  - P0: Writing-specific hero + featured assets — asset prompts + `getPageFamilyHeroMedia(writing)`
  - P1: Theme explore 5-card row fidelity — `PageFamilyThemeExploreShell.astro`
  - P1: Newsletter/updates band shell — new `PageFamilyOptionalUpdatesShell.astro`

### PF-03-pf03-FA-390-LIGHT: public-270-pf03-fa-390-light.png ↔ writing-index-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-03
- **Implementation files:** `WritingPageContent.astro`, `EditorialIndexTemplate`, `PageFamilyFeaturedShell`, `PageFamilyThemeExploreShell`, row placeholders, `PageFamilyPaginationShell`
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Nav **Writing** vs concept **Blog** — Category D. Active state concept uses coral/orange underline; implementation uses brand teal/coral mix via `eyebrowTone="coral"`.

- **Hero:** Concept: **INDEPENDENT WRITING** eyebrow, serif **Blog**, paragraph, gold diamond ornament, large coral architectural hero image right. Implementation: hero copy localized; side media recycles writing rail asset; missing diamond ornament and coral-forward hero framing.

- **Navigation/tabs:** Concept tab row: All (red outline active), Essays, Notes, Memories, Society, Archive + search **Search writing…**. Implementation: disabled tabs + search shell — tab active styling differs (outline vs filled); `PageFamilyThemeExploreShell` added @ dd515a0 but icon cards not matching concept 5-up explore row.

- **Main content sections:**
  - **Featured post:** Concept boxed grey featured with image right. Implementation: `PageFamilyFeaturedShell` — layout inversion on RTL FA must mirror concept.
  - **Post list:** Concept 6 rows with thumbnail, category label (ESSAY/NOTE), title placeholder, excerpt, teal arrow. Implementation: row placeholders — missing category chroma, arrow affordance density.
  - **Explore by theme:** Concept 5 icon cards with red borders. Implementation: `PageFamilyThemeExploreShell` partial.
  - **Newsletter band:** Concept optional updates + Follow updates. Implementation: absent on writing index empty state.
  - **Collaboration + pagination:** Present in concept; pagination shell exists; collaborate via footer promo.

- **Footer:** Same shared footer gaps as PF-01.

- **Typography/color/spacing:** Coral accent for writing family — verify WCAG AA on empty shells (@ dd515a0 fix noted in QA). FA @390: line-length and RTL tab overflow.

- **Imagery/assets:** Concept coral architectural renders distinct from creative teal. Implementation reuses shared rail assets. → Asset prompts: [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (featured), [blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (list thumbs)

- **Animation/interaction:** Row hover slide optional; list is static.

- **CMS/admin dependency:** All post titles/excerpts — Category A. Tab labels structural — B.

- **Priority fixes:**
  - P0: Writing-specific hero + featured assets — asset prompts + `getPageFamilyHeroMedia(writing)`
  - P1: Theme explore 5-card row fidelity — `PageFamilyThemeExploreShell.astro`
  - P1: Newsletter/updates band shell — new `PageFamilyOptionalUpdatesShell.astro`

### PF-04-pf04-EN-1440-DARK: public-270-pf04-en-1440-dark.png ↔ projects-index-dark.png
- **Meta:** locale=en, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-04
- **Implementation files:** `ProjectsPageContent.astro`, `PageFamilyFeaturedShell`, `PageFamilyContentRowPlaceholder`, `PageFamilySortShell`, `PageFamilyPaginationShell`, `projects-page` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Projects** active — aligned. Owner screenshot @061513 shows FA RTL header order correct but lacks concept full brand subtitle prominence.

- **Hero:** Concept: **SELECTED EVIDENCE** gold eyebrow, serif **Projects**, multi-line description, shield badge **No sensitive or real operational data**, large isometric server cluster hero right. Implementation: eyebrow localized; missing shield/status badge; hero media reuses PARS-SQL project preview — wrong motif vs concept server cluster.

- **Navigation/tabs:** Concept pills: All, Research, AI, Data systems, Software, Design + search + **Sort: Latest**. Implementation: disabled chips + `PageFamilySortShell` — sort dropdown styling incomplete vs concept.

- **Main content sections:**
  - **Featured project:** Concept PARS-SQL card with tags, carousel dots, schematic cube render. Implementation: `PageFamilyFeaturedShell` generic — missing tag pills, carousel dots, project-specific inner layout.
  - **Numbered rows 01–06:** Concept large index number, thumbnail, title placeholder, category badge + **Sanitized** shield, description, right tag stack + arrow. Implementation: `PageFamilyContentRowPlaceholder` — missing row numbers, sanitized badge, right tag column.
  - **Evidence Available:** Concept 4-card Methods/Artifacts/Code/Demo/Documentation grid — **MISSING entirely** in implementation.
  - **Pagination:** Shell present; styling gap vs teal active square.

- **Footer:** Concept footer richer; implementation footer promo band simplified (owner screenshot @061523).

- **Typography/color/spacing:** Dark theme gold serif headings vs implementation flatter sans — projects-page dark tokens need display serif on h1.

- **Imagery/assets:** Concept needs unique hero cluster, featured schematic, 6 row thumbnails, evidence icons — implementation repeats single project asset. → Asset prompts: [project-dashboard-systems.md](../PUBLIC-190-asset-prompts/project-dashboard-systems.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md) (row set), ASSET-PF04-EVIDENCE-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Featured carousel implied — not implemented.

- **CMS/admin dependency:** Row titles, tags, evidence links — Category A. Evidence section structure — B (shell without CMS).

- **Priority fixes:**
  - P0: Add `PageFamilyEvidenceGridShell.astro` — Methods/Artifacts/Code/Documentation cards
  - P0: Project row chrome — index numbers, sanitized badge, tag stack — `PageFamilyContentRowPlaceholder.astro`
  - P0: Hero + featured asset swap — asset prompts ASSET-PF04-*

### PF-04-pf04-EN-390-DARK: public-270-pf04-en-390-dark.png ↔ projects-index-dark.png
- **Meta:** locale=en, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-04
- **Implementation files:** `ProjectsPageContent.astro`, `PageFamilyFeaturedShell`, `PageFamilyContentRowPlaceholder`, `PageFamilySortShell`, `PageFamilyPaginationShell`, `projects-page` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Projects** active — aligned. Owner screenshot @061513 shows FA RTL header order correct but lacks concept full brand subtitle prominence.

- **Hero:** Concept: **SELECTED EVIDENCE** gold eyebrow, serif **Projects**, multi-line description, shield badge **No sensitive or real operational data**, large isometric server cluster hero right. Implementation: eyebrow localized; missing shield/status badge; hero media reuses PARS-SQL project preview — wrong motif vs concept server cluster.

- **Navigation/tabs:** Concept pills: All, Research, AI, Data systems, Software, Design + search + **Sort: Latest**. Implementation: disabled chips + `PageFamilySortShell` — sort dropdown styling incomplete vs concept.

- **Main content sections:**
  - **Featured project:** Concept PARS-SQL card with tags, carousel dots, schematic cube render. Implementation: `PageFamilyFeaturedShell` generic — missing tag pills, carousel dots, project-specific inner layout.
  - **Numbered rows 01–06:** Concept large index number, thumbnail, title placeholder, category badge + **Sanitized** shield, description, right tag stack + arrow. Implementation: `PageFamilyContentRowPlaceholder` — missing row numbers, sanitized badge, right tag column.
  - **Evidence Available:** Concept 4-card Methods/Artifacts/Code/Demo/Documentation grid — **MISSING entirely** in implementation.
  - **Pagination:** Shell present; styling gap vs teal active square.

- **Footer:** Concept footer richer; implementation footer promo band simplified (owner screenshot @061523).

- **Typography/color/spacing:** Dark theme gold serif headings vs implementation flatter sans — projects-page dark tokens need display serif on h1.

- **Imagery/assets:** Concept needs unique hero cluster, featured schematic, 6 row thumbnails, evidence icons — implementation repeats single project asset. → Asset prompts: [project-dashboard-systems.md](../PUBLIC-190-asset-prompts/project-dashboard-systems.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md) (row set), ASSET-PF04-EVIDENCE-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Featured carousel implied — not implemented.

- **CMS/admin dependency:** Row titles, tags, evidence links — Category A. Evidence section structure — B (shell without CMS).

- **Priority fixes:**
  - P0: Add `PageFamilyEvidenceGridShell.astro` — Methods/Artifacts/Code/Documentation cards
  - P0: Project row chrome — index numbers, sanitized badge, tag stack — `PageFamilyContentRowPlaceholder.astro`
  - P0: Hero + featured asset swap — asset prompts ASSET-PF04-*

### PF-04-pf04-FA-1440-DARK: public-270-pf04-fa-1440-dark.png ↔ projects-index-dark.png
- **Meta:** locale=fa, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-04
- **Implementation files:** `ProjectsPageContent.astro`, `PageFamilyFeaturedShell`, `PageFamilyContentRowPlaceholder`, `PageFamilySortShell`, `PageFamilyPaginationShell`, `projects-page` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Projects** active — aligned. Owner screenshot @061513 shows FA RTL header order correct but lacks concept full brand subtitle prominence.

- **Hero:** Concept: **SELECTED EVIDENCE** gold eyebrow, serif **Projects**, multi-line description, shield badge **No sensitive or real operational data**, large isometric server cluster hero right. Implementation: eyebrow localized; missing shield/status badge; hero media reuses PARS-SQL project preview — wrong motif vs concept server cluster.

- **Navigation/tabs:** Concept pills: All, Research, AI, Data systems, Software, Design + search + **Sort: Latest**. Implementation: disabled chips + `PageFamilySortShell` — sort dropdown styling incomplete vs concept.

- **Main content sections:**
  - **Featured project:** Concept PARS-SQL card with tags, carousel dots, schematic cube render. Implementation: `PageFamilyFeaturedShell` generic — missing tag pills, carousel dots, project-specific inner layout.
  - **Numbered rows 01–06:** Concept large index number, thumbnail, title placeholder, category badge + **Sanitized** shield, description, right tag stack + arrow. Implementation: `PageFamilyContentRowPlaceholder` — missing row numbers, sanitized badge, right tag column.
  - **Evidence Available:** Concept 4-card Methods/Artifacts/Code/Demo/Documentation grid — **MISSING entirely** in implementation.
  - **Pagination:** Shell present; styling gap vs teal active square.

- **Footer:** Concept footer richer; implementation footer promo band simplified (owner screenshot @061523).

- **Typography/color/spacing:** Dark theme gold serif headings vs implementation flatter sans — projects-page dark tokens need display serif on h1.

- **Imagery/assets:** Concept needs unique hero cluster, featured schematic, 6 row thumbnails, evidence icons — implementation repeats single project asset. → Asset prompts: [project-dashboard-systems.md](../PUBLIC-190-asset-prompts/project-dashboard-systems.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md) (row set), ASSET-PF04-EVIDENCE-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Featured carousel implied — not implemented.

- **CMS/admin dependency:** Row titles, tags, evidence links — Category A. Evidence section structure — B (shell without CMS).

- **Priority fixes:**
  - P0: Add `PageFamilyEvidenceGridShell.astro` — Methods/Artifacts/Code/Documentation cards
  - P0: Project row chrome — index numbers, sanitized badge, tag stack — `PageFamilyContentRowPlaceholder.astro`
  - P0: Hero + featured asset swap — asset prompts ASSET-PF04-*

### PF-04-pf04-FA-390-DARK: public-270-pf04-fa-390-dark.png ↔ projects-index-dark.png
- **Meta:** locale=fa, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-04
- **Implementation files:** `ProjectsPageContent.astro`, `PageFamilyFeaturedShell`, `PageFamilyContentRowPlaceholder`, `PageFamilySortShell`, `PageFamilyPaginationShell`, `projects-page` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Projects** active — aligned. Owner screenshot @061513 shows FA RTL header order correct but lacks concept full brand subtitle prominence.

- **Hero:** Concept: **SELECTED EVIDENCE** gold eyebrow, serif **Projects**, multi-line description, shield badge **No sensitive or real operational data**, large isometric server cluster hero right. Implementation: eyebrow localized; missing shield/status badge; hero media reuses PARS-SQL project preview — wrong motif vs concept server cluster.

- **Navigation/tabs:** Concept pills: All, Research, AI, Data systems, Software, Design + search + **Sort: Latest**. Implementation: disabled chips + `PageFamilySortShell` — sort dropdown styling incomplete vs concept.

- **Main content sections:**
  - **Featured project:** Concept PARS-SQL card with tags, carousel dots, schematic cube render. Implementation: `PageFamilyFeaturedShell` generic — missing tag pills, carousel dots, project-specific inner layout.
  - **Numbered rows 01–06:** Concept large index number, thumbnail, title placeholder, category badge + **Sanitized** shield, description, right tag stack + arrow. Implementation: `PageFamilyContentRowPlaceholder` — missing row numbers, sanitized badge, right tag column.
  - **Evidence Available:** Concept 4-card Methods/Artifacts/Code/Demo/Documentation grid — **MISSING entirely** in implementation.
  - **Pagination:** Shell present; styling gap vs teal active square.

- **Footer:** Concept footer richer; implementation footer promo band simplified (owner screenshot @061523).

- **Typography/color/spacing:** Dark theme gold serif headings vs implementation flatter sans — projects-page dark tokens need display serif on h1.

- **Imagery/assets:** Concept needs unique hero cluster, featured schematic, 6 row thumbnails, evidence icons — implementation repeats single project asset. → Asset prompts: [project-dashboard-systems.md](../PUBLIC-190-asset-prompts/project-dashboard-systems.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md), [project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md) (row set), ASSET-PF04-EVIDENCE-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Featured carousel implied — not implemented.

- **CMS/admin dependency:** Row titles, tags, evidence links — Category A. Evidence section structure — B (shell without CMS).

- **Priority fixes:**
  - P0: Add `PageFamilyEvidenceGridShell.astro` — Methods/Artifacts/Code/Documentation cards
  - P0: Project row chrome — index numbers, sanitized badge, tag stack — `PageFamilyContentRowPlaceholder.astro`
  - P0: Hero + featured asset swap — asset prompts ASSET-PF04-*

### PF-05-pf05-research-EN-1440-LIGHT: public-270-pf05-research-en-1440-light.png ↔ research-publications-index-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `ResearchPageContent.astro`, `PageFamilyConstellationShell`, `PageFamilyResearchFitShell`, tabs, row placeholders
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Shared header; research nav active on research route.

- **Hero:** Concept: **RESEARCH PROFILE**, serif **Research**, description, side arch media, sub-nav tabs (Overview, Research directions, Publications, Statement, Collaborators). Implementation: hero + disabled tablist — tabs lack concept underline active styling and horizontal scroll @390.

- **Navigation/tabs:** Sub-nav tabs — see hero. Publications route shares concept PNG but different main sections.

- **Main content sections:**
  - **Research Constellation:** Concept interactive node diagram with legend (AI, Data, Health, Language, Design colors) and center Human-Centered AI. Implementation: `PageFamilyConstellationShell` — static placeholder, no legend, no node graph fidelity.
  - **Research Fit:** Concept 3 cards (Research questions, Methods, Impact) with icons. Implementation: `PageFamilyResearchFitShell` — structural only.
  - **Research Directions:** Concept 5 rows with icons, status badges, related records links. Implementation: row placeholders — missing status badges.
  - **Selected Publications:** Concept 4 publication rows with type tags, Details/Available files buttons. Implementation: absent on research index (publications on separate route).

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Light theme teal accents — aligned directionally; constellation labels need smaller caps tracking.

- **Imagery/assets:** Constellation diagram is major visual — needs SVG/React island or Canvas; hero arch recycles teaching rail asset. → Asset prompts: [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md) (constellation), ASSET-PF05-FIT-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Constellation may need subtle node pulse — GSAP/SVG acceptable per user mandate.

- **CMS/admin dependency:** All research directions, publication rows — Category A. Constellation structure — B with static nodes.

- **Priority fixes:**
  - P0: Constellation visual — SVG island or static SVG asset ASSET-PF05-CONSTELLATION-SVG
  - P1: Research directions row badges — row placeholder component
  - P2: Selected publications preview block on research index when CMS empty — shell only

### PF-05-pf05-research-EN-390-LIGHT: public-270-pf05-research-en-390-light.png ↔ research-publications-index-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `ResearchPageContent.astro`, `PageFamilyConstellationShell`, `PageFamilyResearchFitShell`, tabs, row placeholders
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Shared header; research nav active on research route.

- **Hero:** Concept: **RESEARCH PROFILE**, serif **Research**, description, side arch media, sub-nav tabs (Overview, Research directions, Publications, Statement, Collaborators). Implementation: hero + disabled tablist — tabs lack concept underline active styling and horizontal scroll @390.

- **Navigation/tabs:** Sub-nav tabs — see hero. Publications route shares concept PNG but different main sections.

- **Main content sections:**
  - **Research Constellation:** Concept interactive node diagram with legend (AI, Data, Health, Language, Design colors) and center Human-Centered AI. Implementation: `PageFamilyConstellationShell` — static placeholder, no legend, no node graph fidelity.
  - **Research Fit:** Concept 3 cards (Research questions, Methods, Impact) with icons. Implementation: `PageFamilyResearchFitShell` — structural only.
  - **Research Directions:** Concept 5 rows with icons, status badges, related records links. Implementation: row placeholders — missing status badges.
  - **Selected Publications:** Concept 4 publication rows with type tags, Details/Available files buttons. Implementation: absent on research index (publications on separate route).

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Light theme teal accents — aligned directionally; constellation labels need smaller caps tracking.

- **Imagery/assets:** Constellation diagram is major visual — needs SVG/React island or Canvas; hero arch recycles teaching rail asset. → Asset prompts: [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md) (constellation), ASSET-PF05-FIT-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Constellation may need subtle node pulse — GSAP/SVG acceptable per user mandate.

- **CMS/admin dependency:** All research directions, publication rows — Category A. Constellation structure — B with static nodes.

- **Priority fixes:**
  - P0: Constellation visual — SVG island or static SVG asset ASSET-PF05-CONSTELLATION-SVG
  - P1: Research directions row badges — row placeholder component
  - P2: Selected publications preview block on research index when CMS empty — shell only

### PF-05-pf05-research-FA-1440-LIGHT: public-270-pf05-research-fa-1440-light.png ↔ research-publications-index-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `ResearchPageContent.astro`, `PageFamilyConstellationShell`, `PageFamilyResearchFitShell`, tabs, row placeholders
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Shared header; research nav active on research route.

- **Hero:** Concept: **RESEARCH PROFILE**, serif **Research**, description, side arch media, sub-nav tabs (Overview, Research directions, Publications, Statement, Collaborators). Implementation: hero + disabled tablist — tabs lack concept underline active styling and horizontal scroll @390.

- **Navigation/tabs:** Sub-nav tabs — see hero. Publications route shares concept PNG but different main sections.

- **Main content sections:**
  - **Research Constellation:** Concept interactive node diagram with legend (AI, Data, Health, Language, Design colors) and center Human-Centered AI. Implementation: `PageFamilyConstellationShell` — static placeholder, no legend, no node graph fidelity.
  - **Research Fit:** Concept 3 cards (Research questions, Methods, Impact) with icons. Implementation: `PageFamilyResearchFitShell` — structural only.
  - **Research Directions:** Concept 5 rows with icons, status badges, related records links. Implementation: row placeholders — missing status badges.
  - **Selected Publications:** Concept 4 publication rows with type tags, Details/Available files buttons. Implementation: absent on research index (publications on separate route).

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Light theme teal accents — aligned directionally; constellation labels need smaller caps tracking.

- **Imagery/assets:** Constellation diagram is major visual — needs SVG/React island or Canvas; hero arch recycles teaching rail asset. → Asset prompts: [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md) (constellation), ASSET-PF05-FIT-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Constellation may need subtle node pulse — GSAP/SVG acceptable per user mandate.

- **CMS/admin dependency:** All research directions, publication rows — Category A. Constellation structure — B with static nodes.

- **Priority fixes:**
  - P0: Constellation visual — SVG island or static SVG asset ASSET-PF05-CONSTELLATION-SVG
  - P1: Research directions row badges — row placeholder component
  - P2: Selected publications preview block on research index when CMS empty — shell only

### PF-05-pf05-research-FA-390-LIGHT: public-270-pf05-research-fa-390-light.png ↔ research-publications-index-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `ResearchPageContent.astro`, `PageFamilyConstellationShell`, `PageFamilyResearchFitShell`, tabs, row placeholders
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Shared header; research nav active on research route.

- **Hero:** Concept: **RESEARCH PROFILE**, serif **Research**, description, side arch media, sub-nav tabs (Overview, Research directions, Publications, Statement, Collaborators). Implementation: hero + disabled tablist — tabs lack concept underline active styling and horizontal scroll @390.

- **Navigation/tabs:** Sub-nav tabs — see hero. Publications route shares concept PNG but different main sections.

- **Main content sections:**
  - **Research Constellation:** Concept interactive node diagram with legend (AI, Data, Health, Language, Design colors) and center Human-Centered AI. Implementation: `PageFamilyConstellationShell` — static placeholder, no legend, no node graph fidelity.
  - **Research Fit:** Concept 3 cards (Research questions, Methods, Impact) with icons. Implementation: `PageFamilyResearchFitShell` — structural only.
  - **Research Directions:** Concept 5 rows with icons, status badges, related records links. Implementation: row placeholders — missing status badges.
  - **Selected Publications:** Concept 4 publication rows with type tags, Details/Available files buttons. Implementation: absent on research index (publications on separate route).

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Light theme teal accents — aligned directionally; constellation labels need smaller caps tracking.

- **Imagery/assets:** Constellation diagram is major visual — needs SVG/React island or Canvas; hero arch recycles teaching rail asset. → Asset prompts: [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md) (constellation), ASSET-PF05-FIT-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Constellation may need subtle node pulse — GSAP/SVG acceptable per user mandate.

- **CMS/admin dependency:** All research directions, publication rows — Category A. Constellation structure — B with static nodes.

- **Priority fixes:**
  - P0: Constellation visual — SVG island or static SVG asset ASSET-PF05-CONSTELLATION-SVG
  - P1: Research directions row badges — row placeholder component
  - P2: Selected publications preview block on research index when CMS empty — shell only

### PF-05-pf05-publications-EN-1440-LIGHT: public-270-pf05-publications-en-1440-light.png ↔ research-publications-index-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `PublicationsPageContent.astro`, shared PF-05 hero/tabs, bibliography row placeholders
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Same as research pair; publications nav context.

- **Hero:** Same research-publications concept hero — implementation uses publications-specific title but same hero media reuse issue.

- **Navigation/tabs:** Concept tabs with Publications tab active — implementation disabled tablist does not show active Publications state distinctly.

- **Main content sections:**
  - **Bibliography list:** Concept publication rows with document icon, type chip, metadata lines, action buttons. Implementation: `PageFamilyBibliographyRowPlaceholder` — missing type chips and dual action buttons.
  - **Filter chips + search:** Concept top filters — implementation filter shell disabled.
  - **Constellation/Fit:** Not shown on publications tab in concept — correct to omit on publications route.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Publication type chips (Journal Article, etc.) — missing.

- **Imagery/assets:** Row icons — inline SVG needed. → Asset prompts: ASSET-PF05-PUB-ROW-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** All publication metadata — Category A.

- **Priority fixes:**
  - P1: Bibliography row fidelity — type chip, Details/Files buttons — `PageFamilyBibliographyRowPlaceholder.astro`
  - P1: Publications tab active state in sub-nav

### PF-05-pf05-publications-EN-390-LIGHT: public-270-pf05-publications-en-390-light.png ↔ research-publications-index-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `PublicationsPageContent.astro`, shared PF-05 hero/tabs, bibliography row placeholders
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Same as research pair; publications nav context.

- **Hero:** Same research-publications concept hero — implementation uses publications-specific title but same hero media reuse issue.

- **Navigation/tabs:** Concept tabs with Publications tab active — implementation disabled tablist does not show active Publications state distinctly.

- **Main content sections:**
  - **Bibliography list:** Concept publication rows with document icon, type chip, metadata lines, action buttons. Implementation: `PageFamilyBibliographyRowPlaceholder` — missing type chips and dual action buttons.
  - **Filter chips + search:** Concept top filters — implementation filter shell disabled.
  - **Constellation/Fit:** Not shown on publications tab in concept — correct to omit on publications route.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Publication type chips (Journal Article, etc.) — missing.

- **Imagery/assets:** Row icons — inline SVG needed. → Asset prompts: ASSET-PF05-PUB-ROW-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** All publication metadata — Category A.

- **Priority fixes:**
  - P1: Bibliography row fidelity — type chip, Details/Files buttons — `PageFamilyBibliographyRowPlaceholder.astro`
  - P1: Publications tab active state in sub-nav

### PF-05-pf05-publications-FA-1440-LIGHT: public-270-pf05-publications-fa-1440-light.png ↔ research-publications-index-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `PublicationsPageContent.astro`, shared PF-05 hero/tabs, bibliography row placeholders
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** Same as research pair; publications nav context.

- **Hero:** Same research-publications concept hero — implementation uses publications-specific title but same hero media reuse issue.

- **Navigation/tabs:** Concept tabs with Publications tab active — implementation disabled tablist does not show active Publications state distinctly.

- **Main content sections:**
  - **Bibliography list:** Concept publication rows with document icon, type chip, metadata lines, action buttons. Implementation: `PageFamilyBibliographyRowPlaceholder` — missing type chips and dual action buttons.
  - **Filter chips + search:** Concept top filters — implementation filter shell disabled.
  - **Constellation/Fit:** Not shown on publications tab in concept — correct to omit on publications route.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Publication type chips (Journal Article, etc.) — missing.

- **Imagery/assets:** Row icons — inline SVG needed. → Asset prompts: ASSET-PF05-PUB-ROW-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** All publication metadata — Category A.

- **Priority fixes:**
  - P1: Bibliography row fidelity — type chip, Details/Files buttons — `PageFamilyBibliographyRowPlaceholder.astro`
  - P1: Publications tab active state in sub-nav

### PF-05-pf05-publications-FA-390-LIGHT: public-270-pf05-publications-fa-390-light.png ↔ research-publications-index-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-05
- **Implementation files:** `PublicationsPageContent.astro`, shared PF-05 hero/tabs, bibliography row placeholders
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** Same as research pair; publications nav context.

- **Hero:** Same research-publications concept hero — implementation uses publications-specific title but same hero media reuse issue.

- **Navigation/tabs:** Concept tabs with Publications tab active — implementation disabled tablist does not show active Publications state distinctly.

- **Main content sections:**
  - **Bibliography list:** Concept publication rows with document icon, type chip, metadata lines, action buttons. Implementation: `PageFamilyBibliographyRowPlaceholder` — missing type chips and dual action buttons.
  - **Filter chips + search:** Concept top filters — implementation filter shell disabled.
  - **Constellation/Fit:** Not shown on publications tab in concept — correct to omit on publications route.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Publication type chips (Journal Article, etc.) — missing.

- **Imagery/assets:** Row icons — inline SVG needed. → Asset prompts: ASSET-PF05-PUB-ROW-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** All publication metadata — Category A.

- **Priority fixes:**
  - P1: Bibliography row fidelity — type chip, Details/Files buttons — `PageFamilyBibliographyRowPlaceholder.astro`
  - P1: Publications tab active state in sub-nav

### PF-06-pf06-EN-1440-DARK: public-270-pf06-en-1440-dark.png ↔ teaching-index-dark.png
- **Meta:** locale=en, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-06
- **Implementation files:** `TeachingPageContent.astro`, `PageFamilyFeaturedPathShell`, `PageFamilyListCardShell`, path workflow shells
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Teaching** vs concept **Learning** — Category D.

- **Hero:** Concept: **LEARNING LIBRARY**, serif **Learning**, description, star ornament, **Browse paths** CTA, moody architectural hero. Implementation: teaching title localized; missing Browse paths CTA and star ornament; hero uses teaching rail asset — closer but not concept crop.

- **Navigation/tabs:** Concept pills: All, Guides, Tutorials, Notes, Reading paths, Resources + search + Level/Topic dropdowns + Sort. Implementation: disabled filters — missing secondary dropdown row.

- **Main content sections:**
  - **Featured path:** Concept card with image, 4-step timeline (Foundations→Expand). Implementation: `PageFamilyFeaturedPathShell` — timeline steps present structurally; step connector styling gap.
  - **List rows:** Concept 6 items with GUIDE/TUTORIAL tags, level/duration columns, topic tag pills. Implementation: `PageFamilyListCardShell` — missing level/duration columns and rich tag pills.
  - **How a path works:** Concept 4-icon flow — check `PageFamilyJourneyFlowShell` reuse.
  - **Empty filter state + dual CTAs:** Concept reset card + Optional updates + Collaborate cards — partially absent.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Dark theme gold headings — teaching-page tokens.

- **Imagery/assets:** List thumbnails need learning-specific set vs recycled assets. → Asset prompts: [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md), [pf-teaching-path-ribbon-dark.md](../PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md), [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md) (list set)

- **Animation/interaction:** Path timeline could use CSS step reveal.

- **CMS/admin dependency:** All list titles, tags, level/duration — Category A.

- **Priority fixes:**
  - P0: Featured path timeline styling — `PageFamilyFeaturedPathShell.astro`
  - P1: List row level/duration columns — `PageFamilyListCardShell.astro`
  - P1: Secondary filter dropdown row (Level, Topic)

### PF-06-pf06-EN-390-DARK: public-270-pf06-en-390-dark.png ↔ teaching-index-dark.png
- **Meta:** locale=en, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-06
- **Implementation files:** `TeachingPageContent.astro`, `PageFamilyFeaturedPathShell`, `PageFamilyListCardShell`, path workflow shells
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Teaching** vs concept **Learning** — Category D.

- **Hero:** Concept: **LEARNING LIBRARY**, serif **Learning**, description, star ornament, **Browse paths** CTA, moody architectural hero. Implementation: teaching title localized; missing Browse paths CTA and star ornament; hero uses teaching rail asset — closer but not concept crop.

- **Navigation/tabs:** Concept pills: All, Guides, Tutorials, Notes, Reading paths, Resources + search + Level/Topic dropdowns + Sort. Implementation: disabled filters — missing secondary dropdown row.

- **Main content sections:**
  - **Featured path:** Concept card with image, 4-step timeline (Foundations→Expand). Implementation: `PageFamilyFeaturedPathShell` — timeline steps present structurally; step connector styling gap.
  - **List rows:** Concept 6 items with GUIDE/TUTORIAL tags, level/duration columns, topic tag pills. Implementation: `PageFamilyListCardShell` — missing level/duration columns and rich tag pills.
  - **How a path works:** Concept 4-icon flow — check `PageFamilyJourneyFlowShell` reuse.
  - **Empty filter state + dual CTAs:** Concept reset card + Optional updates + Collaborate cards — partially absent.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Dark theme gold headings — teaching-page tokens.

- **Imagery/assets:** List thumbnails need learning-specific set vs recycled assets. → Asset prompts: [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md), [pf-teaching-path-ribbon-dark.md](../PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md), [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md) (list set)

- **Animation/interaction:** Path timeline could use CSS step reveal.

- **CMS/admin dependency:** All list titles, tags, level/duration — Category A.

- **Priority fixes:**
  - P0: Featured path timeline styling — `PageFamilyFeaturedPathShell.astro`
  - P1: List row level/duration columns — `PageFamilyListCardShell.astro`
  - P1: Secondary filter dropdown row (Level, Topic)

### PF-06-pf06-FA-1440-DARK: public-270-pf06-fa-1440-dark.png ↔ teaching-index-dark.png
- **Meta:** locale=fa, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-06
- **Implementation files:** `TeachingPageContent.astro`, `PageFamilyFeaturedPathShell`, `PageFamilyListCardShell`, path workflow shells
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Teaching** vs concept **Learning** — Category D.

- **Hero:** Concept: **LEARNING LIBRARY**, serif **Learning**, description, star ornament, **Browse paths** CTA, moody architectural hero. Implementation: teaching title localized; missing Browse paths CTA and star ornament; hero uses teaching rail asset — closer but not concept crop.

- **Navigation/tabs:** Concept pills: All, Guides, Tutorials, Notes, Reading paths, Resources + search + Level/Topic dropdowns + Sort. Implementation: disabled filters — missing secondary dropdown row.

- **Main content sections:**
  - **Featured path:** Concept card with image, 4-step timeline (Foundations→Expand). Implementation: `PageFamilyFeaturedPathShell` — timeline steps present structurally; step connector styling gap.
  - **List rows:** Concept 6 items with GUIDE/TUTORIAL tags, level/duration columns, topic tag pills. Implementation: `PageFamilyListCardShell` — missing level/duration columns and rich tag pills.
  - **How a path works:** Concept 4-icon flow — check `PageFamilyJourneyFlowShell` reuse.
  - **Empty filter state + dual CTAs:** Concept reset card + Optional updates + Collaborate cards — partially absent.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Dark theme gold headings — teaching-page tokens.

- **Imagery/assets:** List thumbnails need learning-specific set vs recycled assets. → Asset prompts: [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md), [pf-teaching-path-ribbon-dark.md](../PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md), [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md) (list set)

- **Animation/interaction:** Path timeline could use CSS step reveal.

- **CMS/admin dependency:** All list titles, tags, level/duration — Category A.

- **Priority fixes:**
  - P0: Featured path timeline styling — `PageFamilyFeaturedPathShell.astro`
  - P1: List row level/duration columns — `PageFamilyListCardShell.astro`
  - P1: Secondary filter dropdown row (Level, Topic)

### PF-06-pf06-FA-390-DARK: public-270-pf06-fa-390-dark.png ↔ teaching-index-dark.png
- **Meta:** locale=fa, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-06
- **Implementation files:** `TeachingPageContent.astro`, `PageFamilyFeaturedPathShell`, `PageFamilyListCardShell`, path workflow shells
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Nav **Teaching** vs concept **Learning** — Category D.

- **Hero:** Concept: **LEARNING LIBRARY**, serif **Learning**, description, star ornament, **Browse paths** CTA, moody architectural hero. Implementation: teaching title localized; missing Browse paths CTA and star ornament; hero uses teaching rail asset — closer but not concept crop.

- **Navigation/tabs:** Concept pills: All, Guides, Tutorials, Notes, Reading paths, Resources + search + Level/Topic dropdowns + Sort. Implementation: disabled filters — missing secondary dropdown row.

- **Main content sections:**
  - **Featured path:** Concept card with image, 4-step timeline (Foundations→Expand). Implementation: `PageFamilyFeaturedPathShell` — timeline steps present structurally; step connector styling gap.
  - **List rows:** Concept 6 items with GUIDE/TUTORIAL tags, level/duration columns, topic tag pills. Implementation: `PageFamilyListCardShell` — missing level/duration columns and rich tag pills.
  - **How a path works:** Concept 4-icon flow — check `PageFamilyJourneyFlowShell` reuse.
  - **Empty filter state + dual CTAs:** Concept reset card + Optional updates + Collaborate cards — partially absent.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Dark theme gold headings — teaching-page tokens.

- **Imagery/assets:** List thumbnails need learning-specific set vs recycled assets. → Asset prompts: [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md), [pf-teaching-path-ribbon-dark.md](../PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md), [learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md) (list set)

- **Animation/interaction:** Path timeline could use CSS step reveal.

- **CMS/admin dependency:** All list titles, tags, level/duration — Category A.

- **Priority fixes:**
  - P0: Featured path timeline styling — `PageFamilyFeaturedPathShell.astro`
  - P1: List row level/duration columns — `PageFamilyListCardShell.astro`
  - P1: Secondary filter dropdown row (Level, Topic)

### PF-07-pf07-about-EN-1440-LIGHT: public-270-pf07-about-en-1440-light.png ↔ about-cv-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `AboutPageContent.astro`, `PageFamilyProfileHeroShell`, sub-nav, HowIWork, JourneyFlow, SplitTimeline, SkillsGrid, SelectedOutputs, CollaborateBand
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** About active — aligned.

- **Hero:** Concept: **PROFILE**, name heading, role line, intro, 3 CTAs (Research profile, Academic CV, Contact), arch image + portrait placeholder box. Implementation: `PageFamilyProfileHeroShell` vs `PageFamilyIndexHero` — missing tri-CTA row and portrait placeholder frame.

- **Navigation/tabs:** Concept secondary tabs: Overview, Experience, Education, Skills, Research, Publications, Certificates. Implementation: `PageFamilySubNavShell` — 7 tabs present; active underline styling gap.

- **Main content sections:**
  - **How I work:** Concept 2×2 grid with colored icons. Implementation: `PageFamilyHowIWorkShell` — aligned structurally.
  - **Interdisciplinary journey:** Concept 5-node horizontal timeline. Implementation: `PageFamilyJourneyFlowShell`.
  - **Experience & Education preview:** Concept split timeline with 6 cards + view full button. Implementation: `PageFamilySplitTimelineShell`.
  - **Skills & Expertise:** Concept 4 skill columns with bullet lists. Implementation: `PageFamilySkillsGridShell`.
  - **Selected outputs:** Concept 4 output cards. Implementation: `PageFamilySelectedOutputsShell`.
  - **CV + Contact CTAs:** Concept dual large cards. Implementation: `PageFamilyCollaborateBandShell` + download shell.

- **Footer:** Shared footer gaps; concept social icons in footer brand block.

- **Typography/color/spacing:** Profile hero name should use display scale; FA @390 hero stack order.

- **Imagery/assets:** Portrait placeholder box missing; hero arch recycles writing asset. → Asset prompts: [pf-about-identity-abstract-light.md](../PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (hero arch)

- **Animation/interaction:** Journey nodes could use scroll-triggered reveal (GSAP optional).

- **CMS/admin dependency:** All timeline cards, skills content — Category A. Shells — B.

- **Priority fixes:**
  - P0: Profile hero tri-CTA + portrait placeholder — `PageFamilyProfileHeroShell.astro`
  - P1: Sub-nav active underline — `PageFamilySubNavShell.astro` CSS

### PF-07-pf07-about-EN-390-LIGHT: public-270-pf07-about-en-390-light.png ↔ about-cv-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `AboutPageContent.astro`, `PageFamilyProfileHeroShell`, sub-nav, HowIWork, JourneyFlow, SplitTimeline, SkillsGrid, SelectedOutputs, CollaborateBand
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** About active — aligned.

- **Hero:** Concept: **PROFILE**, name heading, role line, intro, 3 CTAs (Research profile, Academic CV, Contact), arch image + portrait placeholder box. Implementation: `PageFamilyProfileHeroShell` vs `PageFamilyIndexHero` — missing tri-CTA row and portrait placeholder frame.

- **Navigation/tabs:** Concept secondary tabs: Overview, Experience, Education, Skills, Research, Publications, Certificates. Implementation: `PageFamilySubNavShell` — 7 tabs present; active underline styling gap.

- **Main content sections:**
  - **How I work:** Concept 2×2 grid with colored icons. Implementation: `PageFamilyHowIWorkShell` — aligned structurally.
  - **Interdisciplinary journey:** Concept 5-node horizontal timeline. Implementation: `PageFamilyJourneyFlowShell`.
  - **Experience & Education preview:** Concept split timeline with 6 cards + view full button. Implementation: `PageFamilySplitTimelineShell`.
  - **Skills & Expertise:** Concept 4 skill columns with bullet lists. Implementation: `PageFamilySkillsGridShell`.
  - **Selected outputs:** Concept 4 output cards. Implementation: `PageFamilySelectedOutputsShell`.
  - **CV + Contact CTAs:** Concept dual large cards. Implementation: `PageFamilyCollaborateBandShell` + download shell.

- **Footer:** Shared footer gaps; concept social icons in footer brand block.

- **Typography/color/spacing:** Profile hero name should use display scale; FA @390 hero stack order.

- **Imagery/assets:** Portrait placeholder box missing; hero arch recycles writing asset. → Asset prompts: [pf-about-identity-abstract-light.md](../PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (hero arch)

- **Animation/interaction:** Journey nodes could use scroll-triggered reveal (GSAP optional).

- **CMS/admin dependency:** All timeline cards, skills content — Category A. Shells — B.

- **Priority fixes:**
  - P0: Profile hero tri-CTA + portrait placeholder — `PageFamilyProfileHeroShell.astro`
  - P1: Sub-nav active underline — `PageFamilySubNavShell.astro` CSS

### PF-07-pf07-about-FA-1440-LIGHT: public-270-pf07-about-fa-1440-light.png ↔ about-cv-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `AboutPageContent.astro`, `PageFamilyProfileHeroShell`, sub-nav, HowIWork, JourneyFlow, SplitTimeline, SkillsGrid, SelectedOutputs, CollaborateBand
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** About active — aligned.

- **Hero:** Concept: **PROFILE**, name heading, role line, intro, 3 CTAs (Research profile, Academic CV, Contact), arch image + portrait placeholder box. Implementation: `PageFamilyProfileHeroShell` vs `PageFamilyIndexHero` — missing tri-CTA row and portrait placeholder frame.

- **Navigation/tabs:** Concept secondary tabs: Overview, Experience, Education, Skills, Research, Publications, Certificates. Implementation: `PageFamilySubNavShell` — 7 tabs present; active underline styling gap.

- **Main content sections:**
  - **How I work:** Concept 2×2 grid with colored icons. Implementation: `PageFamilyHowIWorkShell` — aligned structurally.
  - **Interdisciplinary journey:** Concept 5-node horizontal timeline. Implementation: `PageFamilyJourneyFlowShell`.
  - **Experience & Education preview:** Concept split timeline with 6 cards + view full button. Implementation: `PageFamilySplitTimelineShell`.
  - **Skills & Expertise:** Concept 4 skill columns with bullet lists. Implementation: `PageFamilySkillsGridShell`.
  - **Selected outputs:** Concept 4 output cards. Implementation: `PageFamilySelectedOutputsShell`.
  - **CV + Contact CTAs:** Concept dual large cards. Implementation: `PageFamilyCollaborateBandShell` + download shell.

- **Footer:** Shared footer gaps; concept social icons in footer brand block.

- **Typography/color/spacing:** Profile hero name should use display scale; FA @390 hero stack order.

- **Imagery/assets:** Portrait placeholder box missing; hero arch recycles writing asset. → Asset prompts: [pf-about-identity-abstract-light.md](../PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (hero arch)

- **Animation/interaction:** Journey nodes could use scroll-triggered reveal (GSAP optional).

- **CMS/admin dependency:** All timeline cards, skills content — Category A. Shells — B.

- **Priority fixes:**
  - P0: Profile hero tri-CTA + portrait placeholder — `PageFamilyProfileHeroShell.astro`
  - P1: Sub-nav active underline — `PageFamilySubNavShell.astro` CSS

### PF-07-pf07-about-FA-390-LIGHT: public-270-pf07-about-fa-390-light.png ↔ about-cv-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `AboutPageContent.astro`, `PageFamilyProfileHeroShell`, sub-nav, HowIWork, JourneyFlow, SplitTimeline, SkillsGrid, SelectedOutputs, CollaborateBand
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** About active — aligned.

- **Hero:** Concept: **PROFILE**, name heading, role line, intro, 3 CTAs (Research profile, Academic CV, Contact), arch image + portrait placeholder box. Implementation: `PageFamilyProfileHeroShell` vs `PageFamilyIndexHero` — missing tri-CTA row and portrait placeholder frame.

- **Navigation/tabs:** Concept secondary tabs: Overview, Experience, Education, Skills, Research, Publications, Certificates. Implementation: `PageFamilySubNavShell` — 7 tabs present; active underline styling gap.

- **Main content sections:**
  - **How I work:** Concept 2×2 grid with colored icons. Implementation: `PageFamilyHowIWorkShell` — aligned structurally.
  - **Interdisciplinary journey:** Concept 5-node horizontal timeline. Implementation: `PageFamilyJourneyFlowShell`.
  - **Experience & Education preview:** Concept split timeline with 6 cards + view full button. Implementation: `PageFamilySplitTimelineShell`.
  - **Skills & Expertise:** Concept 4 skill columns with bullet lists. Implementation: `PageFamilySkillsGridShell`.
  - **Selected outputs:** Concept 4 output cards. Implementation: `PageFamilySelectedOutputsShell`.
  - **CV + Contact CTAs:** Concept dual large cards. Implementation: `PageFamilyCollaborateBandShell` + download shell.

- **Footer:** Shared footer gaps; concept social icons in footer brand block.

- **Typography/color/spacing:** Profile hero name should use display scale; FA @390 hero stack order.

- **Imagery/assets:** Portrait placeholder box missing; hero arch recycles writing asset. → Asset prompts: [pf-about-identity-abstract-light.md](../PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md), [gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (hero arch)

- **Animation/interaction:** Journey nodes could use scroll-triggered reveal (GSAP optional).

- **CMS/admin dependency:** All timeline cards, skills content — Category A. Shells — B.

- **Priority fixes:**
  - P0: Profile hero tri-CTA + portrait placeholder — `PageFamilyProfileHeroShell.astro`
  - P1: Sub-nav active underline — `PageFamilySubNavShell.astro` CSS

### PF-07-pf07-cv-EN-1440-LIGHT: public-270-pf07-cv-en-1440-light.png ↔ about-cv-light.png
- **Meta:** locale=en, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `CvPageContent.astro`, CV hero, download list shell, timeline shells
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** CV route — not in primary nav concept but in footer RESOURCES.

- **Hero:** Concept (about-cv): CV-specific hero with download emphasis — implementation uses generic index hero.

- **Navigation/tabs:** Concept shows CV/downloads context — implementation minimal.

- **Main content sections:**
  - **Downloads section:** Concept download cards with file type icons. Implementation: `PageFamilyDownloadListShell`.
  - **Experience/Education:** Shared timeline shells — same gaps as about.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** CV page title/display sizing.

- **Imagery/assets:** Download card icons. → Asset prompts: ASSET-PF07-CV-DOWNLOAD-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** CV file records — Category A.

- **Priority fixes:**
  - P1: CV-specific hero variant — `CvPageContent.astro`
  - P1: Download list card styling

### PF-07-pf07-cv-EN-390-LIGHT: public-270-pf07-cv-en-390-light.png ↔ about-cv-light.png
- **Meta:** locale=en, viewport=390px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `CvPageContent.astro`, CV hero, download list shell, timeline shells
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** CV route — not in primary nav concept but in footer RESOURCES.

- **Hero:** Concept (about-cv): CV-specific hero with download emphasis — implementation uses generic index hero.

- **Navigation/tabs:** Concept shows CV/downloads context — implementation minimal.

- **Main content sections:**
  - **Downloads section:** Concept download cards with file type icons. Implementation: `PageFamilyDownloadListShell`.
  - **Experience/Education:** Shared timeline shells — same gaps as about.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** CV page title/display sizing.

- **Imagery/assets:** Download card icons. → Asset prompts: ASSET-PF07-CV-DOWNLOAD-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** CV file records — Category A.

- **Priority fixes:**
  - P1: CV-specific hero variant — `CvPageContent.astro`
  - P1: Download list card styling

### PF-07-pf07-cv-FA-1440-LIGHT: public-270-pf07-cv-fa-1440-light.png ↔ about-cv-light.png
- **Meta:** locale=fa, viewport=1440px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `CvPageContent.astro`, CV hero, download list shell, timeline shells
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.

- **Header:** CV route — not in primary nav concept but in footer RESOURCES.

- **Hero:** Concept (about-cv): CV-specific hero with download emphasis — implementation uses generic index hero.

- **Navigation/tabs:** Concept shows CV/downloads context — implementation minimal.

- **Main content sections:**
  - **Downloads section:** Concept download cards with file type icons. Implementation: `PageFamilyDownloadListShell`.
  - **Experience/Education:** Shared timeline shells — same gaps as about.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** CV page title/display sizing.

- **Imagery/assets:** Download card icons. → Asset prompts: ASSET-PF07-CV-DOWNLOAD-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** CV file records — Category A.

- **Priority fixes:**
  - P1: CV-specific hero variant — `CvPageContent.astro`
  - P1: Download list card styling

### PF-07-pf07-cv-FA-390-LIGHT: public-270-pf07-cv-fa-390-light.png ↔ about-cv-light.png
- **Meta:** locale=fa, viewport=390px, theme=light, status=ready (concept paired), PF=PF-07
- **Implementation files:** `CvPageContent.astro`, CV hero, download list shell, timeline shells
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.

- **Header:** CV route — not in primary nav concept but in footer RESOURCES.

- **Hero:** Concept (about-cv): CV-specific hero with download emphasis — implementation uses generic index hero.

- **Navigation/tabs:** Concept shows CV/downloads context — implementation minimal.

- **Main content sections:**
  - **Downloads section:** Concept download cards with file type icons. Implementation: `PageFamilyDownloadListShell`.
  - **Experience/Education:** Shared timeline shells — same gaps as about.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** CV page title/display sizing.

- **Imagery/assets:** Download card icons. → Asset prompts: ASSET-PF07-CV-DOWNLOAD-ICONS (stub — SVG inline preferred)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** CV file records — Category A.

- **Priority fixes:**
  - P1: CV-specific hero variant — `CvPageContent.astro`
  - P1: Download list card styling

### PF-08-pf08-EN-1440-DARK: public-270-pf08-en-1440-dark.png ↔ contact-dark.png
- **Meta:** locale=en, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-08
- **Implementation files:** `ContactPageContent.astro`, portal hero, topic cards, sidebar, FAQ, form, send workflow
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Contact not in concept primary nav (utility route) — header otherwise aligned.

- **Hero:** Concept: **COLLABORATION**, gold serif **Let's talk**, description, availability CMS line, glowing arch + geometric atmosphere right. Implementation: portal `PageFamilyIndexHero` with gateway atmosphere — closer @ Path A but lacks gold heading treatment and availability badge.

- **Navigation/tabs:** Topic cards row: PhD/Research, Technical, Creative, Other — `PageFamilyTopicCardsShell` present; selection state styling gap.

- **Main content sections:**
  - **Contact methods:** Concept Academic email, LinkedIn, ORCID cards. Implementation: sidebar shell with placeholders.
  - **Before you write:** Concept 4-point list — check sidebar shell.
  - **Form:** Concept full form with topic dropdown, anti-spam ready, send button, privacy note. Implementation: disabled form fields in empty state — structural; needs visual parity with concept field spacing.
  - **Send workflow + FAQ:** `PageFamilySendWorkflowShell`, `PageFamilyFaqShell` — verify accordion styling.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Gold serif **Let's talk** on dark — contact-page heading tokens.

- **Imagery/assets:** Portal atmosphere uses gateway assets — acceptable; concept geometric overlay denser. → Asset prompts: [pf-contact-atmosphere-dark.md](../PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md), [portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)

- **Animation/interaction:** Form state transitions — CSS; send workflow icons.

- **CMS/admin dependency:** Email, LinkedIn, ORCID, availability — Category A.

- **Priority fixes:**
  - P0: Contact hero gold serif + availability badge — `PageFamilyIndexHero` contact variant CSS
  - P1: Topic card selected state — `PageFamilyTopicCardsShell.astro`
  - P1: Form empty-state visual parity — `ContactPageContent.astro`

### PF-08-pf08-EN-390-DARK: public-270-pf08-en-390-dark.png ↔ contact-dark.png
- **Meta:** locale=en, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-08
- **Implementation files:** `ContactPageContent.astro`, portal hero, topic cards, sidebar, FAQ, form, send workflow
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Contact not in concept primary nav (utility route) — header otherwise aligned.

- **Hero:** Concept: **COLLABORATION**, gold serif **Let's talk**, description, availability CMS line, glowing arch + geometric atmosphere right. Implementation: portal `PageFamilyIndexHero` with gateway atmosphere — closer @ Path A but lacks gold heading treatment and availability badge.

- **Navigation/tabs:** Topic cards row: PhD/Research, Technical, Creative, Other — `PageFamilyTopicCardsShell` present; selection state styling gap.

- **Main content sections:**
  - **Contact methods:** Concept Academic email, LinkedIn, ORCID cards. Implementation: sidebar shell with placeholders.
  - **Before you write:** Concept 4-point list — check sidebar shell.
  - **Form:** Concept full form with topic dropdown, anti-spam ready, send button, privacy note. Implementation: disabled form fields in empty state — structural; needs visual parity with concept field spacing.
  - **Send workflow + FAQ:** `PageFamilySendWorkflowShell`, `PageFamilyFaqShell` — verify accordion styling.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Gold serif **Let's talk** on dark — contact-page heading tokens.

- **Imagery/assets:** Portal atmosphere uses gateway assets — acceptable; concept geometric overlay denser. → Asset prompts: [pf-contact-atmosphere-dark.md](../PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md), [portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)

- **Animation/interaction:** Form state transitions — CSS; send workflow icons.

- **CMS/admin dependency:** Email, LinkedIn, ORCID, availability — Category A.

- **Priority fixes:**
  - P0: Contact hero gold serif + availability badge — `PageFamilyIndexHero` contact variant CSS
  - P1: Topic card selected state — `PageFamilyTopicCardsShell.astro`
  - P1: Form empty-state visual parity — `ContactPageContent.astro`

### PF-08-pf08-FA-1440-DARK: public-270-pf08-fa-1440-dark.png ↔ contact-dark.png
- **Meta:** locale=fa, viewport=1440px, theme=dark, status=ready (concept paired), PF=PF-08
- **Implementation files:** `ContactPageContent.astro`, portal hero, topic cards, sidebar, FAQ, form, send workflow
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Contact not in concept primary nav (utility route) — header otherwise aligned.

- **Hero:** Concept: **COLLABORATION**, gold serif **Let's talk**, description, availability CMS line, glowing arch + geometric atmosphere right. Implementation: portal `PageFamilyIndexHero` with gateway atmosphere — closer @ Path A but lacks gold heading treatment and availability badge.

- **Navigation/tabs:** Topic cards row: PhD/Research, Technical, Creative, Other — `PageFamilyTopicCardsShell` present; selection state styling gap.

- **Main content sections:**
  - **Contact methods:** Concept Academic email, LinkedIn, ORCID cards. Implementation: sidebar shell with placeholders.
  - **Before you write:** Concept 4-point list — check sidebar shell.
  - **Form:** Concept full form with topic dropdown, anti-spam ready, send button, privacy note. Implementation: disabled form fields in empty state — structural; needs visual parity with concept field spacing.
  - **Send workflow + FAQ:** `PageFamilySendWorkflowShell`, `PageFamilyFaqShell` — verify accordion styling.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Gold serif **Let's talk** on dark — contact-page heading tokens.

- **Imagery/assets:** Portal atmosphere uses gateway assets — acceptable; concept geometric overlay denser. → Asset prompts: [pf-contact-atmosphere-dark.md](../PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md), [portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)

- **Animation/interaction:** Form state transitions — CSS; send workflow icons.

- **CMS/admin dependency:** Email, LinkedIn, ORCID, availability — Category A.

- **Priority fixes:**
  - P0: Contact hero gold serif + availability badge — `PageFamilyIndexHero` contact variant CSS
  - P1: Topic card selected state — `PageFamilyTopicCardsShell.astro`
  - P1: Form empty-state visual parity — `ContactPageContent.astro`

### PF-08-pf08-FA-390-DARK: public-270-pf08-fa-390-dark.png ↔ contact-dark.png
- **Meta:** locale=fa, viewport=390px, theme=dark, status=ready (concept paired), PF=PF-08
- **Implementation files:** `ContactPageContent.astro`, portal hero, topic cards, sidebar, FAQ, form, send workflow
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Contact not in concept primary nav (utility route) — header otherwise aligned.

- **Hero:** Concept: **COLLABORATION**, gold serif **Let's talk**, description, availability CMS line, glowing arch + geometric atmosphere right. Implementation: portal `PageFamilyIndexHero` with gateway atmosphere — closer @ Path A but lacks gold heading treatment and availability badge.

- **Navigation/tabs:** Topic cards row: PhD/Research, Technical, Creative, Other — `PageFamilyTopicCardsShell` present; selection state styling gap.

- **Main content sections:**
  - **Contact methods:** Concept Academic email, LinkedIn, ORCID cards. Implementation: sidebar shell with placeholders.
  - **Before you write:** Concept 4-point list — check sidebar shell.
  - **Form:** Concept full form with topic dropdown, anti-spam ready, send button, privacy note. Implementation: disabled form fields in empty state — structural; needs visual parity with concept field spacing.
  - **Send workflow + FAQ:** `PageFamilySendWorkflowShell`, `PageFamilyFaqShell` — verify accordion styling.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** Gold serif **Let's talk** on dark — contact-page heading tokens.

- **Imagery/assets:** Portal atmosphere uses gateway assets — acceptable; concept geometric overlay denser. → Asset prompts: [pf-contact-atmosphere-dark.md](../PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md), [portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)

- **Animation/interaction:** Form state transitions — CSS; send workflow icons.

- **CMS/admin dependency:** Email, LinkedIn, ORCID, availability — Category A.

- **Priority fixes:**
  - P0: Contact hero gold serif + availability badge — `PageFamilyIndexHero` contact variant CSS
  - P1: Topic card selected state — `PageFamilyTopicCardsShell.astro`
  - P1: Form empty-state visual parity — `ContactPageContent.astro`

### PF-02-pf02-EN-1440-DARK: public-270-pf02-en-1440-dark.png ↔ creative-detail-dark.png
- **Meta:** locale=en, viewport=1440px, theme=dark, status=blocked-route (PF-02 detail — no capture), PF=PF-02
- **Implementation files:** `CreativeDetailContent.astro` — route blocked (no published detail in static build)
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** N/A — capture not generated.

- **Hero:** N/A

- **Navigation/tabs:** N/A

- **Main content sections:**
  - Concept detail: breadcrumb, hero gallery 1/6, meta grid, thumbnail carousel, process steps, credits, related work, prev/next — all blocked until published creative detail route exists.

- **Footer:** N/A

- **Typography/color/spacing:** N/A

- **Imagery/assets:** Detail hero gallery assets — ASSET-PF02-GALLERY-SET → Asset prompts: [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) (gallery hero), ASSET-PF02-PROCESS-ICONS (stub), ASSET-PF02-RELATED-THUMBS (stub)

- **Animation/interaction:** Gallery carousel — React island or CSS scroll-snap.

- **CMS/admin dependency:** Entire detail record — Category A + route publish.

- **Priority fixes:**
  - P0: Unblock route — published creative detail slug in static build
  - P0: Implement detail template vs creative-detail-dark.png

### PF-02-pf02-EN-390-DARK: public-270-pf02-en-390-dark.png ↔ creative-detail-dark.png
- **Meta:** locale=en, viewport=390px, theme=dark, status=blocked-route (PF-02 detail — no capture), PF=PF-02
- **Implementation files:** `CreativeDetailContent.astro` — route blocked (no published detail in static build)
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** N/A — capture not generated.

- **Hero:** N/A

- **Navigation/tabs:** N/A

- **Main content sections:**
  - Concept detail: breadcrumb, hero gallery 1/6, meta grid, thumbnail carousel, process steps, credits, related work, prev/next — all blocked until published creative detail route exists.

- **Footer:** N/A

- **Typography/color/spacing:** N/A

- **Imagery/assets:** Detail hero gallery assets — ASSET-PF02-GALLERY-SET → Asset prompts: [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) (gallery hero), ASSET-PF02-PROCESS-ICONS (stub), ASSET-PF02-RELATED-THUMBS (stub)

- **Animation/interaction:** Gallery carousel — React island or CSS scroll-snap.

- **CMS/admin dependency:** Entire detail record — Category A + route publish.

- **Priority fixes:**
  - P0: Unblock route — published creative detail slug in static build
  - P0: Implement detail template vs creative-detail-dark.png

### PF-02-pf02-FA-1440-DARK: public-270-pf02-fa-1440-dark.png ↔ creative-detail-dark.png
- **Meta:** locale=fa, viewport=1440px, theme=dark, status=blocked-route (PF-02 detail — no capture), PF=PF-02
- **Implementation files:** `CreativeDetailContent.astro` — route blocked (no published detail in static build)
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** N/A — capture not generated.

- **Hero:** N/A

- **Navigation/tabs:** N/A

- **Main content sections:**
  - Concept detail: breadcrumb, hero gallery 1/6, meta grid, thumbnail carousel, process steps, credits, related work, prev/next — all blocked until published creative detail route exists.

- **Footer:** N/A

- **Typography/color/spacing:** N/A

- **Imagery/assets:** Detail hero gallery assets — ASSET-PF02-GALLERY-SET → Asset prompts: [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) (gallery hero), ASSET-PF02-PROCESS-ICONS (stub), ASSET-PF02-RELATED-THUMBS (stub)

- **Animation/interaction:** Gallery carousel — React island or CSS scroll-snap.

- **CMS/admin dependency:** Entire detail record — Category A + route publish.

- **Priority fixes:**
  - P0: Unblock route — published creative detail slug in static build
  - P0: Implement detail template vs creative-detail-dark.png

### PF-02-pf02-FA-390-DARK: public-270-pf02-fa-390-dark.png ↔ creative-detail-dark.png
- **Meta:** locale=fa, viewport=390px, theme=dark, status=blocked-route (PF-02 detail — no capture), PF=PF-02
- **Implementation files:** `CreativeDetailContent.astro` — route blocked (no published detail in static build)
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** N/A — capture not generated.

- **Hero:** N/A

- **Navigation/tabs:** N/A

- **Main content sections:**
  - Concept detail: breadcrumb, hero gallery 1/6, meta grid, thumbnail carousel, process steps, credits, related work, prev/next — all blocked until published creative detail route exists.

- **Footer:** N/A

- **Typography/color/spacing:** N/A

- **Imagery/assets:** Detail hero gallery assets — ASSET-PF02-GALLERY-SET → Asset prompts: [pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) (gallery hero), ASSET-PF02-PROCESS-ICONS (stub), ASSET-PF02-RELATED-THUMBS (stub)

- **Animation/interaction:** Gallery carousel — React island or CSS scroll-snap.

- **CMS/admin dependency:** Entire detail record — Category A + route publish.

- **Priority fixes:**
  - P0: Unblock route — published creative detail slug in static build
  - P0: Implement detail template vs creative-detail-dark.png

### HOME-HOME-EN-768-LIGHT: wp40-home-en-768-light.png ↔ _(none — capture-only review)_
- **Meta:** locale=en, viewport=768px, theme=light, status=capture-only (no concept reference), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@768 tablet reflow:** No exact concept width — nearest FA mobile concept @390 used for FA light only.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-EN-768-DARK: wp40-home-en-768-dark.png ↔ _(none — capture-only review)_
- **Meta:** locale=en, viewport=768px, theme=dark, status=capture-only (no concept reference), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@768 tablet reflow:** No exact concept width — nearest FA mobile concept @390 used for FA light only.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-FA-768-LIGHT: wp40-home-fa-768-light.png ↔ home-mobile-fa-light-concept-v1.png
- **Meta:** locale=fa, viewport=768px, theme=light, status=ready (concept paired), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@768 tablet reflow:** No exact concept width — nearest FA mobile concept @390 used for FA light only.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-FA-768-DARK: wp40-home-fa-768-dark.png ↔ _(none — capture-only review)_
- **Meta:** locale=fa, viewport=768px, theme=dark, status=capture-only (no concept reference), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@768 tablet reflow:** No exact concept width — nearest FA mobile concept @390 used for FA light only.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-EN-200PCT-LIGHT: wp40-home-en-200pct-light.png ↔ _(none — capture-only review)_
- **Meta:** locale=en, viewport=720px, theme=light, status=capture-only (no concept reference), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@720 (200% zoom):** Accessibility evidence — assess readability, tap targets, text spacing; not pixel-match to desktop concept.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-EN-200PCT-DARK: wp40-home-en-200pct-dark.png ↔ _(none — capture-only review)_
- **Meta:** locale=en, viewport=720px, theme=dark, status=capture-only (no concept reference), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@720 (200% zoom):** Accessibility evidence — assess readability, tap targets, text spacing; not pixel-match to desktop concept.
**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-HOME-FA-200PCT-LIGHT: wp40-home-fa-200pct-light.png ↔ home-mobile-fa-light-concept-v1.png
- **Meta:** locale=fa, viewport=720px, theme=light, status=ready (concept paired), PF=Home
- **Implementation files:** `HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS
- **Viewport/locale notes:** **RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).
**@720 (200% zoom):** Accessibility evidence — assess readability, tap targets, text spacing; not pixel-match to desktop concept.

- **Header:** Home header — aligned with site shell.

- **Hero:** Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).

- **Navigation/tabs:** N/A on home.

- **Main content sections:**
  - Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.

- **Footer:** Shared footer gaps.

- **Typography/color/spacing:** 200% zoom pairs — readability audit only.

- **Imagery/assets:** Home graph backplate, portal orbit — promoted assets exist; mobile crop differs. → Asset prompts: [portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md), [home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)

- **Animation/interaction:** Orbit/graph may need reduced-motion fallbacks.

- **CMS/admin dependency:** Featured cards — partial seed (Category A for production copy).

- **Priority fixes:**
  - P1: Mobile FA hero layout parity — `HomeHero.astro` @768
  - P2: EN tablet concepts missing from authority — capture-only review

### HOME-GATEWAY-200PCT-LIGHT: wp40-gateway-200pct-light.png ↔ language-gateway-dark-concept-v1.png
- **Meta:** locale=neutral, viewport=720px, theme=light, status=ready (concept paired), PF=Gateway
- **Implementation files:** Gateway page / language selection
- **Viewport/locale notes:** **LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).
**@720 (200% zoom):** Accessibility evidence — assess readability, tap targets, text spacing; not pixel-match to desktop concept.

- **Header:** N/A

- **Hero:** Concept dark gateway vs capture light @200% — theme differs by design (Category D). Compare language-choice affordance and scale only.

- **Navigation/tabs:** N/A

- **Main content sections:**
  - Language buttons layout and typography at 200% zoom.

- **Footer:** Minimal/none on gateway.

- **Typography/color/spacing:** 200% readability — a11y not visual concept match.

- **Imagery/assets:** Gateway atmosphere assets exist. → Asset prompts: [portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)

- **Animation/interaction:** Static.

- **CMS/admin dependency:** N/A

- **Priority fixes:**
  - P2: Affordance parity at 200% — not theme match


---

## Owner/CMS-only pairs (no code-only fix)

| Pair ID | Blocker |
|---------|---------|
| PF-02-* (×4) | No published creative detail route in static build — captures skipped |
| All ready PF pairs | Category A record copy (titles, excerpts, tags, publication metadata, contact email/ORCID) |
| HOME-* (featured content) | Production CMS records for featured projects/publications beyond seed slugs |

---

## Regenerate compare evidence

```powershell
cd Front-End/public-site
npm run review:visual
# Opens test-results/visual/compare-report.html (gitignored)
```

---

## Related documents

- [`PUBLIC-190-VISUAL-QA.md`](./PUBLIC-190-VISUAL-QA.md) — verdict REVISE
- [`PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md`](../../Front-End/public-site/docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md)
- [`page-family-visual-compare.mjs`](../../Front-End/public-site/scripts/page-family-visual-compare.mjs) — pair source of truth
- [`PUBLIC-190-asset-prompts/`](./PUBLIC-190-asset-prompts/) — image generation prompts (in progress)

**Do not set PUBLIC-190 PASS until:** owner manual compare, accepted SHA-256 hashes, manual a11y, explicit sign-off.
