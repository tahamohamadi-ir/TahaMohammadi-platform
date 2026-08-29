# Local Development

## Content and design authority

**Seed v1.1 + tracked design authority take priority over the live legacy CMS.** See `LOCAL-RUNTIME-SSOT.md` for the single-source-of-truth map and promotion workflow (`scripts/promote-design-intake.ps1`).

## Existing Docker stacks on this machine

The legacy `tahamohamadi-website` compose stack (nginx, Next.js, Django, PostgreSQL 16) may already run on ports **80/443**. That stack is **not** the new platform runtime. Do not point new-platform development at its database or containers unless a task explicitly documents a one-time migration experiment.

The new platform uses:

| Product | Path | Runtime status |
|---|---|---|
| Backend | `Back-End/` | Migrated Django; use disposable PostgreSQL |
| Public site | `Front-End/public-site/` | Wave 0 scaffold in progress (Astro) |
| Admin panel | `Front-End/admin-panel/` | Wave 0 scaffold in progress (React/Vite) |

## Backend baseline

Run backend commands from `Back-End/`.
Use Python 3.12 and `uv`.
Use a **disposable** PostgreSQL database for the new platform — host port **5433**, database `taha_platform_dev`. See `Back-End/docs/operations/LOCAL-DATABASE.md` and `Back-End/docker-compose.dev.yml`.

Recommended first-time sequence:

1. Start disposable PostgreSQL (Docker or local install).
2. Copy `Back-End/.env.example` to `.env` and set database URL.
3. `uv sync` and activate the virtual environment.
4. `python manage.py migrate --settings=config.settings.development`
5. `python manage.py check --settings=config.settings.development`
6. `pytest`
7. Verify `GET /health/` against the disposable database.

## Public and admin baseline

After Wave 0 scaffold commits:

| Repo | Dev command | Default port |
|---|---|---|
| `Front-End/public-site/` | `npm run dev` | 4321 |
| `Front-End/admin-panel/` | `npm run dev` | 5173 |

Proxy `/api` to `http://127.0.0.1:8000` per each repo's `vite.config` / Astro config.

Do not reuse the legacy local stack script because its paths target the old monorepo.

## Content seed import (development only)

Import source: `Docs/01-product/owner-content-seed-v1/cms-package/content-records.v1.1-seed.json`

All records remain draft or not-public until individually approved. Seed supplement empty states are for development UX only.

## Coordination documents

Multi-agent execution order: `Docs/05-delivery/MULTI-AGENT-TASK-BOARD.md`
