# Frontend Reference Authority Consolidation Implementation Plan

> **For agentic workers:** Execute this plan in the listed order. Every step uses checkbox syntax and produces evidence before the next destructive step.

**Goal:** Replace the duplicate legacy design-reference layout with one curated tracked frontend authority while retaining a hash-registered local incoming source, then align all pre-scaffold documentation and task registers.

**Architecture:** `Front-End/Assets` remains an ignored local owner-input set. `Docs/references/frontend-design-authority` becomes the only tracked design-reference source for agents, containing one canonical byte copy for each promoted visual or machine contract. Central contracts define adoption requirements; each product repository owns its own implementation backlog and agent read order.

**Tech Stack:** Markdown, JSON, SHA-256, PowerShell, Git, Node.js validator, Astro 7 planning baseline, React 19/Vite planning baseline, Django Ninja/OpenAPI planning baseline.

**Spec:** `Docs/superpowers/specs/2026-08-29-frontend-reference-authority-consolidation-design.md`

## Global Constraints

- Treat `concepts/` as the visual UI/UX source and `concepts/page-families/` as the route-family detail source.
- Never use raster concept copy as owner-approved content.
- Remove only a file whose retained hash-identical canonical path is recorded first.
- Preserve unique `others/` evidence under a non-authoritative archive.
- Do not scaffold either frontend or change backend behavior in this plan.
- Do not invent routes, API fields, credentials, owner facts, translations, rights, or production state.
- Keep product repositories independent; commit exact repository scope only.

---

### Task 1: Capture the pre-migration asset baseline

**Files:**
- Create: `Docs/references/frontend-design-authority/provenance/MIGRATION-REPORT.md`
- Create: `Docs/references/frontend-design-authority/provenance/INCOMING-INVENTORY.json`
- Create: `Docs/references/frontend-design-authority/provenance/DELETION-MAP.json`

**Consumes:** `Front-End/Assets/**` and `Docs/references/site-redesign/**`.

**Produces:** Complete before-state file inventory, classification, and one-to-one deletion map.

- [ ] **Step 1: Hash every incoming file and record its relative path, byte count, extension, image dimensions where applicable, and SHA-256.**

  Run:

  ```powershell
  Get-ChildItem 'D:\Project\tahamohammadi-platform\Front-End\Assets' -Recurse -File |
    ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 }
  ```

- [ ] **Step 2: Classify every hash as `promote`, `alias`, `history`, `unmanaged-unique`, or `verified-duplicate`.**

- [ ] **Step 3: Assert that every `verified-duplicate` has one retained canonical relative path before any deletion command is permitted.**

  Expected: zero deletion-map rows with an empty `retained_path`.

- [ ] **Step 4: Record the observed counts and byte totals in `MIGRATION-REPORT.md`.**

- [ ] **Step 5: Commit the baseline only after JSON parses and the deletion map is complete.**

### Task 2: Build the curated tracked authority without deletion

**Files:**
- Create: `Docs/references/frontend-design-authority/{README.md,AUTHORITY-MANIFEST.json,SHA256SUMS.txt,ALIASES.json,design-dna.json}`
- Create: curated `concepts/**`, `art/**`, `brand/**`, `agent-kit/**`, and `provenance/**` files specified by the design spec.

**Consumes:** Task 1 inventory and the exact local incoming files.

**Produces:** A deduplicated tracked authority that is complete before old references or local duplicates change.

- [ ] **Step 1: Copy one canonical file for each promoted hash into the target tree; do not copy alias duplicates.**

- [ ] **Step 2: Write `ALIASES.json` for requested byte-identical names such as final-reference aliases.**

- [ ] **Step 3: Generate `SHA256SUMS.txt` from canonical files and record all semantic asset IDs in `AUTHORITY-MANIFEST.json`.**

- [ ] **Step 4: Rebase `agent-kit/assets.json` and `validate.mjs` to the new root; set token status to `design-approved`, not runtime-authoritative.**

- [ ] **Step 5: Verify canonical files, JSON, aliases, hash uniqueness, component count 24, template count 6, and Figma offline policy.**

  Run:

  ```powershell
  node 'D:\Project\tahamohammadi-platform\Docs\references\frontend-design-authority\agent-kit\validate.mjs'
  ```

- [ ] **Step 6: Commit the authority addition before any old-reference or local duplicate cleanup.**

### Task 3: Document the design and page-family contracts

**Files:**
- Create: `Docs/04-design/{DESIGN-DNA.md,PAGE-FAMILY-UI-UX-CONTRACT.md,ASSET-PROMOTION-LEDGER.md,FONT-ACQUISITION-PLAN.md}`
- Modify: `Docs/04-design/{ASSET-REGISTER.md,DESIGN-AUTHORITY.md,DESIGN-SYSTEM-SPEC.md,PAGE-FAMILY-MATRIX.md,RESPONSIVE-RTL-SPEC.md,CONTENT-STATE-MATRIX.md,VISUAL-QA-CONTRACT.md}`

**Consumes:** Task 2 authority, observed concepts, PF-01 through PF-08, and existing central contracts.

**Produces:** One human-readable design source with no direct dependence on the local incoming tree.

- [ ] **Step 1: Write every Design DNA field with a source category: exact token, visual inference, or deferred runtime behavior.**

- [ ] **Step 2: Map PF-01 through PF-08 to page families, responsive and RTL rules, required states, media roles, and visual-regression matrix.**

- [ ] **Step 3: Add a promotion-ledger row for each runtime candidate with source hash, rights status, owner approval state, alt/caption requirement, crop/focal rule, and derivative state.**

- [ ] **Step 4: Define the four-font acquisition gate without downloading a font binary.**

- [ ] **Step 5: Verify all active design-document links resolve to the new tracked authority.**

### Task 4: Resolve pre-scaffold contracts and topology

**Files:**
- Create: `Docs/02-architecture/{ROUTE-REGISTRY.md,DEPLOYMENT-TOPOLOGY.md}`
- Create: `Docs/03-contracts/{ERROR-COMPATIBILITY-MATRIX.md,OPENAPI-ARTIFACT-CONTRACT.md}`
- Create: `Docs/01-product/OWNER-CONTENT-MANIFEST.md`
- Modify: `Docs/02-architecture/{SYSTEM-ARCHITECTURE.md,REPOSITORY-BOUNDARIES.md,ENVIRONMENT-MATRIX.md,DATA-FLOW.md}`
- Modify: `Docs/03-contracts/{API-CONTRACT.md,AUTH-CONTRACT.md,CONTENT-CONTRACT.md,ERROR-CONTRACT.md,LOCALE-CONTRACT.md,MEDIA-CONTRACT.md}`

**Consumes:** Current backend source and tests plus the tracked design authority.

**Produces:** Honest current-versus-target contract states and blockers that frontends can consume without invention.

- [ ] **Step 1: Replace the error-envelope assertion with a current-shape matrix and a target-normalization gate.**

- [ ] **Step 2: Register locale route families and state that slugs/redirects require owner acceptance before implementation.**

- [ ] **Step 3: Define same-origin reverse-proxy deployment as the planned topology until a separately accepted CORS/cookie design replaces it.**

- [ ] **Step 4: Define public/admin OpenAPI export, authenticated admin fixture, versioning, generated types, and compatibility checks.**

- [ ] **Step 5: Create the owner content manifest with explicit `approved`, `unavailable`, `private`, and `needs-owner-input` states.**

### Task 5: Reconcile governance, tracking, delivery, and operations

**Files:**
- Modify: `PROJECT-MANIFEST.md`, `AGENTS.md`, `.gitignore`
- Modify: `Docs/00-governance/{AUTHORITY-ORDER.md,DOCUMENT-OWNERSHIP.md,CHANGE-PROCESS.md,DEFINITION-OF-DONE.md}`
- Modify: `Docs/05-delivery/{MASTER-ROADMAP.md,MASTER-TASK-LIST.md,DEPENDENCY-MAP.md,MILESTONES.md,RELEASE-GATES.md}`
- Modify: `Docs/06-quality/{TEST-STRATEGY.md,SECURITY-BASELINE.md,ACCESSIBILITY-PLAN.md,PERFORMANCE-BUDGET.md}`
- Modify: `Docs/07-migration/{ASSET-MIGRATION-MANIFEST.md,SOURCE-INVENTORY.md,CONTENT-MIGRATION-MANIFEST.md,LEGACY-REJECTION-LIST.md}`
- Modify: `Docs/08-operations/{ENVIRONMENT-SETUP.md,LOCAL-DEVELOPMENT.md,DEPLOYMENT-RUNBOOK.md,BACKUP-RESTORE-RUNBOOK.md,INCIDENT-RUNBOOK.md}`
- Modify: `Docs/10-tracking/{DEFERRED-VALIDATION.md,DECISION-LOG.md,RISK-REGISTER.md,DEBT-REGISTER.md,WORK-LOG.md}`
- Create: `Docs/06-quality/CI-REQUIRED-CHECKS.md`, `Docs/10-tracking/PRE-SCAFFOLD-READINESS.md`

**Consumes:** Tasks 2–4.

**Produces:** One dependency-aware delivery system with stale state corrected.

- [ ] **Step 1: Add the tracked authority to governance read order and ignore the local incoming tree.**

- [ ] **Step 2: Replace stale DEF-001 with the recorded 636-test result; retain unrun PostgreSQL and staging validations.**

- [ ] **Step 3: Add PS-01 through PS-12 to roadmap, task list, dependency map, risks, and readiness ledger.**

- [ ] **Step 4: Define required CI checks for each repository without claiming a workflow exists.**

- [ ] **Step 5: Record the approved cleanup and supersession decision with evidence links.**

### Task 6: Reconcile public-site documentation

**Files:**
- Modify: `Front-End/public-site/{AGENTS.md,PROJECT-MANIFEST.md,README.md,ROADMAP.md,TASK-LIST.md,CODEX.md,CLAUDE.md,HERMES.md,OPENCODE.md}`
- Modify: `Front-End/public-site/docs/{architecture/ARCHITECTURE.md,contracts/API-CONSUMER-CONTRACT.md,contracts/CONTENT-AND-LOCALE.md,design/ASSET-PIPELINE.md,design/DESIGN-SYSTEM.md,design/ROUTES-AND-PAGE-FAMILIES.md,quality/ACCESSIBILITY.md,quality/PERFORMANCE.md,quality/TESTING.md,quality/VISUAL-QA.md}`

**Consumes:** Central authority and Tasks 3–5.

**Produces:** A greenfield public-site backlog that cannot begin dependent runtime work prematurely.

- [ ] **Step 1: Add the new authority/read order and block direct use of `Front-End/Assets`.**

- [ ] **Step 2: Add PF-01 through PF-08 implementation packets, visual reference paths, no-JS and locale requirements.**

- [ ] **Step 3: Add explicit gates for routes, OpenAPI, assets, fonts, content, Visual Atlas isolation, and quality matrix.**

- [ ] **Step 4: Validate every relative document link.**

### Task 7: Reconcile admin-panel and backend documentation

**Files:**
- Modify: all owned Markdown documents under `Front-End/admin-panel/` listed in its task and documentation indexes.
- Modify: `Back-End/{AGENTS.md,README.md,ROADMAP.md,TASK-LIST.md,PROJECT-MANIFEST.md,.env.example}` and applicable files under `Back-End/docs/`.

**Consumes:** Central authority and Tasks 3–5.

**Produces:** Complete pre-scaffold admin workflow mapping and backend integration prerequisites.

- [ ] **Step 1: Add an admin workflow-to-endpoint/permission/state/error/acceptance map and graph-editor reference boundary.**

- [ ] **Step 2: Add accepted-error and authenticated-OpenAPI dependencies to the admin client plan.**

- [ ] **Step 3: Split `.env.example` local Docker and standalone database profiles so it cannot contradict `config/settings/local.py`.**

- [ ] **Step 4: Add backend snapshot, consumer fixture, topology, and compatibility work items without asserting completion.**

### Task 8: Retire old authority and clean verified duplicates

**Files:**
- Remove: `Docs/references/site-redesign/**` only after Task 2 validation
- Modify: `Docs/references/legacy-planning/**` only to add supersession pointers if needed
- Remove or move: exact incoming duplicate paths listed in `DELETION-MAP.json`

**Consumes:** Completed Tasks 1–7 and a passing new authority verifier.

**Produces:** One active tracked design authority and a compact local incoming tree.

- [ ] **Step 1: Search authoritative documents and confirm no active reference resolves to `Docs/references/site-redesign`.**

- [ ] **Step 2: Remove the old tracked authority in the same commit that adds the supersession/migration record.**

- [ ] **Step 3: Remove only local paths enumerated as `verified-duplicate`; move only enumerated `unmanaged-unique` files into local archive.**

- [ ] **Step 4: Verify root Git no longer reports `Front-End/Assets` because the local-input ignore is active.**

- [ ] **Step 5: Compare every deletion-map `retained_sha256` against the actual retained canonical file.**

### Task 9: Perform final cross-repository verification

**Files:**
- Modify: `Docs/10-tracking/PRE-SCAFFOLD-READINESS.md`, `Docs/10-tracking/WORK-LOG.md`

**Consumes:** All prior tasks.

**Produces:** Honest per-gate pass, open, or blocked evidence.

- [ ] **Step 1: Run manifest/hash/JSON/agent-kit/link/task-ID checks and capture exact results.**

- [ ] **Step 2: Run `git diff --check` and exact Git-status review for root, public, admin, and backend repositories.**

- [ ] **Step 3: Confirm no runtime scaffold, new API behavior, font binary, or release state was accidentally created.**

- [ ] **Step 4: Mark only verified authority and documentation gates complete; leave OpenAPI export, database, font acquisition, CI implementation, and runtime scaffolds open where evidence is absent.**

- [ ] **Step 5: Commit each repository’s exact documentation scope and record commit hashes in the work log.**

## Plan self-review

- Every requirement in the consolidation design maps to Tasks 1–9.
- Destructive cleanup occurs only in Task 8, after Task 2 verification and an explicit deletion map.
- Public, admin, and backend documentation have separate owners and commits.
- The plan does not authorize scaffold or runtime behavior changes.
