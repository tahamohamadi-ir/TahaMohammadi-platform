# Frontend Reference Authority Consolidation Design

**Status:** Owner-approved design, pending implementation-plan review and execution

**Date:** 2026-08-29

**Workspace:** `D:\Project\tahamohammadi-platform`
**Owner instruction:** Retain `Front-End\Assets` as the local incoming source, create one curated and deduplicated tracked authority, remove verified duplicates, and use `concepts/` plus `concepts/page-families/` as the UI/UX basis.

## 1. Goal

Create one coherent frontend reference system that agents can use without path guessing, duplicate-file drift, historical-runtime assumptions, or accidental publication of unapproved material. The result must preserve owner inputs, promote only classified files, prove every destructive cleanup by SHA-256, and leave all pre-scaffold decisions explicit in canonical documents and task lists.

## 2. Current evidence

- `Front-End\Assets` contains 172 files, 174,809,510 bytes, and 105 unique SHA-256 values.
- The incoming package contains 33 duplicate-hash groups.
- `Docs\references\site-redesign` contains 166 files and 100 unique hashes.
- Six incoming hashes absent from `site-redesign` already exist byte-identically under `Docs\references\legacy-planning`.
- One `site-redesign` README hash is not present in the incoming package and must remain as migration evidence until supersession is recorded.
- `Front-End\Assets\agent-kit\validate.mjs` currently fails because it resolves the obsolete `Assets/site-redesign/implementation-reference/...` layout.
- All seven JSON files in the incoming package parse successfully.
- `concepts/` is the owner-selected UI/UX source. `concepts/page-families/` is the owner-selected page-family detail source.
- `others/` contains both byte-identical generated copies and unique unmanaged evidence. It is not implementation authority.
- The workspace root is dirty only because `Front-End/` includes the untracked incoming Assets tree; all three product repositories are otherwise clean.

## 3. Authority model

Authority is divided by responsibility rather than by accidental directory age.

| Layer | Canonical role | Publication/runtime authority |
|---|---|---|
| `Front-End\Assets` | Local owner-provided incoming source and recoverable comparison set | No |
| `Docs\references\frontend-design-authority` | Tracked, curated, deduplicated visual and machine-readable reference | Reference authority only |
| `Docs\04-design` | Accepted written UI/UX, asset, token, page-family, and QA contracts | Yes, for frontend design requirements |
| `Docs\03-contracts` | Accepted API, authentication, locale, media, and error compatibility contracts | Yes, for cross-repository interfaces |
| Product-repository source and tests | Implemented behavior after scaffold | Yes, only after verified implementation |
| `Docs\references\legacy-planning` | Historical planning evidence | No |
| retired `Docs\references\site-redesign` records | Migration evidence and supersession pointers | No |

The tracked reference does not authorize biography, claims, links, publication status, translations, rights, or release status. Those remain controlled by owner-approved content manifests and backend publication projections.

## 4. Target tracked reference tree

The canonical tracked tree will be:

```text
Docs/references/frontend-design-authority/
├── README.md
├── AUTHORITY-MANIFEST.json
├── SHA256SUMS.txt
├── ALIASES.json
├── design-dna.json
├── concepts/
│   ├── home-dark-concept-v3-final.png
│   ├── home-light-concept-v3-final.png
│   ├── home-mobile-fa-light-concept-v1.png
│   ├── language-gateway-dark-concept-v1.png
│   ├── blog-detail-fa-light-concept-v1.png
│   ├── project-detail-fa-dark-concept-v1.png
│   ├── admin-graph-editor-dark-concept-v1.png
│   ├── variants/
│   │   ├── home-dark-safe-reference.png
│   │   └── home-light-alternate-reference.png
│   └── page-families/
│       ├── creative-index-light.png
│       ├── creative-detail-dark.png
│       ├── writing-index-light.png
│       ├── projects-index-dark.png
│       ├── research-publications-index-light.png
│       ├── teaching-index-dark.png
│       ├── about-cv-light.png
│       └── contact-dark.png
├── art/
│   ├── blog-coral-stairs.png
│   ├── gallery-ivory-forms.png
│   ├── learning-sage-library.png
│   ├── portal-centered-dark.png
│   ├── portal-centered-light.png
│   ├── portal-orbit-dark.png
│   ├── portal-orbit-light.png
│   ├── project-dashboard-systems.png
│   ├── project-data-architecture.png
│   ├── project-placeholder-ivory-stairs.png
│   └── project-visual-communication-network.png
├── brand/
│   ├── taha-mark-favicon.png
│   ├── taha-mark-primary.png
│   └── SOURCE-NOTE.md
├── agent-kit/
│   ├── README.md
│   ├── assets.json
│   ├── components.json
│   ├── templates.json
│   ├── tokens.json
│   ├── validate.mjs
│   └── figma-plugin/
│       ├── README.md
│       ├── manifest.json
│       └── code.js
└── provenance/
    ├── ASSET-MANIFEST.md
    ├── PROMPTS.md
    ├── SOURCE-INVENTORY.md
    ├── PRODUCTION-REGISTER.md
    └── MIGRATION-REPORT.md
```

No two files in this tree may have the same SHA-256 unless a format itself requires byte-identical test fixtures and the exception is explicitly recorded in `AUTHORITY-MANIFEST.json`. Semantic aliases are stored in `ALIASES.json` instead of duplicating bytes.

## 5. Local incoming tree after consolidation

`Front-End\Assets` remains local and is excluded explicitly by the root `.gitignore`. It is reorganized only after the tracked authority passes validation.

```text
Front-End/Assets/
├── README.md
├── INCOMING-SHA256SUMS.txt
├── concepts/          # one local source copy per unique visual hash
├── art/               # one local source copy per unique art hash
├── brand/             # one local source copy per unique brand hash
├── agent-kit/         # original source package, paths marked historical
├── provenance/        # original package documents
└── archive/
    └── unmanaged-unique/  # only unique non-authoritative evidence from others/
```

The nested mirror `Front-End\Assets\assets` is removed after every file is proven present by hash in the tracked authority or retained local archive. Byte-identical `others/exec-*.png` copies are removed after the same proof. Unique `others/` files are moved to `archive/unmanaged-unique/`; they are never silently deleted or promoted.

## 6. Deduplication and destructive-action protocol

Deletion is authorized only for verified duplicates and follows this sequence:

1. Record every incoming path, byte count, dimensions where applicable, and SHA-256.
2. Classify every file as `promote`, `alias`, `history`, `unmanaged-unique`, or `verified-duplicate`.
3. Copy or move one canonical byte source into the tracked authority.
4. Generate canonical `SHA256SUMS.txt`, `AUTHORITY-MANIFEST.json`, and `ALIASES.json`.
5. Validate file count, expected semantic IDs, JSON syntax, image dimensions, and SHA-256.
6. Prove every deletion candidate has a same-hash retained path.
7. Produce `provenance/MIGRATION-REPORT.md` with before/after counts and a deleted-path-to-retained-path map.
8. Remove only the proven duplicate paths.
9. Re-run the full manifest verifier and Git diff review.

A missing retained path, mismatched hash, ambiguous owner role, or unique hash stops deletion for that file. No wildcard recursive deletion is permitted.

## 7. UI/UX interpretation contract

### 7.1 Visual hierarchy

- `concepts/home-light-concept-v3-final.png` defines Light Editorial composition, spacing rhythm, airy surface treatment, navy typography, turquoise action, and restrained gold signature.
- `concepts/home-dark-concept-v3-final.png` defines Dark Scientific Atlas composition, depth, graph language, deep navy surfaces, warm ivory type, turquoise identity/action, and restrained contextual accents.
- Light and Dark themes share content order, component anatomy, semantics, and route meaning.
- `concepts/home-mobile-fa-light-concept-v1.png` defines RTL narrow-screen recomposition, not copy or factual content.
- `concepts/language-gateway-dark-concept-v1.png` defines the separate gateway art direction.
- Generated text visible inside raster concepts is never content authority.

### 7.2 Page-family authority

| ID | Canonical visual | Required implementation family |
|---|---|---|
| PF-01 | `creative-index-light.png` | Creative/Gallery collection index |
| PF-02 | `creative-detail-dark.png` | Visual/evidence detail |
| PF-03 | `writing-index-light.png` | Writing/Blog editorial index |
| PF-04 | `projects-index-dark.png` | Sanitized projects collection index |
| PF-05 | `research-publications-index-light.png` | Research and Publications index |
| PF-06 | `teaching-index-dark.png` | Teaching/Learning index |
| PF-07 | `about-cv-light.png` | About, profile, experience, and CV family |
| PF-08 | `contact-dark.png` | Contact and collaboration family |

Each family contract must record layout regions, component roles, responsive recomposition, RTL behavior, content-state behavior, CMS-field dependencies, approved media roles, and representative visual-regression viewports. A concept is never sliced into controls or treated as pixel-exact content copy.

### 7.3 Design DNA

`design-dna.json` must populate every field in the local Design DNA schema across:

- measurable design system: colors, typography, spacing, grid, shapes, elevation, icons, motion, and components;
- qualitative design style: mood, visual metaphor, composition, imagery, interaction feel, and UI voice;
- visual effects: background atmosphere, graph/particle behavior, 2D-first interaction, optional 3D phase, glass limits, reduced-motion behavior, performance tier, and static fallbacks.

The file must distinguish exact values inherited from `agent-kit/tokens.json` from visual estimates inferred from raster references.

## 8. Machine-readable agent kit corrections

- Rebase all asset paths to `Docs/references/frontend-design-authority/...` or paths relative to the agent-kit directory.
- Remove references to the old `apps/web` runtime and old `docs/contracts` locations.
- Set both Light and Dark token sets to `design-approved` until the greenfield public runtime implements and verifies them; neither is currently runtime-authoritative.
- Preserve 24 component definitions and six template definitions unless a separately accepted contract change alters the counts.
- Add schema/version fields and a workspace-relative authority identifier.
- Make `validate.mjs` location-independent by deriving the authority root from its own file URL.
- Validate canonical asset existence, hash, alias resolution, duplicate hashes, required files, component/template counts, and offline Figma-plugin policy.
- Treat Figma output as optional documentation, never runtime or content authority.

## 9. Canonical documents to create

| File | Responsibility |
|---|---|
| `Docs/04-design/DESIGN-DNA.md` | Human-readable interpretation of the machine Design DNA |
| `Docs/04-design/PAGE-FAMILY-UI-UX-CONTRACT.md` | Exact PF-01 through PF-08 implementation and QA requirements |
| `Docs/04-design/ASSET-PROMOTION-LEDGER.md` | Asset ID, source hash, role, route, rights, owner approval, alt/caption, crop, derivatives, and publication state |
| `Docs/04-design/FONT-ACQUISITION-PLAN.md` | Font source, license, weights, subsets, formats, preload policy, and acceptance tests |
| `Docs/02-architecture/ROUTE-REGISTRY.md` | Canonical locale routes, slugs, aliases, redirects, canonical URLs, and hreflang rules |
| `Docs/02-architecture/DEPLOYMENT-TOPOLOGY.md` | Public, admin, backend, media, proxy, cookie, CORS, and CSRF origin model |
| `Docs/03-contracts/ERROR-COMPATIBILITY-MATRIX.md` | Actual current backend error shapes plus target normalization and client behavior |
| `Docs/01-product/OWNER-CONTENT-MANIFEST.md` | Owner-approved facts, links, documents, translations, source paths, hashes, and publication status |
| `Docs/03-contracts/OPENAPI-ARTIFACT-CONTRACT.md` | Public/admin schema export, secure admin fixture, versioning, generated types, and compatibility gates |
| `Docs/06-quality/CI-REQUIRED-CHECKS.md` | Required checks per repository before merge and release |
| `Docs/10-tracking/PRE-SCAFFOLD-READINESS.md` | Single pass/fail ledger for every prerequisite in this specification |

## 10. Existing documents to reconcile

### 10.1 Workspace governance and architecture

- `PROJECT-MANIFEST.md`: replace the old design-reference source with the incoming/canonical two-layer model.
- `AGENTS.md`: add the new authority read order and ban direct reads from local incoming assets during normal agent work.
- `.gitignore`: ignore only `/Front-End/Assets/`; keep both child repositories independently ignored as before.
- `Docs/00-governance/AUTHORITY-ORDER.md`: name the tracked design authority and define raster-versus-written-contract conflict handling.
- `Docs/00-governance/DOCUMENT-OWNERSHIP.md`: assign owners for the new design, content, route, topology, OpenAPI, and readiness files.
- `Docs/02-architecture/{SYSTEM-ARCHITECTURE,REPOSITORY-BOUNDARIES,ENVIRONMENT-MATRIX,DATA-FLOW}.md`: align the three-repository data and deployment model.

### 10.2 Contracts and design

- Replace the unconditional claim in `Docs/03-contracts/ERROR-CONTRACT.md` with current-versus-target status and a link to the compatibility matrix.
- Reconcile `API-CONTRACT.md`, `AUTH-CONTRACT.md`, `CONTENT-CONTRACT.md`, `LOCALE-CONTRACT.md`, and `MEDIA-CONTRACT.md` with accepted snapshots and pre-scaffold gates.
- Rewrite `ASSET-REGISTER.md`, `DESIGN-AUTHORITY.md`, `DESIGN-SYSTEM-SPEC.md`, `PAGE-FAMILY-MATRIX.md`, `RESPONSIVE-RTL-SPEC.md`, `CONTENT-STATE-MATRIX.md`, and `VISUAL-QA-CONTRACT.md` to reference the new tracked authority.
- Preserve the rule that concepts define composition and visual language but never factual content.

### 10.3 Delivery, migration, quality, and operations

- Expand `MASTER-ROADMAP.md`, `MASTER-TASK-LIST.md`, `DEPENDENCY-MAP.md`, `MILESTONES.md`, and `RELEASE-GATES.md` with explicit authority-consolidation and pre-scaffold gates.
- Replace `ASSET-MIGRATION-MANIFEST.md` with the hash-guarded migration model in this specification.
- Reconcile `SOURCE-INVENTORY.md`, `CONTENT-MIGRATION-MANIFEST.md`, and `LEGACY-REJECTION-LIST.md`.
- Close stale `DEF-001` with the recorded 636-test backend baseline; do not close PostgreSQL or staging validations without execution evidence.
- Add CI, font, content, OpenAPI, deployment-topology, and asset-rights risks to tracking registers.
- Expand environment and deployment runbooks only to the accepted topology; do not invent production credentials or hosts.

## 11. Product-repository reconciliation

### 11.1 Public site

Update `AGENTS.md`, `PROJECT-MANIFEST.md`, `README.md`, `ROADMAP.md`, `TASK-LIST.md`, and owned design/contract/quality documents so the repository:

- reads the new Design Authority, Design DNA, page-family contract, route registry, and content manifest before scaffold work;
- consumes tracked reference assets only;
- records PF-01 through PF-08 adoption packets and their exact tests;
- keeps Astro as the static-first shell and React as bounded interactive islands;
- requires no-JS-readable public content, semantic graph/list parity, RTL/LTR parity, and honest unavailable states;
- blocks runtime asset copying until promotion-ledger approval;
- blocks route scaffolding until the route registry passes;
- blocks API client generation until accepted OpenAPI artifacts exist;
- blocks font activation until license, subset, and local font files pass.

### 11.2 Admin panel

Update `AGENTS.md`, `PROJECT-MANIFEST.md`, `README.md`, `ROADMAP.md`, `TASK-LIST.md`, and owned architecture/design/contract/quality documents so the repository:

- uses the admin graph concept only as behavioral and visual reference;
- maps every workflow to endpoint, method, permission, lifecycle state, errors, audit behavior, and acceptance evidence;
- blocks auth implementation until session, cookie, CSRF, MFA, timeout, and re-authentication behavior is frozen;
- blocks typed-client generation until authenticated admin OpenAPI export is accepted;
- preserves unsaved changes and exposes validation, permission, conflict, rate-limit, and network states;
- never treats hidden controls as server authorization.

### 11.3 Backend

Update `TASK-LIST.md` and owned contract/operation documents so the repository:

- exports versioned public and authenticated-admin OpenAPI snapshots;
- inventories actual response and error shapes before normalization;
- defines backward-compatible error-envelope adoption rather than claiming it already exists;
- fixes the local environment profile discrepancy between `.env.example` and `config/settings/local.py`;
- records the selected same-origin/reverse-proxy or explicit cross-origin topology;
- supplies consumer fixtures and compatibility tests for both frontends;
- retains the 636-test baseline as evidence but keeps PostgreSQL migration and health checks open until actually run.

## 12. Pre-scaffold gates

Frontend scaffold work may start only when all mandatory gates below pass:

| Gate | Required evidence |
|---|---|
| PS-01 Authority | New tracked authority validates; old authority is marked superseded; no stale active references remain |
| PS-02 Deduplication | Canonical authority has no unapproved duplicate hashes; every removed path maps to a retained hash-identical path |
| PS-03 Design | Design DNA, tokens, PF-01..PF-08, responsive/RTL, content states, and visual QA contracts agree |
| PS-04 Routes | Locale route registry, slugs, redirects, canonical, and hreflang rules are accepted |
| PS-05 API | Public/admin OpenAPI artifacts and endpoint inventory are versioned and accepted |
| PS-06 Errors | Current backend shapes and target error behavior are documented for both clients |
| PS-07 Auth/topology | Host topology, session, cookies, CSRF, CORS, MFA, and proxy behavior are accepted |
| PS-08 Content | Owner content manifest distinguishes approved, missing, private, translated, and unavailable values |
| PS-09 Media | Promotion ledger records rights, owner approval, alt/caption, crop, derivatives, and publication eligibility |
| PS-10 Fonts | Four font sources, OFL notices, subsets, WOFF2 files, fallback metrics, and preload policy are accepted |
| PS-11 CI | Required workflows/check names are documented for all three repositories |
| PS-12 Tracking | Central and repository task lists, risks, deferrals, dependencies, and release gates agree |

PS-05 through PS-11 may be recorded as explicit blockers, but public/admin runtime scaffolding must not claim those dependent slices ready until their gates pass.

## 13. Validation

Implementation of this design must produce and pass:

- pre/post file counts, unique-hash counts, byte totals, and deletion mapping;
- zero missing manifest paths;
- zero unexpected SHA-256 mismatches;
- zero unapproved duplicate hashes in the tracked authority;
- all JSON parsed and schema/version fields present;
- agent-kit validator pass from both workspace root and its own directory;
- zero active references to `Assets/site-redesign` or the retired authority path outside historical files;
- zero broken relative Markdown links in authoritative documents;
- zero placeholder markers such as `TBD` in accepted contracts;
- task-ID uniqueness and dependency validity across central/public/admin/backend lists;
- root Git status free of untracked `Front-End/Assets` noise after the explicit ignore rule;
- all product repositories unchanged unless their owned documentation is intentionally reconciled and separately committed;
- exact changed-file and deletion review before each commit.

## 14. Commit and rollback boundaries

The work is split into independently reviewable commits:

1. Root design specification and implementation plan.
2. New tracked authority copied and validated; no deletion yet.
3. Canonical design/contracts/tracking documentation reconciliation.
4. Public-site documentation reconciliation.
5. Admin-panel documentation reconciliation.
6. Backend documentation reconciliation.
7. Verified duplicate cleanup and old-authority retirement.
8. Final cross-repository validation evidence.

Until commit 2 validates, rollback is removal of only the newly added tracked authority. During cleanup, every deleted untracked duplicate must remain recoverable from a same-hash canonical file. Git-tracked old authority removal remains recoverable from its parent commit.

## 15. Explicit non-goals

- No public or admin runtime scaffold is created in this documentation/consolidation phase.
- No backend behavior, endpoint, migration, authentication, or deployment code is changed.
- No owner content, route slug, API field, URL, claim, translation, right, or approval is invented.
- No image is regenerated, edited, color-corrected, or sliced.
- No font binary is downloaded before its source and license gate is accepted.
- No production or staging deployment is authorized.

## 16. Acceptance criteria

This design is complete only when:

1. the owner-approved `concepts` and `page-families` roles are explicit;
2. one tracked curated authority exists with no accidental byte duplicates;
3. local incoming evidence remains available without dirtying root Git;
4. every removed duplicate is hash-proven recoverable;
5. unique unmanaged evidence is retained outside authority;
6. all stale paths and old-runtime authority claims are removed from active documents;
7. all pre-scaffold contracts and blocker states are explicit;
8. central and repository task lists cover every gate and agree on dependencies;
9. validators, links, manifests, JSON, hashes, and Git scopes pass;
10. no runtime scaffold or release-readiness claim is made prematurely.
