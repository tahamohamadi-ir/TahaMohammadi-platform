# PUBLIC-190 Visual Remediation Plan

**Status:** Analysis + phased fix plan (no implementation in this pass)  
**Public-site commit analyzed:** `dd515a0`  
**Compare report:** `Front-End/public-site/test-results/visual/compare-report.html`  
**Concept authority:** `Docs/references/frontend-design-authority/concepts/`  
**QA contract:** `Docs/04-design/VISUAL-QA-CONTRACT.md`  
**Verdict:** `REVISE` — unchanged; owner sign-off still required after remediation

---

## Executive summary

Owner compare-report review (39 ready pairs @ `dd515a0`) shows **structural shells exist** but **visual fidelity remains far below design authority**. Gaps are not primarily “missing routes” — they are **typography scale, surface/glow treatment, hero composition, diagram fidelity, filter-bar density, footer/header chrome, and layout rhythm**. Several captures (PF-05 Publications, PF-07 CV) suggest **rendering or scroll/viewport bugs** in addition to styling debt.

**Path A constraint holds:** no invented CMS copy, dates, titles, or API fields. Use approved placeholders (`Awaiting approved CMS copy` / localized equivalent from `getCmsPlaceholderCopy`) and decorative authority assets only.

**Subagent overlap:** [Close concept-implementation visual gap](9c29878c-5ea8-443f-af26-32595df5446e) was launched to implement the same priority stack but **has no commits** as of this plan (transcript shows doc read only). Parallel work through `a6dbca1`–`dd515a0` already added page-family shell **components** and partial CSS. **Do not duplicate shell scaffolding** — next pass should focus on **CSS fidelity, SVG/canvas illustration upgrades, layout bugs, and home mobile restructure**.

---

## 1. Compare-report pair inventory

**Totals:** 48 rows · **39 ready** (concept-paired) · **9 non-ready** (4 PF-02 skip + 5 home capture-only)

Pairing logic: `Front-End/public-site/scripts/page-family-visual-compare.mjs`  
Report generator: `Front-End/public-site/scripts/generate-visual-compare-report.mjs`

### 1.1 Ready pairs (39)

| # | Pair ID | Implementation capture | Concept reference | Locale | Breakpoint | Theme |
|---|---------|------------------------|-------------------|--------|------------|-------|
| 1 | PF-01-EN-1440-L | `public-270-pf01-en-1440-light.png` | `concepts/page-families/creative-index-light.png` | en | 1440 | light |
| 2 | PF-01-EN-390-L | `public-270-pf01-en-390-light.png` | same | en | 390 | light |
| 3 | PF-01-FA-1440-L | `public-270-pf01-fa-1440-light.png` | same | fa | 1440 | light |
| 4 | PF-01-FA-390-L | `public-270-pf01-fa-390-light.png` | same | fa | 390 | light |
| 5 | PF-03-EN-1440-L | `public-270-pf03-en-1440-light.png` | `concepts/page-families/writing-index-light.png` | en | 1440 | light |
| 6 | PF-03-EN-390-L | `public-270-pf03-en-390-light.png` | same | en | 390 | light |
| 7 | PF-03-FA-1440-L | `public-270-pf03-fa-1440-light.png` | same | fa | 1440 | light |
| 8 | PF-03-FA-390-L | `public-270-pf03-fa-390-light.png` | same | fa | 390 | light |
| 9 | PF-04-EN-1440-D | `public-270-pf04-en-1440-dark.png` | `concepts/page-families/projects-index-dark.png` | en | 1440 | dark |
| 10 | PF-04-EN-390-D | `public-270-pf04-en-390-dark.png` | same | en | 390 | dark |
| 11 | PF-04-FA-1440-D | `public-270-pf04-fa-1440-dark.png` | same | fa | 1440 | dark |
| 12 | PF-04-FA-390-D | `public-270-pf04-fa-390-dark.png` | same | fa | 390 | dark |
| 13 | PF-05R-EN-1440-L | `public-270-pf05-research-en-1440-light.png` | `concepts/page-families/research-publications-index-light.png` | en | 1440 | light |
| 14 | PF-05R-EN-390-L | `public-270-pf05-research-en-390-light.png` | same | en | 390 | light |
| 15 | PF-05R-FA-1440-L | `public-270-pf05-research-fa-1440-light.png` | same | fa | 1440 | light |
| 16 | PF-05R-FA-390-L | `public-270-pf05-research-fa-390-light.png` | same | fa | 390 | light |
| 17 | PF-05P-EN-1440-L | `public-270-pf05-publications-en-1440-light.png` | same concept (publications band) | en | 1440 | light |
| 18 | PF-05P-EN-390-L | `public-270-pf05-publications-en-390-light.png` | same | en | 390 | light |
| 19 | PF-05P-FA-1440-L | `public-270-pf05-publications-fa-1440-light.png` | same | fa | 1440 | light |
| 20 | PF-05P-FA-390-L | `public-270-pf05-publications-fa-390-light.png` | same | fa | 390 | light |
| 21 | PF-06-EN-1440-D | `public-270-pf06-en-1440-dark.png` | `concepts/page-families/teaching-index-dark.png` | en | 1440 | dark |
| 22 | PF-06-EN-390-D | `public-270-pf06-en-390-dark.png` | same | en | 390 | dark |
| 23 | PF-06-FA-1440-D | `public-270-pf06-fa-1440-dark.png` | same | fa | 1440 | dark |
| 24 | PF-06-FA-390-D | `public-270-pf06-fa-390-dark.png` | same | fa | 390 | dark |
| 25 | PF-07A-EN-1440-L | `public-270-pf07-about-en-1440-light.png` | `concepts/page-families/about-cv-light.png` | en | 1440 | light |
| 26 | PF-07A-EN-390-L | `public-270-pf07-about-en-390-light.png` | same | en | 390 | light |
| 27 | PF-07A-FA-1440-L | `public-270-pf07-about-fa-1440-light.png` | same | fa | 1440 | light |
| 28 | PF-07A-FA-390-L | `public-270-pf07-about-fa-390-light.png` | same | fa | 390 | light |
| 29 | PF-07C-EN-1440-L | `public-270-pf07-cv-en-1440-light.png` | same | en | 1440 | light |
| 30 | PF-07C-EN-390-L | `public-270-pf07-cv-en-390-light.png` | same | en | 390 | light |
| 31 | PF-07C-FA-1440-L | `public-270-pf07-cv-fa-1440-light.png` | same | fa | 1440 | light |
| 32 | PF-07C-FA-390-L | `public-270-pf07-cv-fa-390-light.png` | same | fa | 390 | light |
| 33 | PF-08-EN-1440-D | `public-270-pf08-en-1440-dark.png` | `concepts/page-families/contact-dark.png` | en | 1440 | dark |
| 34 | PF-08-EN-390-D | `public-270-pf08-en-390-dark.png` | same | en | 390 | dark |
| 35 | PF-08-FA-1440-D | `public-270-pf08-fa-1440-dark.png` | same | fa | 1440 | dark |
| 36 | PF-08-FA-390-D | `public-270-pf08-fa-390-dark.png` | same | fa | 390 | dark |
| 37 | HOME-FA-768-L | `wp40-home-fa-768-light.png` | `concepts/home-mobile-fa-light-concept-v1.png` (390 ref) | fa | 768→390 | light |
| 38 | HOME-FA-200-L | `wp40-home-fa-200pct-light.png` | same | fa | 720→390 | light |
| 39 | GATE-200-L | `wp40-gateway-200pct-light.png` | `concepts/language-gateway-dark-concept-v1.png` (affordance only) | neutral | 720→1440 | light vs dark concept |

### 1.2 Non-ready pairs (9)

| # | Pair ID | Implementation capture | Concept | Reason |
|---|---------|------------------------|---------|--------|
| N1–N4 | PF-02-* | `public-270-pf02-{en\|fa}-{1440\|390}-dark.png` | `creative-detail-dark.png` | **Skipped** — no published creative detail route in static build |
| N5 | HOME-EN-768-L | `wp40-home-en-768-light.png` | — | Capture-only (no EN tablet concept) |
| N6 | HOME-EN-768-D | `wp40-home-en-768-dark.png` | — | Capture-only |
| N7 | HOME-EN-200-L | `wp40-home-en-200pct-light.png` | — | Capture-only (a11y zoom evidence) |
| N8 | HOME-EN-200-D | `wp40-home-en-200pct-dark.png` | — | Capture-only |
| N9 | HOME-FA-768-D | `wp40-home-fa-768-dark.png` | — | Capture-only (no FA dark mobile concept) |

### 1.3 Owner screenshot → pair mapping (20 attachments)

| Screenshot (timestamp) | Mapped pair ID(s) | Notes |
|------------------------|-------------------|-------|
| 061513 | PF-05R-EN-1440-L | Research hero, tabs, constellation, research-fit |
| 061523 | PF-05P-EN-1440-L | Publications — black main content void |
| 061538 | PF-06-EN-1440-D | Teaching hero + featured path (upper) |
| 061544 | PF-06-EN-1440-D | Teaching list, path process, dual CTAs, footer (lower scroll) |
| 061601 | PF-06-FA-1440-D | RTL teaching index |
| 061609 | PF-06-FA-1440-D | Footer/CTA band (compare crop may cross-pair with teaching concept) |
| 061621 | PF-07A-EN-1440-L | About hero — wrong title scale vs profile hero concept |
| 061628 | PF-07A-EN-1440-L | About mid-page — journey/timeline/skills (lower scroll) |
| 061639 | PF-07A-EN-1440-L | About/CV lower — skills, outputs, CV band, 4-col footer (concept ref crop) |
| 061646 | PF-07C-EN-1440-L | CV capture mostly empty vs concept stack |
| 061701 | PF-08-EN-1440-D | Contact hero — portal glow, “Let’s talk” typography |
| 061710 | PF-08-EN-1440-D | Contact form, FAQ, send workflow, footer (lower scroll) |
| 061716 | HOME-FA-768-L | Home research constellation / paths map vs watercolor concept |
| 061730 | HOME-FA-768-L | Home FA mobile hero — overlay card vs split arch layout |
| 061739 | GATE-200-L | Gateway logo order, portal nodes, language buttons |
| 061757 | PF-01-EN-1440-L or PF-04-EN-1440-D | Creative or Projects index (pagination/masonry) — confirm in report TOC |
| 061825 | Multi (PF-05–08) | Subagent context bundle |
| 061833 | Multi (PF-05–08) | Subagent context bundle |
| _(first 4 images in batch 1)_ | PF-01, PF-03, PF-04, PF-05 | Not re-attached in subagent transcript; use compare-report for PF-01/03/04 |

---

## 2. Cross-cutting gap themes

| Theme | Severity | Fix types | Primary files |
|-------|----------|-----------|---------------|
| Header chrome — nav labels (Creative/Writing/Teaching vs Gallery/Blog/Learning), brand lockup, theme icon | P2 (IA) / P1 (visual) | CSS + `navigation.ts` labels if owner approves | `Header.astro`, `shell.css`, `navigation.ts` |
| Footer 4-column — structure exists; visual weight, social icons, contact email/location, glow | P0 | CSS + icon SVG set + optional real links when CMS provides | `Footer.astro`, `shell.css`, `navigation.ts` |
| Hero pattern — side media vs integrated arch, serif display scale, gold/teal accents, CTA cluster | P0 | CSS + `PageFamilyIndexHero` / `PageFamilyProfileHeroShell` | `page-families.css`, hero shells |
| Tab/sub-nav shell — present but flat chips vs underlined tabs | P1 | CSS | `page-families.css`, `PageFamilySubNavShell.astro` |
| Filter bars — missing Level/Topic/Sort dropdowns on teaching; flat chips elsewhere | P1 | Astro component + CSS | `TeachingPageContent.astro`, new `PageFamilyFilterBarShell.astro` |
| Placeholder honesty — grey bars OK; need concept-matching card chrome + “Awaiting approved CMS copy” | P1 | CSS + shell markup | row/card shells |
| Surface/glow — dark atlas glow, light editorial warmth missing | P0 | CSS gradients, box-shadow, `color-mix` tokens | `global.css`, `page-families.css` |
| Diagram fidelity — constellation, journey flow, portal, home orbit | P0 | SVG illustration (+ optional GSAP/Motion orbit) | constellation/journey/portal components |
| RTL/LTR parity | P1 | CSS logical properties audit | all PF CSS |
| Capture bugs — publications/CV black void | P0 | layout/CSS bugfix | `CollectionIndexTemplate`, `AboutContactUtilityTemplate`, `about.css` |

---

## 3. Per-pair gap analysis (39 ready + PF-02 note + home)

Severity: **P0** = blocks owner acceptance · **P1** = major fidelity · **P2** = polish  
Complexity: **S** ≤1 day · **M** 1–3 days · **L** >3 days

### PF-01 Creative (pairs 1–4) — `creative-index-light.png`

**Implementation state @ `dd515a0`:** `CreativePageContent` + `PageFamilyIndexHero`, featured shell, masonry grid placeholder, pagination, theme-explore.

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Layout | Masonry density/spans vs concept; hero media proportion (42% column still boxed) | P1 | CSS | `page-families.css`, `PageFamilyMediaGridPlaceholder.astro` | M |
| Typography | Eyebrow letter-spacing; featured title serif scale | P1 | CSS | `page-families.css`, `SectionLead` | S |
| Imagery | Rail preview asset in rounded box vs concept integrated gallery lead | P1 | CSS + asset crop | `PageFamilyIndexHero.astro`, `page-family-empty-chrome.ts` | M |
| Components | Theme-explore band present but low contrast; pagination styling | P2 | CSS | `PageFamilyThemeExploreShell.astro`, `PageFamilyPaginationShell.astro` | S |
| Footer/header | Shared gaps (§2) | P0–P1 | CSS | `Footer.astro`, `Header.astro` | M |
| RTL | FA mirror of filter row + grid | P1 | CSS logical | `page-families.css` | S |

### PF-03 Writing (pairs 5–8) — `writing-index-light.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Layout | Editorial list row density; featured coral card proportions | P1 | CSS | `page-families.css`, `EditorialIndexTemplate` | M |
| Color | Coral accent hierarchy vs concept (AA fix @ `a6dbca1` may still be muted) | P1 | CSS tokens | `global.css`, writing featured modifiers | S |
| Components | Theme-explore + pagination shells need concept spacing | P2 | CSS | theme-explore, pagination shells | S |
| Typography | Section lead vs concept editorial serif | P1 | CSS | `SectionLead`, `page-families.css` | S |

### PF-04 Projects (pairs 9–12) — `projects-index-dark.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Layout | Featured case study — tags, dual-column copy, metadata row | P0 | CSS + shell markup | `PageFamilyFeaturedShell.astro`, `ProjectsPageContent.astro` | M |
| Components | Sort dropdown shell (`PageFamilySortShell`) — visual only, disabled | P1 | Astro + CSS | sort shell, `page-families.css` | S |
| Components | Numbered project rows with status chips | P1 | CSS | `PageFamilyContentRowPlaceholder.astro` | M |
| Surface | Dark atlas background gradient + card glow | P0 | CSS | `page-families.css`, `global.css` | M |
| Typography | Uppercase featured label, monospace index numbers | P2 | CSS | project featured modifiers | S |

### PF-05 Research (pairs 13–16) — upper band of `research-publications-index-light.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Hero | Uses generic index hero not profile-style copy block + arch media integration | P0 | Use `PageFamilyProfileHeroShell` pattern or extend index hero | `ResearchPageContent.astro`, `PageFamilyIndexHero.astro` | M |
| Layout | Sub-nav tabs styled as disabled chips not tab bar | P1 | CSS tab shell | `research-page__tabs`, `page-families.css` | S |
| Imagery | Hero media — horizontal rail vs vertical arch niche in concept | P1 | asset swap + CSS | `page-family-empty-chrome.ts` | M |
| Components | **Research constellation** — vector nodes vs watercolor orbital concept | P0 | **SVG illustration** (+ optional GSAP slow orbit) | `PageFamilyConstellationShell.astro`, new `research-constellation.svg` or React island | L |
| Components | Research-fit 3-column (questions/methods/impact) — shell exists, low fidelity | P0 | CSS + icons | `PageFamilyResearchFitShell.astro` | M |
| Components | Direction rows — thumbnail + metadata | P1 | CSS | `PageFamilyContentRowPlaceholder.astro` | S |
| Interaction | Constellation legend + node labels | P1 | SVG text + CSS | constellation shell | M |

### PF-05 Publications (pairs 17–20) — lower band of same concept PNG

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| **Rendering** | Capture shows **black void** — main layout not visible | **P0** | Debug template slots / min-height / overflow / theme background | `CollectionIndexTemplate.astro`, `publications-page` CSS, `template-base.css` | M |
| Hero | Title “Research Outputs” / bibliography vs concept “Selected Publications” band | P1 | Copy labels only (route titles, not CMS) | `publications-content.ts`, hero eyebrow | S |
| Layout | Sidebar interests + main list 2-column | P0 | CSS grid | `PublicationsPageContent.astro`, `page-families.css` | M |
| Components | Selected publications cards — file icon, status badges, dual buttons | P0 | CSS + shell markup | `PageFamilySelectedPublicationsShell.astro`, `PageFamilyBibliographyRowPlaceholder.astro` | M |
| Components | Collaborate band + info banner | P1 | CSS | `PageFamilyCollaborateBandShell.astro` | S |
| Footer | Shared 4-col fidelity | P0 | CSS | `Footer.astro`, `shell.css` | M |

### PF-06 Teaching (pairs 21–24) — `teaching-index-dark.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Hero | Missing hero summary paragraph + “Browse paths →” CTA; eyebrow “LEARNING LIBRARY” vs “Courses & talks” | P0 | structural copy labels + CSS | `TeachingPageContent.astro`, `PageFamilyIndexHero.astro`, `page-family-empty-chrome.ts` | M |
| Imagery | Hero media boxed vs glow-integrated 3D scene | P1 | CSS blend modes | `page-families.css` | M |
| Components | Featured path — **01–04 step timeline** with dotted connector | P0 | CSS + markup | `PageFamilyFeaturedPathShell.astro` | M |
| Components | Filter bar — Level/Topic/Sort dropdowns | P1 | new filter bar shell | new shell + `TeachingPageContent.astro` | M |
| Components | List cards — level, duration, tags, arrow | P0 | CSS | `PageFamilyListCardShell.astro` | M |
| Components | “How a path works” 4-icon process row | P0 | CSS + SVG icons | `PageFamilyPathProcessShell.astro` | M |
| Components | Dual CTA cards (updates + collaborate) vs single ContactCTA | P1 | CSS | `PageFamilyCollaborateBandShell.astro`, `ContactCTA.astro` | M |
| Components | Empty filter state card + reset | P2 | Astro | teaching empty state | S |
| RTL | FA teaching — mirror featured + filters | P1 | CSS logical | `page-families.css` | S |

### PF-07 About (pairs 25–28) — upper/mid `about-cv-light.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Hero | Capture uses `PageFamilyIndexHero` title “About” in some builds; empty state uses `PageFamilyProfileHeroShell` — verify capture age. Need **name + role line + 3 CTAs + portrait placeholder** | P0 | Ensure profile hero on empty; CSS | `AboutPageContent.astro`, `PageFamilyProfileHeroShell.astro`, `about.css` | M |
| Imagery | Full-bleed photo vs light arch illustration + portrait dashed frame | P0 | asset + layout | profile hero shell, `about.css` | L |
| Components | Sub-nav tabs (7 items) — present, need underline active state | P1 | CSS | `PageFamilySubNavShell.astro` | S |
| Components | How I Work 4-pillar grid with icons | P0 | CSS + SVG icon set | `PageFamilyHowIWorkShell.astro` | M |
| Components | Interdisciplinary journey horizontal flow | P0 | **SVG** connector system | `PageFamilyJourneyFlowShell.astro` | L |
| Components | Experience/education split timeline | P0 | CSS + node styling | `PageFamilySplitTimelineShell.astro` | M |
| Components | Skills 2×2 + selected outputs 4-col | P0 | CSS | skills/outputs shells | M |
| Components | CV download + collaborate bands | P1 | CSS | download/collaborate shells | S |
| Empty-state | Single ContentState card should not dominate when shells present | P1 | reorder/hide redundant empty | `AboutPageContent.astro` | S |

### PF-07 CV (pairs 29–32) — lower `about-cv-light.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| **Rendering** | Capture mostly black — shells wired in `CvPageContent` @ `dd515a0` | **P0** | Template/CSS bug same as publications | `AboutContactUtilityTemplate.astro`, `about.css`, `cv-page` | M |
| Hero | “CV” vs documents band + download hero | P1 | profile/documents hero variant | `CvPageContent.astro` | S |
| Components | Skills, outputs, download list — present, need concept styling | P0 | CSS | shells + `about.css` | M |
| Footer | Full stack visible in concept | P0 | scroll/capture + footer CSS | shared footer | M |

### PF-08 Contact (pairs 33–36) — `contact-dark.png`

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Hero | “Contact” vs **“Let’s talk”** gold serif; missing availability line | P0 | route title + CSS typography | `ContactPageContent.astro`, `page-families.css` | M |
| Imagery | Portal atmosphere low glow vs concept | P0 | CSS filters + optional **SVG overlay** / GSAP pulse | `PageFamilyIndexHero` portal mode, `gateway.atmosphere` assets | L |
| Layout | 2-column methods + form vs stacked | P0 | CSS grid | `contact-page__layout`, `page-families.css` | M |
| Components | Topic **cards** with icons/glow borders vs flat pills | P0 | CSS + SVG | `PageFamilyTopicCardsShell.astro` | M |
| Components | Contact method cards (email, LinkedIn) | P0 | CSS | `PageFamilyContactSidebarShell.astro` | M |
| Components | Form fields — topic dropdown, subject, anti-spam, send states | P0 | Astro form markup (disabled/honest) | `ContactPageContent.astro` | M |
| Components | FAQ accordion | P1 | Astro + minimal JS or `<details>` | `PageFamilyFaqShell.astro` | M |
| Components | Send workflow 4-state strip | P1 | CSS | `PageFamilySendWorkflowShell.astro` | S |
| Interaction | Card hover glow | P2 | CSS / Motion | topic cards | S |

### Home FA (pairs 37–38)

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Layout | Overlay card hero vs **split column** (arch left, copy+CTAs right) | P0 | restructure `HomeHero.astro` + `home.css` | `HomeHero.astro`, `home.css` | L |
| Typography | Teal headline line, larger name, chip→CTA swap | P0 | CSS + markup | `home.css`, `HomeHero.astro` | M |
| Components | Research constellation / graph — simplified vs watercolor | P0 | **SVG/Canvas** illustration | `HomeResearchGraph.astro`, `global.css` | L |
| Header | Busy header vs icon-only mobile | P1 | CSS responsive | `Header.astro`, `shell.css` | M |
| RTL | FA mirror split layout | P0 | CSS logical | `home.css` | M |

### Gateway (pair 39)

| Category | Gap | Sev | Fix | Files | Cx |
|----------|-----|-----|-----|-------|-----|
| Layout | Logo **above** portal vs below in capture | P0 | CSS flex order | `gateway.css`, gateway page | S |
| Imagery | Missing golden nodes on orbital paths | P1 | SVG overlay | gateway atmosphere component | M |
| Typography | Language button serif + padding | P1 | CSS | `gateway.css` | S |
| Note | Theme intentionally differs (light capture vs dark concept) — compare affordance only | — | — | — | — |

### PF-02 Creative detail (non-ready N1–N4) — skip until route exists

When published detail route lands: wire `EvidenceVisualDetailTemplate`, pair against `creative-detail-dark.png`. No work in this remediation pass.

---

## 4. Gap item register (actionable)

| ID | Item | Pairs | Sev | Fix type | Files (primary) | Cx |
|----|------|-------|-----|----------|-----------------|-----|
| G-001 | Fix publications/CV template render void | PF-05P, PF-07C | P0 | CSS/layout bug | `CollectionIndexTemplate.astro`, `AboutContactUtilityTemplate.astro`, `template-base.css` | M |
| G-002 | Footer visual fidelity (4-col, social, contact details) | All | P0 | CSS + SVG icons | `Footer.astro`, `shell.css` | M |
| G-003 | Header brand lockup + theme toggle iconography | All | P1 | CSS | `Header.astro`, `shell.css` | M |
| G-004 | Design tokens — gold accent, glow shadows, warm light canvas | All | P0 | CSS tokens | `global.css`, design tokens | M |
| G-005 | Profile hero pattern for About + Research | PF-07A, PF-05R | P0 | Astro + CSS | profile/index hero shells | M |
| G-006 | Research constellation SVG (+ optional GSAP orbit) | PF-05R, HOME-FA | P0 | SVG + React island | `PageFamilyConstellationShell`, `HomeResearchGraph` | L |
| G-007 | Interdisciplinary journey SVG flow | PF-07A | P0 | SVG | `PageFamilyJourneyFlowShell` | L |
| G-008 | Contact portal glow + topic cards | PF-08 | P0 | CSS + SVG (+ GSAP optional) | contact shells, `page-families.css` | L |
| G-009 | Teaching featured path timeline + filter dropdowns | PF-06 | P0 | Astro + CSS | featured path, new filter bar | M |
| G-010 | Home FA split hero restructure | HOME-FA | P0 | Astro + CSS | `HomeHero.astro`, `home.css` | L |
| G-011 | Publications selected rows + sidebar styling | PF-05P | P0 | CSS | publications shells | M |
| G-012 | Projects featured + numbered rows | PF-04 | P0 | CSS | project shells | M |
| G-013 | Sub-nav tab underline system | PF-07, PF-05R | P1 | CSS | `PageFamilySubNavShell` | S |
| G-014 | Empty-state de-emphasis (shells visible without duplicate card) | PF-07, all | P1 | Astro | `*PageContent.astro` | S |
| G-015 | Gateway logo stack order + portal nodes | GATE-200 | P1 | CSS + SVG | `gateway.css` | S |

---

## 5. Phased implementation plan

### Phase 0 — Shared foundations (blocker for all PFs)

**Goal:** Tokens, footer/header, hero primitives, tab shell, illustration utilities.

| Task | Depends | Libs | Files | Re-verify captures |
|------|---------|------|-------|-------------------|
| P0.1 Design token pass (gold, glow, warm light surfaces) | — | — | `global.css`, token source | All 39 |
| P0.2 Footer fidelity + icon SVG set | P0.1 | — | `Footer.astro`, `shell.css` | PF-05P, PF-06, PF-07, PF-08 lower scroll |
| P0.3 Header brand + utilities | P0.1 | — | `Header.astro`, `shell.css` | All |
| P0.4 Tab/sub-nav + filter chip system | P0.1 | — | `PageFamilySubNavShell`, `page-families.css` | PF-05R, PF-07 |
| P0.5 Template render bugfix (publications/CV void) | — | — | templates + `about.css` | PF-05P-*, PF-07C-* |
| P0.6 Shared SVG icon pack (discipline, contact, teaching) | — | inline SVG | `src/components/icons/` | PF-07, PF-08, PF-06 |

**Test gates:** `npm test`, `npm run lint`, `npm run build`, `npm run test:a11y`, `npm run test:visual -- --grep PUBLIC-280` (320 overflow)

### Phase 1 — PF-07 About/CV (owner pain #1)

| Task | Depends | Libs | Re-verify |
|------|---------|------|-----------|
| P1.1 Profile hero + portrait placeholder + arch media | Phase 0 | — | PF-07A-EN-1440-L, PF-07A-FA-* |
| P1.2 How I Work + journey SVG + split timeline styling | P0.6 | SVG | PF-07A mid scroll |
| P1.3 Skills + outputs + download/collaborate bands | Phase 0 | — | PF-07A lower, PF-07C-* |
| P1.4 CV page render + documents hero | P0.5 | — | PF-07C-* |

**Test gates:** `public-200.behavior.test.ts`, PUBLIC-270 PF-07 captures, compare-report pairs 25–32

### Phase 2 — PF-08 Contact (owner pain #2)

| Task | Depends | Libs | Re-verify |
|------|---------|------|-----------|
| P2.1 Portal hero glow (CSS + optional GSAP/Motion pulse) | Phase 0 | GSAP or Motion (optional) | PF-08-EN-1440-D |
| P2.2 Topic cards + 2-col layout + method cards | Phase 0 | SVG | PF-08-* |
| P2.3 Form field structure + FAQ + send workflow | Phase 0 | `<details>` or small React island | PF-08 lower scroll |

**Test gates:** `public-230.behavior.test.ts`, PF-08 captures, no-JS contact form readable

### Phase 3 — PF-05 Research + Publications (owner pain #3)

| Task | Depends | Libs | Re-verify |
|------|---------|------|-----------|
| P3.1 Research profile hero + tab bar | Phase 0 | — | PF-05R-* |
| P3.2 Constellation SVG (+ optional GSAP orbit) | P0.6 | SVG + GSAP optional | PF-05R-*, HOME-FA |
| P3.3 Research-fit 3-col + direction rows | Phase 0 | — | PF-05R-* |
| P3.4 Publications layout + selected pubs + sidebar | P0.5 | — | PF-05P-* |

**Test gates:** `public-201.behavior.test.ts`, PF-05 captures

### Phase 4 — PF-06 Teaching (owner pain #4)

| Task | Depends | Libs | Re-verify |
|------|---------|------|-----------|
| P4.1 Hero copy labels + browse CTA + glow media | Phase 0 | — | PF-06-* |
| P4.2 Featured path timeline 01–04 | Phase 0 | CSS | PF-06 upper |
| P4.3 Filter bar dropdowns + list cards + path process | Phase 0 | — | PF-06 mid |
| P4.4 Dual CTA band | P0.2 | — | PF-06 lower |

**Test gates:** `public-220.behavior.test.ts`, PF-06 captures

### Phase 5 — PF-04 Projects + PF-01/03 polish

| Task | Depends | Re-verify |
|------|---------|-----------|
| P5.1 Projects featured case + dark glow surfaces | Phase 0 | PF-04-* |
| P5.2 Creative masonry + writing editorial polish | Phase 0 | PF-01-*, PF-03-* |

### Phase 6 — Home FA + Gateway

| Task | Depends | Libs | Re-verify |
|------|---------|------|-----------|
| P6.1 Home split hero (mobile-first FA) | Phase 0 | — | HOME-FA-768-L, HOME-FA-200-L |
| P6.2 Home research graph illustration | P3.2 | SVG/Canvas | HOME-FA-* |
| P6.3 Gateway stack order + portal nodes | Phase 0 | SVG | GATE-200-L |

**Final gate:** `npm run review:visual` → regenerate compare-report → owner manual compare → `npm run report:signoff-hashes -- --ready-only`

---

## 6. Libraries (allowed — use where CSS/SVG insufficient)

| Library | Use case | Phase |
|---------|----------|-------|
| Inline SVG | Icons, journey flow, constellation static art | 0–3 |
| GSAP + ScrollTrigger (optional) | Slow constellation orbit, portal pulse | 3, 2, 6 |
| Motion (`motion`) | Reduced-motion-safe micro-interactions on cards | 2, 4 |
| Canvas / Three.js | Only if SVG cannot match watercolor orbit (home FA) — prefer exported authority raster first | 6 |

Prefer **CSS + SVG first** per ADR-ANIMATION; add GSAP/Motion only for motion explicitly shown in concepts.

---

## 7. What cannot match without CMS / owner content

| Element | Blocker |
|---------|---------|
| Real publication titles, authors, venues, dates | API/CMS |
| Real course/path titles, duration, level | API/CMS |
| Real about bio paragraphs, experience cards | API/CMS |
| Live contact email/LinkedIn/ORCID URLs in footer | Owner-approved contact config |
| GitHub/social URLs (currently placeholder spans) | Owner links |
| PF-02 creative detail page | Published slug in static build |
| Nav label rename to Gallery/Blog/Learning | Product/IA decision (category D in deviation log) |

---

## 8. Subagent overlap note

| Agent | ID | Status @ plan time | Overlap |
|-------|-----|-------------------|---------|
| Close concept-implementation visual gap | `9c29878c-5ea8-443f-af26-32595df5446e` | **No commits** — started doc read | Intended same shell work already landed `60845bd`–`dd515a0`. **Next agent should execute Phase 0–2 CSS/SVG fidelity**, not re-scaffold shells. |
| Assess PUBLIC-* remaining work | `5d1abeff` | Landed `dd515a0` (PF-01/03/04 pagination/theme-explore) | Partial; do not redo. |

---

## 9. Success criteria (still not PASS)

- [ ] All **39** ready pairs show structural + visual alignment at capture viewport (owner judgment)
- [ ] No invented CMS records in captures
- [ ] Publications + CV captures show full page stack (no void)
- [ ] `npm run review:visual` green; compare-report regenerated
- [ ] Owner §4 SHA-256 sign-off table filled
- [ ] Manual a11y checklist complete
- [ ] Explicit owner approval to change `PUBLIC-190` to `PASS`

---

*Generated 2026-09-02 — coordination repo analysis pass. Public-site implementation commits remain on `Front-End/public-site` repository.*
