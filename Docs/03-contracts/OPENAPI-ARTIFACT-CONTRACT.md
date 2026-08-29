# OpenAPI Artifact Contract

## Required artifacts

| Artifact | Producer | Access condition | Consumer |
|---|---|---|---|
| `public-openapi.json` | Backend public schema endpoint | Anonymous test client | Public site |
| `admin-openapi.json` | Backend admin schema endpoint | Verified staff plus OTP fixture | Admin panel |
| `endpoint-inventory.md` | Backend source plus both schemas | Read-only generation | All repositories |
| TypeScript client/types | Accepted schema version | Deterministic generator (`OPENAPI-TYPESCRIPT-GENERATION.md`) | Owning frontend only |
| Consumer fixtures | Backend-approved DTO examples | No production data | Public and admin tests (`CONTRACT-FIXTURE-PATHS.md`) |

## Versioning rules

- Store artifacts with source commit, generation command, date, SHA-256, and authentication fixture description.
- Validate generated artifacts against the exact backend source commit that produced them.
- A schema artifact never grants a frontend permission to invent a field not present in the accepted projection.
- Admin schemas must not be fetched anonymously in production or documentation automation; use a disposable verified test fixture.
- Breaking changes require a compatibility decision before either frontend adopts them.

## Hash verification and line endings

Accepted artifact SHA-256 values in `OPENAPI-ACCEPTANCE.md`, `PROVENANCE.json`, and frontend hash pins were recorded from **CRLF-encoded** exports. The workspace normalizes OpenAPI JSON to **LF** (`.gitattributes` / `eol=lf`). Drift tests (`Back-End/tests/test_openapi_hash_drift.py`) hash **LF-canonical** file content and prove that re-encoding accepted bytes to CRLF reproduces the recorded acceptance hash. A raw `sha256sum` on the working-tree file may therefore differ (`be8fdbea…` vs `0f672693…`) while content is byte-identical under LF normalization — this does **not** reopen PS-05 acceptance. New acceptance records should prefer LF hashes and note the encoding used at lock time.

## Source-generated review snapshot

The backend may generate non-network review snapshots through `Back-End/scripts/export_openapi.py` into `Back-End/docs/contracts/openapi/current/`. Their `PROVENANCE.json` must state `source-generated-unaccepted`, the backend commit, schema hashes, settings module, and the still-required endpoint-access fixture. A source-generated snapshot is useful for inventory and review, but it does not unblock generated frontend clients by itself. It becomes a scaffold-accepted artifact only when `OPENAPI-ACCEPTANCE.md` locks its exact hashes and cites passing anonymous-public and verified-staff-plus-OTP endpoint tests.

The corresponding route/workflow review and explicit unresolved decisions are recorded in `OPENAPI-REVIEW-REPORT.md`.
