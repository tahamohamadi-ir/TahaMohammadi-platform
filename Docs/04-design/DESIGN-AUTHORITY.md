# Design Authority

<!-- PRODUCT-V2.1 -->
Active V2.1 override: Home uses the graph inside the hero; portal geometry belongs only to `/`. Historical `portal-orbit-*` Home roles and graph backplates below are retained asset history, not required runtime composition. New independent page families follow PRODUCT-SPEC and share the story renderer; tracked concepts guide appearance only. ADR-0008/0010 and EXECUTION.md supersede conflicting old freeze/motion/placement assumptions. Do not rewrite pinned binary hashes or factual source content.
<!-- /PRODUCT-V2.1 -->

## Binding target

For the current public visual recovery, apply [ADR-0008](../09-decisions/ADR-0008-HOME-GRAPH-HERO-AND-PROCEDURAL-MOTION.md) and [V2 design specification](../05-delivery/concept-alignment-v2/DESIGN-SPEC.md) as an explicit overlay on the tracked reference. Home's separate portal/graph composition and historical disabled-3D settings are superseded for assigned CA-* packets. The reference bytes stay pinned; palette, fonts, content and release guarantees remain. No Figma output is required to dispatch these packets.

The new public and admin frontends are built from scratch. The sole tracked visual reference is `Docs/references/frontend-design-authority/`.

Read these files in order:

1. `references/frontend-design-authority/README.md`
2. `references/frontend-design-authority/AUTHORITY-MANIFEST.json`
3. `references/frontend-design-authority/design-dna.json`
4. `references/frontend-design-authority/concepts/` and `concepts/page-families/`
5. `references/frontend-design-authority/agent-kit/tokens.json`
6. `references/frontend-design-authority/agent-kit/components.json`
7. `references/frontend-design-authority/agent-kit/templates.json`
8. `ASSET-PROMOTION-LEDGER.md` and `PAGE-FAMILY-UI-UX-CONTRACT.md`

## Reference boundary

- Concept PNG files show hierarchy and art direction.
- Concept PNG files must not be sliced into production UI.
- Concept copy is not publishable content.
- Artwork is a candidate asset until owner publication approval.
- Runtime components must use semantic HTML, real fonts, logical CSS properties, and accessible controls.
- `Front-End/Assets` is local incoming evidence, not active agent authority.

## Visual direction

- Light Editorial: warm ivory, navy, turquoise, and limited gold.
- Dark Scientific Atlas: deep navy, warm ivory, and restrained contextual accents.
- Glass is limited to the gateway and sticky header.
- Cards, prose, forms, tables, and empty states use readable solid surfaces.
