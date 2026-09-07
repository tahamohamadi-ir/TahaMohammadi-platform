# Master Roadmap

<!-- PRODUCT-V2.1 -->
Current product/implementation authority: ADR-0010, `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` and `Docs/05-delivery/concept-alignment-v2/EXECUTION.md` (coordination-root paths). Keep Astro/TypeScript with bounded Three.js/GSAP, existing React admin/Django backend, Pagefind and first-party aggregate analytics. Earlier stack/phase assumptions apply only where compatible. Rebuild jobs/edge invalidation are a planned interface, not an already operating deployment.
<!-- /PRODUCT-V2.1 -->

Goal: Deliver three production-ready repositories without importing the broken legacy frontend.

## Phase 0 — Workspace foundation

Outcome: Repositories, authority, references, and migration evidence are stable.

Gate: `R0-FOUNDATION`.

## Phase 1 — Backend migration baseline

Outcome: Migrated Django code installs, tests, migrates, and exposes documented OpenAPI.

Gate: `R1-BACKEND-BASELINE`.

## Phase 2 — Shared contracts

Outcome: Public and admin consumers use validated API, auth, locale, media, and error contracts.

Gate: `R2-CONTRACTS`.

## Phase 3 — Public design foundation

Outcome: Tokens, fonts, primitives, shell, themes, and local Visual Atlas pass browser checks.

Gate: `R3-PUBLIC-DESIGN-SYSTEM`.

## Phase 4 — Public page families

Outcome: Every public route uses a shared template and honest content states.

Gate: `R4-PUBLIC-FEATURES`.

## Phase 5 — Admin foundation

Outcome: Authentication, routing, API client, design system, forms, and permissions are stable.

Gate: `R5-ADMIN-FOUNDATION`.

## Phase 6 — Admin workflows

Outcome: Content, media, home, timeline, graph, preview, revision, and publishing workflows pass integration tests.

Gate: `R6-ADMIN-WORKFLOWS`.

## Phase 7 — Integrated staging

Outcome: Three builds run together against staging data without cross-repository path coupling.

Gate: `R7-STAGING`.

## Phase 8 — Quality and security closure

Outcome: Accessibility, performance, security, backup, restore, and browser matrices pass.

Gate: `R8-QUALITY`.

## Phase 9 — Production release

Outcome: Versioned releases deploy with rollback evidence and owner acceptance.

Gate: `R9-PRODUCTION`.
