# HERO VISUAL SPECIFICATION — v1

**Project:** Taha Mohammadi — premium research portfolio  
**Surface:** Home hero, `/en/` and `/fa/`  
**Date:** 2026-09-14  
**Document owner:** ROOT coordination; intended production owners: Blender artist and PUBLIC frontend team  
**Status:** Production specification prepared for review. No artwork, implementation, publication, or visual acceptance is certified by this document.

## Production brief and authority

Create a quiet, cinematic constellation of tactile, organic spheres: an editorial portrait of a research practice through objects, light, and relationships. The first impression is human, deliberate, and scientifically curious. The name and introduction remain the primary reading surface; the constellation supplies depth and character.

This specification defines new art direction in response to the owner's current brief. Numeric values are production targets, not measured results. It retains the integrated Home graph, native HTML controls, palette, typography, and bounded Three.js/GSAP direction in [ADR-0008](Docs/09-decisions/ADR-0008-HOME-GRAPH-HERO-AND-PROCEDURAL-MOTION.md) and [DESIGN-SPEC](Docs/05-delivery/concept-alignment-v2/DESIGN-SPEC.md). The three research-axis meanings come from [PRODUCT-SPEC §1](Docs/05-delivery/concept-alignment-v2/PRODUCT-SPEC.md), under [ADR-0009](Docs/09-decisions/ADR-0009-RESEARCH-FIRST-CONTENT-COMPLETE-PRODUCT.md).

The tracked Light, Dark, and Persian mobile Home concepts inform warmth, typography, spacing, and orbital balance. Their historical portal placement and raster copy do not carry into this hero. The portal remains exclusive to the language gateway.

Existing RU-3 assets describe different project-domain objects. They are not silently renamed or reassigned to the research axes below. This document specifies a separate sphere family. Runtime adoption must be assigned through the active leaf-packet queue in [EXECUTION.md](Docs/05-delivery/concept-alignment-v2/EXECUTION.md); it does not reopen or mark an existing packet complete. Backend/admin interfaces are unchanged.

## 1. Visual concept

**Working title: Quiet Intelligence — a living research constellation.**

An ivory or mineral-navy central form sits slightly forward of three companion spheres. Each companion has one intelligible physical distinction: an open protective shell, a gently layered body, or a compact segmented surface. Broad highlights move across satin materials as the viewpoint shifts subtly. Fine relationship lines occupy the space between forms only when supported by published graph data.

The Apple-style storytelling reference translates into careful object presentation, a controlled camera, exceptional material finish, and one focal moment. It does not prescribe copying a product campaign or adding lengthy scroll choreography. Editorial restraint comes from generous empty space and a small number of memorable objects.

Human-centered identity is communicated through rounded forms, soft asymmetry, warmth, and clear access to the research. Avoid anatomical brains, humanoid faces, robots, medical-device depictions, DNA helices, holographic dashboards, stars, neon mist, and arbitrary streams of data. These would introduce unsupported subject matter or overwhelm the portfolio.

The settled composition must be convincing as a still image. Animation improves its physical presence; it never repairs a weak composition.

## 2. Node system architecture

Maintain four independent production layers:

| Layer | Blender responsibility | Frontend responsibility |
|---|---|---|
| Identity form | Author the central sphere and its physical finish | Place it as non-interactive decoration unless an exact published identity-node mapping exists |
| Research forms | Author three distinguishable, reusable sphere assets | Bind each to a verified published node; preserve its exact localized label and summary |
| Relationships | Provide material and line-weight reference only | Construct edges from published graph relationships; preserve direction and explanation |
| Information | Reserve clear label and detail areas; render no text | Render name, introduction, labels, selection, and links as accessible HTML |

Artist identifiers in this document are asset names, not API identifiers. At integration, record the exact published node ID, locale, asset mapping, source revision, and eligible related-record links. The meaning of proximity, depth, and size is compositional only. None represents influence, confidence, research maturity, citation count, or strength of evidence.

Do not bake topology, labels, URLs, or research claims into a model or texture. Do not automatically connect every sphere to the center. If the center is decorative, no semantic edge terminates there. Any background orbit is an incomplete, faint ellipse without node endpoints or traveling dots, so it cannot be mistaken for a relationship.

## 3. Number of nodes

**Canonical art-directed composition: four major spheres — one identity form plus three research-axis forms.** This is a design composition, not a claim that the currently published graph contains exactly four nodes.

| Role | Canonical count | Rule |
|---|---:|---|
| Identity form | 1 | Decorative by default; not counted as an additional semantic research node |
| Main research-axis forms | 3 | Equal visual rank; bind only when the exact axis records are published in the current locale |
| Supporting record spheres | 0 | Add only for actual eligible graph records, using the smaller hierarchy below |
| Decorative particles | 0 | No random satellite dots or star field |

For a larger published graph, cap the overview at **eight semantic spheres plus the decorative identity form: nine visible objects maximum**. All eligible nodes remain available in the HTML list, including those outside this overview. Use existing authored selection/order; otherwise use stable ID order. Selecting an off-overview record replaces a supporting slot deterministically and updates its incident edges. The core is not duplicated if it maps to an actual graph node.

Fewer available records produce fewer spheres; do not fill vacancies with plausible research topics. With no usable graph, show the correct existing content state and, optionally, the isolated decorative identity form. A four-sphere layout with unbound asset roles may be used for clearly identified internal art review only.

## 4. Meaning of each node

| Asset ID | Meaning and source | Physical expression | Label and interpretation rules |
|---|---|---|---|
| `HV_CORE` | Taha Mohammadi's identity; the owner's brief supplies the name | Broad, softly asymmetric mineral sphere; one recessed seam and a small warm accent | Represents the portfolio's organizing identity. It is not an AI model, achievement, or scientific entity |
| `HV_HCAI` | Human-Centered AI; PRODUCT-SPEC §1 | Rounded shell with a shallow, generous opening around a smaller inset form | Suggests room for the human perspective. No face, person icon, brain, or claim of a particular method |
| `HV_HEALTH` | AI for Health & Human Behavior; PRODUCT-SPEC §1 | Continuous sphere with two shallow, offset contours following its volume | Suggests observation across layers and contexts. No pulse trace, diagnosis, medical certification, or clinical-benefit implication |
| `HV_EDGE` | Wearable / Edge Intelligence; PRODUCT-SPEC §1 | Compact sphere with three broad, rounded segments and a fine inset band | Suggests compact systems and distributed operation. No invented wearable product or hardware specification |

The descriptions above are artistic metaphors, not public scientific copy. Main-axis labels and Persian equivalents must come from the exact-locale published content. The product direction establishes the themes; it does not prove that corresponding graph records or translations exist. Do not infer those mappings from label similarity alone.

Supporting spheres represent whichever real records the graph provides. Their meaning is supplied by HTML, never by an invented material taxonomy. Selection emphasizes the chosen form and its real incident edges; it does not imply endorsement or a ranked research priority.

## 5. Node size hierarchy

Use a domain-sphere bounding diameter of **1.00 Blender unit**, with metric scene units. Author every node at its own origin and assemble using parent transforms.

| Object | Bounding diameter | Approximate diameter in a 600px-wide desktop scene |
|---|---:|---:|
| Identity core | 1.45 units | 145–170 CSS px |
| Each main axis | 1.00 unit | 100–117 CSS px |
| Supporting record | 0.38–0.52 units | 38–61 CSS px |

All three main axes have equal base diameter. Apparent size may vary slightly through depth, but keep the largest-to-smallest apparent main-axis ratio below 1.12. Use depth primarily for occlusion and lighting, not rank.

Organic deformation: broad silhouette displacement within 2–4% of diameter; no lumpy noise. Bevels: 0.01–0.025 units on domain-scale seams. A maximum of one distinctive opening or segmentation motif per form keeps the set coherent. An inset must remain readable in grayscale at mobile size.

Keep at least 12 CSS px between major projected silhouettes on mobile and 20px on desktop. Allow an edge to disappear behind a form; do not let one main axis hide another. A small supporting sphere still receives a separate HTML target of at least 44 × 44 CSS px.

## 6. Material specification

**Material language:** satin ceramic, fine mineral composite, restrained brushed metal. Glass is not the sphere's primary material. Opaque PBR materials make the form readable in both themes and keep the runtime simple.

| Material role | Metallic | Roughness | Physical direction |
|---|---:|---:|---|
| `HV_SHELL` | 0 | 0.34–0.44 | Satin mineral ceramic; dielectric IOR starting point 1.45 |
| `HV_INSET` | 0 | 0.48–0.60 | Slightly more matte inner surface; darker through light and occlusion |
| `HV_ACCENT` | 0.75–0.90 | 0.28–0.38 | Small brushed signature-metal seam; never a whole gold sphere |
| `HV_BRAND` | 0 | 0.28–0.38 | Restrained teal inset, with no bloom or emission required |

Transmission and subsurface scattering are zero in the runtime target. Use geometry, broad reflection, and warm fill to produce softness. Metallic detail occupies at most 5% of the visible object area. No mirror-polished chrome or rainbow coating.

| Palette role | Light | Dark |
|---|---|---|
| Page canvas | `#f7f8f5` | `#071225` |
| Reading ink | `#182328` | `#f7f3ea` |
| Brand | `#087c73` | `#16b8a6` |
| Signature | `#a77b28` | `#c89b3c` |

These values are existing theme authority. Use canvas-derived mineral shells in Light and navy shells with warm edge separation in Dark; teal and gold occupy limited details. Reading ink belongs to HTML. Dark materials must show their shape without requiring a luminous background. These are base-color targets; rendered highlights are not expected to equal flat CSS swatches.

Use one shared mesh family and four stable material slots. The frontend assigns current theme roles. Do not export duplicate light/dark geometry or introduce new semantic color categories. Light and Dark look-development renders must use genuinely adjusted material/light setups, not an inverted image.

## 7. Texture specification

Base delivery is texture-free at runtime: smooth normals, geometry, and material constants must carry the design. In Blender, use very low-frequency procedural variation for look development; keep microtexture below 1% visible luminance variation at final display size. No bitmap text, scientific diagrams, stock photograph overlays, fingerprints, scratches, or dirty concrete.

If the final visual review demonstrates a clear need for surface detail, allow one **shared 512 × 512 tangent-space normal map** and one **512 × 512 packed occlusion/roughness/metallic map**, within the performance budget. Bake procedural detail before export; do not expect the browser to reproduce an arbitrary Blender shader graph. Blender's glTF exporter supports a defined material mapping, including metallic/roughness conventions. [Blender glTF export reference](https://docs.blender.org/manual/en/5.0/addons/import_export/scene_gltf2.html).

Texture rules: packed map R = occlusion, G = roughness, B = metallic; normal and packed maps are non-color data. Base-color/emissive maps, if later authorized, are sRGB. Keep UV seams on the rear; use 8px island padding at 512px and inspect mip levels for seams. No runtime displacement. Provide lossless PNG bake masters and record normal-map orientation.

Keep an untextured comparison render: if the tiny texture does not improve the object at 320px scene width, omit its web export. Treat color textures and non-color data distinctly in the renderer. [Three.js color-management reference](https://threejs.org/manual/en/color-management.html).

## 8. Lighting setup

Build a three-light studio rig. Coordinates below use Blender X = screen-right, Y = away from the camera, Z = up, with the composition near the origin. They are calibration starting points at the unit scale in §5.

| Light | Position | Source dimensions | Relative level | Purpose |
|---|---|---|---:|---|
| Key | (−3, −4, 5) | 4 × 4 units area | 1.00 | Broad upper-left highlight and readable sphere curvature |
| Fill | (4, −2, 1) | 5 × 5 units area | 0.30 Light / 0.18 Dark | Preserve shadow detail without flattening the form |
| Rim | (2, 3, 4) | 2 × 4 units area | 0.35 Light / 0.55 Dark | Separate silhouettes and reveal openings |

Begin with a 600W key; adjust all powers together to the exposure reference before changing ratios. Use near-neutral key/fill and a slightly warm rim. Physical power is a starting setting, not a brightness guarantee across different renderers.

World illumination is low and neutral. No star HDRI, visible horizon, floor, volumetric fog, lens flare, or atmospheric particles. The network floats; contact shading is limited to nearby surfaces inside each node. Any soft halo remains within 8% of the form's diameter and must not touch the copy zone.

Render on transparent film, plus theme-composited review outputs. Inspect highlight clipping, dark-side detail, and alpha edges against both exact page canvases. Capture a neutral reference swatch and exposure in the handoff. Record the Blender view transform and exposure; produce a browser-matched PBR reference as well as the cinematic beauty. Do not bake the artistic view transform into base-color textures.

For web, approximate the broad illumination with simple lights and a small shared environment only if necessary. Default to no real-time shadow maps and no post-processing. The frontend matches the visual result within budget; it does not reproduce the Cycles rig light-for-light.

## 9. Camera setup

Use a stable, near-frontal perspective. In Blender, start at **(0, −11, 3)** looking at **(0, 0, 0)** with a **70mm lens and 36mm sensor**. Fit the constellation by camera distance; do not distort individual nodes to meet the crop.

| Format | Projection | Framing | Depth of field |
|---|---|---|---|
| Desktop | 70mm perspective | Shallow, asymmetrical diamond; core slightly forward | Beauty starting point f/8; all major forms remain recognizable |
| Tablet | 85mm perspective | More centered with less depth separation | f/11 or disabled |
| Mobile | Orthographic | Recompose the four forms into a compact diamond | Disabled |

Lens values and sensor fit must be recorded with camera transforms and output aspect ratio. Export a camera sheet for the frontend; do not embed cameras in the web model. Translate Blender Z-up into the frontend's coordinate convention once, and verify with a labeled axis reference in the production handoff.

Web depth of field is disabled. Depth comes from geometry, shading, and slight occlusion. No handheld camera shake, fisheye, rack focus, auto-orbit, zoom-through, or full-screen fly-in. Maximum fine-pointer view change is ±3° yaw and ±2° pitch; mobile has a fixed camera.

## 10. Desktop composition

At 1280–1440 CSS px viewport width, use the existing 12-column system, a maximum 1280px content width, and 32px outer gutters. Text occupies five columns at inline-start; the scene occupies seven at inline-end. At 1024px use 24px gutters. Scene height target: 520–620px. The hero has natural content height and no enclosing rounded card.

Use these **projected scene-slot coordinates**, measured from its top-left, to block the canonical four-form pose:

| Form | Center X | Center Y | Relative depth |
|---|---:|---:|---|
| Core | 50% | 49% | Front |
| HCAI | 29% | 24% | Middle |
| Health | 76% | 43% | Slightly behind core |
| Edge | 30% | 76% | Back |

Keep all main silhouettes inside an 8% inset. Tune centers within ±3 percentage points to resolve label collisions. Maintain an open composition, with at least roughly half the scene-slot area visually quiet. The art never extends beneath the H1, paragraph, or CTA targets.

Labels remain stable in nearby HTML rails or below the scene. Use short leaders when needed; move a label out of the art rather than shrink it. The selected-node detail occupies reserved space below the scene, growing naturally with text. No hover-only information.

EN places copy left and art right; FA places copy right and art left. Move the scene slot logically without mirroring the model, lighting, texture, or text. DOM and keyboard order stay copy → actions → graph controls → details. Existing Newsreader/Inter and Estedad/Vazirmatn pairings remain; use approved copy only, a starting display size up to 64px, and body text at least 16px.

## 11. Tablet composition

At 768–1023px, default to a stacked composition: copy and actions, scene, then selected detail. Use eight columns, 24px gutters, and a 400–460px-high scene. At 1024px and above, retain the 5/7 split only while actual labels and copy fit.

Use centers at core (50%, 50%), HCAI (28%, 25%), Health (75%, 40%), and Edge (31%, 77%). Reduce perspective depth by 40% relative to desktop. Keep all four primary forms; remove optional supporting forms from the overview before reducing label size. Their HTML entries remain available.

Touch selection is first-class. No pointer tilt on coarse pointers, no drag-to-discover dependency, and no automatic camera change when a user scrolls past the hero. Check landscape, portrait, and resizing between them without retaining a stale canvas width.

## 12. Mobile composition

At 320–767px use one column and 16px gutters. Reading order is name/intro → existing CTAs → scene → graph list/details. Target scene height is **280–360px**, approximately 300px at a 390px viewport. A long Persian introduction may make the hero taller than the viewport; that is acceptable.

Use a dedicated mobile camera, not a crop of the desktop image. Core center: (50%, 49%); HCAI: (26%, 23%); Health: (77%, 33%); Edge: (33%, 78%). Target core diameter 80–94px and axis diameter 54–64px, adjusted to preserve the minimum silhouette gaps at 320px. Keep the lowest form clear of the list below.

Show four major forms only in the canonical overview. Put labels in a stable HTML list below the art, using 44px minimum targets and at least 8px between adjacent targets. Selection adds a visible ring and text state; color alone is insufficient. Do not squeeze three long labels around tiny spheres or bake identifiers into the artwork.

No tilt, autoplay, gyroscope access, swipe carousel, forced landscape, or captured vertical scrolling. The browser retains pinch zoom. At 200% zoom the layout reflows and the scene may yield space to the list. CSS owns canvas dimensions; its drawing-buffer dimensions must never widen the page.

## 13. Required render frames

Produce **26 rendered views** for art review: 18 composition frames and eight isolated-form views. These are review/reference renders, not a downloadable web frame sequence.

| View family | Resolution | Themes | Poses | Rendered views |
|---|---|---|---|---:|
| Desktop scene slot | 1920 × 1600 | Light + Dark | F000, F001, F002 | 6 |
| Tablet scene slot | 1440 × 1200 | Light + Dark | F000, F001, F002 | 6 |
| Mobile scene slot | 780 × 720 | Light + Dark | F000, F001, F002 | 6 |
| Four isolated forms | 1024 × 1024 each | Light + Dark | F000 | 8 |

Frame definitions are exact review states, not frame-rate timestamps:

| ID | Required state |
|---|---|
| F000 | Neutral settled pose; default and reduced-motion appearance |
| F001 | Desktop/tablet maximum positive view offset: yaw +3°, pitch +2°; mobile fixed camera with HCAI selection appearance |
| F002 | Desktop/tablet maximum negative view offset: yaw −3°, pitch −2°; mobile fixed camera with Health selection appearance |

For each composition view deliver a scene-linear half-float multilayer EXR containing beauty/alpha, depth, and object-ID masks, plus a theme-composited sRGB PNG. Each isolated view needs a transparent sRGB PNG. Total base image package: **18 EXR + 26 PNG files**. Depth and ID passes are archival QA data, never public web downloads. Record near/far depth normalization and object-ID assignments in the render manifest.

Use Cycles with a starting target of 256 samples, adaptive noise threshold 0.01, and denoising; raise quality only where seams or metal exhibit residual noise. Inspect full resolution and downsampled views at 320px scene width. Do not add visible grain to hide render noise.

Produce a review contact sheet from these views and layout composites at 1440 × 900, 768 × 1024, and 390 × 844 in both themes and locales: **12 composites**, using approved HTML copy in a layout tool, never Blender text. These are assembled review sheets, not additional 3D render jobs. They are viewport windows into a scrolling page, not instructions to fit the whole mobile hero above the fold.

Unbound art-review frames contain no research edges. Once the exact graph mapping is validated, capture runtime edges and labels in frontend QA; do not invent a Blender edge network to make a preview look finished.

## 14. Animation illusion strategy

**Use shallow 3D with sparse, event-driven motion.** A small change in viewpoint, soft parallax, and moving reflections provide cinematic depth without a movie or continuous simulation. The still renders establish the look and camera envelope. Three.js renders live geometry; existing bounded GSAP choreography supplies transitions.

| Trigger | Motion | Duration / limit |
|---|---|---|
| First successful scene mount | Settle from a 1.5° yaw offset into F000; all text already visible | 750ms once, smooth ease-out |
| Fine-pointer movement inside scene | Small camera-rig offset; labels track the corresponding projected node | Clamp yaw ±3°, pitch ±2°; smooth response around 200ms |
| Node selection | Add ring/tonal emphasis and emphasize real incident edges | 220ms; no rearrangement or camera flight |
| Pointer leaves | Return to F000 | 280ms, then stop rendering |
| Scroll, idle, offscreen, hidden document | No decorative motion | Zero idle animation work |
| Reduced motion | F000 and immediate selection appearance | Zero transform animation and zero pointer tilt |

Do not crossfade between F001 and F002 as an animation technique: it produces doubled edges and ghosted spheres. Do not ship a sprite sheet or image sequence. No breathing loop, edge-travel particles, changing topology, force simulation, or scroll scrubbing.

On constrained devices or renderer failure, the deterministic 2D graph and semantic list carry the research. An approved isolated core still can retain physical warmth as decoration; it must not replace the semantic graph with a frozen, potentially stale network. The fallback is fully usable without JavaScript. An image is empty-alt decoration when the adjacent HTML carries its meaning; do not announce duplicated graph descriptions.

Use one scheduled rendering source during changes and return to idle afterward. Rendering on demand is an established fit for interactive scenes that do not need continuous animation. [Three.js rendering-on-demand reference](https://threejs.org/manual/en/rendering-on-demand.html).

## 15. File naming convention

Use lowercase ASCII, hyphens, explicit version, theme, viewport, state, and dimensions. Artist IDs inside the Blender file remain the uppercase names in §4.

| Deliverable | Naming pattern or example |
|---|---|
| Editable master | `tm-home-hero-spheres-v1.blend` |
| Runtime geometry candidate | `tm-home-hero-spheres-v1.glb` |
| Composition beauty | `tm-home-hero-v1-desktop-dark-f000-beauty-1920x1600.png` |
| Multilayer source | `tm-home-hero-v1-desktop-dark-f000-passes-1920x1600.exr` |
| Isolated form | `tm-home-hero-v1-core-light-f000-isolated-1024x1024.png` |
| Mobile example | `tm-home-hero-v1-mobile-light-f002-beauty-780x720.png` |
| Layout composite | `tm-home-hero-v1-mobile-dark-fa-layout-390x844.png` |
| Optional web core still | `tm-home-hero-v1-core-dark-static-w384.webp` |
| Handoff manifest | `tm-home-hero-v1-manifest.md` |

Allowed view tokens: `desktop`, `tablet`, `mobile`; themes: `light`, `dark`; isolated form tokens: `core`, `hcai`, `health`, `edge`. Art contains no locale-specific text, so locale belongs only in layout composites and QA captures. Delivery names are proposed filenames, not existing routes or approved runtime paths.

Use `v1.1`, `v1.2`, etc. for later revisions; never overwrite a reviewed delivery silently. At runtime promotion, fingerprint the approved bytes through the existing asset pipeline. Record the resulting filename and SHA-256 in the handoff.

## 16. Asset export specification

| Package | Required contents | Recipient |
|---|---|---|
| Editable art | Dedicated `.blend`, organized geometry/material/light/camera collections, documented exposure and versions | Blender team |
| Web model candidate | One GLB with four independent sphere groups, shared material slots, applied scales and documented origins | Frontend team |
| Render reference | §13 image package, contact sheet, camera/lighting sheet, optional texture masters | Art review and frontend matching |
| Handoff manifest | File inventory, dimensions, bytes, SHA-256, color spaces, alpha convention, renderer/exporter versions, measured triangles/materials, node-map state and review status | Both teams |

GLB contains mesh geometry and supported PBR material defaults only: no lights, cameras, floor, text, full-scene image planes, physics, animation clips, or unused materials. Preserve separate `HV_CORE`, `HV_HCAI`, `HV_HEALTH`, and `HV_EDGE` groups under `HV_ROOT`; do not merge nodes into one mesh. Place each asset at its local origin and deliver layout/camera coordinates in the manifest. The frontend owns placement and connections.

Target budgets: core ≤6,000 triangles; each axis ≤3,000; base four-form family ≤15,000. Exporting may split vertices at discontinuous normals or UVs, so inspect the actual imported result. [Blender glTF export reference](https://docs.blender.org/manual/en/5.0/addons/import_export/scene_gltf2.html). Supporting spheres should be instanced low-detail primitives, not copies of the high-detail core.

Check a clean re-import for applied scale, diameters, normals, empty geometry, unintended duplicate faces, material-slot names, and recognizable silhouettes. Do not enable compression or material extensions that the assigned frontend loader cannot already decode. Simplify geometry first; the base candidate must fit without assuming a new decoder dependency.

Render color handling: EXR remains scene-linear with recorded view-transform metadata; review PNG is display-referred sRGB. Transparent PNG uses straight alpha; inspect compositing against both page colors for dark/white fringes. Treat procedural Blender finishes as look references unless their supported PBR equivalent or explicit bake is included.

If an isolated-core fallback is selected for promotion, export widths **192, 384, and 768px**, square, in AVIF plus WebP fallback, for both themes: **12 derivatives**. Select only the appropriate theme, width, and supported format per request. Do not download both formats or both themes initially. These derivatives are optional runtime candidates; composition PNGs and EXRs remain offline.

Do not write directly over the existing RU-3 or portal assets. Runtime media requires an explicit entry in the existing [Asset Promotion Ledger](Docs/04-design/ASSET-PROMOTION-LEDGER.md), provenance, and the responsive/accessible plan. No render generation or model export is performed by this specification delivery.

## 17. Performance constraints for web

The following are acceptance targets to measure during implementation. Existing project ceilings remain in force; none of these numbers is a claimed result.

| Budget | Target / ceiling | Measurement boundary |
|---|---|---|
| Initial semantic hero | Available before scene import | Name, copy, actions, and graph list must not wait for GLB or renderer |
| Optional isolated-core still | ≤80 KiB mobile; ≤160 KiB desktop | One selected compressed image; do not preload an unused still alongside a model |
| GLB | Target ≤650 KiB; hard ceiling 1 MiB | Actual downloaded model; no light/dark duplicate models |
| Optional surface maps | ≤128 KiB total | Additional maps only; count embedded maps inside the GLB once |
| Optional environment | ≤128 KiB transfer, ≤512 × 256 source | Omit when the simple light setup is sufficient |
| All optional scene assets | ≤1.25 MiB total | Model + separate maps + environment + any fetched still; excludes JS below |
| Optional scene JavaScript | ≤300 KiB gzip per Home route | Renderer, motion, model loaders, and any decoders combined |
| Geometry | Base family ≤15k; complete scene ≤50k triangles | Count the scene actually rendered, including supporting nodes and edge meshes |
| Draw calls | Target ≤30; ceiling 60 | Include lines, rings, highlights, and selected-state geometry |
| Active canvas | One per route | No second decorative canvas |
| Drawing buffer | ≤1.5 million pixels | Effective DPR ≤1.5 desktop/tablet and ≤1 mobile; lower DPR further when pixel cap requires |
| Texture allocation | ≤16 MiB estimated decoded texture memory | Include mipmaps and generated environment maps; exclude framebuffers and driver overhead |
| Interaction rendering | Desktop target p95 ≤16.7ms; mobile ≤33ms | Test on recorded representative devices, not only the artist's workstation |
| Idle work | Zero continuous scene frames | Redraw only for active transitions, resize, theme, or selection |
| Page quality | LCP ≤2.5s; CLS ≤0.1; INP ≤200ms | Retain existing project gates; deployed p75 needs field data |

Reserve scene space from the first HTML render. Load enhancement after useful content, and skip optional 3D under reduced motion, a data-saving preference, or a demonstrated resource constraint. A theme change reuses geometry and changes material roles. Repeated frame-budget failures disable motion, then optional effects, then restore the deterministic fallback. Context loss or import failure restores usable content without reloading the page.

Measure cold-cache mobile loading and scene-on versus semantic-only performance on the same device/network. Record actual transfer bytes, decoded texture estimates, scene statistics, frame-time p95, long tasks, and layout shifts. Release geometry, textures, listeners, and render resources on navigation; repeat entry/exit to detect retained resources.

### Acceptance and handoff checklist

- Art: all four forms are distinct in grayscale and at 320px scene width; broad highlights and controlled seams read in both themes; copy areas stay calm.
- Content: exact-locale mappings and real edges are verified before public graph rendering; empty and unavailable states contain no fabricated network.
- Responsive: check 320, 390, 768, 1024, 1280, and 1440 CSS px × EN/FA × Light/Dark, including an in-place desktop-to-mobile resize and real 200% zoom.
- Interaction: keyboard selection/reset, visible focus, native links, long Persian labels, touch, reduced motion, no JavaScript, WebGL failure, context loss, and theme switching remain usable.
- Delivery: reopen the Blender master, re-import the GLB, validate the manifest, and inspect final compressed candidates against the page canvases.
- Evidence: record the reviewed revision and measured budgets. Artist completion, frontend verification, asset promotion, owner visual acceptance, and deployment remain separate statuses.

**Definition of done for this document:** all 17 production areas are specified. The next production step is a four-form graybox and paired Light/Dark look-development review, followed by the render/export package and separately assigned frontend integration. No new profile facts, node IDs, translations, or release status are supplied by this document.
