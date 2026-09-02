# ADR-0007: Visual assets and CMS-driven page blocks

**Status:** Accepted (coordination)  
**Date:** 2026-09-02  
**Context:** PUBLIC-190 visual remediation — concepts require both **ledger-promoted decorative art** and **admin-managed structured content**.

## Decision

1. **Decorative runtime images** enter public-site only through `ASSET-PROMOTION-LEDGER.md` with SHA-pinned masters in `Docs/references/frontend-design-authority/art/` and promoted copies under `Front-End/public-site/src/assets/media/`. Owner regeneration uses [PUBLIC-190-asset-prompts](../10-tracking/PUBLIC-190-asset-prompts/README.md); agents do not invent masters.

2. **Page-family section content** (featured records, rows, FAQ, timeline, graph nodes, home modules) comes from **Django public APIs** documented in `OPENAPI-REVIEW-REPORT.md`. Public-site maps entity kinds to Astro shells; empty `ContentState` when unpublished — no concept-text fallback.

3. **Block composition pattern** follows headless CMS page-builder ergonomics (typed section array → renderer) but **implementation stays Django + admin-panel** — no parallel Sanity/Strapi authority.

4. **New media slots** (e.g. PF hero panels, contact atmosphere) require: ledger row + `MediaSlot` in `promoted-media-registry.ts` + transform recipe + ADR/ledger cross-link before runtime import.

5. **Graph visualization** defaults to **DOM + SVG + decorative backplate**; WebGL (R3F) only if DOM path fails visual acceptance and admin graph payload requires it (`PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md` §3.3).

6. **Admin media** must expose focal point and optional light/dark variant pairing before public `object-position` and `ThemePicture` consume CMS uploads (`MEDIA-CONTRACT.md`).

## Consequences

- Asset prompt pack and remediation plan are the owner-facing path for atmosphere/graph gaps.
- ADMIN-190/200/210 remain prerequisites for dynamic concept fidelity beyond structural shells.
- PUBLIC-190 cannot PASS on CSS-only work without owner asset approval where concepts depend on art.

## References

- [PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md](../10-tracking/PUBLIC-190-IMPLEMENTATION-REQUIREMENTS.md)
- [PUBLIC-190-VISUAL-REMEDIATION-PLAN.md](../10-tracking/PUBLIC-190-VISUAL-REMEDIATION-PLAN.md)
- [MEDIA-CONTRACT.md](../03-contracts/MEDIA-CONTRACT.md)
- [CONTENT-CONTRACT.md](../03-contracts/CONTENT-CONTRACT.md)
