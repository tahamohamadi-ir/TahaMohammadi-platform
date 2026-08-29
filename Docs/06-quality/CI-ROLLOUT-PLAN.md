# CI rollout plan

CI is managed in two explicit phases so no workflow pretends a missing frontend scaffold can build.

## Phase 0 — now, before frontend scaffold

| Repository | Required check | Owner | Trigger |
|---|---|---|---|
| Coordination docs | Agent-kit checksum/alias validation, authority JSON parse, Markdown/link review, `git diff --check` | Documentation maintainer | Every coordination change |
| Backend | `manage.py check`, OpenAPI export/provenance consistency, public/admin OpenAPI fixture tests, Ruff, pytest | Backend maintainer | Every backend change |
| Public/admin repositories | Markdown governance and task-list review only | Frontend maintainer | Every documentation change |

Phase 0 must not add a fake `npm run build` job before the package manager, lockfile, and runtime exist.

## Phase 1 — immediately with each scaffold

| Public site | Admin panel |
|---|---|
| Install from lockfile; typecheck; lint; unit tests; production build; no-JS smoke; route/locale contract fixture; visual baseline artifact | Install from lockfile; typecheck; lint; unit/component tests; production build; authenticated browser fixture; CSRF/OTP/error matrix; visual baseline artifact |

Each workflow must fail if it cannot locate the accepted OpenAPI hash, design authority version, or required environment schema. It must never insert real credentials or owner content into logs/artifacts.

## Phase 2 — integration and release

1. Backend schema compatibility and generated-client drift check.
2. Public visual matrix: two locales, two themes, six widths, 200% zoom.
3. Admin browser matrix: signed out, MFA required, verified, forbidden, validation, stale revision, network failure.
4. Accessibility, dependency/secret scanning, performance budget, staging smoke, and preview/draft-leak checks.
5. Protected branches require Phase 1 checks before merge and Phase 2 release evidence before deployment.

## Ownership and activation checklist

- On scaffold creation, add the exact package-manager setup, cache key, lockfile command, and build/test commands to the matching repository workflow.
- Pin action revisions and Node/Python versions; do not use floating major tags for release-gating checks.
- Enable required status checks and restrict direct pushes only after the workflow has passed on a branch.
- Keep generated visual artifacts short-lived and exclude private owner content.
- Update `CI-REQUIRED-CHECKS.md`, the relevant repository task list, and `PRE-SCAFFOLD-READINESS.md` with each activation result.
