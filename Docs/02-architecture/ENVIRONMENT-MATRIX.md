# Environment Matrix

| Environment | Data | Secrets | Public indexing | Purpose |
|---|---|---|---|---|
| Local | Fixtures or local database | Local `.env` only | Disabled | Development |
| Test | Disposable database | CI secrets | Disabled | Automated verification |
| Staging | Sanitized or staging data | Staging secret store | Disabled | Integration and acceptance |
| Production | Production data | Production secret store | Enabled | Public service |

Production data must not be copied into local development.
