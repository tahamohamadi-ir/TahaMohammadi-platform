# Contract Fixture Paths

Status: **active contract** (COORD-050, 2026-08-29).

This document registers where **backend-approved DTO examples** and **error-shape fixtures** live for public and admin consumers. Fixtures support tests and adapters; they are not runtime configuration and must not contain production data or invented API fields.

Authority: `OPENAPI-ARTIFACT-CONTRACT.md`, `ERROR-COMPATIBILITY-MATRIX.md`, accepted schemas in `OPENAPI-ACCEPTANCE.md`. Type generation rules: `OPENAPI-TYPESCRIPT-GENERATION.md`.

## Layer model

| Layer | Role | May invent fields? |
|---|---|---|
| Backend fixtures | Authoritative examples derived from accepted OpenAPI and observed responses | No — must match accepted schema or documented matrix row |
| Frontend consumer fixtures | Test inputs copied from or validated against backend fixtures | No |
| Generated types | `src/generated/public-api.ts`, `src/generated/admin-api.ts` | No — generator output only |

## Backend — authoritative fixtures

Repository: `Back-End/`. Paths relative to repository root.

| Directory | Purpose | Populated by |
|---|---|---|
| `tests/fixtures/contracts/public/` | Published-projection JSON examples for canonical public families (`/api/articles`, `/api/profiles`, etc.) | BACKEND-130 |
| `tests/fixtures/contracts/admin/` | Admin DTO examples for authenticated workflows (session, content, media, …) | BACKEND-130 |
| `tests/fixtures/contracts/errors/` | Documented error bodies per `ERROR-COMPATIBILITY-MATRIX.md` (admin `AdminError`, public 404 `detail`, contact JSON/HTML failures) | BACKEND-130 |

Naming convention: `{operation-or-shape}.{status}.json` (example: `profiles-about.get.404.json`, `admin-error.validation.422.json`).

OpenAPI access fixtures (anonymous public + verified staff-plus-OTP admin) remain in backend tests (`tests/test_public_openapi.py`, `tests/test_admin_openapi.py`); they gate schema export acceptance but are not duplicated here.

## Public site — consumer fixtures

Repository: `Front-End/public-site/`. Paths relative to repository root.

| Directory | Purpose | Populated by |
|---|---|---|
| `tests/fixtures/contracts/responses/` | Public response examples used in unit/route/contract tests | PUBLIC-310 |
| `tests/fixtures/contracts/errors/` | Public error normalization cases (profile not found, contact failure, unknown safe failure) | PUBLIC-310 |

Each file must either:

- match a backend fixture byte-for-byte, or
- record in the test harness which backend fixture hash it was validated against.

Schema drift checks compare consumer fixtures to the public OpenAPI hash pin in `contracts/openapi.public.sha256` (see `OPENAPI-TYPESCRIPT-GENERATION.md`).

## Admin panel — consumer fixtures

Repository: `Front-End/admin-panel/`. Paths relative to repository root.

| Directory | Purpose | Populated by |
|---|---|---|
| `tests/fixtures/contracts/responses/` | Admin workflow response examples (auth, content, media, …) | ADMIN tasks paired with BACKEND-130 |
| `tests/fixtures/contracts/errors/` | Admin error matrix cases (`code`, `message`, optional `fields`) | ADMIN-070, ADMIN-290 |

Schema drift checks compare consumer fixtures to the admin OpenAPI hash pin in `contracts/openapi.admin.sha256`.

Admin fixtures must never be generated from anonymously fetched admin OpenAPI; use backend-approved files or disposable verified staff-plus-OTP test paths only.

## Error compatibility fixtures

Minimum set aligned with `ERROR-COMPATIBILITY-MATRIX.md` (implement under each repo `tests/fixtures/contracts/errors/`):

| Matrix row | Suggested fixture basename | Owner repo |
|---|---|---|
| Admin `AdminError` | `admin-error.json` | Backend → admin consumer copy |
| Public profile not found | `profile-not-found.404.json` | Backend → public consumer copy |
| Public contact JSON failure | `contact.post.error.json` | Backend → public consumer copy |
| Public contact HTML 422 | `contact.post.validation.html` (fixture snippet or recorded hash reference) | Backend → public consumer copy |
| Framework validation (unknown safe failure) | `framework-validation.unhandled.json` | Backend only until accepted in OpenAPI |

## Workspace-relative quick reference

```text
Back-End/tests/fixtures/contracts/
  public/
  admin/
  errors/

Front-End/public-site/tests/fixtures/contracts/
  responses/
  errors/

Front-End/admin-panel/tests/fixtures/contracts/
  responses/
  errors/
```

## Verification gates

| Check | When |
|---|---|
| Fixture JSON validates against accepted OpenAPI components | PUBLIC-310, ADMIN-290, BACKEND-130 |
| Error fixtures match `ERROR-COMPATIBILITY-MATRIX.md` rows | CI contract fixture validation |
| Hash pin matches `OPENAPI-ACCEPTANCE.md` before fixture refresh | Any schema regeneration (see `OPENAPI-TYPESCRIPT-GENERATION.md`) |

## Related tasks

| Task ID | Scope |
|---|---|
| BACKEND-130 | Create backend authoritative fixtures |
| BACKEND-140 | Schema hash compatibility tests |
| PUBLIC-310 | Public contract fixture tests vs OpenAPI |
| ADMIN-070 / ADMIN-290 | Admin error normalizer and browser matrix |
