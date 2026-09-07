# Dependency Policy

<!-- PRODUCT-V2.1 -->
Current product/implementation authority: ADR-0010, `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` and `Docs/05-delivery/concept-alignment-v2/EXECUTION.md` (coordination-root paths). Keep Astro/TypeScript with bounded Three.js/GSAP, existing React admin/Django backend, Pagefind and first-party aggregate analytics. Earlier stack/phase assumptions apply only where compatible. Rebuild jobs/edge invalidation are a planned interface, not an already operating deployment.
<!-- /PRODUCT-V2.1 -->

- Pin direct dependencies.
- Add one dependency only for a documented missing capability.
- Prefer platform APIs and existing dependencies.
- Record license and runtime cost before adoption.
- Keep public JavaScript optional and bounded.
- Keep admin-only dependencies out of the public bundle.
- Block dependencies with unresolved critical vulnerabilities.
