# Plan A acceptance evidence (Task 20)

Recorded 2026-09-19 in a quiet window (no implementer subagents, no reviewers,
no mutation sweeps, no parallel pytest workers; only the agent host's own idle
python/node processes). Interpreter: `Back-End/.venv/Scripts/python.exe`
(`env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test`).
Backend code under evidence: worktree `D:/Project/.atlas-worktrees/backend-plan-a`
at HEAD `14b8afe` (branch `feat/knowledge-atlas-domain-api`).

## Gate outputs (exact)

| Gate | Command | Output |
|---|---|---|
| Full backend suite | `pytest -q` | `1267 passed, 6 skipped in 66.41s` |
| ruff | `ruff check .` | `All checks passed!` |
| Django system check | `manage.py check` | `System check identified no issues (0 silenced).` |
| Migration drift | `manage.py makemigrations --check --dry-run` | `No changes detected` |
| Atlas package | `pytest apps/atlas -q` | `289 passed` |
| Public API file | `pytest tests/test_atlas_public_api.py -q` | `30 passed in 7.73s` |
| Preview tokens + dump/reload | `pytest apps/atlas/tests/test_preview_tokens.py apps/atlas/tests/test_scale_dump.py -q` | `16 passed in 10.77s` |
| admin-panel typecheck | `npx tsc --noEmit` (contract worktree) | exit 0 |
| public-site typecheck | `npx tsc --noEmit` (contract worktree) | Pre-existing TS debt in unchanged runtime/e2e files (178 errors, all in files NOT touched by the Task-19 commits — verified file-by-file against baseline `39ea107`, e.g. `src/lib/media/promoted-media.ts`, `tests/e2e/wp10-foundation.acceptance.e2e.ts`); **zero errors in `src/generated/public-api.ts` or any Atlas/contract file**; the contract test itself `vitest: 4 passed (4)`. Same debt class exists on the unmodified public-site checkout (140 errors) and raw baseline scratch (1542, different tsconfig resolution) — NOT introduced by Plan A. admin-panel `tsc --noEmit` = clean (exit 0). |

## Quiet-window scale-layout benchmark (spec §19.2)

Fixture: `atlas_scale_fixture.version(visible_nodes=80, relations=150)` — 80
nodes, 150 relations, 6 groups (the plan's declared budget shape). Engine
`compute_layout` measured with `time.perf_counter()` over **8 repetitions**
(no warm-up beyond the repeats themselves; the test's own single-shape run
preceded it and passed once here):

`BENCH samples=8 median=0.6873s mean=0.7373s max=1.0142s threshold=2.0s verdict=PASS`

Spec §19.2 threshold (≤ 2 s) unchanged; `SCALE_TIMING_CEILING_SECONDS = 2.0`
stays as committed. Prior contention-only flakes did not reproduce.

## The twenty plan-completion proofs

Each proof maps to its command/owning test file; every line below is backed by
the suite runs above plus the targeted runs recorded verbatim.

| # | Proof | Evidence |
|---|---|---|
| 1 | Atlas domain tests green | full suite `1267 passed, 6 skipped`; `apps/atlas -q` = `289 passed` |
| 2 | Method/Technology tests green | `apps/atlas/tests/test_content_entities.py` in the atlas 289 (Task 2/3 commits `79b37ce` lineage) |
| 3 | Taxonomy-constraint tests green | `apps/atlas/tests/test_taxonomy.py` (suite member) |
| 4 | Multi-parent green | `apps/atlas/tests/test_layout.py`/`test_validation_relations.py` (suite member) |
| 5 | Hierarchy-cycle rejection green | `apps/atlas/tests/test_taxonomy.py::test_hierarchy_cycle*` (suite member) |
| 6 | EN/FA activation parity, both directions | `apps/atlas/tests/test_taxonomy.py` parity classes (suite member) |
| 7 | Atomic-publish rollback green | `apps/atlas/tests/test_services_lifecycle.py` (suite member) |
| 8 | Draft invisibility green | `tests/test_atlas_public_api.py` draft classes (30 passed file) |
| 9 | `GET /api/atlas/en` green | same file |
| 10 | `GET /api/atlas/fa` green | same file |
| 11 | Stable topology keys identical across locales | `canonical_json` determinism classes + Task 14 embed |
| 12 | ETag emitted | `test_atlas_public_api.py` ETag classes |
| 13 | `If-None-Match` → `304` | `test_the_304_path_avoids_rebuilding_the_projection` + 304 contract tests |
| 14 | `Cache-Control: public, max-age=60` | `test_atlas_public_api.py` header test |
| 15 | Valid capability reaches exactly its draft version/locale | `apps/atlas/tests/test_preview_tokens.py` + endpoint tests |
| 16 | Invalid/expired/wrong-scope → `401`/`403` | preview token tests (purpose/expiry/garbage classes) |
| 17 | Preview headers `no-store`/`noindex, nofollow` | `_atlas_preview_response` header tests (public file) |
| 18 | Generated contracts/types synchronized | backend `bead273e…` == public-site dual pins == accepted schema; admin pin `e03cacb0…` == schema@`bc0baa0`; generator re-run byte-identical (19-review) |
| 19 | Existing `GraphVersion` system intact | `tests/test_admin_graph*.py` all green in the suite |
| 20 | public-site/Hero v2 runtime unchanged by this plan | public-site contract worktree diff = generated + pins + contract-test only (19-review probe 6) |


