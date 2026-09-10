# CI Required Checks

<!-- PRODUCT-V2.1 -->
V2.1 acceptance adds every independent detail family and the admin→preview→publish→deployed URL→revise→remove journey. Use PU-25-admin-journey, PU-25-public-journey, CA-17 and PU-25-review from EXECUTION.md. Keep FA/EN, light/dark, six widths, keyboard, 200% zoom and no-JS content evidence. Pagefind full-text interaction may require JS; linked collection browsing must remain available. No prior PASS is advanced by this documentation change.
<!-- /PRODUCT-V2.1 -->

All three repositories now implement CI workflows that run on `main`
(2026-09-10): build/unit/design/SEO for the frontends and locked sync, Ruff,
Django check, pytest, OpenAPI provenance, dependency audit
(`npm audit --audit-level=high` / `uv run --with pip-audit pip-audit`) and a
detect-secrets baseline gate for the backend. The secret/dependency scan row is
therefore enforced in CI (`Front-End/public-site` CI run 34522624331; admin and
backend equivalents). Branch protection is an owner GitHub setting.

| Repository | Required checks before merge |
|---|---|
| Public site | install lock verification, type/check, build, unit/route tests, visual-atlas exclusion test, accessibility smoke, contract fixture validation, asset-reference verifier, secret/dependency scan |
| Admin panel | install lock verification, type/check, unit/component tests, browser workflow smoke, auth/error fixture validation, accessibility smoke, secret/dependency scan |
| Backend | locked dependency sync, Ruff, pytest, Django check, migration plan, public/admin OpenAPI artifact verification, contract fixture tests, secret/dependency scan |

Each workflow must report the exact commit, keep generated build output out of Git, and fail when required artifacts are missing. A locally successful command does not become a CI result until the workflow has run.
