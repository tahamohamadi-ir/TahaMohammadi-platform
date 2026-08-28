# Risk Register

| ID | Risk | Level | Mitigation | Closure evidence |
|---|---|---|---|---|
| RISK-001 | Legacy backend assumptions reference the old monorepo | High | Keep legacy infra inactive; rewrite paths under R1 | New deployment tests pass |
| RISK-002 | API changes drift across three repositories | High | OpenAPI and consumer contract tests | R2 passes in all repositories |
| RISK-003 | Reference copy is mistaken for publishable content | High | Authority order and asset approval register | Owner publication approval recorded |
| RISK-004 | Visual QA becomes false-green | High | Computed-style checks and manual comparison | R8 evidence complete |
| RISK-005 | Root coordination documents lack a remote | Medium | Keep a local Git repository; create a governance remote before team scaling | Remote configured and pushed |
