# Concept alignment V2 — implementation design contract

<!-- PRODUCT-V2.1 -->
V2.1 execution amendment: exact scheduling is execution-tasks.json. §3 list-adapter ID resolution is superseded by PRODUCT-INTERFACES-V2 §I04 and PU-03-resolver/PU-SYNC-graph; current public lists generally omit IDs. No guessed slug is allowed. New family details follow PRODUCT-SPEC/shared StoryDocument. CA-09–16 are retired dispatch aliases; retain their visual criteria in successor PU packets.
<!-- /PRODUCT-V2.1 -->

Authority: [ADR-0008](../../09-decisions/ADR-0008-HOME-GRAPH-HERO-AND-PROCEDURAL-MOTION.md). Scope: existing public site, both locales and themes. This is the assigned design target; no runtime or visual acceptance is claimed. References are evidence only. Numeric layout/motion limits below are V2 engineering/design targets, not pixel measurements extracted from a raster or measured results.

## 1. Final composition

**Gateway owns the portal; Home owns the constellation.** Do not wrap the Home constellation in a portal, add portal wallpaper to Home, or render a second graph section under it. Do not move this choice back to a later worker. The owner delegated that decision and it is resolved here.

Home order: header → integrated identity/graph hero → research interests & fit → journey → selected projects → selected publications when eligible → gallery/blog/education rails → concise collaboration band → footer. Preserve authorized research statement text by relocating it to a readable paragraph or native disclosure inside the hero, or the existing research-fit region; removing a duplicate section must not silently delete content.

One meaningful H1. Retain name, approved role, intro and legitimate CTAs. Use `HomeHeroContent.namePrimary/nameAccent` where appropriate to restore typographic distinction in English; Persian uses the existing full name with locale-safe wrapping. Never split Persian letters for animation. Long professional titles stay supporting text. A paragraph-length statement must not be styled as a billboard H2; reuse an already authorized section label as heading and retain the statement as body text. No invented shorter research claims.

The graph carries visual interest formerly split across the portal and a separate graph. Keep text against calm opaque canvas, never across moving edges. A small existing brand mark may occupy the graph's visual center; it is decorative and must not imply a new graph node or relationship.

## 2. Layout and typography

| Viewport | Grid and composition | Behavior |
|---|---|---|
| 1280–1440 | 12 columns; max inline width 1280px; 32px gutters; text 5 columns, graph 7 | Copy on inline-start; graph on inline-end. EN left/right, FA right/left. Hero padding 64–96px block; no rounded outer card, no large empty media well. |
| 1024 | 12 columns with 24px gutters; balanced 5/7 split | Graph labels stay legible; reduce ornament before shrinking body copy. |
| 768 | 8 columns; 24px gutters; stack if real text/labels cannot fit | Prefer reading order over forcing a compressed two-column hero. |
| 320–390 | 4 columns; 16px gutters; single hero containing copy/CTAs, graph, node detail | Graph height target 280–360px; no fixed full-screen height. Hero can be taller than viewport. No clipped labels or horizontal page scroll. |

Desktop scene slot target: 520–620px high; mobile uses a flatter camera and less depth. These are intrinsic/reserved scene dimensions, not fixed heights for text. At 200% zoom use natural flow and permit the hero to grow. Copy and actions precede graph controls in DOM in both locales. No CSS ordering that disagrees with focus order.

Use exact existing palette roles: Light canvas `#f7f8f5`, ink `#182328`, brand `#087c73`, signature `#a77b28`; Dark canvas `#071225`, ink `#f7f3ea`, brand `#16b8a6`, signature `#c89b3c`. Read actual CSS variables for theme changes; do not create a second palette in a renderer. Font pairs: EN Newsreader/Inter; FA Estedad/Vazirmatn. Body 16px or more in the main reading surface; use current display scale up to 64px as the starting point. FA line height must accommodate joined glyphs and long labels. All interactive targets at least 44×44 CSS px.

Use thin orbital geometry, a stable central focus, limited contextual colors, quiet lighting and transparent scene background. The dark theme is not permission for neon fog, starfields or bloom over text. Light mode uses fine dark/teal lines with subtle shadows rather than turning the whole graph into pale invisible gold.

## 3. Graph data: existing contract, new presentation

Verified local source: `Front-End/public-site/src/generated/public-api.ts` exposes `GET /api/graph/{locale}` and `GraphPayloadOut` with `nodes` and `edges`. `GraphNodePublicOut` has `id`, `label`, `accessibleLabel`, `type`, `weight`, optional `summary`, `colorRole`, `iconRole`, `position {x,y,z?}`, and `relatedRecords {family,id}[]`. Edges have `id`, `source`, `target`, `relationType`, `weight`, `directed`, optional `explanation`.

**There is no public `groups` array and no `href` or `slug` on relatedRecords.** Do not synthesize URLs from IDs or add endpoints. Resolve eligible exact-locale published records through existing family adapters and canonical route helpers. A record whose family/ID cannot resolve is not a link. Report unresolved mappings separately; selection can still show the node's existing label/summary.

Use generated types rather than hand-maintained copies. Use the current API URL resolver/client patterns; do not cast arbitrary strings to `keyof paths` to bypass routing safety. Runtime-check boundary values: unique IDs, finite positions/weights, recognized color/icon roles, and edges whose ends exist. Render optional missing arrays as empty. Unknown visual roles use a neutral supported role, never raw CSS or arbitrary icon import.

Build-time published graph input becomes static semantic HTML plus serialized renderer data; renderer does not contact admin endpoints. Preserve locale isolation. Published nodes may differ across languages; parity means equivalent functionality and honest data states, not fabricated translations or equal counts.

Current `HomeResearchGraph.astro` does `nodes.slice(0, 3)` and hard-codes unavailable node states. Replace that truncation with deterministic layout of all eligible nodes. For large graphs, group *presentation* or offer native list selection with a bounded visible subset; do not invent scientific categories or drop records silently. Use API positions when valid; otherwise derive stable layout from ID/order. `z` added for visual depth is presentation only and has no scientific meaning. Connected decorative orbit points are not records; visually distinguish orbital decoration from semantic edges. Only API edges represent research relationships.

Empty/unavailable data must not become a convincing fake research network. Show the appropriate existing ContentState, available identity/CTAs and a quiet decorative orbit if desired. A clearly labeled local Atlas fixture may exercise 0, 1, 3, 5, 12 and 50 node cases without entering public output. Published-data readiness and visual readiness are separate gates.

## 4. Semantic controls and interactions

Implement the base with native HTML, e.g. one list of node `<details>` elements with `<summary>` labels and summaries/eligible links in their bodies. The renderer enhances this same semantic source; it must not create a second conflicting keyboard tree. Alternative native buttons + a permanently available list are acceptable only after equivalent no-JS behavior is proven.

| State/action | Required behavior |
|---|---|
| Initial | Name, intro, CTAs and graph list usable before scripts. No text at opacity zero waiting for JS. |
| Focus/hover node | Highlight corresponding node and incident API edges; title and accent both identify it. Focus does not unexpectedly navigate. |
| Enter/Space/tap node | Select node; show its exact summary and resolved links in a reserved HTML detail area. No automatic route change. |
| Select another | Replace detail without resetting scroll or stealing focus. Preserve all nodes in the accessible list. |
| Escape/reset | Clear selection, return focus to the initiating control if necessary. Reset never empties semantic HTML. |
| Follow related link | Normal anchor navigation to an existing published exact-locale route. |
| Pan/zoom | Omit free OrbitControls initially; restrained pointer tilt on fine pointers only. Browser scroll and pinch zoom must work. |
| Many/long labels | Use stable label rails around the scene or a list below it. Labels remain HTML; do not clip or shrink to unreadable text. |
| Error/context loss | Restore fallback immediately, preserve selection/content, report no success status for failed graphics. |

Canvas is `aria-hidden`; its geometry is redundant with semantic content. Labels should be visually anchored to node positions with collision rules. Pointer hit testing, if added, dispatches into the same selection model. Touch is tap-to-select, not hover-to-discover. Use existing locale-approved utility copy where available; any newly required control strings must be added to the public-site localization source as UI copy, not personal factual content.

## 5. Three.js / GSAP ownership

Rebuild the scene from primitives: shallow elliptical orbit lines, subtle depth planes, instanced node discs/spheres, restrained central identity. Use a fixed, near-frontal perspective or orthographic camera as the initial composition. Avoid a free force simulation that drifts labels or hides relationships. One renderer for the Home hero, one for the gateway on its separate route; no canvas per card. The Home shader/model path must not import the gateway portal.

Proposed new modules (internal paths, not existing files): `src/lib/visual/scene-contract.ts`, `graph-scene.ts`, `graph-layout.ts`, `graph-controller.ts`, `graph-motion.ts`, `gateway-scene.ts`, `gateway-motion.ts`, `hero-enhancement.ts`; components under `src/components/hero/` and `src/components/gateway/`. Reuse existing primitives, route/content adapters and theme events.

Suggested internal API: `createGraphScene({canvas,payload,palette,onFrame})` returns `render`, `resize`, `setPalette`, `setSelection`, `dispose`. `onFrame` supplies projected positions by node ID for HTML label placement. The controller owns native state; scene and motion consume it. This is a proposed frontend-only interface, not a new backend schema. CA-03 locks exact TypeScript signatures before CA-04/05/07 implementation.

GSAP animates camera offset, orbit group pose and selection emphasis. Use one scheduled render source, not both an endless `requestAnimationFrame` loop and a separate GSAP ticker. Render during changes, then idle. Suggested choreography: one 600–900ms scene settle after successful mount; 180–280ms selection feedback; fine-pointer tilt clamped to approximately ±3 degrees. These are targets for review. Text stays visible throughout. No looping autoplay, forced scroll, pinned full-screen hero, camera travel through text, or scroll-hijacking.

Scope animations with `gsap.context`, register reduced-motion behavior with `gsap.matchMedia`, and revert/kill listeners/timelines on disposal using the installed package's supported API. Reduced motion uses static pose and instant selection, no pointer tilt or transforms. A user motion preference change takes effect without reload. Avoid a second motion library.

Load Three.js only on eligible scene routes after semantic content renders. GSAP already exists in `package.json`; verify lockfile before selecting a compatible Three.js version. Do not install `latest` blindly. No React/R3F migration is required to animate vanilla Astro DOM. [Astro scripts documentation](https://docs.astro.build/en/guides/client-side-scripts/) describes processed browser scripts and reusable script patterns.

## 6. Lifecycle, fallbacks and performance

Reserve scene size before load. Keep semantic list present regardless of JS/network/GPU failure. Gateway can retain an approved `portal-centered-*` raster as a static fallback until its procedural scene succeeds; an image-free HTML gateway is also valid if that fallback has not passed QA. Home fallback is semantic list plus a deterministic 2D graph, never the old portal image.

Detect unavailable WebGL, import rejection, context loss and repeated frame-budget failures. Restore fallback without a reload. Pause work when offscreen or document hidden. Re-render on resize, theme change, selection and active animation only. Dispose all geometry/material/texture/render resources and remove event handlers when leaving the page. Three.js resources require explicit cleanup ([official cleanup guide](https://threejs.org/manual/en/cleanup.html)).

Proposed first-pass ceilings for CA-04/06/07: one active canvas per route; desktop effective DPR ≤1.5, mobile ≤1; drawing buffer ≤1.5 million pixels; ≤60 scene draw calls; ≤50,000 triangles; optional scene JS including renderer/motion ≤300 KiB gzip per route; authored gateway geometry is procedural with no external model required. **These are proposed engineering ceilings, not measurements or universal capability claims.** If measured costs exceed a ceiling, simplify geometry and suspend optional effects before requesting a targeted budget revision. Don't weaken existing LCP/INP/CLS tests to pass.

Existing project targets remain LCP ≤2.5s, CLS ≤0.1, INP ≤200ms; field p75 acceptance requires actual deployed telemetry. Local tests are guardrails. Compare scene-on vs semantic-only on the same device/network, log bundle bytes, transfer bytes, frame-time p95 and long tasks. Initial useful content may not wait for canvas completion. Mobile motion may fall back automatically if it cannot sustain a 33ms frame budget; desktop target 16.7ms during interaction. No field performance PASS is claimed in this plan.

Use CSS size + explicit drawing-buffer size and camera aspect to avoid stretched scenes and unbounded high-DPI rendering ([Three.js responsive guide](https://threejs.org/manual/en/responsive.html)). Prefer rendering on change when idle ([rendering on demand](https://threejs.org/manual/en/rendering-on-demand.html)).

## 7. Gateway direction

Use the existing dark gateway concept for silhouette: one centered, tall arch, shallow steps/threshold, a restrained halo and orbital detailing. Reconstruct geometry procedurally rather than texturing a rectangular plane with the full raster. Light uses mineral/ivory material and teal/gold detail; dark uses navy structural material, teal interior light and restrained gold edges. Transparent background integrates with page canvas. Brand and language labels are real HTML. No text, buttons or logo redesign baked into a texture. Language selection navigates immediately; do not wait for a cinematic transition. Entrance occurs once and can be skipped by reduced motion.

## 8. Remaining page families

| Family | Required correction | Preferred technology |
|---|---|---|
| PF-07 About/CV | Restore compact identity hierarchy, tab/anchor rhythm, timeline/skills rows; remove misleading gallery-as-portrait treatment; no invented portrait/certificates | Astro/CSS, genuine approved media only |
| PF-05 Research/Publications | Reuse semantic graph/renderer with page-specific layout; real bibliography rows, metadata and resolved links | Shared graph + HTML/SVG; no second Home graph |
| PF-04 Projects | Distinct project preview roles, numbered editorial rows, real evidence affordances, truthful missing-media state | Static responsive media + CSS |
| PF-03 Blog | Editorial type, featured content and compact rows; no fake subscriptions/archive counts | Astro/CSS, approved coral art if appropriate |
| PF-06 Education | Library identity, path/list rhythm, native filters only with real data | Astro/SVG path + static art; no WebGL per card |
| PF-01/02 Gallery/detail | Varied authorized work in grid; original artwork, captions/rights and detail navigation; never fill empty CMS with duplicate decorative images | Real media + accessible HTML; optional bounded transitions |
| PF-08 Contact | Clear heading, topic/form/sidebar alignment and native validation; no portal repeated as decorative hero | Astro/CSS; preserve tested form/API behavior |
| Shell/Home lower sections | Thin section dividers, restrained surfaces, readable titles and compact collaboration band; hide unavailable fake affordances using approved state rules | Existing components and CSS |

Canonical routes are `/blog/`, `/education/`, `/gallery/` per route registry; existing `writing`, `teaching`, `creative` source component names can remain. Do not introduce route renames in visual packets. Reference images show populated compositions; compare real empty/unavailable pages against explicit empty-state design, never require fake data to achieve screenshot similarity.

## 9. Acceptance protocol

Capture 320, 390, 768, 1024, 1280, 1440 CSS px × FA/EN × Light/Dark. Gateway has both languages in one route: two themes at each width. Record viewport height, DPR, content state, commit, URL, renderer state, motion preference and capture hash. For Home compare V2 integrated-hero requirements plus the old concept's palette/type/density; do not treat disappearance of the old portal/separate graph as a regression.

Before render acceptance, verify selected node, reset, theme change, long Persian label, empty graph, rejected graph data, missing related record, JS disabled, reduced motion, unavailable WebGL, context loss and resize. Then native keyboard, real 200% zoom, screen-reader reading order and mobile touch. No severe/critical accessibility findings or clipped controls. Reviewer must inspect paired images for geometry, typography, color, media role, label legibility and section density; screenshot existence is not approval.

Gate sequence: semantic behavior PASS → independent scene/layout review PASS → complete responsive/interaction/performance evidence → owner visual acceptance. Track content publication, visual acceptance and staging/production readiness separately. Existing PUBLIC-190 and PUBLIC-350 cannot be closed by this plan.
