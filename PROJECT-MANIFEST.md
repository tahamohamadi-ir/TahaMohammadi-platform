# Project Manifest

## Workspace

- Root: `D:\Project\tahamohammadi-platform`
- Coordination documents: `Docs/`
- Default branch: `main`
- Working model: three independent product repositories

## Repositories

| ID | Path | Remote | Bootstrap HEAD | Owner |
|---|---|---|---|---|
| `PUBLIC` | `Front-End/public-site` | `TahaMohammadi-platform-FrontEnd-publicSite` | `288ec860f00eba4b595dcb0692ce88b3391317d8` | Public web experience |
| `ADMIN` | `Front-End/admin-panel` | `TahaMohammadi-platform-FrontEnd-adminPanel` | `4d229b1828aeb2589636f8e429a6218452ac7cff` | Authenticated content administration |
| `BACKEND` | `Back-End` | `TahaMohammadi-platform-backEnd` | `82e3984520154b60146009ae4a0d21eb5c30373e` | Data, publication, media, authentication, APIs |

## Technical baseline

| Product | Baseline |
|---|---|
| Public site | Astro 7, TypeScript 5.9, Tailwind CSS 4, bounded React 19 islands |
| Admin panel | React 19, TypeScript 5.9, Vite, accessible SPA patterns |
| Backend | Python 3.12, Django 5.2.9, Django Ninja 1.6.2, PostgreSQL 17 |

## Source boundaries

- Backend migration source: `D:\Project\Taha-personal-platform\apps\cms`
- Backend source commit: `cdaa283fac9da57c6d88e22aa0751be6214b6cf6`
- Design reference source: `D:\Project\Taha-personal-platform\New\site-redesign`
- Legacy public frontend: audit evidence only
- Legacy admin frontend: audit evidence only

## Canonical documents

- Authority: `Docs/00-governance/AUTHORITY-ORDER.md`
- Architecture: `Docs/02-architecture/SYSTEM-ARCHITECTURE.md`
- Interfaces: `Docs/03-contracts/`
- Design: `Docs/04-design/`
- Roadmap: `Docs/05-delivery/MASTER-ROADMAP.md`
- Tasks: `Docs/05-delivery/MASTER-TASK-LIST.md`
- Migration: `Docs/07-migration/`
- Bootstrap completion: `Docs/10-tracking/BOOTSTRAP-COMPLETION-REPORT.md`
