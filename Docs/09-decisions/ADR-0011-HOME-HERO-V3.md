# ADR-0011 — Home Hero v3

Date: 2026-11-01. Status: **Proposed — three prototypes built behind the atlas build; the owner picks one before anything replaces the live hero.**

## Context

The live Home hero (Hero v2, `HeroSequence.astro`) is a four-frame scroll-scrubbed image sequence pinned inside a tall scroll shell. It satisfies ADR-0008's "graph inside the hero" only symbolically: the frames are rendered spheres, the real published graph is not shown, nodes are not links, and the scroll-jacked travel adds height before the reader reaches content. The owner decided on 2026-10-30 to redesign the Home hero from scratch (UI/UX upgrade plan, Phase 5).

Verified inputs on 2026-11-01:

- `GET /api/graph/{en,fa}` publishes 4 nodes (identity + 3 research topics) and 3 `research-focus` edges, each with API positions and a colour role (`brand`, `research`, `signature`, `context`).
- `GET /api/v1/records/{locale}/resolve` maps every topic's `relatedRecords` to a real published slug, so constellation nodes can be genuine links.
- The authored Hero v2 renders (frame 04, both themes, desktop + mobile cameras) show exactly those four colour-coded spheres and are already promoted media.
- `createGraphScene` (CA-04, `src/lib/visual/graph-scene.ts`) already renders a procedural Three.js constellation from a `ScenePayload` under the scene contract's performance ceilings.

## Decision

The Home hero becomes a single, non-pinned first viewport: an editorial copy column (two-tone serif name, signature-gold role line, authored intro, the three managed CTAs, focus chips) beside one visual built only from the published graph or from already-promoted art. No scroll-jacking, no scroll travel shell.

Three candidates are built on atlas-only routes (`/_design/home-hero/{en,fa}/{a,b,c}/`, `DESIGN_ATLAS=1`), all sharing one copy component:

- **A — Editorial constellation.** Server-rendered SVG of the real graph (orbital rings, curved edges, colour-role nodes) with HTML node links positioned over it. CSS-only motion (edge draw-in, slow ring drift). Zero JS.
- **B — Live constellation.** A's SVG is the poster and the no-JS / reduced-motion / no-WebGL state. When idle, visible, motion-allowed and WebGL-capable, `createGraphScene` is lazy-imported and crossfaded in; the HTML links follow the projected node positions.
- **C — Refined still.** The promoted Hero v2 frame 04 (theme- and device-correct) with a one-time CSS reveal, plus a colour-role legend whose entries are the real topic links.

The owner chooses one in a local review. The chosen candidate then replaces `HomeHero`'s visual column and the scroll shell in `HomeContent.astro`; `HeroSequence.astro`, `hero-sequence.css`, `lib/visual/hero-sequence.ts` and the unused frames 01–03 are removed in the same change.

This supersedes the Home portion of ADR-0008 (the procedural Three.js constellation with HTML node controls remains a valid implementation — candidate B — but is no longer mandatory) and the Hero v2 scroll-sequence direction. The gateway portal decision in ADR-0008 is unchanged.

## Constraints for every candidate

LCP ≤ 2.5 s; hero image ≤ 240 KiB desktop / ≤ 140 KiB mobile; no scroll-jacking; readable and navigable without JavaScript; static under `prefers-reduced-motion: reduce`; fa/en mirrored copy column; both themes without downloading the other theme's media; no invented nodes, edges, links, or copy — an absent graph hides the visual rather than faking one.

## Consequences

- Positive: the hero shows real, linked research structure; the page loses the pinned scroll travel; the copy column is reused unchanged by whichever visual wins.
- Negative: B adds a lazy Three.js chunk on capable devices and must stay inside the scene contract's ceilings. A and C are static and lighter but less striking. The graph is small (4 nodes), so A/B depend on the CMS graph growing to stay interesting.

## Verification

Atlas build renders all six candidate pages; fa/en × light/dark screenshots at 390/768/1440 per candidate; `npm run lint`, `format:check`, `test`, `build`; reduced-motion and no-JS checks; then the owner's pick recorded here, flipping Status to Accepted.
