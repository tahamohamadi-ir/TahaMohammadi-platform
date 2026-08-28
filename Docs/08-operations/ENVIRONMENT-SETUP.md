# Environment Setup

Create one uncommitted `.env` per repository from its committed `.env.example`.

Use these categories:

- Backend: database, mail provider, allowed hosts, CSRF origins, secret key, media storage.
- Public site: public API base and public site URL.
- Admin panel: admin API base and admin site URL.

Never reuse production credentials in local development.
