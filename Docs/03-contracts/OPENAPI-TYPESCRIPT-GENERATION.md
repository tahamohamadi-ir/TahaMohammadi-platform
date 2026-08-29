# OpenAPI → TypeScript Generation

Status: **active contract** (COORD-040, 2026-08-29).

This document binds the accepted OpenAPI snapshots to deterministic TypeScript type output in each frontend repository. It does not grant permission to invent API fields, routes, or error shapes beyond the locked schemas in `OPENAPI-ACCEPTANCE.md`.

## Authority chain

| Layer | Document / artifact |
|---|---|
| Acceptance gate | `OPENAPI-ACCEPTANCE.md` |
| Artifact rules | `OPENAPI-ARTIFACT-CONTRACT.md` |
| Canonical client paths | `API-CONTRACT.md` |
| Consumer fixtures | `CONTRACT-FIXTURE-PATHS.md` |

## Source schemas (Back-End)

Generate types only from the **accepted** snapshot files in the backend repository. Paths below are relative to `Back-End/`.

| Surface | Repository path | OpenAPI version | Path count |
|---|---|---|---|
| Public | `docs/contracts/openapi/current/public-openapi.json` | `0.4.0` | 40 |
| Admin | `docs/contracts/openapi/current/admin-openapi.json` | `0.1.0` | 47 |

Workspace-relative paths:

- `Back-End/docs/contracts/openapi/current/public-openapi.json`
- `Back-End/docs/contracts/openapi/current/admin-openapi.json`

Supporting inventory (not a type-generation input): `Back-End/docs/contracts/openapi/current/endpoint-inventory.md`.

## Locked SHA-256 hashes

These values are copied exactly from `OPENAPI-ACCEPTANCE.md`. Any drift reopens PS-05 and blocks adoption of regenerated client types until a new acceptance record is written.

| Artifact | SHA-256 |
|---|---|
| `public-openapi.json` | `0f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5` |
| `admin-openapi.json` | `1328f8244c5541f225648082891a0a1244961c0dead6692488992ac8c7606f09` |
| `endpoint-inventory.md` | `618ab18826875a5f27357ab87a3917082291d2e8610959b18aa2f936a7f3aa96` |

Accepted backend commit at lock time: `82e3984520154b60146009ae4a0d21eb5c30373e` (`config.settings.development`).

## Generator tool

Use **`openapi-typescript`** (not a hand-maintained stub). It emits schema-derived `paths`, `components`, and operation types without inventing runtime client code.

Recommended dev dependency (pin in each frontend lockfile when implementing PUBLIC-090 / ADMIN-050):

```bash
npm install --save-dev openapi-typescript
```

### Exact generation commands

Run from the owning frontend repository root. Verify the source hash **before** writing output (see Hash pins below).

**Public site** (`Front-End/public-site/`):

```bash
npx openapi-typescript ../../Back-End/docs/contracts/openapi/current/public-openapi.json -o src/generated/public-api.ts
```

**Admin panel** (`Front-End/admin-panel/`):

```bash
npx openapi-typescript ../../Back-End/docs/contracts/openapi/current/admin-openapi.json -o src/generated/admin-api.ts
```

Optional npm scripts (add to each repo `package.json` when types are first generated):

```json
{
  "scripts": {
    "generate:api-types": "openapi-typescript <schema-path> -o <output-path>"
  }
}
```

Use the repository-specific schema and output paths from the commands above. Do not commit generated files until the hash pin matches the accepted row in this document.

## Output paths (generated — do not edit by hand)

| Repository | Generated types | Producer task |
|---|---|---|
| `Front-End/public-site/` | `src/generated/public-api.ts` | PUBLIC-090 |
| `Front-End/admin-panel/` | `src/generated/admin-api.ts` | ADMIN-050 |

Rules:

- Treat `src/generated/**` as build input produced from the accepted schema only.
- Public types expose canonical `/api/` families per `API-CONTRACT.md`; deprecated alias paths in the schema are not client authority.
- Admin types are for authenticated `/api/v1/admin/` adapters only; never fetch admin OpenAPI anonymously in CI or local scripts.

## Hash pin files

Each frontend repository stores a single-line SHA-256 pin for its schema source. CI and local pre-generate checks compare the backend snapshot hash to this file.

| Repository | Pin file | Expected value |
|---|---|---|
| `Front-End/public-site/` | `contracts/openapi.public.sha256` | `0f672693de28ed33286789e5119eb3226c062693fb15168b1aba5513c257c0a5` |
| `Front-End/admin-panel/` | `contracts/openapi.admin.sha256` | `1328f8244c5541f225648082891a0a1244961c0dead6692488992ac8c7606f09` |

Pin file format: one lowercase hex SHA-256 string, optional trailing newline, no other content.

Example verification before generation (POSIX shell):

```bash
expected=$(cat contracts/openapi.public.sha256)
actual=$(sha256sum ../../Back-End/docs/contracts/openapi/current/public-openapi.json | awk '{print $1}')
test "$expected" = "$actual"
```

Replace paths and pin filename for the admin repository.

## Regeneration workflow when hashes change

1. **Detect drift** — Backend export, OpenAPI access tests, or frontend pin check reports a hash mismatch against `OPENAPI-ACCEPTANCE.md` or a repo pin file.
2. **Stop adoption** — Do not merge regenerated `src/generated/*.ts` until PS-05 is re-evidenced.
3. **Regenerate backend snapshots** — From `Back-End/`, run `scripts/export_openapi.py` (or the documented export path) under `config.settings.development`; update `PROVENANCE.json`.
4. **Re-run access tests** — `tests/test_public_openapi.py` and `tests/test_admin_openapi.py` (9 checks: anonymous public + verified staff-plus-OTP admin).
5. **Update acceptance docs** — New hashes, path counts, versions, and backend commit in `OPENAPI-ACCEPTANCE.md`; review deltas in `OPENAPI-REVIEW-REPORT.md`.
6. **Update workspace pins** — Set new values in this document and in each frontend `contracts/openapi.*.sha256` file.
7. **Regenerate TypeScript** — Run the `npx openapi-typescript` commands above in `public-site` and `admin-panel`.
8. **Refresh consumer fixtures** — Update or add examples under the paths in `CONTRACT-FIXTURE-PATHS.md`; run contract fixture validation in CI.
9. **Record handoff** — Task board / release evidence notes new commit, hashes, and commands run.

Until step 5 completes, regenerated types are **review artifacts only**, not scaffold-accepted client input.

## Related tasks

| Task ID | Repository | Depends on this doc |
|---|---|---|
| PUBLIC-090 | `Front-End/public-site/` | Public command, output path, public hash pin |
| ADMIN-050 | `Front-End/admin-panel/` | Admin command, output path, admin hash pin |
| PUBLIC-310 | `Front-End/public-site/` | Contract fixture paths |
| BACKEND-140 | `Back-End/` | Schema hash compatibility tests |
