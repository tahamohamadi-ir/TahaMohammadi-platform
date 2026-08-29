# CI Required Checks

No repository currently has a CI workflow. These are required check names and scope; they become enforced only when each repository implements the workflow and branch protection.

| Repository | Required checks before merge |
|---|---|
| Public site | install lock verification, type/check, build, unit/route tests, visual-atlas exclusion test, accessibility smoke, contract fixture validation, asset-reference verifier, secret/dependency scan |
| Admin panel | install lock verification, type/check, unit/component tests, browser workflow smoke, auth/error fixture validation, accessibility smoke, secret/dependency scan |
| Backend | locked dependency sync, Ruff, pytest, Django check, migration plan, public/admin OpenAPI artifact verification, contract fixture tests, secret/dependency scan |

Each workflow must report the exact commit, keep generated build output out of Git, and fail when required artifacts are missing. A locally successful command does not become a CI result until the workflow has run.
