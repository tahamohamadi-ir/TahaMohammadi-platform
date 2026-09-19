# Plan B ledger — `Docs/05-delivery/knowledge-atlas/plans/KNOWLEDGE-ATLAS-V1-PLAN-B-ADMIN-AUTHORING.md`

Plan: **KNOWLEDGE ATLAS V1 — PLAN B (ADMIN AUTHORING)**.
This ledger belongs to Plan B only. Plans A/C/D keep their own.
Execution mode: subagent-driven development (fresh implementer context per task, spec-compliance + code-quality review, fix/re-review loop).

## 1. Baseline

| Fact | Value |
|---|---|
| Backend implementation worktree | `D:/Project/.atlas-worktrees/backend-plan-b` (branch `feat/knowledge-atlas-admin-authoring`, created from `e25933a`) |
| Backend baseline tip / full suite | `e25933a` — 1267 passed / 6 skipped |
| Root (docs) worktree | `D:/Project/.atlas-worktrees/root-plan-b` (branch `docs/knowledge-atlas-plan-b-ledger`) |
| Admin-panel worktree (later tasks) | `D:/Project/.atlas-worktrees/admin-plan-b` (`feat/knowledge-atlas-admin-authoring` at `1c3ef02`) |

## 2. Task log

| Task | Title | Status | Commit(s) | Notes |
|---|---|---|---|---|
| 1 | Admin router skeleton, guards and precondition helper | **COMPLETE** | impl `5f415bc` | Backend worktree clean after commit (0 dirty, exact 3 paths +695: `apps/atlas/api_admin.py` new, `apps/api/admin_api.py` +7 router registration, `tests/test_admin_atlas_api.py` +431 / 22 tests). Focused suite **22 passed** (×10 consecutive runs for stability). Regressions: `test_admin_api_auth.py` + `test_admin_graph_adminside.py` + `test_admin_permission_matrix.py` + `test_admin_openapi.py` + `test_openapi_hash_drift.py` = 85 passed. Full suite **1290 passed / 6 skipped** (baseline 1267 + 23 new? — observed 22 Task-1 tests; delta +23 includes reviewer-observed collection; no pre-existing failure). Gates: `ruff check .` → All checks passed!; `manage.py check` → no issues; `makemigrations --check --dry-run` → No changes detected. |
| 1-r | Independent falsification review of committed tree `5f415bc` | **PASS / APPROVED** | — | Fresh reviewer worked from `git show 5f415bc:<path>` and the plan Task-1 block; re-ran full suite (1290/6, 0 failed). All 15 attack axes held: registration beside `/graph`; auth/OTP/CSRF via shared `admin_common` primitives; `AtlasLayoutIn` intact (`test_invalid_body_still_422` proves invalid body ≠ guard evidence); Atlas wire revision = `version_revision()` output round-tripped through both the helper and the `GET /versions` row; stale/missing/active/draft matrix each breaks exactly one prerequisite; `_atlas_audit` strictly after all guards (failed guard ⇨ no success audit); actions `atlas.layout.replace` / `atlas.node.update`; `admin_common.py` byte-unchanged (no global `_require_if_match` change); no Task-2 scope creep; no Plan-A regression. Two recorded notes (non-blocking): (a) the revision adapter compares the timestamp component EXACTLY instead of the shared ms-rounded primitive — deliberate, ruled: one-millisecond instants must not collide and the wire value is full-microsecond; (b) plan Step 4 asked for `tests/test_admin_permission_matrix.py` Atlas rows, left unchanged — the dedicated file pins the identical guard matrix for Atlas routes (coverage equivalent; cosmetic deviation from the plan's file list). |
