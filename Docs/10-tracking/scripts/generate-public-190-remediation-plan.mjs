#!/usr/bin/env node
/**
 * Generates PUBLIC-190-VISUAL-REMEDIATION-PLAN.md with exhaustive 48-pair gap analysis.
 * Source of truth for pair list: Front-End/public-site/scripts/page-family-visual-compare.mjs
 */
import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const scriptDir = path.dirname(fileURLToPath(import.meta.url))
const coordinationRoot = path.resolve(scriptDir, '../..')
const publicSiteRoot = path.resolve(coordinationRoot, '../Front-End/public-site')

function toFileUrl(p) {
  return `file:///${p.replace(/\\/g, '/')}`
}

const compareModule = await import(
  toFileUrl(path.join(publicSiteRoot, 'scripts/page-family-visual-compare.mjs')),
)

const {
  buildPublic270CompareRows,
  buildHomeCompareRows,
  defaultDesignAuthorityRoot,
  HOME_VISUAL_ENTRIES,
} = compareModule

const pfRows = buildPublic270CompareRows(defaultDesignAuthorityRoot)
const homeRows = buildHomeCompareRows(defaultDesignAuthorityRoot)

/** @typedef {'ready' | 'capture-only' | 'blocked-route'} PairStatus */

/**
 * @param {typeof pfRows[0] | typeof homeRows[0]} row
 * @returns {{ pairId: string, pf: string, locale: string, viewport: number, theme: string, status: PairStatus, capture: string, concept: string | null }}
 */
function metaFromRow(row) {
  if ('pf' in row && row.pf) {
    const m = row.captureFile.match(
      /public-270-(.+?)-(en|fa)-(\d+)-(light|dark)\.png$/,
    )
    const captureSlug = m?.[1] ?? 'unknown'
    const locale = (m?.[2] ?? '?').toUpperCase()
    const viewport = m?.[3] ?? '?'
    const theme = (m?.[4] ?? '?').toUpperCase()
    const optional = row.optional
    return {
      pairId: `${row.pf}-${captureSlug}-${locale}-${viewport}-${theme}`,
      pf: row.pf,
      locale: m?.[2] ?? '?',
      viewport: Number(m?.[3] ?? 0),
      theme: m?.[4] ?? '?',
      status: optional ? 'blocked-route' : 'ready',
      capture: row.captureFile,
      concept: row.conceptRelative,
    }
  }

  const entry = HOME_VISUAL_ENTRIES.find((e) => e.captureFile === row.captureFile)
  const status = row.conceptRelative ? 'ready' : 'capture-only'
  const locale = entry?.locale ?? '?'
  const theme = entry?.theme ?? '?'
  const viewport = entry?.captureViewport ?? 0
  const slug = row.captureFile.replace('wp40-', '').replace('.png', '')
  return {
    pairId: `HOME-${slug.toUpperCase()}`,
    pf: row.captureFile.includes('gateway') ? 'Gateway' : 'Home',
    locale,
    viewport,
    theme,
    status,
    capture: row.captureFile,
    concept: row.conceptRelative,
  }
}

const allPairs = [...pfRows.map(metaFromRow), ...homeRows.map(metaFromRow)]

/** Family-level gap templates — applied per pair with locale/viewport deltas. */
const FAMILY_GAPS = {
  'PF-01': {
    impl: '`CreativePageContent.astro`, `PageFamilyIndexHero`, `PageFamilyFeaturedShell`, `PageFamilyMediaGridPlaceholder`, `PageFamilyPaginationShell`, `CollectionIndexTemplate`, `creative-page` CSS',
    header:
      'Nav label reads **Creative** / **آثار خلاقه** vs concept **Gallery** / **Blog** adjacent — Category D (route registry). Header chrome otherwise aligned: brand mark, role line, theme toggle, EN/FA switch present.',
    hero:
      'Concept: two-column hero — serif **Gallery** title, descriptive paragraph, tall side media with arch/stair motif + geometric overlay. Implementation: `PageFamilyIndexHero` single-column on mobile; side media uses recycled `home.rail.preview` asset (`gallery-ivory-forms`) not concept-specific crop; hero media column ~42% @1440 but lacks concept depth/glow frame.',
    nav:
      'Concept filter bar: **All work** + Medium/Year/Role dropdown chips + Contact CTA on same row. Implementation: disabled filter shell with chip placeholders — correct empty-state honesty but missing dropdown chevrons, chip spacing rhythm, and right-aligned Contact link styling.',
    main:
      '**Featured work:** Concept large landscape featured card with teal label, CMS placeholder title, **View work** CTA, distinct wide render. Implementation: `PageFamilyFeaturedShell` — structural shell only; card proportions and inner media aspect differ; per-family styling @ `dd515a0` partial.\n- **Masonry grid:** Concept 9+ varied aspect tiles (dense masonry, mixed portrait/landscape). Implementation: `PageFamilyMediaGridPlaceholder` uses uniform placeholders + `grid-auto-flow: dense` — lacks thumbnail diversity, hover states, and per-tile metadata.\n- **Pagination:** Concept numbered 1–4 with chevrons. Implementation: `PageFamilyPaginationShell` present — verify active state teal square matches concept.\n- **Collaborate band:** Concept full-width CTA before footer. Implementation: via `ContactCTA` in `Footer.astro` — similar copy but band surface/glow differs.',
    footer:
      'Concept 4-column footer: EXPLORE, RESOURCES, CONNECT with CMS placeholders for email/location. Implementation: 3-column grid; GitHub/LinkedIn are non-link placeholders; CONNECT email works via contact route but lacks location line and concept column headers styling.',
    typo:
      'Concept uses display serif for **Gallery** and teal eyebrow **Selected visual work**. Implementation: tokenized but eyebrow copy differs; FA locale needs verified display/body font pairing @390.',
    imagery:
      'Concept requires unique gallery hero side media, featured landscape, and 9+ distinct masonry thumbnails. Implementation reuses promoted rail/project assets — visual monotony vs concept.',
    motion:
      'Concept implies subtle tile hover lift and filter affordance. Implementation: CSS-only per ADR-ANIMATION; no grid hover choreography.',
    cms:
      'Featured title/body, grid records, footer CONNECT copy — **Category A** (blocked). Filter labels and empty-state chrome — **Category B/C** fixable.',
    assets: [
      '[gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md)',
      '[pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md)',
      '[gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (grid thumbs)',
    ],
    p0: [
      'P0: Replace hero side media with PF-01-specific promoted asset — `page-family-empty-chrome.ts`, `PageFamilyIndexHero.astro`, new asset prompt ASSET-PF01-HERO-SIDE-ARCH',
      'P0: Masonry placeholder diversity (mixed aspects) — `PageFamilyMediaGridPlaceholder.astro` + CSS grid template areas',
      'P1: Featured card aspect ratio + inner media frame — `PageFamilyFeaturedShell.astro`, family CSS',
    ],
    phase: 6,
    severity: 'High',
  },
  'PF-03': {
    impl: '`WritingPageContent.astro`, `EditorialIndexTemplate`, `PageFamilyFeaturedShell`, `PageFamilyThemeExploreShell`, row placeholders, `PageFamilyPaginationShell`',
    header: 'Nav **Writing** vs concept **Blog** — Category D. Active state concept uses coral/orange underline; implementation uses brand teal/coral mix via `eyebrowTone="coral"`.',
    hero: 'Concept: **INDEPENDENT WRITING** eyebrow, serif **Blog**, paragraph, gold diamond ornament, large coral architectural hero image right. Implementation: hero copy localized; side media recycles writing rail asset; missing diamond ornament and coral-forward hero framing.',
    nav: 'Concept tab row: All (red outline active), Essays, Notes, Memories, Society, Archive + search **Search writing…**. Implementation: disabled tabs + search shell — tab active styling differs (outline vs filled); `PageFamilyThemeExploreShell` added @ dd515a0 but icon cards not matching concept 5-up explore row.',
    main:
      '**Featured post:** Concept boxed grey featured with image right. Implementation: `PageFamilyFeaturedShell` — layout inversion on RTL FA must mirror concept.\n- **Post list:** Concept 6 rows with thumbnail, category label (ESSAY/NOTE), title placeholder, excerpt, teal arrow. Implementation: row placeholders — missing category chroma, arrow affordance density.\n- **Explore by theme:** Concept 5 icon cards with red borders. Implementation: `PageFamilyThemeExploreShell` partial.\n- **Newsletter band:** Concept optional updates + Follow updates. Implementation: absent on writing index empty state.\n- **Collaboration + pagination:** Present in concept; pagination shell exists; collaborate via footer promo.',
    footer: 'Same shared footer gaps as PF-01.',
    typo: 'Coral accent for writing family — verify WCAG AA on empty shells (@ dd515a0 fix noted in QA). FA @390: line-length and RTL tab overflow.',
    imagery: 'Concept coral architectural renders distinct from creative teal. Implementation reuses shared rail assets.',
    motion: 'Row hover slide optional; list is static.',
    cms: 'All post titles/excerpts — Category A. Tab labels structural — B.',
    assets: [
      '[blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md)',
      '[blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (featured)',
      '[blog-coral-stairs.md](../PUBLIC-190-asset-prompts/blog-coral-stairs.md) (list thumbs)',
    ],
    p0: [
      'P0: Writing-specific hero + featured assets — asset prompts + `getPageFamilyHeroMedia(writing)`',
      'P1: Theme explore 5-card row fidelity — `PageFamilyThemeExploreShell.astro`',
      'P1: Newsletter/updates band shell — new `PageFamilyOptionalUpdatesShell.astro`',
    ],
    phase: 6,
    severity: 'High',
  },
  'PF-04': {
    impl: '`ProjectsPageContent.astro`, `PageFamilyFeaturedShell`, `PageFamilyContentRowPlaceholder`, `PageFamilySortShell`, `PageFamilyPaginationShell`, `projects-page` CSS',
    header: 'Nav **Projects** active — aligned. Owner screenshot @061513 shows FA RTL header order correct but lacks concept full brand subtitle prominence.',
    hero: 'Concept: **SELECTED EVIDENCE** gold eyebrow, serif **Projects**, multi-line description, shield badge **No sensitive or real operational data**, large isometric server cluster hero right. Implementation: eyebrow localized; missing shield/status badge; hero media reuses PARS-SQL project preview — wrong motif vs concept server cluster.',
    nav: 'Concept pills: All, Research, AI, Data systems, Software, Design + search + **Sort: Latest**. Implementation: disabled chips + `PageFamilySortShell` — sort dropdown styling incomplete vs concept.',
    main:
      '**Featured project:** Concept PARS-SQL card with tags, carousel dots, schematic cube render. Implementation: `PageFamilyFeaturedShell` generic — missing tag pills, carousel dots, project-specific inner layout.\n- **Numbered rows 01–06:** Concept large index number, thumbnail, title placeholder, category badge + **Sanitized** shield, description, right tag stack + arrow. Implementation: `PageFamilyContentRowPlaceholder` — missing row numbers, sanitized badge, right tag column.\n- **Evidence Available:** Concept 4-card Methods/Artifacts/Code/Demo/Documentation grid — **MISSING entirely** in implementation.\n- **Pagination:** Shell present; styling gap vs teal active square.',
    footer: 'Concept footer richer; implementation footer promo band simplified (owner screenshot @061523).',
    typo: 'Dark theme gold serif headings vs implementation flatter sans — projects-page dark tokens need display serif on h1.',
    imagery: 'Concept needs unique hero cluster, featured schematic, 6 row thumbnails, evidence icons — implementation repeats single project asset.',
    motion: 'Featured carousel implied — not implemented.',
    cms: 'Row titles, tags, evidence links — Category A. Evidence section structure — B (shell without CMS).',
    assets: [
      '[project-dashboard-systems.md](../PUBLIC-190-asset-prompts/project-dashboard-systems.md)',
      '[project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md)',
      '[project-data-architecture.md](../PUBLIC-190-asset-prompts/project-data-architecture.md) (row set)',
      'ASSET-PF04-EVIDENCE-ICONS (stub — SVG inline preferred)',
    ],
    p0: [
      'P0: Add `PageFamilyEvidenceGridShell.astro` — Methods/Artifacts/Code/Documentation cards',
      'P0: Project row chrome — index numbers, sanitized badge, tag stack — `PageFamilyContentRowPlaceholder.astro`',
      'P0: Hero + featured asset swap — asset prompts ASSET-PF04-*',
    ],
    phase: 5,
    severity: 'Critical',
  },
  'PF-05-research': {
    impl: '`ResearchPageContent.astro`, `PageFamilyConstellationShell`, `PageFamilyResearchFitShell`, tabs, row placeholders',
    header: 'Shared header; research nav active on research route.',
    hero: 'Concept: **RESEARCH PROFILE**, serif **Research**, description, side arch media, sub-nav tabs (Overview, Research directions, Publications, Statement, Collaborators). Implementation: hero + disabled tablist — tabs lack concept underline active styling and horizontal scroll @390.',
    nav: 'Sub-nav tabs — see hero. Publications route shares concept PNG but different main sections.',
    main:
      '**Research Constellation:** Concept interactive node diagram with legend (AI, Data, Health, Language, Design colors) and center Human-Centered AI. Implementation: `PageFamilyConstellationShell` — static placeholder, no legend, no node graph fidelity.\n- **Research Fit:** Concept 3 cards (Research questions, Methods, Impact) with icons. Implementation: `PageFamilyResearchFitShell` — structural only.\n- **Research Directions:** Concept 5 rows with icons, status badges, related records links. Implementation: row placeholders — missing status badges.\n- **Selected Publications:** Concept 4 publication rows with type tags, Details/Available files buttons. Implementation: absent on research index (publications on separate route).',
    footer: 'Shared footer gaps.',
    typo: 'Light theme teal accents — aligned directionally; constellation labels need smaller caps tracking.',
    imagery: 'Constellation diagram is major visual — needs SVG/React island or Canvas; hero arch recycles teaching rail asset.',
    motion: 'Constellation may need subtle node pulse — GSAP/SVG acceptable per user mandate.',
    cms: 'All research directions, publication rows — Category A. Constellation structure — B with static nodes.',
    assets: [
      '[home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)',
      '[home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md) (constellation)',
      'ASSET-PF05-FIT-ICONS (stub — SVG inline preferred)',
    ],
    p0: [
      'P0: Constellation visual — SVG island or static SVG asset ASSET-PF05-CONSTELLATION-SVG',
      'P1: Research directions row badges — row placeholder component',
      'P2: Selected publications preview block on research index when CMS empty — shell only',
    ],
    phase: 4,
    severity: 'Critical',
  },
  'PF-05-publications': {
    impl: '`PublicationsPageContent.astro`, shared PF-05 hero/tabs, bibliography row placeholders',
    header: 'Same as research pair; publications nav context.',
    hero: 'Same research-publications concept hero — implementation uses publications-specific title but same hero media reuse issue.',
    nav: 'Concept tabs with Publications tab active — implementation disabled tablist does not show active Publications state distinctly.',
    main:
      '**Bibliography list:** Concept publication rows with document icon, type chip, metadata lines, action buttons. Implementation: `PageFamilyBibliographyRowPlaceholder` — missing type chips and dual action buttons.\n- **Filter chips + search:** Concept top filters — implementation filter shell disabled.\n- **Constellation/Fit:** Not shown on publications tab in concept — correct to omit on publications route.',
    footer: 'Shared footer gaps.',
    typo: 'Publication type chips (Journal Article, etc.) — missing.',
    imagery: 'Row icons — inline SVG needed.',
    motion: 'Static.',
    cms: 'All publication metadata — Category A.',
    assets: ['ASSET-PF05-PUB-ROW-ICONS (stub — SVG inline preferred)'],
    p0: [
      'P1: Bibliography row fidelity — type chip, Details/Files buttons — `PageFamilyBibliographyRowPlaceholder.astro`',
      'P1: Publications tab active state in sub-nav',
    ],
    phase: 4,
    severity: 'High',
  },
  'PF-06': {
    impl: '`TeachingPageContent.astro`, `PageFamilyFeaturedPathShell`, `PageFamilyListCardShell`, path workflow shells',
    header: 'Nav **Teaching** vs concept **Learning** — Category D.',
    hero: 'Concept: **LEARNING LIBRARY**, serif **Learning**, description, star ornament, **Browse paths** CTA, moody architectural hero. Implementation: teaching title localized; missing Browse paths CTA and star ornament; hero uses teaching rail asset — closer but not concept crop.',
    nav: 'Concept pills: All, Guides, Tutorials, Notes, Reading paths, Resources + search + Level/Topic dropdowns + Sort. Implementation: disabled filters — missing secondary dropdown row.',
    main:
      '**Featured path:** Concept card with image, 4-step timeline (Foundations→Expand). Implementation: `PageFamilyFeaturedPathShell` — timeline steps present structurally; step connector styling gap.\n- **List rows:** Concept 6 items with GUIDE/TUTORIAL tags, level/duration columns, topic tag pills. Implementation: `PageFamilyListCardShell` — missing level/duration columns and rich tag pills.\n- **How a path works:** Concept 4-icon flow — check `PageFamilyJourneyFlowShell` reuse.\n- **Empty filter state + dual CTAs:** Concept reset card + Optional updates + Collaborate cards — partially absent.',
    footer: 'Shared footer gaps.',
    typo: 'Dark theme gold headings — teaching-page tokens.',
    imagery: 'List thumbnails need learning-specific set vs recycled assets.',
    motion: 'Path timeline could use CSS step reveal.',
    cms: 'All list titles, tags, level/duration — Category A.',
    assets: [
      '[learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md)',
      '[pf-teaching-path-ribbon-dark.md](../PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md)',
      '[learning-sage-library.md](../PUBLIC-190-asset-prompts/learning-sage-library.md) (list set)',
    ],
    p0: [
      'P0: Featured path timeline styling — `PageFamilyFeaturedPathShell.astro`',
      'P1: List row level/duration columns — `PageFamilyListCardShell.astro`',
      'P1: Secondary filter dropdown row (Level, Topic)',
    ],
    phase: 5,
    severity: 'High',
  },
  'PF-07-about': {
    impl: '`AboutPageContent.astro`, `PageFamilyProfileHeroShell`, sub-nav, HowIWork, JourneyFlow, SplitTimeline, SkillsGrid, SelectedOutputs, CollaborateBand',
    header: 'About active — aligned.',
    hero: 'Concept: **PROFILE**, name heading, role line, intro, 3 CTAs (Research profile, Academic CV, Contact), arch image + portrait placeholder box. Implementation: `PageFamilyProfileHeroShell` vs `PageFamilyIndexHero` — missing tri-CTA row and portrait placeholder frame.',
    nav: 'Concept secondary tabs: Overview, Experience, Education, Skills, Research, Publications, Certificates. Implementation: `PageFamilySubNavShell` — 7 tabs present; active underline styling gap.',
    main:
      '**How I work:** Concept 2×2 grid with colored icons. Implementation: `PageFamilyHowIWorkShell` — aligned structurally.\n- **Interdisciplinary journey:** Concept 5-node horizontal timeline. Implementation: `PageFamilyJourneyFlowShell`.\n- **Experience & Education preview:** Concept split timeline with 6 cards + view full button. Implementation: `PageFamilySplitTimelineShell`.\n- **Skills & Expertise:** Concept 4 skill columns with bullet lists. Implementation: `PageFamilySkillsGridShell`.\n- **Selected outputs:** Concept 4 output cards. Implementation: `PageFamilySelectedOutputsShell`.\n- **CV + Contact CTAs:** Concept dual large cards. Implementation: `PageFamilyCollaborateBandShell` + download shell.',
    footer: 'Shared footer gaps; concept social icons in footer brand block.',
    typo: 'Profile hero name should use display scale; FA @390 hero stack order.',
    imagery: 'Portrait placeholder box missing; hero arch recycles writing asset.',
    motion: 'Journey nodes could use scroll-triggered reveal (GSAP optional).',
    cms: 'All timeline cards, skills content — Category A. Shells — B.',
    assets: [
      '[pf-about-identity-abstract-light.md](../PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md)',
      '[gallery-ivory-forms.md](../PUBLIC-190-asset-prompts/gallery-ivory-forms.md) (hero arch)',
    ],
    p0: [
      'P0: Profile hero tri-CTA + portrait placeholder — `PageFamilyProfileHeroShell.astro`',
      'P1: Sub-nav active underline — `PageFamilySubNavShell.astro` CSS',
    ],
    phase: 2,
    severity: 'Critical',
  },
  'PF-07-cv': {
    impl: '`CvPageContent.astro`, CV hero, download list shell, timeline shells',
    header: 'CV route — not in primary nav concept but in footer RESOURCES.',
    hero: 'Concept (about-cv): CV-specific hero with download emphasis — implementation uses generic index hero.',
    nav: 'Concept shows CV/downloads context — implementation minimal.',
    main:
      '**Downloads section:** Concept download cards with file type icons. Implementation: `PageFamilyDownloadListShell`.\n- **Experience/Education:** Shared timeline shells — same gaps as about.',
    footer: 'Shared footer gaps.',
    typo: 'CV page title/display sizing.',
    imagery: 'Download card icons.',
    motion: 'Static.',
    cms: 'CV file records — Category A.',
    assets: ['ASSET-PF07-CV-DOWNLOAD-ICONS (stub — SVG inline preferred)'],
    p0: ['P1: CV-specific hero variant — `CvPageContent.astro`', 'P1: Download list card styling'],
    phase: 2,
    severity: 'High',
  },
  'PF-08': {
    impl: '`ContactPageContent.astro`, portal hero, topic cards, sidebar, FAQ, form, send workflow',
    header: 'Contact not in concept primary nav (utility route) — header otherwise aligned.',
    hero: 'Concept: **COLLABORATION**, gold serif **Let\'s talk**, description, availability CMS line, glowing arch + geometric atmosphere right. Implementation: portal `PageFamilyIndexHero` with gateway atmosphere — closer @ Path A but lacks gold heading treatment and availability badge.',
    nav: 'Topic cards row: PhD/Research, Technical, Creative, Other — `PageFamilyTopicCardsShell` present; selection state styling gap.',
    main:
      '**Contact methods:** Concept Academic email, LinkedIn, ORCID cards. Implementation: sidebar shell with placeholders.\n- **Before you write:** Concept 4-point list — check sidebar shell.\n- **Form:** Concept full form with topic dropdown, anti-spam ready, send button, privacy note. Implementation: disabled form fields in empty state — structural; needs visual parity with concept field spacing.\n- **Send workflow + FAQ:** `PageFamilySendWorkflowShell`, `PageFamilyFaqShell` — verify accordion styling.',
    footer: 'Shared footer gaps.',
    typo: 'Gold serif **Let\'s talk** on dark — contact-page heading tokens.',
    imagery: 'Portal atmosphere uses gateway assets — acceptable; concept geometric overlay denser.',
    motion: 'Form state transitions — CSS; send workflow icons.',
    cms: 'Email, LinkedIn, ORCID, availability — Category A.',
    assets: [
      '[pf-contact-atmosphere-dark.md](../PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md)',
      '[portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)',
    ],
    p0: [
      'P0: Contact hero gold serif + availability badge — `PageFamilyIndexHero` contact variant CSS',
      'P1: Topic card selected state — `PageFamilyTopicCardsShell.astro`',
      'P1: Form empty-state visual parity — `ContactPageContent.astro`',
    ],
    phase: 3,
    severity: 'Critical',
  },
  'PF-02': {
    impl: '`CreativeDetailContent.astro` — route blocked (no published detail in static build)',
    header: 'N/A — capture not generated.',
    hero: 'N/A',
    nav: 'N/A',
    main: 'Concept detail: breadcrumb, hero gallery 1/6, meta grid, thumbnail carousel, process steps, credits, related work, prev/next — all blocked until published creative detail route exists.',
    footer: 'N/A',
    typo: 'N/A',
    imagery: 'Detail hero gallery assets — ASSET-PF02-GALLERY-SET',
    motion: 'Gallery carousel — React island or CSS scroll-snap.',
    cms: 'Entire detail record — Category A + route publish.',
    assets: [
      '[pf-creative-hero-editorial-light.md](../PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) (gallery hero)',
      'ASSET-PF02-PROCESS-ICONS (stub)',
      'ASSET-PF02-RELATED-THUMBS (stub)',
    ],
    p0: ['P0: Unblock route — published creative detail slug in static build', 'P0: Implement detail template vs creative-detail-dark.png'],
    phase: 7,
    severity: 'Blocked',
  },
  Home: {
    impl: '`HomeHero.astro`, `HomeResearchGraph.astro`, section components, `wp40-home` CSS',
    header: 'Home header — aligned with site shell.',
    hero: 'Concept mobile FA: side-by-side or overlay hero with orbit portal, graph list, scrim. Implementation: WP-40 overlay direction documented — orbit hero differs from concept side-by-side (Category D/C documented).',
    nav: 'N/A on home.',
    main: 'Featured projects/publications, research graph, journey sections — seed content vs concept CMS placeholders; card link gating @ F-16 correct.',
    footer: 'Shared footer gaps.',
    typo: '200% zoom pairs — readability audit only.',
    imagery: 'Home graph backplate, portal orbit — promoted assets exist; mobile crop differs.',
    motion: 'Orbit/graph may need reduced-motion fallbacks.',
    cms: 'Featured cards — partial seed (Category A for production copy).',
    assets: [
      '[portal-orbit-light.md](../PUBLIC-190-asset-prompts/portal-orbit-light.md)',
      '[home-graph-backplate-light.md](../PUBLIC-190-asset-prompts/home-graph-backplate-light.md)',
    ],
    p0: ['P1: Mobile FA hero layout parity — `HomeHero.astro` @768', 'P2: EN tablet concepts missing from authority — capture-only review'],
    phase: 8,
    severity: 'Medium',
  },
  Gateway: {
    impl: 'Gateway page / language selection',
    header: 'N/A',
    hero: 'Concept dark gateway vs capture light @200% — theme differs by design (Category D). Compare language-choice affordance and scale only.',
    nav: 'N/A',
    main: 'Language buttons layout and typography at 200% zoom.',
    footer: 'Minimal/none on gateway.',
    typo: '200% readability — a11y not visual concept match.',
    imagery: 'Gateway atmosphere assets exist.',
    motion: 'Static.',
    cms: 'N/A',
    assets: ['[portal-centered-dark.md](../PUBLIC-190-asset-prompts/portal-centered-dark.md)'],
    p0: ['P2: Affordance parity at 200% — not theme match'],
    phase: 8,
    severity: 'Low',
  },
}

function familyKey(pair) {
  if (pair.pf === 'PF-05') {
    if (pair.capture.includes('publications')) return 'PF-05-publications'
    return 'PF-05-research'
  }
  if (pair.pf === 'PF-07') {
    if (pair.capture.includes('cv')) return 'PF-07-cv'
    return 'PF-07-about'
  }
  if (pair.pf === 'PF-02') return 'PF-02'
  if (pair.pf === 'Home') return 'Home'
  if (pair.pf === 'Gateway') return 'Gateway'
  return pair.pf
}

function localeDelta(pair, gaps) {
  const parts = []
  if (pair.locale === 'fa') {
    parts.push(
      '**RTL:** Mirror hero media/text column order; verify `dir=rtl` on filter bars, row arrows, and footer grid; FA nav labels longer — check @390 wrap/overflow (PUBLIC-280 gate).',
    )
  } else {
    parts.push('**LTR:** Concept reference is EN authority; nav labels differ (Creative/Writing/Teaching vs Gallery/Blog/Learning).')
  }
  if (pair.viewport === 390) {
    parts.push(
      '**@390 mobile:** Hero stacks single-column; filter bar may wrap to two rows; masonry/list becomes single column; sub-nav tabs horizontal scroll; reduce hero min-height and pagination touch targets.',
    )
  } else if (pair.viewport === 1440) {
    parts.push('**@1440 desktop:** Full two-column hero, multi-column grids, footer 4-column target.')
  } else if (pair.viewport === 768) {
    parts.push('**@768 tablet reflow:** No exact concept width — nearest FA mobile concept @390 used for FA light only.')
  } else if (pair.viewport === 720) {
    parts.push('**@720 (200% zoom):** Accessibility evidence — assess readability, tap targets, text spacing; not pixel-match to desktop concept.')
  }
  if (pair.theme === 'dark') {
    parts.push('**Dark theme:** Verify gold/teal contrast on `--surface-*` tokens; project/teaching/contact families.')
  }
  return parts.join('\n')
}

function pairSection(pair, gaps) {
  const statusLabel =
    pair.status === 'ready'
      ? 'ready (concept paired)'
      : pair.status === 'capture-only'
        ? 'capture-only (no concept reference)'
        : 'blocked-route (PF-02 detail — no capture)'

  const conceptLabel = pair.concept ?? '_(none — capture-only review)_'

  return `### ${pair.pairId}: ${pair.capture} ↔ ${conceptLabel.split('/').pop() ?? 'n/a'}
- **Meta:** locale=${pair.locale}, viewport=${pair.viewport}px, theme=${pair.theme}, status=${statusLabel}, PF=${pair.pf}
- **Implementation files:** ${gaps.impl}
- **Viewport/locale notes:** ${localeDelta(pair, gaps)}

- **Header:** ${gaps.header}

- **Hero:** ${gaps.hero}

- **Navigation/tabs:** ${gaps.nav}

- **Main content sections:**
${gaps.main.split('\n').map((l) => (l.startsWith('-') ? `  ${l}` : `  - ${l}`)).join('\n')}

- **Footer:** ${gaps.footer}

- **Typography/color/spacing:** ${gaps.typo}

- **Imagery/assets:** ${gaps.imagery} → Asset prompts: ${gaps.assets.join(', ')}

- **Animation/interaction:** ${gaps.motion}

- **CMS/admin dependency:** ${gaps.cms}

- **Priority fixes:**
${gaps.p0.map((p) => `  - ${p}`).join('\n')}
`
}

// Executive table rows
const tableRows = allPairs.map((pair) => {
  const key = familyKey(pair)
  const gaps = FAMILY_GAPS[key]
  return `| ${pair.pairId} | ${pair.capture} | ${pair.concept?.split('/').pop() ?? '—'} | ${pair.locale} | ${pair.viewport} | ${pair.theme} | ${pair.status === 'ready' ? 'ready' : pair.status === 'capture-only' ? 'capture-only' : 'blocked'} | ${gaps.severity} | Phase ${gaps.phase} |`
})

const readyCount = allPairs.filter((p) => p.status === 'ready').length
const captureOnlyCount = allPairs.filter((p) => p.status === 'capture-only').length
const blockedCount = allPairs.filter((p) => p.status === 'blocked-route').length

const pairSections = allPairs
  .map((pair) => pairSection(pair, FAMILY_GAPS[familyKey(pair)]))
  .join('\n')

const doc = `# PUBLIC-190 Visual Remediation Plan

**Packet:** PUBLIC-190 gap analysis (analysis + plan only — does **not** set PASS)  
**Public-site base:** \`dd515a0\` (Path A visual fidelity slice)  
**Compare pairing fix:** \`c14508a\` (\`page-family-visual-compare.mjs\` concept root)  
**Generated:** 2026-09-02  
**Pairs analyzed:** **48 / 48** (${readyCount} ready + ${captureOnlyCount} capture-only + ${blockedCount} blocked-route)  
**Asset prompts:** [\`PUBLIC-190-asset-prompts/\`](./PUBLIC-190-asset-prompts/) (sibling agent 65eccafb — stub IDs linked below; populate prompt files as delivered)  
**QA verdict:** remains \`REVISE\` — owner manual compare + sign-off still required

---

## Executive summary

Owner feedback (2026-09-02, Persian): **concepts read much weaker than implementation** in side-by-side compare — meaning promoted empty-state chrome exists but **visual density, asset diversity, section fidelity, and dark/light token application** still diverge materially from design authority. Path A @ \`dd515a0\` improved pagination/theme-explore shells and hero proportions but did not close the gap.

**Top P0 themes across families:**

1. **Missing sections** — Projects Evidence Available grid; Writing newsletter band; Research constellation graph fidelity.
2. **Asset monotony** — Hero/list thumbnails reuse \`home.rail.preview\` / single project preview across PF families.
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

**Allowed libraries (per owner mandate):** GSAP, Motion, Three.js, Canvas, SVG — prefer CSS-first per \`ADR-ANIMATION.md\`; reach for islands only when concept fidelity requires it (constellation, gallery carousel).

---

## Executive summary table (48 pairs)

| Pair ID | Capture | Concept | Locale | Viewport | Theme | Compare status | Severity | Phase |
|---------|---------|---------|--------|----------|-------|----------------|----------|-------|
${tableRows.join('\n')}

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

${pairSections}

---

## Owner/CMS-only pairs (no code-only fix)

| Pair ID | Blocker |
|---------|---------|
| PF-02-* (×4) | No published creative detail route in static build — captures skipped |
| All ready PF pairs | Category A record copy (titles, excerpts, tags, publication metadata, contact email/ORCID) |
| HOME-* (featured content) | Production CMS records for featured projects/publications beyond seed slugs |

---

## Regenerate compare evidence

\`\`\`powershell
cd Front-End/public-site
npm run review:visual
# Opens test-results/visual/compare-report.html (gitignored)
\`\`\`

---

## Related documents

- [\`PUBLIC-190-VISUAL-QA.md\`](./PUBLIC-190-VISUAL-QA.md) — verdict REVISE
- [\`PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md\`](../../Front-End/public-site/docs/quality/PUBLIC-270-PAGE-FAMILY-VISUAL-EVIDENCE.md)
- [\`page-family-visual-compare.mjs\`](../../Front-End/public-site/scripts/page-family-visual-compare.mjs) — pair source of truth
- [\`PUBLIC-190-asset-prompts/\`](./PUBLIC-190-asset-prompts/) — image generation prompts (in progress)

**Do not set PUBLIC-190 PASS until:** owner manual compare, accepted SHA-256 hashes, manual a11y, explicit sign-off.
`

const outPath = path.join(
  coordinationRoot,
  '10-tracking/PUBLIC-190-VISUAL-REMEDIATION-PLAN.md',
)
writeFileSync(outPath, doc, 'utf8')
console.log(`Wrote ${outPath} (${allPairs.length} pairs)`)
