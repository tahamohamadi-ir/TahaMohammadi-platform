# Deferred Validation

| ID | Validation | Reason | Blocking gate |
|---|---|---|---|
| DEF-001 | Backend full tests | Closed: locked environment installed and 636 pytest tests passed on 2026-08-28 | Closed |
| DEF-002 | PostgreSQL clean migration | Disposable database not created yet | R1 |
| DEF-003 | Public visual matrix | Public application not scaffolded yet | R3–R4 |
| DEF-004 | Admin workflow matrix | Admin application not scaffolded yet | R5–R6 |
| DEF-005 | Staging restore drill | New infrastructure not accepted yet | R7 |
| DEF-006 | Public/admin OpenAPI artifact export | Closed: `OPENAPI-ACCEPTANCE.md` locks schema hashes; `Back-End/docs/contracts/openapi/current/` provenance is `scaffold-accepted`; 9 endpoint-access tests pass | Closed |
| DEF-007 | Owner content and document sources | No approved content-manifest entries exist in the new workspace | PS-08 / R4 |
| DEF-008 | Font acquisition and subset verification | No font binaries or subset evidence exist in the workspace | PS-10 / R3 |
| DEF-009 | CI workflows and branch protection | Required checks are documented but not implemented in GitHub Actions | PS-11 / R3–R8 |
