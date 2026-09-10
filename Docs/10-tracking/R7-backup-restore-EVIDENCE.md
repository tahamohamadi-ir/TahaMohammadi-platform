# R7 Backup + Restore Drill Evidence

Two drills exist: the live-staging drill (current release, below) and the
2026-09-05 disposable-profile drill (preserved at the end).

## Live staging drill — release `stage-601b2294-f1cfa37d-9c2c7045`

**Status: PASS** — executed automatically by the staging deploy workflow, which
fails the release if any verification below fails.

**Release:** `stage-601b2294-f1cfa37d-9c2c7045` (PUBLIC `601b2294` / ADMIN
`f1cfa37d` / BACKEND `9c2c7045`).

**Workflow run:** `Front-End/public-site` Deploy staging run **34507930950**
(2026-09-10, success). Log line: `Staging release
stage-601b2294-f1cfa37d-9c2c7045 deployed with isolated ingress and restore
verification.`

### Backup artifact set

Written to `$STAGING_APP_DIR/backups/<release-id>/` on the staging host
(path value lives in the `STAGING_APP_DIR` repository secret; not printed):

| Artifact                                       | Producer / assertion                                |
| ---------------------------------------------- | --------------------------------------------------- |
| `database.dump`                                | `pg_dump -Fc`; non-empty assert                     |
| `media.tar`                                    | `tar -C /app/media`; non-empty assert               |
| `backend.sha` / `admin.sha` / `public.sha`     | exact release SHAs                                  |
| `backend-image.id` / `admin-image.id` / `public-image.id` | `docker image inspect` IDs                |
| `caddy-base.sha256` / `Caddyfile.compose.before` | edge ingress snapshot before managed-block replace |

### Isolated restore proof

| Step                                             | Assertion                                              |
| ------------------------------------------------ | ------------------------------------------------------ |
| Create isolated DB `${POSTGRES_DB}_restore_probe` | `dropdb --if-exists` then `createdb`                  |
| `pg_restore --exit-on-error --no-owner`          | full dump restored without errors                      |
| Table-count equality                             | `source_tables == restored_tables` on `information_schema.tables` |
| `manage.py migrate --plan`                       | contains `No planned migration operations`             |
| `manage.py check`                                | exit 0 on the restored database                        |
| Probe cleanup                                    | restore DB dropped after verification                  |

**PASS assessment:** drill executed and enforced on the current release; no
manual step or credential is required. Scheduled backups, retention, and
monitoring/alerting for the deployed host remain owner actions.

---

## Disposable-profile drill — 2026-09-05 (historical, preserved)

**Date:** 2026-09-05 (Docker daemon available)
**Scope:** the only R7 family executable before a deployed staging host existed
(per COORD-070's own execution order).
**Status:** drill EXECUTED and PASSED.

### Backup (steps 1–4 of the checklist)

| Step                    | Command                                                                                                                                                     | Result                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Stack up                | `docker compose -f docker-compose.dev.yml up -d`                                                                                                            | db healthy, api healthy                                      |
| DB dump (custom format) | `docker exec taha-platform-dev-db pg_dump -U taha_dev -d taha_platform_dev -Fc -f /tmp/taha_platform_dev-20260904-224844.dump` → `docker cp` → container rm | `backup/taha_platform_dev-20260904-224844.dump` **276.6 KB** |
| Media copy              | `Copy-Item -Recurse media backup/media-20260904-224844`                                                                                                     | 112 files copied                                             |
| Config inventory        | tracked git files; commit recorded with the backup                                                                                                          | this repo @ `da1ceac` (Back-End)                             |
| `.env`                  | NOT copied into `backup/` (contains secrets)                                                                                                                | per checklist                                                |

### Restore drill (checklist steps 1–7)

| Step                                                                                      | Command                                                                                                                     | Result                                                  |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Stop api (release connections)                                                            | `docker compose stop api`                                                                                                   | stopped                                                 |
| Drop + recreate DB                                                                        | `psql -c "DROP DATABASE IF EXISTS taha_platform_dev"` / `CREATE DATABASE … OWNER taha_dev`                                  | `DROP DATABASE` / `CREATE DATABASE`                     |
| Copy dump back                                                                            | `docker cp backup/….dump taha-platform-dev-db:/tmp/restore.dump`                                                            | done                                                    |
| Restore                                                                                   | `docker exec taha-platform-dev-db pg_restore -U taha_dev -d taha_platform_dev --no-owner --exit-on-error /tmp/restore.dump` | **OK (no errors, exit-on-error clean)**                 |
| Remove temp dump                                                                          | `docker exec … rm /tmp/restore.dump`                                                                                        | done                                                    |
| `manage.py migrate --plan` (settings `config.settings.local` + disposable `DATABASE_URL`) | **No planned migration operations.**                                                                                        | checklist criterion                                     |
| API back up + health                                                                      | `compose up -d api` → `GET /health/`                                                                                        | **200** `{"status": "ok", "db": "ok", "contact": "ok"}` |

Note: `compose stop api` (not `down`) was used so the named volume/network
stayed intact; after the destructive drop/recreate the api container was
started again and answered healthy.
