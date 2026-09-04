# Master Task List

Status markers: `[x]` verified complete, `[ ]` not complete.

**Detailed parallel execution:** `MULTI-AGENT-TASK-BOARD.md` (task IDs, dependencies, multi-agent lanes).  
**Per-repository detail:** `Back-End/TASK-LIST.md`, `Front-End/public-site/TASK-LIST.md`, `Front-End/admin-panel/TASK-LIST.md`.

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
- [x] Write and approve the frontend reference consolidation design.
- [x] Create and validate the curated tracked frontend design authority.

## PS — Mandatory pre-scaffold readiness

- [x] PS-01: Establish the tracked frontend design authority and agent-kit validator.
- [x] PS-02: Remove 65 hash-proven local duplicates, preserve 30 unique local files, and retire the old authority after stale-reference check.
- [x] PS-03: Publish Design DNA and PF-01 through PF-08 UI/UX contracts.
- [x] PS-04: Publish locale route registry and redirect rule.
- [x] PS-05a: Export source-generated public/admin OpenAPI review snapshots with commit, hash, and path-count provenance.
- [x] PS-05b: Verify anonymous-public and verified-staff-plus-OTP endpoint access with disposable test fixtures.
- [x] PS-05c: Review the route/workflow coverage of the source snapshot and record every canonicalization or ownership decision.
- [x] PS-05d: Accept the resolved OpenAPI artifacts for scaffold foundation with exact schema hashes and access-test evidence.
- [x] PS-06: Publish current-versus-target error compatibility matrix.
- [x] PS-07: Accept same-origin reverse-proxy, cookie, CSRF, and MFA topology baseline.
- [ ] PS-08: Seed v1.1 imported to backend (`import_content_seed`; 85 draft records); per-record production approval still open.
- [ ] PS-09: Approve runtime media promotion ledger records.
- [ ] PS-10: Acquire, license, subset, and test four self-hosted font families.
- [ ] PS-11: Implement documented CI checks and branch protection (see `MULTI-AGENT-TASK-BOARD.md` COORD-030).
- [x] PS-12: Reconcile central readiness, risk, and deferred-validation tracking.

## R1 — Backend baseline

- [ ] Review `Infra/legacy-monorepo` and classify each file.
- [x] Create a Python 3.12 virtual environment with `uv`.
- [x] Install the locked backend dependencies.
- [x] Run Ruff without modifying migrations; all checks pass.
- [x] Run the full pytest suite; 636 tests pass.
- [x] Record the migrated test baseline; no failures occurred.
- [x] Start the backend with development settings.
- [x] Verify `/health/` against a local PostgreSQL database.
- [x] Apply all migrations to an empty PostgreSQL database.
- [x] Export the current public OpenAPI schema (PS-05; `Back-End/docs/contracts/openapi/current/public-openapi.json`).
- [x] Export the current admin OpenAPI schema (PS-05; `Back-End/docs/contracts/openapi/current/admin-openapi.json`).
- [x] Generate an endpoint inventory from source and OpenAPI (PS-05; `endpoint-inventory.md`).
- [x] Reconcile `.env.example` with Docker-local and standalone-local database profiles.
- [ ] Confirm same-origin reverse-proxy routing in disposable local/staging browser checks.
- [ ] Remove legacy SPA-serving responsibility from backend only after admin cutover.
- [ ] Rewrite active backend container and deployment files for the new repository paths.

## R2 — Shared contracts

- [ ] Normalize new stable endpoints under `/api/v1/` with compatibility decisions.
- [ ] Freeze the public published-projection schema.
- [ ] Freeze the admin authentication and CSRF behavior.
- [ ] Freeze the error envelope.
- [ ] Freeze media identifiers and rendition fields.
- [ ] Freeze locale and untranslated-content behavior.
- [x] Generate TypeScript API types from accepted OpenAPI (public-site + admin-panel; hash drift guard active — see WORK-LOG).
- [ ] Add backend schema compatibility tests.
- [ ] Add public-site contract fixtures.
- [ ] Add admin-panel contract fixtures.
- [ ] Add response-shape compatibility fixtures for current public, admin, and contact error forms.

## R3 — Public design foundation

- [x] Scaffold Astro 7 and TypeScript 5.9.
- [x] Configure Tailwind CSS 4 with a verified processing pipeline.
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
- [ ] Implement only assets whose promotion-ledger rows are owner-approved.

## R4 — Public page families

- [x] Implement the language gateway.
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
- [ ] Adopt PF-01 through PF-08 with matching visual, RTL, state, and no-JS evidence.

## R5 — Admin foundation

- [x] Scaffold React 19, TypeScript 5.9, and Vite.
- [x] Configure routing and guarded layouts.
- [x] Implement session and CSRF client behavior.
- [x] Generate or validate the admin API client.
- [x] Build admin design tokens and primitives.
- [x] Implement accessible form controls and validation summaries.
- [x] Implement permission-aware navigation.
- [x] Implement global loading, error, unauthorized, and forbidden states.
- [ ] Add unit, component, and browser test infrastructure.

## R6 — Admin workflows

- [x] Implement dashboard health (release status still open).
- [x] Implement profile and site settings.
- [x] Implement articles and series.
- [x] Implement research, publications, and projects.
- [x] Implement books, talks, downloads, courses, and creative work.
- [x] Implement media upload, metadata, and selection.
- [ ] Implement Home composition.
- [ ] Implement timeline editing.
- [ ] Implement graph version, node, group, and edge editing.
- [ ] Implement preview-share workflow.
- [x] Implement revision history and restore.
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
