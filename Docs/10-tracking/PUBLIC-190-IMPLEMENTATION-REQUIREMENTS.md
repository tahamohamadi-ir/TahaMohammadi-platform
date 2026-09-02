# PUBLIC-190 — Implementation requirements (visual fidelity + dynamic CMS)

**Status:** Research synthesis @ 2026-09-02  
**Verdict:** `PUBLIC-190` remains **`REVISE`** — this document records **gaps as needed**, not implemented contracts.

**Related**

- [PUBLIC-190-VISUAL-QA.md](./PUBLIC-190-VISUAL-QA.md)
- [PUBLIC-190-VISUAL-REMEDIATION-PLAN.md](./PUBLIC-190-VISUAL-REMEDIATION-PLAN.md)
- [PUBLIC-190-asset-prompts/README.md](./PUBLIC-190-asset-prompts/README.md)
- [OPENAPI-REVIEW-REPORT.md](../03-contracts/OPENAPI-REVIEW-REPORT.md)
- [ADR-0007-VISUAL-ASSETS-AND-CMS-BLOCKS.md](../09-decisions/ADR-0007-VISUAL-ASSETS-AND-CMS-BLOCKS.md)

---

## Executive summary

Concept-faithful **dynamic** public pages require three layers beyond today's static shells: (1) **approved decorative masters** promoted per ledger ([asset prompt pack](./PUBLIC-190-asset-prompts/README.md)), (2) **CMS-driven section data** from Django admin APIs already sketched in OpenAPI review, and (3) a **visual fidelity stack** (CSS + selective islands: Motion/GSAP for scroll, DOM/SVG graph for constellation, optional R3F only if DOM graph cannot meet concept). Headless CMS products (Sanity, Strapi, Payload) offer block/page-builder patterns useful as **reference architecture**; this platform's **source of truth remains Django + custom admin-panel**, not a second CMS.

---

## 1. Headless CMS + Astro patterns (reference, not adoption)

| Pattern | How it works | Relevance to this platform |
|---|---|---|
| **Sanity page builder** | `pageBuilder` array of typed blocks → Astro catch-all route maps block `_type` to components; GROQ fetch at build or SSR ([sanity-page-builder-astro-example](https://github.com/maciejtrzcinski/sanity-page-builder-astro-example)) | Mirrors our **home composition** + **content entities** — but we fetch `/api/home-composition/{locale}` and `/api/content/*` instead of GROQ |
| **Sanity + Astro static** | `@sanity/astro`, Content Layer loaders, optional Visual Editing with SSR + read token ([Sanity Astro docs](https://www.sanity.io/docs/astro/introduction)) | Visual editing analogue = **preview-share** + `/preview/` routes (backend); static rebuild on publish |
| **Strapi dynamic zones** | Collection types with block components; `strapi-community-astro-loader` + Zod schemas ([astro-strapi-example](https://github.com/PaulBratslavsky/astro-strapi-example-project)) | Same block-renderer idea as admin `/content/schema` + entity payloads |
| **Direct Django admin** | Single API origin, session/CSRF for admin, published-only public reads | **Chosen architecture** — avoids dual CMS, matches `ADR-0004` |

**Implication:** Implement a **block renderer** in public-site that maps **known backend entity kinds** to Astro shells — do not add Sanity/Strapi unless product explicitly forks authority.

---

## 2. Backend + admin: observed vs concepts

Source: `Docs/03-contracts/OPENAPI-REVIEW-REPORT.md`, `API-CONTRACT.md`, `MEDIA-CONTRACT.md`, public-site `page-family-empty-chrome.ts` (structural chrome only).

### 2.1 Public API families (candidate / recorded)

| Concept need | Observed public endpoint(s) | HAVE today (public-site) | NEED for concept fidelity |
|---|---|---|---|
| Home blocks (identity, graph, featured, rails) | `GET /api/home-composition/{locale}`, `GET /api/site` | Static `home-content.ts` seed + honest draft cards | Wire home sections to **published** composition API; rebuild on publish |
| About profile tabs, timeline, skills, outputs | `GET /api/profiles/{locale}/about` | Route + shells; empty structural chrome | CMS sections: experience, education, skills, outputs with ordering |
| Research tabs, graph, fit, directions | `GET /api/research/*` per locale | Index shells + `PageFamilyConstellationShell` (static DOM) | Published graph payload + filter model; interactive preview |
| Publications rows, citation style | `GET /api/publications/{locale}` | Row placeholders | List + metadata fields from API; sidebar filters |
| Projects evidence rows | `GET /api/projects/{locale}` | Row placeholders + 2 preview assets | Per-record media IDs, sanitized states, methods/artifacts flags |
| Writing filters, theme explore | `GET /api/articles/{locale}` | Theme explore **structural** chips | Topic/archive filters from API tags |
| Teaching path, library sequence | `GET /api/teaching/{locale}` | Path/list shells | Path entity with ordered steps + resource kinds |
| Contact form, FAQ, topics | `POST /api/contact`, `GET /api/site` | Disabled form shell + structural FAQ | CMS-bound email slots, live form, FAQ records |
| CV downloads | `GET /api/downloads/{locale}`, site | CV shell | Owner-approved file availability |
| Search | None (Pagefind) | Built | **HAVE** — no API needed |

### 2.2 Admin workflows (candidate)

| Concept UI | Observed admin group | HAVE (admin-panel board) | NEED |
|---|---|---|---|
| Content blocks / revisions | `/content/schema`, `/content/{entity}`, revisions | ADMIN-160 skeleton | Full editor per entity; block field types |
| Home module ordering | `/home-modules/{locale}` | ADMIN-190 planned | Drag-order UI + validation |
| Timeline items | `/timeline/{locale}` | ADMIN-200 planned | Reorder + link validation |
| Research graph nodes/edges | `/graph/versions`, payload, activation | ADMIN-210 planned | Graph editor matching `admin-graph-editor-dark-concept-v1.png` |
| Media upload, focal, replace | `/media/*` | ADMIN-180 planned | Focal point + theme variants in UI |
| Preview / publish | preview links, transitions | ADMIN-220–240 planned | Owner approval gate (ADMIN-280) |
| Featured / tags | `/featured`, `/tags` | ADMIN-150+ | Featured records per family |

**None of the above admin UIs are closed** on the task board — public-site empty chrome is intentional until CMS + visual remediation land.

---

## 3. Visual fidelity stack

### 3.1 Current stack (HAVE)

| Layer | Implementation | Notes |
|---|---|---|
| Layout / tokens | Tailwind 4 + `tokens.json` projection | `PUBLIC-130` complete |
| Theme pictures | `ThemePicture`, `PromotedPicture`, hash-pinned registry | 12 runtime assets; 2 deferred |
| Page-family shells | 30+ `PageFamily*Shell.astro` components | Structural empty chrome @ `dd515a0` |
| Graph | DOM nodes on `home-graph-backplate` + `PageFamilyConstellationShell` | No canvas/WebGL |
| Motion policy | `ADR-ANIMATION.md` — CSS-first, reduced-motion | GSAP/Motion not in production bundle yet |
| Compare harness | `review:visual`, 39/48 concept pairs | Owner compare blocking |

### 3.2 Options researched (NEED / selective adoption)

| Tool | Best for | Astro fit | Recommendation |
|---|---|---|---|
| **Motion** (`useScroll`, `whileInView`) | Scroll-linked parallax, reveal on view; uses `ScrollTimeline` when available ([Motion scroll docs](https://motion.dev/docs/react-scroll-animations)) | React island + `client:visible` ([Netlify guide](https://developers.netlify.com/guides/motion-animation-library-with-astro/)) | **P1** for section reveals — lighter than GSAP for simple fades |
| **GSAP ScrollTrigger** | Pinned sections, scrub timelines, complex scroll storytelling ([GSAP + Astro VT caveats](https://gsap.com/community/forums/topic/40950-compatibility-with-gsap-scrolltrigger-astro-view-transitiosn-api/)) | Vanilla `gsap.context` + kill on navigation if View Transitions enabled | **P2** only for hero scrub or path ribbon — avoid site-wide |
| **Three.js / R3F** | Large interactive 3D graphs, instanced nodes ([R3F Html overlays](https://www.intelligentgraphicandcode.com/development/threejs-interfaces/html-integration)) | Heavy island; isolate from UI state | **P2 fallback** if DOM+SVG graph cannot match PF-05 concept + admin graph editor |
| **Lottie** | Icon micro-motion, one-shot hero accents | `client:visible`, files in `public/animations/` | **P3** — optional; prefer CSS/SVG for brand calm |
| **SVG illustration pipeline** | Constellation edges, portal lines, teaching path ribbon | Inline SVG + CSS variables | **P0** alongside regenerated backplates |

### 3.3 Constellation / graph strategy

**Phase A (needed now):** Keep **semantic HTML list** + improved backplate assets + SVG edge layer driven by published graph API coordinates (2D layout from backend or CSS grid anchors).

**Phase B (if concept still fails):** Worker-based 2D force layout (e.g. d3-force) in canvas **or** lightweight R3F with `InstancedMesh` + `Html` labels ([graphier pattern](https://github.com/CocoRoF/graphier)) — admin graph payload must drive node positions/labels.

**Reduced motion:** Static graph list + 2D fallback per `tokens.json` motion.reduced.

---

## 4. Admin-managed media (focal, crops, theme variants)

| Capability | Industry pattern | Platform status |
|---|---|---|
| Focal point `fp-x`/`fp-y` or crop/hotspot | Sanity hotspot, DatoCMS auto focal ([DatoCMS images](https://www.datocms.com/docs/content-delivery-api/images-and-videos)), Strapi focal picker ([Strapi PR #25267](https://github.com/strapi/strapi/pull/25267)) | **NEEDED** — `MEDIA-CONTRACT.md` requires alt + derivatives; registry has empty `focalByLocale` until WP-40 review |
| Theme variants (light/dark art) | `picture` + `prefers-color-scheme` ([SleekCMS theme variants](https://docs.sleekcms.com/media/images)) | **HAVE pattern** — `ThemePicture` pair per slot; **NEED** admin pairing UI for promoted + CMS media |
| Responsive widths AVIF/WebP | Transform recipes in `transform-recipes.ts` | **HAVE** scaffold; byte ceilings open |
| Consumer vs decorative alt | Registry `AltPolicy` | **HAVE**; project previews need CMS alt |

---

## 5. Gap matrix — HAVE vs NEED

| Area | HAVE | NEED (priority) |
|---|---|---|
| Decorative promoted assets | 12 runtime PNGs staged | Regenerate/refine per [asset prompts](./PUBLIC-190-asset-prompts/README.md) **P0** |
| Family-specific hero art | Reused rail/previews across PF | Dedicated PF hero/path/contact/about assets **P1** |
| CMS copy on index routes | Honest `ContentState` + structural labels | Published records via API **P0** (content authority) |
| Home dynamic composition | Static seed | `home-composition` API + rebuild **P0** |
| Graph interactivity | Static DOM nodes | API graph + filter + optional SVG/canvas **P0** |
| Admin graph editor | OpenAPI candidate only | ADMIN-210 UI **P1** |
| Home/timeline modules admin | OpenAPI candidate | ADMIN-190/200 **P1** |
| Media focal in admin | Contract mention | ADMIN-180 focal fields + public `object-position` **P1** |
| Scroll motion | CSS only | Motion islands for reveals **P2** |
| Visual acceptance | 39/48 pairs, REVISE | Owner sign-off + hash table **blocking** |

---

## 6. Top 5 missing capabilities (blocking concept-faithful dynamic site)

1. **Owner-approved decorative asset set** matching concepts (hero arch, backplates, PF-specific panels) — prompt pack ready; promotion + wiring pending.
2. **Published CMS content on PF index routes** — shells exist but API-backed heroes, featured cards, rows, FAQ, and form fields are blocked without owner-approved records.
3. **Research graph data + interaction model** — public DOM constellation without published node/edge payload and filter/sync behavior from admin graph editor.
4. **Admin workflows for composition** — home module ordering, timeline, graph editor, media focal/theme variants not shipped in admin-panel (ADMIN-190–210).
5. **Integrated rebuild/preview loop** — static Astro build must refresh when admin publishes (rebuild trigger + preview-share); staging smoke (`PUBLIC-320` / `BACKEND-180`) still open.

---

## Sources (web research)

- [Sanity page builder + Astro example](https://github.com/maciejtrzcinski/sanity-page-builder-astro-example)
- [Starter Astro + Sanity](https://github.com/ericmikkelsen/starter-astro-sanity)
- [Astro + Strapi blocks example](https://github.com/PaulBratslavsky/astro-strapi-example-project)
- [Sanity and Astro introduction](https://www.sanity.io/docs/astro/introduction)
- [Motion scroll animations](https://motion.dev/docs/react-scroll-animations)
- [Motion with Astro (Netlify)](https://developers.netlify.com/guides/motion-animation-library-with-astro/)
- [GSAP ScrollTrigger + Astro View Transitions](https://gsap.com/community/forums/topic/40950-compatibility-with-gsap-scrolltrigger-astro-view-transitiosn-api/)
- [Scroll experience playbook (Lenis/GSAP/R3F tiers)](https://github.com/Eneryleen/ai-web-design-codex/blob/main/09-playbooks-and-checklists/playbook-scroll-experience.md)
- [DatoCMS focal points](https://www.datocms.com/docs/content-delivery-api/images-and-videos)
- [Strapi focal point picker](https://github.com/strapi/strapi/pull/25267)
- [Sanity image crop/hotspot](https://www.sanity.io/docs/apis-and-sdks/presenting-images)
- [R3F Html overlay integration](https://www.intelligentgraphicandcode.com/development/threejs-interfaces/html-integration)
- [Graphier WebGL graph renderer](https://github.com/CocoRoF/graphier)
