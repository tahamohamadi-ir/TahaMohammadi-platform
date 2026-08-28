# System Architecture

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
- React islands own only stateful, bounded interactions.
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
