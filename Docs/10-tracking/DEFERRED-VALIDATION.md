# Deferred Validation

| ID | Validation | Reason | Blocking gate |
|---|---|---|---|
| DEF-001 | Backend full tests | Closed: locked environment installed and 636 pytest tests passed on 2026-08-28 | Closed |
| DEF-002 | PostgreSQL clean migration | Closed: fresh-database forward rehearsal applied 53 migrations, 0 unapplied, with rollback/forward proof (`Back-End/docs/quality/BACKEND-200-STAGING-ARTIFACT-EVIDENCE.md`); staging deploy re-verifies `migrate --plan` each release | Closed |
| DEF-003 | Public visual matrix | Closed: `review:visual` 39/39 captures and full browser matrix 461 passed / 0 failed on release set `f3e9032` (2026-09-10) | Closed |
| DEF-004 | Admin workflow matrix | Closed: mocked-boundary browser matrix 5/5 plus CI e2e on release set `f1cfa37` (2026-09-10) | Closed |
| DEF-005 | Staging restore drill | Closed: deploy workflow backs up database + media, restores into an isolated probe database, verifies table-count equality and `migrate --plan`/`check` on release `stage-f3e90323-f1cfa37d-9c2c7045` (2026-09-10) | Closed |
| DEF-006 | Public/admin OpenAPI artifact export | Closed: `OPENAPI-ACCEPTANCE.md` locks schema hashes; `Back-End/docs/contracts/openapi/current/` provenance is `scaffold-accepted`; 9 endpoint-access tests pass | Closed |
| DEF-007 | Owner content and document sources | Superseded under ADR-0009/0010: owner content authority is the CMS publication flow; owner content acceptance is tracked in `COORD-080` F-01/F-02 | COORD-080 |
| DEF-008 | Font acquisition and subset verification | Closed: font tokens/coverage fixtures exist and the `@foundation` computed-font + subset gates pass (`public-060`) | Closed |
| DEF-009 | CI workflows and branch protection | Partially closed: workflows implemented and green in all three repositories (2026-09-10); branch protection remains an owner GitHub setting | Owner |
