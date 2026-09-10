# Risk Register

| ID | Risk | Level | Mitigation | Closure evidence |
|---|---|---|---|---|
| RISK-001 | Legacy backend assumptions reference the old monorepo | High | Keep legacy infra inactive; rewrite paths under R1 | New deployment tests pass |
| RISK-002 | API changes drift across three repositories | High | OpenAPI and consumer contract tests | R2 passes in all repositories |
| RISK-003 | Duplicate or unmanaged design files drift from the active visual reference | High | Curated tracked authority, SHA-256 manifest, alias map, deletion map | PS-01 and PS-02 pass |
| RISK-004 | Concept copy or unapproved asset becomes published content | High | Owner content manifest and asset promotion ledger | PS-08 and PS-09 pass |
| RISK-005 | Cross-origin deployment breaks session, CSRF, or MFA | High | Same-origin baseline and staging browser checks | Staging live 2026-09-10: CSRF 403 `CSRF_FAILED`, `Secure`/`SameSite` session cookie flags, HSTS/security headers, admin API 401, internal 404 (`R7-csrf-EVIDENCE.md`); authenticated MFA journey deferred to R9 |
| RISK-006 | Missing font rights or subset coverage breaks bilingual rendering | Medium | Font acquisition plan and computed-style QA | PS-10 closed; computed-font + subset gates green (`public-060`) |
| RISK-007 | Local-only checks are mistaken for CI enforcement | Medium | Required CI checks plus implemented workflows | Workflows implemented and green in all three repositories 2026-09-10; branch protection + in-CI dependency/secret scan wiring owner-pending |
| RISK-008 | Reference copy is mistaken for publishable content | High | Authority order and asset approval register | Owner publication approval recorded |
| RISK-009 | Visual QA becomes false-green | High | Computed-style checks and manual comparison | R8 automated captures 39/39 + full browser matrix 461 pass on `601b2294`; owner compare/sign-off in progress (`COORD-080` F-01) |
| RISK-010 | Root coordination documents lack a remote | Medium | Keep a local Git repository; create a governance remote before team scaling | Remote configured at `tahamohamadi-ir/TahaMohammadi-platform` (2026-08-29) |
