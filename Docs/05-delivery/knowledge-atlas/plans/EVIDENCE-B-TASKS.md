# Plan B acceptance evidence (Task 18)

Recorded 2026-09-21. Acceptance run only — no feature development (no
defect found).

Code under evidence:

- Backend worktree `D:/Project/.atlas-worktrees/backend-plan-b` at HEAD
  `bdb546f` (branch `feat/knowledge-atlas-admin-authoring`).
- Admin-panel worktree `D:/Project/.atlas-worktrees/admin-plan-b` at HEAD
  `16d44e2` (branch `feat/knowledge-atlas-admin-authoring`).
- Ledger at `53c223d` (17/19 COMPLETE at evidence time).

Interpreter: `D:/Project/tahamohammadi-platform/Back-End/.venv/Scripts/python.exe`
(`env -u PYTHONPATH DJANGO_SETTINGS_MODULE=config.settings.test`), run with
the backend worktree as cwd. Admin gates run inside the admin worktree.

## Backend gates (exact)

| Gate | Command | Output |
|---|---|---|
| Full suite | `pytest tests/ apps/ -q` | `1331 passed, 6 skipped in 54.70s` (1 pre-existing ninja tuple-deprecation warning) |
| Atlas admin API + preview + validation report + auth + permission matrix + openapi + hash drift | `pytest tests/test_admin_atlas_api.py tests/test_admin_atlas_preview.py apps/atlas/tests/test_validation_report.py tests/test_admin_api_auth.py tests/test_admin_permission_matrix.py tests/test_admin_openapi.py tests/test_openapi_hash_drift.py -q` | `153 passed in 11.27s` |
| ruff | `ruff check .` | `All checks passed!` |
| Django system check | `manage.py check` | `System check identified no issues (0 silenced).` |
| Migration drift | `manage.py makemigrations --check --dry-run` | `No changes detected` |
| OpenAPI export verify | `scripts/verify_openapi_export.py` | `MATCH admin-openapi.json: sha256 85008de031715c44887c7f33f583411566f017b4375d2160c6fa5ba15d24eedf` · `MATCH endpoint-inventory.md: sha256 f215d56bc377d089b5515f528a69095d89bebf5f6f04ac59c6bd16aa509de62f` · `MATCH public-openapi.json: sha256 bead273e13a6296030e3255b4a527e956cac8c09ccfff6b2c056df61bbf42139` · `OpenAPI export matches the accepted record.` |

## Admin gates (exact)

| Gate | Command | Output |
|---|---|---|
| Full vitest | `npm test` | `341 passed (341)`, 61 files |
| Contract pins | `vitest run src/lib/api/product-contract.test.ts` | `3 passed (3)` |
| Types | `npx tsc -b` | exit 0, no output |
| Lint | `npm run lint` | `0 errors, 6 pre-existing react-refresh warnings` (none in Plan-B task files) |
| Format | `npm run format:check` | `All matched files use Prettier code style!` |
| Build | `npm run build` (`tsc -b && vite build`) | `✓ built in 2.94s` (170 modules; `dist/assets/index-7odxAuMi.js 473.10 kB`, gzip 134.55 kB). `dist/` is ignored — worktree clean after build. |
| E2E (whole dir) | `npx playwright test` (Edge channel, `npm run dev` webServer) | `6 passed`, `1 skipped` (the skip is `product-journey-live @live @staging`, staging-only by design) incl. `atlas-authoring 1/1` and `admin-matrix 5/5` |

## Cross-repo contract drift

Zero drift: backend `verify_openapi_export.py` MATCH ×3 (public snapshot
byte-stable at `bead273e…`), admin `product-contract.test.ts` 3/3
(`openapi-hash.json` pathCount 79, accepted backend commit pinned). No
backend change since the Task-12 re-pin; no admin contract change since.

## Authoring journey record (E2E, mocked network boundary)

Spec `tests/e2e/atlas-authoring.e2e.ts`, green on Edge (2.7s). Admin API
mocked at the network boundary per the ADMIN-290 precedent; server-side
guard enforcement is proven by the backend suite above, so the journey
proves the UI drives the contract honestly end to end:

1. `/admin/atlas` versions list → Clone on `Live` (id 7) → draft id 8,
   navigated to `/admin/atlas/8`.
2. Graph keyboard selection: focus `project-2b3c4d5e`, ArrowRight moves
   the picker to `method-11223344`, Enter selects into the node form.
3. Importance → 70, Enter on Save → exactly one
   `PATCH /atlas/versions/8/nodes/project-2b3c4d5e` (If-Match sent).
4. Relation form (Source project / Type uses / Target method) → one
   `POST /atlas/versions/8/relations`.
5. Real pointer drag (+40/−10 px) on the node → exactly one pin PATCH
   with finite changed `{x, y}`; a plain click pins nothing.
6. Validation panel: `No validation issues`, Publish enabled.
7. Publish → Confirm → `POST /atlas/versions/8/activate` (once) →
   `This version is published` + `Publication job 42`; editor read-only.
8. `/admin/atlas/8/preview`: frame `src` carries `#token=`, no canvas,
   read-only notice. `/admin/atlas/taxonomy`: node type listed.

## Verdict

All gates green, zero drift, journey complete. No acceptance defect found;
no new feature work performed in this task.
