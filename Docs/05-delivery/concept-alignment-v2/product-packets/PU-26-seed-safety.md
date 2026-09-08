# PU-26-seed-safety — Preserve owner edits during seed import and enforce safe create-missing-only initialization.

Owner: **BACKEND** (`D:/Project/tahamohammadi-platform/Back-End`). Status: **IMPLEMENTED_UNREVIEWED**.

Dependencies: PU-02. Family: shared.

## Read only this context

Workspace and owner AGENTS.md; EXECUTION.md common rules; PRODUCT-SPEC shared rules; `Docs/03-contracts/PRODUCT-INTERFACES-V2.md`. Current generated schema and named source files are evidence, not proposed support.

## Exact write allowlist

- `apps/content/management/commands/import_content_seed.py`
- `apps/content/management/commands/import_profile_seed.py`
- `apps/content/services/content_seed_import.py`
- `tests/test_seed_safety.py` — NEW/PROPOSED
- `docs/quality/product-v2/PU-26-seed-safety-HANDOFF.md` — NEW/PROPOSED

All paths above are relative to the owner repository. Every other path is read-only.

## Purpose and Rules

1. Seed data must only initialize missing database records (`create-missing-only` default).
2. Re-running `import_content_seed` or `import_profile_seed` must never revert an owner-edited record, reset published states to draft, or wipe custom relations.
3. Overwriting existing records must require an explicit, targeted option (e.g. `--overwrite-id <content_id>`).
4. Re-running seed must emit a clear change log / summary report of actions taken (created vs preserved vs overwritten).
5. Regression test suite must prove: `seed initial -> edit via admin/ORM -> seed re-run -> owner edits, publication status, and custom relations are preserved`.

## Acceptance and verification

- uv run pytest tests/test_seed_safety.py

- uv run ruff check .

- Verify `--overwrite-id` flag behavior, dry-run reporting, and zero unhandled exceptions.

## Handoff

Return exact base/result commits (or explicitly uncommitted), changed paths, tests with results, schema hash/impact, screenshots where UI changed, dirty status and remaining risks in `docs/quality/product-v2/PU-26-seed-safety-HANDOFF.md`.

Stop: **PU-26-seed-safety_HANDOFF_READY**. Do not begin another packet, edit another repository, merge, push, deploy or mark owner acceptance.

## Continued content completion scope

- `apps/content/management/commands/seed_managed_copy.py`
- `tests/test_managed_copy_seed.py`
- `apps/siteconfig/seeds/public-copy.json`
- `apps/content/management/commands/seed_site_content.py`
- `tests/test_admin_seed_policy.py`
- `tests/test_seed_admin_only_records.py`
