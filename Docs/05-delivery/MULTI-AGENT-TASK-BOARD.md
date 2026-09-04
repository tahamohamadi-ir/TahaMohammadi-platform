# Multi-Agent Task Board

Status: **Wave 0 complete** (2026-08-29). Wave 1 active: seed import + OpenAPI types.  
Canonical rollup: `MASTER-TASK-LIST.md` (milestones only).  
This document is the **detailed work queue** with dependencies and verification gates.

## How agents use this board

1. Pick **one lane** (COORD, BACKEND, PUBLIC, ADMIN) and **one task ID**.
2. Work in **one repository** unless the task is explicitly COORD-only.
3. Declare in your handoff: `task_id`, `repository`, `files touched`, `commands run`, `blockers`.
4. Do not mark a task done without the listed **Done when** evidence.
5. Two agents must not edit the same file in the same wave unless the dependency row assigns a merge owner.

## Local environment note

A legacy `tahamohamadi-website` Docker stack may run on ports 80/443 with its own PostgreSQL. The new platform must use a **separate disposable PostgreSQL** profile documented in `Docs/08-operations/LOCAL-DEVELOPMENT.md`.

---

## Wave map (parallel lanes)

```text
Wave 0 — COMPLETE (2026-08-29)
  BACKEND-010..050  disposable PostgreSQL :5433, migrate, /health/
  PUBLIC-010..040   Astro 7 + Tailwind 4 + i18n gateway
  ADMIN-010..040    React 19 + Vite + /admin/ shell

Wave 1 — IN PROGRESS (2026-08-29)
  BACKEND-060..080  seed import — **complete** (`4e4fb75`)
  BACKEND-081..082  empty-state route copy + admin-only seed records — **complete**
  BACKEND-041       backend CI workflow — **complete** (`.github/workflows/ci.yml`)
  COORD-040..050   OpenAPI TS contract docs — **complete**
  PUBLIC-090       OpenAPI types + client skeleton — **complete**; PUBLIC-100..120 open
  ADMIN-050..060   admin types + client skeleton — **complete**; ADMIN-070..110 open

Wave 2 (after Wave 1)
  PUBLIC-130..220  design system + shell + atlas
  ADMIN-120..180   primitives + permissions shell
  BACKEND-130..160 contract fixtures + error normalization plan

Wave 3 (after Wave 2)
  PUBLIC-230..350  page families PF-01..PF-08
  ADMIN-190..320   CMS workflows
  BACKEND-170..200 staging integration hooks

Wave 4 (release)
  COORD-060..090   integrated staging + quality gates
```

---

## COORD lane (workspace `Docs/` + cross-repo interfaces)

| ID | Depends | Task | Done when |
|---|---|---|---|
| COORD-010 | — | Register this board; link from `MASTER-TASK-LIST.md` and each repo `TASK-LIST.md` | Board committed; links resolve |
| COORD-020 | — | Update `PRE-SCAFFOLD-READINESS.md` for Seed v1.1 supplement ingestion | PS-08 evidence mentions v1.1 |
| COORD-030 | — | Activate CI Phase 0 workflows (coordination validator + backend pytest/ruff/OpenAPI) | Workflows green on `main` |
| COORD-040 ✅ | PUBLIC-090, ADMIN-080 | Add shared OpenAPI → TypeScript generation contract doc path in `Docs/03-contracts/` | **Done** — `OPENAPI-TYPESCRIPT-GENERATION.md`: generator command, output paths, hash pins |
| COORD-050 ✅ | COORD-040 | Add public/admin contract fixture file locations in `Docs/03-contracts/` | **Done** — `CONTRACT-FIXTURE-PATHS.md`; referenced from generation doc |
| COORD-060 [~] | BACKEND-200, PUBLIC-350, ADMIN-320 | Staging topology checklist against `DEPLOYMENT-TOPOLOGY.md` | **Plan ready** — `Docs/10-tracking/COORD-060-STAGING-TOPOLOGY-CHECKLIST.md`; execution blocked on staging infra; owner columns awaiting owner fill |
| COORD-070 [~] | COORD-060 | Run draft-leak + CSRF + MFA staging evidence collection | **Plan ready, NOT executed** — `Docs/10-tracking/COORD-070-STAGING-EVIDENCE-PLAN.md`; needs live staging |
| COORD-080 [~] | COORD-070 | Visual/public + admin quality matrix sign-off package | **Template ready** — `Docs/10-tracking/COORD-080-R8-SIGNOFF-PACKAGE.md`; R8 NOT passed |
| COORD-090 [~] | COORD-080 | Owner production acceptance record | **Template ready** — `Docs/10-tracking/COORD-090-OWNER-ACCEPTANCE-RECORD.md`; owner sign-off pending |

---

## BACKEND lane (`Back-End/`)

| ID | Depends | Task | Done when |
|---|---|---|---|
| BACKEND-010 | — | Document disposable PostgreSQL profile (port, db name, user) in `Back-End/docs/operations/` | Doc merged; no legacy stack coupling |
| BACKEND-020 | BACKEND-010 | Reconcile `.env.example` for Docker-local + standalone profiles | Example env covers both paths |
| BACKEND-030 | BACKEND-020 | Start Django with `config.settings.development` against disposable PostgreSQL | Server boots; no settings errors |
| BACKEND-040 | BACKEND-030 | Apply all migrations on empty database | `migrate` exit 0 |
| BACKEND-050 | BACKEND-040 | Verify `GET /health/` and document response | Health check passes; recorded in task handoff |
| BACKEND-060 | BACKEND-050 | Add management command or script to import `content-records.v1.1-seed.json` | Command runs idempotently on empty DB |
| BACKEND-070 | BACKEND-060 | Import seed with all records `draft`/`not-public` | DB count matches 85; zero published leak in public API |
| BACKEND-080 | BACKEND-070 | Add pytest for seed import + public API non-leak | Tests pass in CI |
| BACKEND-090 ✅ | BACKEND-050 | Inventory `Infra/legacy-monorepo` paths; classify rewrite vs delete | **Done** — `Back-End/docs/operations/LEGACY-MONOREPO-INVENTORY.md` (46 files: 20 rewrite / 18 reference / 8 delete-recommended; tree untouched) |
| BACKEND-100 ✅ | BACKEND-090 | Draft standalone Docker Compose for **new** platform only | **Done** — `api` service on `127.0.0.1:18010` + root `Dockerfile`; `docker compose config` passes; runtime build/run pending Docker daemon |
| BACKEND-101 ✅ | BACKEND-090 | Replace monorepo path assumptions in active scripts | **Done** — audit in `Back-End/docs/operations/STANDALONE-VALIDATION.md` §A; `run_e2e_stack.sh` fixed (+ regression test); `manual-rebuild.sh` blocked on rebuild-contract decision |
| BACKEND-102 ✅ | BACKEND-100 | Validate `config.settings.local` against Docker profile | **Done (static)** — `manage.py check` passes both env variants; live-5433 `migrate --plan` pending Docker (documented §B) |
| BACKEND-160 ✅ | BACKEND-100 | Validate backup/restore commands for new repo layout | **Done (documented)** — `Back-End/docs/operations/BACKUP-RESTORE.md`; drill is R7-gated |
| BACKEND-110 ✅ | — | Reconcile public endpoints vs `ROUTE-REGISTRY.md` | **Done** — gap list at `Back-End/docs/contracts/PUBLIC-ROUTE-RECONCILIATION.md` (gaps A–E) |
| BACKEND-120 ✅ | — | Reconcile admin endpoints vs admin workflow map | **Done** — `Back-End/docs/contracts/ADMIN-ROUTE-RECONCILIATION.md` (63 ops verified; gaps G-A..G-I; G-E media-delete + G-G sibling-create are blocking decisions) |
| BACKEND-130 ✅ | BACKEND-110, BACKEND-120 | Add response-shape fixtures per `ERROR-COMPATIBILITY-MATRIX.md` | **Done** — `Back-End/tests/fixtures/contracts/{public,admin,errors}/` + `tests/test_contract_fixtures.py` |
| BACKEND-140 ✅ | BACKEND-130 | Schema compatibility tests for accepted OpenAPI hashes | **Done** — `tests/test_openapi_hash_drift.py` (LF-canonical; CRLF acceptance provenance documented) |
| BACKEND-150 ✅ | — | Plan error envelope normalization (no breaking change) | **Done** — ADR-0006 Accepted 2026-09-02 (owner-delegated review; DECISION-LOG); phase 1 (`field_errors` on AdminError) shipped and tested |
| BACKEND-151 ✅ | — | Deprecation plan for legacy `/admin/`, `/staff/`, `/api/admin/` routes | **Done** — plan approved by owner 2026-09-02 (`Back-End/docs/contracts/LEGACY-ROUTE-DEPRECATION.md`); removals evidence-gated via separate ADR |
| BACKEND-170 ✅ | PUBLIC-120, ADMIN-110 | Same-origin proxy integration test plan with frontends | **Done** — `Back-End/docs/quality/INTEGRATION-TEST-PLAN.md` (checklist per `DEPLOYMENT-TOPOLOGY.md` evidence list) |
| BACKEND-180 ✅ | BACKEND-170 | Session, CSRF, MFA, preview, contact smoke tests | **Done** — `Back-End/tests/test_staging_smoke.py` 3/3 pass on disposable settings; suite 678 pass. Staging browser capture remains COORD-060/070 |
| BACKEND-190 | ADMIN-250 | Permission regression tests for every state-changing admin route | Matrix tests pass |
| BACKEND-200 | BACKEND-180, BACKEND-190 | Staging-ready backend artifact + migration evidence | `R7` backend slice complete |

---

## PUBLIC lane (`Front-End/public-site/`)

| ID | Depends | Task | Done when |
|---|---|---|---|
| PUBLIC-010 | — | Initialize Astro 7 + TypeScript 5.9 + package manager lockfile | `npm run build` succeeds (minimal) |
| PUBLIC-020 | PUBLIC-010 | Configure Tailwind CSS 4 pipeline on semantic CSS variables | Build emits processed CSS; no raw `@tailwind` leak |
| PUBLIC-030 | PUBLIC-020 | Add `astro:i18n` with `fa`/`en`; no fallback | `/fa/` and `/en/` routes build |
| PUBLIC-040 | PUBLIC-030 | Implement language gateway `/` per `ROUTE-REGISTRY.md` | Gateway renders; sets locale links |
| PUBLIC-050 | PUBLIC-020 | Pin self-hosted fonts (Newsreader, Inter, Estedad, Vazirmatn) | WOFF2 in repo; license files present |
| PUBLIC-060 | PUBLIC-050 | Wire `--font-display` / `--font-body` tokens per locale | Computed-style test passes |
| PUBLIC-070 ✅ | PUBLIC-020 | Light/Dark/system theme via CSS variables + island toggle | **Done** — WP-10 persists and announces requested/resolved state before paint; focused acceptance covers preference changes, persistence, event detail/count, and multiple controls. |
| PUBLIC-080 ✅ | PUBLIC-070 | Reduced-motion and focus-visible baseline | **Done** — WP-10 visible-focus and reduced-motion acceptance pass. |
| PUBLIC-090 | PUBLIC-010 | Generate public API types from accepted OpenAPI hash | Types committed; hash pin in repo |
| PUBLIC-100 ✅ | PUBLIC-090 | Implement typed API client with published-only filter | **Verified 2026-09-02** — `src/lib/api/client.ts` `assertPublishedOnly` + client tests pass (244-test suite green) |
| PUBLIC-110 ✅ | PUBLIC-100 | Locale route helpers + canonical/hreflang utilities | **Verified 2026-09-02** — `routes.ts`/`seo.ts` + `routes.test.ts`/`seo.test.ts` pass |
| PUBLIC-120 ✅ | PUBLIC-110, BACKEND-050 | Env schema (`PUBLIC_API_BASE`, etc.) + dev proxy config | **Verified 2026-09-02** — `env.ts` + astro `envField` + `/api`,`/health`,`/media` proxy; `.env.example` present |
| PUBLIC-130 ✅ | PUBLIC-080 | Map design tokens from `agent-kit/tokens.json` | **Done** — complete primitive/semantic/type/motion/layout/component projection, portable snapshot, and authority-equal contract validate locally and centrally. |
| PUBLIC-140 ✅ | PUBLIC-130 | Build primitives (button, link, card, tag, badge, …) per `components.json` | **Verified 2026-09-02** — 24/24 components pinned vs authority snapshot; `validate:design` pass |
| PUBLIC-150 ✅ | PUBLIC-140 | Build Header, Footer, skip link, page shell | **Verified 2026-09-02** — shell behavior tests + `@a11y` crawl (29 pass) |
| PUBLIC-160 ✅ | PUBLIC-150 | Build six shared templates from `templates.json` | **Verified 2026-09-02** — 6/6 templates asserted; Atlas template gallery |
| PUBLIC-170 ✅ | PUBLIC-160 | Local-only Visual Atlas `DESIGN_ATLAS=1` → `/_design/` | **Verified 2026-09-02** — prod build contains no `/_design/` (`dist\_design` absent); atlas gate e2e |
| PUBLIC-180 ✅ | PUBLIC-100 | Content-state components: loading, empty, unavailable, error, untranslated | **Verified 2026-09-02** — `public-180.behavior.test.ts` 15 tests pass; Atlas state specimens |
| PUBLIC-190 [~] | PUBLIC-180, BACKEND-070 | Home page both locales using seed (draft-safe: no false publish) | **Structure complete; visual acceptance open.** Gate SHA `c7581b7` (About/Contact/Research leftover chrome PF-05/07/08). Prior PF-02 empty-shell @ `798e8b2`; Phase 8 @ `84e83e9`; Phase 6 @ `0e6a552`; evidence grid @ `cf81f6f`; Path A shells @ `dd515a0`; compare **43/48** ready confirmed by owner `review:visual` run @ `675a08f` (39 index + 4 PF-02 empty-shell; 5 capture-only). **Remediation:** owner asset prompts (`Docs/10-tracking/PUBLIC-190-asset-prompts/`), phased plan + requirements research, ADR-0007. Independent QA `PASS`, owner asset handback, and explicit sign-off remain required — **REVISE**. |
| PUBLIC-200 | PUBLIC-190 | About + research routes | Profile fetch uses `/api/profiles/{locale}/about` only |
| PUBLIC-210 | PUBLIC-200 | Projects + writing indexes and detail routes | Slug only from API; unavailable honest |
| PUBLIC-220 | PUBLIC-210 | Publications, teaching, creative routes with seed empty states | Creative/teaching/CV empty copy from seed v1.1 |
| PUBLIC-230 | PUBLIC-220 | Contact form (progressive + JSON) per error matrix | 422 HTML path handled |
| PUBLIC-240 | PUBLIC-230 | Pagefind per-locale index | Search works offline |
| PUBLIC-250 | PUBLIC-240 | SEO: sitemap, robots, canonical, hreflang | Validation script passes |
| PUBLIC-260 | PUBLIC-130 | Promote decorative assets per ledger (group A) | Derivatives + alt recorded |
| PUBLIC-270 | PUBLIC-260 | PF-01..PF-08 visual evidence vs `concepts/page-families/` | Visual QA checklist |
| PUBLIC-280 | PUBLIC-270 | Six-width responsive matrix | Evidence captured |
| PUBLIC-290 | PUBLIC-280 | Performance budget report (LCP, CLS) | Within budget or deferrals logged |
| PUBLIC-300 | PUBLIC-290 | No-JS crawl test for all route families | All routes readable without JS |
| PUBLIC-310 | PUBLIC-300 | Contract fixture tests vs OpenAPI | CI green |
| PUBLIC-320 | BACKEND-180 | Integrated smoke with backend staging | Cookies/proxy pass |
| PUBLIC-350 | PUBLIC-320 | Public release evidence package | `R4` + `R8` public slice complete |

### Home recovery hold

- WP-10 closes only `PUBLIC-070`, `PUBLIC-080`, and `PUBLIC-130`; `PUBLIC-140` through `PUBLIC-180` remain owned by their assigned packets.
- `PUBLIC-190` is not Done: its structure is complete, but visual acceptance is open pending `PUBLIC-180`, `BACKEND-070`, independent visual QA `PASS`, and explicit owner acceptance.
- Page-family development `PUBLIC-200` through `PUBLIC-240` is frozen until that acceptance. `WP-25` and `PUBLIC-260` remain allowed. This does not mark R3 or R4 complete.

---

## ADMIN lane (`Front-End/admin-panel/`)

| ID | Depends | Task | Done when |
|---|---|---|---|
| ADMIN-010 | — | Initialize React 19 + Vite + TypeScript 5.9 + lockfile | `npm run build` succeeds |
| ADMIN-020 | ADMIN-010 | Configure router, base path, and guarded layout shells | Routes render |
| ADMIN-030 | ADMIN-010 | Env schema (`VITE_API_BASE`, etc.) | `.env.example` validated |
| ADMIN-040 | ADMIN-030 | Confirm same-origin proxy dev setup documented | README + env align with topology |
| ADMIN-050 | ADMIN-010 | Generate admin API types from accepted OpenAPI | Types committed with hash pin |
| ADMIN-060 | ADMIN-050 | API client with CSRF header injection hooks | Unit tests for client wrapper |
| ADMIN-070 | ADMIN-060 | Error normalizer for `code/message/fields` + network | Matrix unit tests |
| ADMIN-080 | ADMIN-070 | Sign-in page (session cookie flow) | Login against dev backend |
| ADMIN-090 | ADMIN-080 | MFA / OTP challenge flow | Verified staff fixture path works |
| ADMIN-100 | ADMIN-090 | Sign-out, session expiry, re-auth | Browser test passes |
| ADMIN-110 | ADMIN-100 | CSRF token fetch + attach on mutations | Fails without token |
| ADMIN-120 | ADMIN-070 | Admin tokens + primitives (table, form, dialog, notice) | a11y keyboard tests |
| ADMIN-130 | ADMIN-120 | Permission-aware navigation (UI ≠ authorization) | Forbidden routes show honest state |
| ADMIN-140 | ADMIN-130 | Dashboard health / degraded status | Reads backend health |
| ADMIN-150 | ADMIN-140 | Profile + site settings screens | CRUD against API |
| ADMIN-160 | ADMIN-150 | Articles/series list + editor skeleton | Create draft works |
| ADMIN-170 | ADMIN-160 | Research, publications, projects collections | Maps to API inventory |
| ADMIN-180 | ADMIN-170 | Media upload + metadata + usage guard | Upload test with fixture |
| ADMIN-190 | ADMIN-180 | Home module composition UI | Ordering persisted |
| ADMIN-200 | ADMIN-190 | Timeline editor | Validation errors surface |
| ADMIN-210 | ADMIN-200 | Graph editor (nodes/edges/groups) | Reference boundary only; no invented API |
| ADMIN-220 | ADMIN-210 | Preview-share workflow | Token expiry tested |
| ADMIN-230 | ADMIN-220 | Revision history + restore | Conflict handling |
| ADMIN-240 | ADMIN-230 | Schedule / publish / archive / bulk actions | Server permission tests paired |
| ADMIN-250 | ADMIN-240 | Workflow map: every mutation → permission test | `WORKFLOW-API-MAP.md` complete |
| ADMIN-260 | ADMIN-120 | Seed admin-only records visible in admin (not public) | admin.* records from supplement |
| ADMIN-270 | ADMIN-260 | Owner approval queue UI from `owner-approval-queue.json` | Queue renders counts |
| ADMIN-280 | ADMIN-270 | Publication gate enforced in UI | Cannot mark published without approval |
| ADMIN-290 | ADMIN-280 | Browser matrix (signed out, MFA, forbidden, validation) | CI workflow green |
| ADMIN-300 | BACKEND-180 | Integrated smoke with backend staging | Session/CSRF pass |
| ADMIN-320 | ADMIN-300 | Admin release evidence package | `R6` + `R8` admin slice complete |

---

## Owner lane (human — not agent-owned)

| ID | Task | Done when |
|---|---|---|
| OWNER-010 | Review `owner-content-gaps.md` top 5 items | Edits or explicit approve in queue |
| OWNER-020 | Supply CV/resume PDFs or keep unavailable | Files + hashes in manifest |
| OWNER-030 | Confirm image mapping group B (or defer) | Note in `ASSET-PROMOTION-LEDGER.md` |
| OWNER-040 | Stanford credential source attachment | `admin.credential.stanford` evidence linked |
| OWNER-050 | Production publication approval per record | `approval_state=approved` for chosen rows |

---

## Suggested 4-agent split (Wave 0)

| Agent | Lane | First tasks | Repository |
|---|---|---|---|
| A | COORD | COORD-010, COORD-020, COORD-030 | workspace root |
| B | BACKEND | BACKEND-010 → 050 | `Back-End/` |
| C | PUBLIC | PUBLIC-010 → 080 | `Front-End/public-site/` |
| D | ADMIN | ADMIN-010 → 171, 180–200, 210, 220, 230 | `Front-End/admin-panel/` |

After BACKEND-050 and PUBLIC-010/ADMIN-010 complete, start Wave 1 (seed import + API clients) without waiting for full UI.

---

## Status sync rule

When a task ID completes, update:

1. This board (check off in repo copy if mirrored).
2. Owning repository `TASK-LIST.md`.
3. `MASTER-TASK-LIST.md` only when an entire milestone section (`R1`, `R3`, …) is fully evidenced.
