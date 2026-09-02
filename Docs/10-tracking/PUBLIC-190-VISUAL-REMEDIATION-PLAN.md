# PUBLIC-190 — Visual remediation plan

**Status:** Analysis + phased plan @ 2026-09-02  
**Verdict:** `PUBLIC-190` stays **`REVISE`**  
**Public-site reference:** `dd515a0` (Path A shells; compare 39/48 pairs @ `c14508a`)

**Companion docs**

- [PUBLIC-190-VISUAL-QA.md](./PUBLIC-190-VISUAL-QA.md)
- [PUBLIC-190-asset-prompts/README.md](./PUBLIC-190-asset-prompts/README.md)
- [PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md](./PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md)

---

## Executive summary

Implementation delivers **structural empty chrome** (heroes, tabs, placeholders) but compare-report + owner screenshots show large gaps vs page-family concepts in **footer density, hero atmosphere, graph/constellation, featured card richness, and family-specific art**. Remediation splits into: **(A) owner asset regeneration** via prompt pack, **(B) layout/CSS/shell fidelity** per PF, **(C) CMS/API wiring** when published content exists, **(D) selective motion/graph islands**. No invented CMS copy.

---

## Compare inventory (48 rows)

### PUBLIC-270 page families (40 rows → 36 required + 4 optional PF-02)

| PF | Capture ID | Locales | Widths | Theme | Concept | Ready pairs |
|---|---|---|---|---|---|:---:|
| PF-01 | pf01 | en, fa | 1440, 390 | light | `creative-index-light.png` | 4 |
| PF-03 | pf03 | en, fa | 1440, 390 | light | `writing-index-light.png` | 4 |
| PF-04 | pf04 | en, fa | 1440, 390 | dark | `projects-index-dark.png` | 4 |
| PF-05 | pf05-research | en, fa | 1440, 390 | light | `research-publications-index-light.png` | 4 |
| PF-05 | pf05-publications | en, fa | 1440, 390 | light | same concept | 4 |
| PF-06 | pf06 | en, fa | 1440, 390 | dark | `teaching-index-dark.png` | 4 |
| PF-07 | pf07-about | en, fa | 1440, 390 | light | `about-cv-light.png` | 4 |
| PF-07 | pf07-cv | en, fa | 1440, 390 | light | same concept | 4 |
| PF-08 | pf08 | en, fa | 1440, 390 | dark | `contact-dark.png` | 4 |
| PF-02 | pf02 | en, fa | 1440, 390 | dark | `creative-detail-dark.png` | 0 (optional — no static route) |

**PUBLIC-270 ready:** 36 required (+ optional PF-02 when route exists).

### WP-40 home / gateway (8 captures)

| Capture | Viewport | Concept | Ready |
|---|---|---|:---:|
| wp40-home-en-768-light/dark | 768 | none (capture-only) | 0 |
| wp40-home-fa-768-light | 768 | `home-mobile-fa-light-concept-v1.png` | 1 |
| wp40-home-fa-768-dark | 768 | none | 0 |
| wp40-home-en/fa-200pct-light/dark | 720 | FA light → mobile concept; EN none | 1 |
| wp40-gateway-200pct-light | 720 | `language-gateway-dark-concept-v1.png` (affordance only) | 1 |

**Home ready:** 3 (+ gateway affordance)  
**Total ready:** **39 / 48** (per `c14508a` pairing rules)

---

## Cross-cutting gaps (all families)

| Gap | Severity | Fix type | Files / assets |
|---|---|---|---|
| Footer 4-column density + collaboration band | P0 | CSS + `Footer.astro` | `Footer.astro`, `shell.css` |
| Hero atmosphere scale / glow vs concept | P0 | Asset swap + CSS | [portal-orbit-*](./PUBLIC-190-asset-prompts/README.md), `home.css` |
| Featured card elevation, media frame, typography | P0 | CSS | `page-families.css`, `PageFamilyFeaturedShell.astro` |
| Wrong preview asset reuse across families | P1 | Mapping + new assets | `page-family-empty-chrome.ts`, prompt pack |
| CMS copy slots show placeholder only | P0 (content) | API wiring when published | loaders per family — **no invented text** |
| Graph/constellation flat vs concept | P0 | Asset + SVG/DOM | `home-graph-backplate-*`, `PageFamilyConstellationShell.astro` |

---

## Per-family priority (owner pain order)

### PF-07 About / CV — Phase 1

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Missing abstract identity plate | P0 | New asset + hero shell | M — [pf-about-identity-abstract-light](./PUBLIC-190-asset-prompts/pf-about-identity-abstract-light.md) |
| Sub-nav tabs present but weak visual weight | P0 | CSS tabs + `PageFamilySubNavShell` | S |
| How I work / journey / skills grid density | P0 | CSS grid | M — `page-families.css`, shells |
| Timeline education/experience preview | P1 | `PageFamilyTimelineShell` + API timeline | M |
| Selected outputs categories | P1 | Shell + API | M |

**Re-verify:** `public-270-pf07-about-*`, `public-270-pf07-cv-*`

### PF-08 Contact — Phase 2

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Atmosphere weaker than concept | P0 | Dedicated dark atmosphere asset | M — [pf-contact-atmosphere-dark](./PUBLIC-190-asset-prompts/pf-contact-atmosphere-dark.md) |
| Topic chips + sidebar density | P0 | CSS | S |
| FAQ / send workflow shells vs concept | P1 | Present — polish accordion styles | S |
| Live form + CMS email slots | P0 content | API + progressive form | L — blocked on owner site settings |

**Re-verify:** `public-270-pf08-*`

### PF-05 Research / Publications — Phase 3

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Constellation panel flat | P0 | Backplate regen + SVG edges | L — graph API + `ResearchPageContent.astro` |
| Section tabs + publications sidebar | P0 | CSS + shells | M |
| Research fit / directions blocks | P1 | API sections | M |
| Publications row citation chrome | P1 | API list + CSS | M |

**Re-verify:** `public-270-pf05-research-*`, `public-270-pf05-publications-*`

### PF-06 Teaching — Phase 4

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Featured path illustration missing | P0 | [pf-teaching-path-ribbon-dark](./PUBLIC-190-asset-prompts/pf-teaching-path-ribbon-dark.md) | M |
| Library list + path process steps | P1 | Shells exist — density CSS | S |
| Sage hero asset | P0 | [learning-sage-library](./PUBLIC-190-asset-prompts/learning-sage-library.md) | M |

**Re-verify:** `public-270-pf06-*`

### PF-04 Projects — Phase 5

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Hero + row thumbs generic | P0 | [project-data-architecture](./PUBLIC-190-asset-prompts/project-data-architecture.md), [project-dashboard-systems](./PUBLIC-190-asset-prompts/project-dashboard-systems.md) | M |
| Evidence row anatomy (methods/artifacts) | P1 | CSS + API flags | M |
| Sanitized disclosure band | P1 | Static copy from seed only | S |

**Re-verify:** `public-270-pf04-*`

### PF-01 Creative / PF-03 Writing — Phase 6

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| PF-01 hero portrait proportion | P0 | [pf-creative-hero-editorial-light](./PUBLIC-190-asset-prompts/pf-creative-hero-editorial-light.md) | M |
| Masonry grid density | P0 | CSS `grid-auto-flow: dense` tuning | S — partial @ `dd515a0` |
| PF-03 theme explore + coral accent | P0 | CSS + [blog-coral-stairs](./PUBLIC-190-asset-prompts/blog-coral-stairs.md) | M |
| Pagination shells | P1 | Done @ `dd515a0` — verify capture | S |

**Re-verify:** `public-270-pf01-*`, `public-270-pf03-*`

### Home / Gateway — Phase 7

| Gap | Sev | Fix | Complexity |
|---|---|---|---|
| Hero arch atmosphere | P0 | [portal-orbit-*](./PUBLIC-190-asset-prompts/README.md) | M |
| Graph backplate + nodes | P0 | [home-graph-backplate-*](./PUBLIC-190-asset-prompts/README.md) | M |
| FA mobile overlay hero | P2 | Documented WP-40 direction — not re-opened | — |
| Gateway centered portal | P1 | [portal-centered-*](./PUBLIC-190-asset-prompts/README.md) | M |

**Re-verify:** `wp40-home-*`, gateway 200%

---

## Phase 0 — Shared foundations (before PF phases)

1. Regenerate **P0 assets** from prompt pack; update `ASSET-PROMOTION-LEDGER.md` + SHA pins.
2. Footer 4-column + collaboration band alignment (`Footer.astro`, `shell.css`).
3. Hero pattern tokens: scrim, media column %, min-height (`page-families.css`, `home.css`).
4. Tab nav shell polish (`PageFamilySubNavShell.astro`).
5. Run `npm run review:visual` after asset drop-in.

**Gates:** Vitest promoted-media hash tests, `validate:design`, compare report refresh.

---

## Libraries (add only when phase requires)

| Phase | Library | Scope |
|---|---|---|
| 0–1 | None | CSS + assets |
| 3 | SVG + optional `d3-force` worker | Graph edges/layout |
| 6–7 | `motion` (React island) | Section reveals `client:visible` |
| 3 fallback | `@react-three/fiber` + `drei` | Only if DOM graph fails acceptance |

GSAP ScrollTrigger: defer unless pinned hero scrub required; kill/reinit if View Transitions enabled.

---

## Overlap with parallel agent work

| Agent / commit | Scope | This plan |
|---|---|---|
| `9c29878c` Close concept gap | Footer, About, Contact, Research, Teaching, Projects shells | **Overlaps Phase 1–5 CSS** — merge before duplicate shell work |
| `dd515a0` Path A | PF-01/03 pagination, featured styling, hero % | **Phase 6 partial** — verify captures, do not redo |
| Asset prompt pack (this delivery) | Owner image generation | **Phase 0** — prerequisite for atmosphere/graph gaps |

---

## Acceptance gates (unchanged)

1. Owner manual compare on refreshed `compare-report.html`
2. `npm run report:signoff-hashes -- --ready-only` — owner pastes accepted SHA rows into PUBLIC-190 §4
3. Manual a11y §3 (keyboard, 200% zoom, reduced motion)
4. Explicit owner approval to flip verdict from `REVISE` to `PASS`

**Do not close PUBLIC-190** on automated greens alone.

---

## Top 10 P0 remediation items

1. Regenerate home hero atmosphere (`portal-orbit-light/dark`)
2. Regenerate graph backplates (`home-graph-backplate-light/dark`)
3. PF-07 abstract identity plate asset + hero wiring
4. PF-08 dedicated contact atmosphere (not gateway reuse)
5. PF-05 constellation backplate + SVG edge layer
6. Footer 4-column + collaboration band vs concept
7. PF-01 portrait hero editorial panel asset
8. PF-06 teaching path ribbon + sage library regen
9. PF-04 project preview assets (data-architecture + dashboard-systems)
10. Owner-approved CMS publication for featured/row slots (content — not decorative art)

**Pairs analyzed:** 48 inventory rows (39 concept-ready + 9 capture-only / optional PF-02)
