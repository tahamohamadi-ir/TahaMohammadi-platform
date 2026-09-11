# R9 Legacy Backup Evidence — tahamohammadi.ir

**Status: COMPLETE** — legacy production backed up in place; no destructive action
taken on the old stack.

## Where the old production actually runs

- Host: `taha-nl` (85.192.29.196:2222, user `deploy`) — the same server that
  also hosts the new staging stack (`taha-cms-stage`).
- Legacy stack project: `taha-cms` from `/home/deploy/cms-repo`
  (`Taha-personal-platform.git`, HEAD `76526c2`, 2026-09-05).
- Legacy database container: `taha-cms-db-1` (postgres:17-alpine), database/user
  `taha_cms`.
- Legacy app containers: `taha-cms-cms-1`, `taha-cms-web-1`,
  `taha-cms-admin-1`, `taha-cms-caddy-1`.
- The host Caddy serves the `tahamohammadi.ir` block for the legacy stack.
- DNS note: `tahamohammadi.ir` currently resolves to `213.176.74.133`, which is
  unreachable on 80/443 from both the agent network and the server itself; the
  domain move will replace this record.

## Backup artifacts

Directory on the staging host:
`/home/deploy/taha-cms-stage/backups/legacy-20260911-165545/`

| Artifact               | Size  | SHA-256                                                          |
| ---------------------- | ----- | ---------------------------------------------------------------- |
| `database.dump`        | 543K  | `055d92304f8604180211be9e9047e8ae3455308a31dea3d2562ef28fe90379b4` |
| `media.tar`            | 10K   | recorded in `media.tar.sha256`                                    |
| `web-static.tar`       | 91M   | recorded in `web-static.tar.sha256` (old built site)              |

Also recorded in the directory: legacy image tags (`legacy-cms-image.txt`,
`legacy-web-image.txt`), legacy repo HEAD (`legacy-repo-head.txt`), and the
resolved apex DNS at backup time (`notes.txt`).

## Legacy data inventory (published unless noted)

| Model                         | Rows |
| ----------------------------- | ---- |
| `content_article`             | 4    |
| `content_project`             | 6    |
| `content_publication`         | 6    |
| `content_profile`             | 2 (en/fa) |
| `content_landing`             | 2 (en/fa home) |
| `content_research_statement`  | 2    |
| `content_research_topic`      | 6    |
| `composition_compositionpage` | 1    |
| `users`                       | 1 (`taha`, staff+superuser) |
| `siteconfig_localizedsitesettings` | 0 |
| `media_media`                 | 0 (no CMS media records; media dir empty) |
| `content_seed_record`         | 28 (seed provenance rows) |

## Rehearsal result (Phase 2)

- Restore into `taha_prod_migration_probe` on `taha-cms-stage-db-1`:
  `pg_restore` exit 0, 0 errors.
- New backend migrations on the restored legacy schema:
  **"No migrations to apply."**; `migrate --plan` → **No planned migration
  operations**; `manage.py check` clean.
- Row-level comparison vs the staging database: `content_article`,
  `content_project`, `content_publication`, `content_landing` (home rows),
  `content_research_statement`, `content_research_topic`, `content_profile`,
  `composition_compositionpage` are **identical including content hashes and
  update timestamps** — staging was seeded from this exact legacy data and has
  no later owner edits.
