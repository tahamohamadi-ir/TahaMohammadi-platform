# System Architecture

<!-- PRODUCT-V2.1 -->
Current product/implementation authority: ADR-0010, `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` and `Docs/05-delivery/concept-alignment-v2/EXECUTION.md` (coordination-root paths). Keep Astro/TypeScript with bounded Three.js/GSAP, existing React admin/Django backend, Pagefind and first-party aggregate analytics. Earlier stack/phase assumptions apply only where compatible. Rebuild jobs/edge invalidation are a planned interface, not an already operating deployment.
<!-- /PRODUCT-V2.1 -->

## Decision

Use three independently versioned and deployed products.

```text
Public browser -> public-site -> published API -> backend -> PostgreSQL/media
Admin browser  -> admin-panel -> admin API     -> backend -> PostgreSQL/media
```

## Public site

- Astro owns routes, document structure, metadata, and static output.
- TypeScript owns typed adapters and build-time validation.
- Tailwind CSS 4 consumes semantic CSS variables.
- Vanilla TypeScript owns bounded public interactions; Three.js/GSAP enhance only assigned scene surfaces. React is optional, not a required public runtime.
- Public content remains complete without JavaScript.

## Admin panel

- React and Vite own the authenticated SPA.
- A generated or contract-tested API client owns transport.
- Server permissions remain authoritative.
- Client routing never replaces backend authorization.

## Backend

- Django owns data, lifecycle, authentication, permissions, and media.
- Django Ninja owns versioned JSON APIs and OpenAPI.
- PostgreSQL is the production data authority.
- Anonymous projections expose published content only.

## Release boundary

Each repository builds and releases independently.
An interface change is not releasable until every affected consumer passes contract tests.
