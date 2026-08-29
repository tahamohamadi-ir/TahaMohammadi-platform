# Risk Register

| ID | Risk | Level | Mitigation | Closure evidence |
|---|---|---|---|---|
| RISK-001 | Legacy backend assumptions reference the old monorepo | High | Keep legacy infra inactive; rewrite paths under R1 | New deployment tests pass |
| RISK-002 | API changes drift across three repositories | High | OpenAPI and consumer contract tests | R2 passes in all repositories |
| RISK-003 | Duplicate or unmanaged design files drift from the active visual reference | High | Curated tracked authority, SHA-256 manifest, alias map, deletion map | PS-01 and PS-02 pass |
| RISK-004 | Concept copy or unapproved asset becomes published content | High | Owner content manifest and asset promotion ledger | PS-08 and PS-09 pass |
| RISK-005 | Cross-origin deployment breaks session, CSRF, or MFA | High | Same-origin baseline and staging browser checks | PS-07 and R7 pass |
| RISK-006 | Missing font rights or subset coverage breaks bilingual rendering | Medium | Font acquisition plan and computed-style QA | PS-10 passes |
| RISK-007 | Local-only checks are mistaken for CI enforcement | Medium | Required CI checks plus implemented workflows | PS-11 and R8 pass |
| RISK-008 | Reference copy is mistaken for publishable content | High | Authority order and asset approval register | Owner publication approval recorded |
| RISK-009 | Visual QA becomes false-green | High | Computed-style checks and manual comparison | R8 evidence complete |
| RISK-010 | Root coordination documents lack a remote | Medium | Keep a local Git repository; create a governance remote before team scaling | Remote configured and pushed |
