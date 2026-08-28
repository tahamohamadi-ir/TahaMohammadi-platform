# Repository Boundaries

| Repository | May own | Must not own |
|---|---|---|
| Public site | Public rendering, public adapters, SEO, search index | Draft state, admin permissions, database models |
| Admin panel | Authenticated UI, forms, editor state, admin adapters | Public page rendering, server authorization |
| Backend | Data, lifecycle, auth, APIs, media, audit | Public visual templates, SPA component library |

Shared behavior moves through documented contracts. Source files are not shared by relative path.
