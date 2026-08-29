# Local Runtime — Single Source of Truth

Status: active for Wave 0 multi-agent execution (2026-08-29).

## Content authority decision

**Seed v1.1 + tracked design authority outrank the live legacy CMS.** The greenfield platform starts from:

- `Docs/01-product/owner-content-seed-v1/cms-package/content-records.v1.1-seed.json` (85 records, all draft/not-public until owner approval)
- `Docs/references/frontend-design-authority/` (promoted from `Front-End/Assets`)

Legacy `tahamohamadi-website` data is not migrated in Wave 0. Production cutover replaces the old stack when the new stack passes staging gates.

## Layer map

| Layer | Edit here | Generated / consumed by |
|---|---|---|
| Owner visuals (working) | `Front-End/Assets/` (gitignored) | `scripts/promote-design-intake.ps1` → design authority |
| Design contracts | `Docs/references/frontend-design-authority/agent-kit/*.json` | CSS tokens, component checklist, asset registry |
| Runtime images | `ASSET-PROMOTION-LEDGER.md` + authority `art/`/`brand/` | `public-site` build pipeline (Wave 1+) |
| Public content | `content-records.v1.1-seed.json` → backend import | Public API → Astro pages |
| Routes | `Docs/02-architecture/ROUTE-REGISTRY.md` | Route helpers in `public-site` (generated, Wave 1) |
| API | `Back-End/docs/contracts/openapi/current/` | TypeScript types in frontends (hash-pinned, Wave 1) |

**Rule:** Never edit generated outputs by hand. Change the source layer, then run the generator or promotion script.

## Local port plan

| Service | Host port | Notes |
|---|---|---|
| Legacy stack | 80, 443 | Do not use for new platform |
| New PostgreSQL | **5433** | `Back-End/docker-compose.dev.yml` |
| Django API | 8000 | `config.settings.development` |
| Astro public dev | 4321 | `Front-End/public-site` |
| Vite admin dev | 5173 | `Front-End/admin-panel` |
| Dev reverse proxy (later) | 8080 | Same-origin cookie/CSRF rehearsal |

## Wave 0 agent lanes (parallel)

| Lane | Task IDs | Repository |
|---|---|---|
| COORD | Decision log, SSOT docs, promotion scripts | `Docs/` |
| BACKEND | BACKEND-010..050 | `Back-End/` |
| PUBLIC | PUBLIC-010..040 | `Front-End/public-site/` |
| ADMIN | ADMIN-010..040 | `Front-End/admin-panel/` |

Wave 1 starts after BACKEND-050 and both frontend scaffolds build: seed import (BACKEND-060..080) + OpenAPI type generation.

## Promotion workflow (Assets → authority)

1. Owner edits files under `Front-End/Assets/`.
2. Run `scripts/promote-design-intake.ps1` from workspace root.
3. Script copies changed binaries into `Docs/references/frontend-design-authority/`, updates `SHA256SUMS.txt`, runs `agent-kit/validate.mjs`.
4. For runtime `art/`/`brand/` use, add or update a row in `ASSET-PROMOTION-LEDGER.md` before shipping to `public-site`.

Do not import `Front-End/Assets` directly from application build configs.
