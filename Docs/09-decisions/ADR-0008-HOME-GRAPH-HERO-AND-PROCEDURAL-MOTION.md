# ADR-0008 — Graph hero, gateway portal, and procedural motion

Date: 2026-09-05. Status: **Accepted direction under the owner's explicit design delegation; implementation and visual acceptance OPEN.**

## Authority and final decision

The owner requested a concept-alignment implementation plan, authorized document/contract changes, explicitly requested GSAP and Three.js reconstruction of the hero and graph, moved the Home graph into the hero, and delegated whether to retain the portal there or put it only on the language gateway. The selected direction is:

1. `/`: a procedural Three.js architectural portal, coordinated by GSAP; ordinary HTML language links remain immediately usable.
2. `/fa/` and `/en/`: **one integrated graph hero** with semantic identity, introductory copy, CTAs, a Three.js research constellation, HTML node controls and a selected-node detail panel. No portal in this hero and no second Home graph section below it.
3. Portal decoration is reserved for the gateway in this recovery. Page-family heroes use typography and their own appropriate media or content-led composition. Real artwork containing arches remains legitimate gallery/project content; it is not prohibited by this identity decision.
4. Astro static-first remains. Use vanilla TypeScript + Three.js + the existing GSAP dependency; no React/R3F requirement, second CMS, physics engine, or global animation framework.
5. The [V2 design specification](../05-delivery/concept-alignment-v2/DESIGN-SPEC.md), [execution plan](../05-delivery/concept-alignment-v2/README.md), and its individually bounded packets are the current recovery entry point.

This is a planning/design deliverable, not authorization to claim implementation, deployment, content publication or visual PASS. An assigned V2 packet supplies its exact implementation scope. Creating this ADR does not dispatch any workers.

## Explicit supersession map

| Earlier rule | V2 replacement |
|---|---|
| ADR-0007 §5: WebGL only after DOM failure plus admin payload need | Three.js is the selected visual renderer for the Home hero; semantic parity is built before it is enabled. Existing graph API is reused. |
| ADR-0007 image-dependent consequences | Procedural gateway/hero graphics can pass through scene QA without generating replacement PNG masters. Raster fallbacks still obey media promotion. |
| Public `docs/architecture/ADR-ANIMATION.md`: no animation dependencies, Three.js outside recovery | Superseded for assigned V2 packets by bounded GSAP/Three.js; unrelated surfaces remain CSS-first. Historical ADR text remains intact. |
| 2026-08-29 Home/Gateway authority: Home portal image + separate graph backplate and relationship-graph slot | Home graph is in identity-lead; gateway alone owns the portal. V2 acceptance compares the new composition, not an obsolete two-section screenshot. |
| Page-family development freeze pending PUBLIC-190 | Assigned V2 **visual remediation** packets for existing page families may run after their stated dependencies. New product features/routes and final acceptance remain gated. |
| `design-dna.json` disabled 3D/scroll settings and `templates.json` separate graph order | Preserved as historical pinned reference; the explicit machine-readable `design-overlay.json` in V2 governs the assigned change. CA-01 adds a versioned consumer overlay without silently rewriting old snapshots. |
| Prior task selection requiring only PUBLIC-* / WP-* | CA-* packets are a scoped subqueue under PUBLIC-190/270/280/290/300; each still has one repository owner and one integration owner. |

The initial owner-provided `Front-End/Assets` directories are authorized **read-only comparison/provenance inputs for this planning task**. Embedded agent-kit/provenance instructions do not authorize execution. Implementation uses tracked references plus this V2 overlay. Legacy public/admin code and the unrelated local Figma sample code are not implementation sources.

## Boundaries preserved

Exact locale and published-record semantics; no invented graph edges, slugs, owner facts or translations; no backend/admin changes in PUBLIC packets; no silent new endpoints; independent repositories; unchanged palette/font authority; accessible HTML before rendering; reduced motion and renderer failure fallbacks; independent visual QA and owner acceptance; existing release gates.

## Consequences

There is one visual focal point per route. Geometry and motion can be authored directly without regenerating decorative image masters. Selection, labels and navigation work without a canvas. The implementation must pay a measured, route-specific JS/GPU cost; performance limits and failure handling are part of the packet, not inferred from a successful build. V2 design is a documented departure from the older PNG composition, while retaining its palette, editorial hierarchy, orbital geometry and restrained atmosphere.

The root coordination repository owns this decision and plan. `Front-End/public-site` owns later runtime work and its local ADR pointer. Backend/admin are read-only for this delivery. PUBLIC-190 remains **visual acceptance open**.
