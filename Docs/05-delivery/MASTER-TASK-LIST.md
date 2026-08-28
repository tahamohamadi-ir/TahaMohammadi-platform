# Master Task List

Status markers: `[x]` verified complete, `[ ]` not complete.

## R0 — Workspace foundation

- [x] Connect public-site to its GitHub remote.
- [x] Connect admin-panel to its GitHub remote.
- [x] Connect backend to its GitHub remote.
- [x] Copy 198 tracked backend files from the exact legacy commit.
- [x] Verify zero backend copy hash mismatches.
- [x] Copy the design-reference pack.
- [x] Verify all 33 managed reference hashes.
- [x] Create canonical workspace governance.
- [x] Create cross-repository architecture and contracts.
- [x] Create and validate repository-specific governance, roadmaps, task lists, quality plans, and agent adapters.
- [x] Commit and push repository-specific bootstrap documents.
- [x] Commit the root coordination repository locally.

## R1 — Backend baseline

- [ ] Review `Infra/legacy-monorepo` and classify each file.
- [x] Create a Python 3.12 virtual environment with `uv`.
- [x] Install the locked backend dependencies.
- [x] Run Ruff without modifying migrations; all checks pass.
- [x] Run the full pytest suite; 636 tests pass.
- [x] Record the migrated test baseline; no failures occurred.
- [ ] Start the backend with development settings.
- [ ] Verify `/health/` against a local PostgreSQL database.
- [ ] Apply all migrations to an empty PostgreSQL database.
- [ ] Export the current public OpenAPI schema.
- [ ] Export the current admin OpenAPI schema.
- [ ] Generate an endpoint inventory from source and OpenAPI.
- [ ] Remove legacy SPA-serving responsibility from backend only after admin cutover.
- [ ] Rewrite active backend container and deployment files for the new repository paths.

## R2 — Shared contracts

- [ ] Normalize new stable endpoints under `/api/v1/` with compatibility decisions.
- [ ] Freeze the public published-projection schema.
- [ ] Freeze the admin authentication and CSRF behavior.
- [ ] Freeze the error envelope.
- [ ] Freeze media identifiers and rendition fields.
- [ ] Freeze locale and untranslated-content behavior.
- [ ] Generate TypeScript API types from accepted OpenAPI.
- [ ] Add backend schema compatibility tests.
- [ ] Add public-site contract fixtures.
- [ ] Add admin-panel contract fixtures.

## R3 — Public design foundation

- [ ] Scaffold Astro 7 and TypeScript 5.9.
- [ ] Configure Tailwind CSS 4 with a verified processing pipeline.
- [ ] Self-host Newsreader, Inter, Estedad, and Vazirmatn.
- [ ] Implement semantic Light and Dark tokens.
- [ ] Add computed-style token tests.
- [ ] Build the required primitive components.
- [ ] Build Gateway, Header, Footer, and skip link.
- [ ] Build six shared page templates.
- [ ] Build a local-only Visual Atlas.
- [ ] Verify the atlas is excluded from production builds.
- [ ] Implement system, Light, and Dark theme selection.
- [ ] Add reduced-motion behavior.
- [ ] Generate responsive derivatives from approved asset masters.

## R4 — Public page families

- [ ] Implement the language gateway.
- [ ] Implement Persian and English Home pages.
- [ ] Implement About and profile routes.
- [ ] Implement Research and Publications indexes and details.
- [ ] Implement Projects index and details.
- [ ] Implement Writing index and long-form details.
- [ ] Implement Books, Talks, and Downloads.
- [ ] Implement Teaching and course details.
- [ ] Implement Creative index and details.
- [ ] Implement CV and Resume downloads.
- [ ] Implement Contact with backend validation.
- [ ] Implement per-locale Pagefind indexes.
- [ ] Implement honest empty, untranslated, unavailable, and error states.
- [ ] Implement semantic research graph Phase 1.
- [ ] Add optional enhanced graph only after Phase 1 acceptance.
- [ ] Add SEO, sitemap, robots, canonical, and hreflang output.

## R5 — Admin foundation

- [ ] Scaffold React 19, TypeScript 5.9, and Vite.
- [ ] Configure routing and guarded layouts.
- [ ] Implement session and CSRF client behavior.
- [ ] Generate or validate the admin API client.
- [ ] Build admin design tokens and primitives.
- [ ] Implement accessible form controls and validation summaries.
- [ ] Implement permission-aware navigation.
- [ ] Implement global loading, error, unauthorized, and forbidden states.
- [ ] Add unit, component, and browser test infrastructure.

## R6 — Admin workflows

- [ ] Implement dashboard health and release status.
- [ ] Implement profile and site settings.
- [ ] Implement articles and series.
- [ ] Implement research, publications, and projects.
- [ ] Implement books, talks, downloads, courses, and creative work.
- [ ] Implement media upload, metadata, and selection.
- [ ] Implement Home composition.
- [ ] Implement timeline editing.
- [ ] Implement graph version, node, group, and edge editing.
- [ ] Implement preview-share workflow.
- [ ] Implement revision history and restore.
- [ ] Implement schedule, publish, archive, and bulk actions.
- [ ] Verify server permissions for every state-changing action.

## R7 — Integrated staging

- [ ] Build three immutable staging artifacts.
- [ ] Run backend migrations in staging.
- [ ] Deploy backend, admin, and public site independently.
- [ ] Verify CORS, cookies, CSRF, proxy headers, and media URLs.
- [ ] Run published-content and draft-leak smoke tests.
- [ ] Run preview-token expiry and authorization tests.
- [ ] Run contact delivery tests with the staging provider.
- [ ] Run a staging backup and isolated restore.

## R8 — Quality closure

- [ ] Run six-width, two-locale, two-theme public visual matrix.
- [ ] Run real 200 percent zoom checks.
- [ ] Run keyboard and screen-reader checks.
- [ ] Run automated accessibility checks.
- [ ] Meet public performance budgets.
- [ ] Run admin browser and form-error matrices.
- [ ] Run dependency and secret scans.
- [ ] Resolve or explicitly defer every finding.
- [ ] Obtain owner visual and content acceptance.

## R9 — Production

- [ ] Tag exact release commits in all three repositories.
- [ ] Record artifact hashes.
- [ ] Apply production migrations with rollback preparation.
- [ ] Deploy backend, admin, and public site.
- [ ] Run production smoke tests.
- [ ] Verify monitoring and backups.
- [ ] Record owner production acceptance.
