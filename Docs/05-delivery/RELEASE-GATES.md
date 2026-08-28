# Release Gates

## R0 — Foundation

- Three repositories track the correct remotes.
- Migration and reference integrity checks pass.
- Canonical documents and agent adapters exist.

## R1 — Backend baseline

- Python 3.12 environment installs from `uv.lock`.
- Ruff and pytest pass.
- Migrations apply to disposable PostgreSQL.
- OpenAPI and endpoint inventories are captured.

## R2 — Contracts

- Public and admin schemas are versioned.
- Consumer contract tests pass.
- Authentication, locale, media, and errors are stable.

## R3–R6 — Product delivery

- Shared components and workflows pass their repository matrices.
- No legacy frontend source is imported.
- No owner content is invented.

## R7 — Staging

- Integrated deployment and smoke tests pass.
- Drafts remain private.
- Backup and restore are proven on staging.

## R8 — Quality

- Accessibility, visual, browser, performance, and security gates pass.
- Every deferral is named, owned, and non-blocking.

## R9 — Production

- Tagged artifacts are immutable.
- Deployment and rollback commands are verified.
- Owner acceptance is recorded.
- Production smoke tests pass.
