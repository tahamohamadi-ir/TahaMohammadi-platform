# R7 Backup/Restore Drill Evidence — Disposable Profile (COORD-070 family 8)

**Date:** 2026-09-05 (Docker daemon available)
**Scope:** the only R7 family executable without a deployed staging host (the
backup/restore drill runs against the disposable Docker profile, per
COORD-070's own execution order).
**Status:** drill EXECUTED and PASSED. Checklist in
`Back-End/docs/operations/BACKUP-RESTORE.md` ("NOT yet drilled") — all steps now
checked below. Live-staging backup schedule/monitoring remain owner actions.

## Backup (steps 1–4 of the checklist)

| Step                    | Command                                                                                                                                                     | Result                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Stack up                | `docker compose -f docker-compose.dev.yml up -d`                                                                                                            | db healthy, api healthy                                      |
| DB dump (custom format) | `docker exec taha-platform-dev-db pg_dump -U taha_dev -d taha_platform_dev -Fc -f /tmp/taha_platform_dev-20260904-224844.dump` → `docker cp` → container rm | `backup/taha_platform_dev-20260904-224844.dump` **276.6 KB** |
| Media copy              | `Copy-Item -Recurse media backup/media-20260904-224844`                                                                                                     | 112 files copied                                             |
| Config inventory        | tracked git files; commit recorded with the backup                                                                                                          | this repo @ `da1ceac` (Back-End)                             |
| `.env`                  | NOT copied into `backup/` (contains secrets)                                                                                                                | per checklist                                                |

## Restore drill (checklist steps 1–7)

| Step                                                                                      | Command                                                                                                                     | Result                                                  |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Stop api (release connections)                                                            | `docker compose stop api`                                                                                                   | stopped                                                 |
| Drop + recreate DB                                                                        | `psql -c "DROP DATABASE IF EXISTS taha_platform_dev"` / `CREATE DATABASE … OWNER taha_dev`                                  | `DROP DATABASE` / `CREATE DATABASE`                     |
| Copy dump back                                                                            | `docker cp backup/….dump taha-platform-dev-db:/tmp/restore.dump`                                                            | done                                                    |
| Restore                                                                                   | `docker exec taha-platform-dev-db pg_restore -U taha_dev -d taha_platform_dev --no-owner --exit-on-error /tmp/restore.dump` | **OK (no errors, exit-on-error clean)**                 |
| Remove temp dump                                                                          | `docker exec … rm /tmp/restore.dump`                                                                                        | done                                                    |
| `manage.py migrate --plan` (settings `config.settings.local` + disposable `DATABASE_URL`) | **No planned migration operations.**                                                                                        | ✅ checklist criterion                                  |
| API back up + health                                                                      | `compose up -d api` → `GET /health/`                                                                                        | **200** `{"status": "ok", "db": "ok", "contact": "ok"}` |

Note: `compose stop api` (not `down`) was used so the named volume/network
stayed intact; after the destructive drop/recreate the api container was
started again and answered healthy.

## Acceptance per workspace rule

`Docs/08-operations/BACKUP-RESTORE-RUNBOOK.md`: a backup is accepted only when
it restores into an isolated environment. **Criterion met:** the dump restored
into a freshly dropped/recreated `taha_platform_dev` with
`pg_restore --exit-on-error` clean, zero pending migrations, and a healthy
`/health/`.

## Remaining owner actions (live staging, not this drill)

- Scheduled backups + retention (7 daily / 4 weekly / 12 monthly) against the
  deployed staging/production instances.
- Monitoring/health alerting.
- The other seven COORD-070 families (draft-leak, CSRF, MFA, session expiry,
  contact delivery, preview expiry, media boundary) need the deployed staging
  origin (COORD-060 P2–P5).
