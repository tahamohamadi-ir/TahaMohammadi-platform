# Design DNA

<!-- PRODUCT-V2.1 -->
Active V2.1 override: Home uses the graph inside the hero; portal geometry belongs only to `/`. Historical `portal-orbit-*` Home roles and graph backplates below are retained asset history, not required runtime composition. New independent page families follow PRODUCT-SPEC and share the story renderer; tracked concepts guide appearance only. ADR-0008/0010 and EXECUTION.md supersede conflicting old freeze/motion/placement assumptions. Do not rewrite pinned binary hashes or factual source content.
<!-- /PRODUCT-V2.1 -->

## Authority

The machine-readable source is [design-dna.json](../references/frontend-design-authority/design-dna.json). The curated visual sources are `concepts/` for system-level UI/UX and `concepts/page-families/` for page detail. Exact token values are marked as such; qualitative visual observations never override accessibility, content, or API contracts.

## System identity

- Light Editorial: warm ivory canvas, mineral-white surfaces, navy reading ink, turquoise action, and limited gold signature.
- Dark Scientific Atlas: deep navy canvas, layered blue surfaces, warm ivory reading ink, turquoise identity/action, and restrained violet, emerald, coral, and gold context.
- The visual metaphor is a portal to a connected research constellation. It supports hierarchy; it never replaces content or navigation.
- English uses Newsreader plus Inter. Persian uses Estedad plus Vazirmatn. Each locale activates only its assigned pair after the font gate passes.
- Layout is a 4/8/12 logical-column system at 320, 390, 768, 1024, 1280, and 1440 pixels.

## Effects boundary

- Glass is limited to the language gateway and sticky header, with opaque fallback.
- Current recovery direction is [ADR-0008](../09-decisions/ADR-0008-HOME-GRAPH-HERO-AND-PROCEDURAL-MOTION.md): an integrated Three.js graph hero on Home, a Three.js portal only on the language gateway, and bounded GSAP choreography. The pinned historical `design-dna.json` is read with the explicit [V2 overlay](../05-delivery/concept-alignment-v2/design-overlay.json); CA-01 owns consumer adoption.
- Semantic HTML is implemented before scene enhancement. The list and enhanced view expose identical information and eligible links; content never requires a renderer.
- No custom cursor or free decorative particle field. Custom shader experiments, global scroll effects, and new libraries outside assigned V2 packet scope require a specific scope amendment.
- Reduced motion removes continuous motion and transform-based non-essential effects.

## Design decision rule

When a raster concept conflicts with an accepted semantic, responsive, RTL, content-state, or accessibility requirement, the written requirement wins. Record an intended visual deviation in visual QA rather than changing the underlying contract.
