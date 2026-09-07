# اجرای چهاربسته‌ای — بازبینی PU-03-settings و PU-SYNC-graph، اصلاح PU-07-revisions و PU-07-runner (2026-09-06)

Scope: mission four-packet execution, not startup check. No commit/push/merge/deploy, no real DB change. Disposable DB only via pytest. Previous reports are historical; current code re-verified.

## ۱. پایه (HEAD، وضعیت، هش)

- ROOT `c69e339c8c26788467d29ad346fb7df99b1c2842` branch `main`, modified + untracked (docs + Infra/staging runner).
- BACKEND `bd6682ea9dae7e5bf6957c36691dc3a94a00ea37` branch `main`, modified + untracked (allowlisted product-v2 code/tests/openapi).
- PUBLIC `b895b2cb9c6ad9519d55bd2663448461931c0a39` branch `main`, modified + untracked (sync-graph + CA visual).
- ADMIN `ca4dd3d26484d4468465c756d302b8e3247a3cbe` branch `main`, modified (docs) + untracked quality; no runtime change for these four.
- Queue before: PU-03-settings IMPLEMENTED_UNREVIEWED, PU-SYNC-graph IMPLEMENTED_UNREVIEWED, PU-07-revisions REVISE, PU-07-runner REVISE. ready_to_start empty does not block review/fix.
- Accepted manifest `reviews/ACCEPTED-LOCAL-2026-09-06.json` before: CA-01 (5 files) and PU-03-resolver (8 files) all matched working copy (verified via sha256). No blind replacement below; changed accepted files are listed with effect and re-verification, history preserved (old reviews/handoffs kept, old hashes recorded here).

## ۲. PU-03-settings (BACKEND, IMPLEMENTED_UNREVIEWED — positive review, gate open)

Reviewed: `apps/siteconfig/models.py` (LocalizedSiteSettings), `apps/api/api.py` public `GET /v1/site/{locale}` (404 fail-closed, no fallback), `apps/api/admin_siteconfig.py` (GET draft, PUT OTP+CSRF+If-Match, POST publish OTP+CSRF, link/preset validation, legacy `/api/site` untouched, publish enqueues `[/{locale}/, /{locale}/site/]`), `tests/test_product_localized_settings.py`, migration `0005`, re-exported OpenAPI (public/admin hashes unchanged semantically).

Gaps found (coverage, not behavior): auth/CSRF on mutations and data:/http:/unknown hrefs were untested. Added 5 regression tests (all in allowlist):
- `test_admin_put_requires_auth`, `test_admin_publish_requires_auth` (401/403).
- `test_admin_put_requires_csrf`, `test_admin_publish_requires_csrf` (403 CSRF_FAILED).
- `test_admin_put_rejects_data_http_and_unknown_hrefs` (400 VALIDATION; `/fa/about` accepted).

Evidence:
- Before: 12 passed. After: `uv run pytest tests/test_product_localized_settings.py -q` → 17 passed.
- `uv run pytest tests/test_product_publication_invalidation.py -q -k settings` → 1 passed (enqueue paths `/fa/`, `/fa/site/`).
- `uv run ruff check .` → All checks passed. `makemigrations --check` → No changes detected. `export_openapi.py` → public 48 paths `47980f…`, admin 57 paths `1176c0…` (no semantic schema change from this packet).
- Changed files (BACKEND): `tests/test_product_localized_settings.py` only (plus re-export timestamp churn in PROVENANCE, handled in §6).

Contract effect: none (no schema shape change). Legacy preserved. Enqueue correct per invalidation test.

Review result: implementation correct, now locked with regression. Dependencies: PU-02 DOC_COMPLETE, PU-03-resolver ACCEPTED (with §6 hash update, behavior unchanged) → ready_for_review, not locally accepted here (owner acceptance gate remains; do not use to unblock unrelated ADMIN).

## ۳. PU-SYNC-graph (PUBLIC, IMPLEMENTED_UNREVIEWED — positive review, gate open)

Reviewed: `src/generated/public-api.ts` (from accepted public-openapi via `npm run generate:api-types`), `tests/fixtures/contracts/product-record-resolver.json`, `src/lib/product-resolver.contract.test.ts`, backend `record_resolver.py` + `test_product_record_resolver.py` (33 passed).

Findings (real, fixed in allowlist):
- Fixture `sourceOpenApiSha256` was `8739e5…` vs accepted pin `47980f…` (drift; contract test only checked hex regex, not equality). Before fix, pin-equality would fail (recorded hashes: fixture 8739…, pin 47980…).
- Fixture `resolveLessonWithCourseSlug` claimed 200 lesson resolution with courseSlug, but backend rejects `lesson:*` with 400 INVALID_INPUT (verified live: `GET /api/v1/records/fa/resolve?refs=lesson:1` → 400 Unknown family). Backend supports 13 families (landing/profile/article/series/researchtopic/researchstatement/project/publication/book/talk/download/course/creativework), not lesson/collection until projections exist (I05). Fixture fiction corrected, not weakened.
- `public-api.ts` was already from accepted schema (`generate:api-types` PASS, no manual types).

Fixes:
- Fixture sha → `47980f8f1992d885398676cf984b80e7068c7aa8e8b8f76a856565ffc9033681`; `resolveLessonWithCourseSlug` → `resolveLessonCurrentlyUnsupported` (400 INVALID_INPUT, documented 13-family scope).
- Contract test: pin-equality vs `src/generated/openapi-hash.json`, lesson-unsupported (400) test, all-200-items null courseSlug test (backend always null currently). Count 8 → 9.

Evidence:
- `npm run generate:api-types` → PASS (openapi-typescript 7.13.0, hash check PASS).
- `npm test -- src/lib/product-resolver.contract.test.ts` → 9 passed.
- `npx prettier --check` + `eslint` → PASS. `npm test -- --run` (full PUBLIC) → 61 files, 354 passed. `npm run build` → 33 pages, Pagefind en/fa, sitemap PASS.
- Backend resolver: `uv run pytest tests/test_product_record_resolver.py -q` → 33 passed.
- Changed files (PUBLIC): fixture, contract test (plus regenerated `public-api.ts` byte-identical, no runtime change). Not visual/hero acceptance; sync only.

Review result: types/fixture now from reviewed schema, hashes correct, resolver-consumer compatible (lesson documented as unsupported). Dependencies: PU-03-resolver ACCEPTED (updated) → ready_for_review, not locally accepted here.

## ۴. PU-07-revisions (BACKEND, REVISE → IMPLEMENTED_UNREVIEWED after fix)

Required: full snapshot/restore mapping with real fields, repro with nonempty relations, public from published snapshot, HTTP publish→change/restore→GET old→republish→GET new, archive removes/restore creates no removal, history + ordering, no invented data, scheduled/shared impact.

Repro before fix (recorded):
- New `test_project_snapshot_with_nonempty_relations_regression` with Project + CaseStudyDetails + Evidence + Collaborator + Funding → `_build_full_content_snapshot(project,'project')` → `AttributeError: 'ProjectCaseStudyDetails' object has no attribute 'solution'` (first hit; same root as reported `affiliation` — wrong field names for details/evidence/collaborators/funding + wrong `funding_entries`).

Fixes (BACKEND, with documented allowlist extension for `apps/api/api.py` in packet spec + queue):
- `apps/api/admin_content.py` `_serialize_project_case_study`: real fields only (details depth/problem/constraints/technical_decisions/trade_offs/outcomes_summary/lessons_learned/testing_summary with snake+camel aliases; evidence label/value/source/last_verified/visibility ordered by id; collaborators name/role/publication_approved; funding via `funding_items` funder/grant_id/publication_approved). Removed solution/impact/architectureNotes, kind/title/url/doi/evidenceType/weight/sourceReference, affiliation/url/is_approved/position, grantName/funderName/awardNumber/url/isApproved/position.
- Restore: real fields, `funding_items`, date parsing for last_verified, visibility gating, approved-only filtering, case-study get_or_create with depth validation, skip empty funder, series M2M from snapshot fields (not live), ordered by id.
- `apps/content/published.py` `materialize_published_item`: attach `_published_project_case_study` + `_published_snapshot_data` (scalar-only no longer sufficient).
- `apps/api/api.py` `ProjectDetailOut` resolvers (extension reason recorded): evidence/collaborators/funding/case_study prefer frozen snapshot when present (public/approved-only, date parsing, SimpleNamespace for case-study), else live. No route/schema shape change.
- Tests: repro test above (now asserts no `solution`/`evidenceType`/`affiliation`/`grantName`); `tests/test_product_draft_published_isolation.py` +2 HTTP cycle tests (project publish→edit→restore→GET frozen v1→republish→GET v0 with approved-only relations; archive removes + ordering).

Evidence:
- Before: repro 1 failed (AttributeError). After: `test_product_revision_snapshot.py` + `test_product_draft_published_isolation.py` → 12 passed.
- `uv run pytest -k product -q` → 188 passed. `test_product_project_evidence.py` + `test_product_publication_lifecycle_a03.py` → 12 passed (scheduled/shared impact checked; no model/migration change, `makemigrations --check` PASS).
- `ruff` PASS. OpenAPI public/admin hashes unchanged (no schema change); PROVENANCE timestamp churn handled in §6.
- Changed files: `apps/api/admin_content.py`, `apps/content/published.py`, `apps/api/api.py` (extension), `tests/test_product_revision_snapshot.py`, `tests/test_product_draft_published_isolation.py`. No new migration (no model change). Preview `funding_entries` typo in `views_preview.py` noted as remaining (outside allowlist, preview packet scope, not fixed here to avoid scope creep).

Review result: REVISE findings closed, now IMPLEMENTED_UNREVIEWED (needs owner re-review). Dependencies (12 PU-04/05/06 + evidence) are IMPLEMENTED_UNREVIEWED, not accepted → gate remains closed (correct; do not accept unrelated to unblock).

## ۵. PU-07-runner (ROOT, REVISE → IMPLEMENTED_UNREVIEWED after fix)

Finding: `remove_revocations` return ignored in normal publish cleanup and resume cleanup → false succeeded possible.

Repro before fix (recorded, isolated mocks):
- `test_remove_revocations_failure_blocks_success_normal_path` (queued not_requested with affectedPaths, remove→False, build/swap succeed) → before: True (succeeded), expected False.
- `test_remove_revocations_failure_blocks_success_resume_path` (running active same rev, not_requested, remove→False, no rebuild) → before: True, expected False.
- `python -m unittest discover -s Infra/staging -p test_rebuild_product.py -k *remove_revocations*` → 2 failed (AssertionError True is not false).

Fixes (ROOT, within allowlist):
- `Infra/staging/rebuild-product.py`: both paths now `if not remove_revocations(...): return fail("REMOVAL_FAILED")` (no rollback after successful swap — keep new active, report failure for retry; resume same). No succeeded on write/apply/probe failure (already fail-closed: EDGE_DENY_FAILED, BUILD_FAILED, SITEMAP/PAGEFIND_FAILED, VALIDATION_FAILED, 409 claim).
- `Infra/staging/test_rebuild_product.py`: +2 regression tests above.
- `Docs/08-operations/PRODUCT-PUBLISHING-RUNBOOK.md`: document publish-cleanup fail-closed + resume same (REMOVAL_FAILED, no stale-deny success).

Evidence:
- After: repro 2 → OK. Full `python -m unittest discover -s Infra/staging -p test_rebuild_product.py` → 29 passed (27 +2).
- Success/retry/worker-cut/last-good covered by existing tests (all 29 pass): successful_publish, revoke_before_rebuild, edge_deny_failure_aborts, build_failure_rollback (preserves rev-initial), duplicate_idempotent, A01 split (revoked vs affected, legacy fallback, republish clears), A03 claim/validation/sitemap/pagefind/terminal-noop/resume-after-cut/held-elsewhere, A02 file-vs-probe (stale edge fails, reload/validate fail, unreachable probe fails).
- Validation/callback never false-success (409 claim, VALIDATION_FAILED, idempotent terminal). No real ingress hidden: runbook states file-local without probe is not operational acceptance; real-ingress gate remains open. Localhost/mock (127.0.0.1 ThreadingHTTPServer, fake http_client) used only for unit isolation, not claimed as operational.
- Configs: compose/caddy/nginx exist and contain expected blocks (`services:`, `edge_denied`, `/api/v1/internal`); `docker compose config` requires missing `.env.stage` (no secrets committed — correct, not a failure to hide).

Review result: REVISE closed, now IMPLEMENTED_UNREVIEWED. Dependencies PU-07-jobs/PU-23-invalidation are IMPLEMENTED_UNREVIEWED → gate remains closed.

## ۶. قرارداد و پذیرش (بدون جایگزینی کور)

- Backend re-export: public `47980f…` (48 paths), admin `1176c0…` (57), inventory `154a…` (124) — unchanged semantically (no schema shape change from these four; resolvers/project detail return same Schemas). PROVENANCE timestamp churn only.
- Changed accepted file `apps/api/api.py` (project detail snapshot-aware, resolver endpoint untouched): old `d673f3…` → new `42df30…`. Effect re-checked: resolver 33 passed, public/admin hashes unchanged, settings/sync unaffected (different endpoints). Updated in `ACCEPTED-LOCAL-2026-09-06.json` with this report as evidence; old hashes recorded here, old reviews/handoffs kept.
- Changed accepted file `PROVENANCE.json` (timestamp only, same artifacts): old `0a4d0d…` → new `3469b4…`. Updated with same evidence; no semantic contract change.
- CA-01 hashes unchanged (verified). No new ACCEPTED for the four (gates honest): settings/sync remain IMPLEMENTED_UNREVIEWED ready_for_review (deps satisfied after resolver hash update); revisions/runner move REVISE → IMPLEMENTED_UNREVIEWED (deps unsatisfied → not ready, gate open). No unrelated packet accepted to unblock.
- Allowlist extension recorded before execution: `PU-07-revisions.md` + `execution-tasks.json` add `apps/api/api.py` with reason (public relations must come from snapshot; scalar-only materialize insufficient; limited to 4 resolvers).

## ۷. اعتبارسنجی نهایی (واقعی، بدون حذف/skip)

- BACKEND targeted: settings 17 passed; resolver 33 passed; revision_snapshot 6 passed (incl. repro); isolation 6 passed (incl. 2 project HTTP); product -k 188 passed.
- BACKEND full: 892 passed, 1 failed, 0 skipped. The 1 failure is pre-existing `test_provenance_matches_accepted_record` (expects `scaffold-accepted`, has `source-generated-unaccepted`; owned by PU-20-events/OPENAPI-ACCEPTANCE, not these four; file outside our allowlists — not edited, reported honestly).
- BACKEND ruff: PASS. `makemigrations --check`: No changes detected. No new migration (no model change); prior 0005/0031 forward/backward in handoffs remain valid.
- Runner: 29 passed. PUBLIC contract: 9 passed; full unit: 61 files 354 passed; `generate:api-types` PASS; prettier/eslint PASS; `build` PASS (33 pages, Pagefind en/fa, sitemap).
- ADMIN: 121 passed (unaffected, no runtime change).
- Staging configs: parser-level PASS (expected blocks present, no production contact; compose env missing correctly).
- `validate-plan.py`: PASS after §6 updates (structure only, not runtime/deployment acceptance). `git diff --check`: PASS in all four repos (CRLF warnings only).
- Frontend runtime change? PUBLIC runtime unchanged (only fixture/test/types bytes-identical regeneration); no browser flow retest required beyond unit/build. Backend runtime changed (revisions/runner) — covered by HTTP cycle + runner unit isolation on disposable DB; no real ingress claimed.

## ۸. وضعیت پذیرش، آماده‌ها، موانع، uncommitted

- Local acceptance: existing CA-01 + PU-03-resolver remain ACCEPTED (with updated hashes above, history preserved). No new local acceptance for the four (honest gates).
- Ready_for_review (IMPLEMENTED_UNREVIEWED with satisfied deps): PU-03-settings, PU-SYNC-graph (existing, now strengthened). Not ready (deps unsatisfied): PU-07-revisions, PU-07-runner (now IMPLEMENTED_UNREVIEWED, awaiting owner review + dependency acceptance). ready_to_start remains empty (no new work started).
- Remaining blockers: PU-07-revisions/runner dependency chain (PU-04/05/06/evidence/jobs/invalidation) still IMPLEMENTED_UNREVIEWED; real-ingress edge acceptance (A02) open by design; visual/rollout gates open; provenance scaffold-accepted mismatch (PU-20-events scope) open.
- Uncommitted (preserved, no stash/reset/clean): ROOT modified docs + Infra runner/test/runbook; BACKEND modified code/tests/openapi (incl. api.py, published.py, admin_content.py, settings/revision/isolation tests, PROVENANCE); PUBLIC modified sync fixture/test (+ regenerated types identical); ADMIN only docs. No commit/push/merge/deploy performed. Database: disposable test DB only.

Validator PASS is structural only, not runtime or release acceptance.
