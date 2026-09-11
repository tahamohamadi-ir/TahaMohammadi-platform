# R9 Merge Conflict Report — legacy production vs staging

**Result: no content conflicts.** The legacy production database and the new
staging database hold identical content rows (see
`R9-LEGACY-BACKUP-EVIDENCE.md` for the row-level comparison). The merge reduces
to excluding two staging-only test artifacts from the production database.

## Differences found

| Difference                                   | Legacy (`taha_cms`) | Staging (`taha_stage`) | Production decision |
| -------------------------------------------- | ------------------- | ---------------------- | ------------------- |
| Landing `en/staging-acceptance-20260905`      | absent              | present (test record)  | **Exclude** — acceptance-test artifact |
| User `staging-mfa-test`                       | absent              | present (staff)        | **Exclude** — test account |
| `siteconfig_localizedsitesettings`            | 0 rows              | 2 rows (fa/en, seed)   | **Keep staging rows** (new platform needs them) |
| All content tables (articles/projects/publications/profiles/landings/research/composition) | identical rows | identical rows | No action |

Everything else matches exactly, including `updated_at` timestamps
(`content_article` max `2026-08-19 18:23:12+00`, `content_profile` max
`2026-08-18 13:19:24+00`).

## Production database preparation (at promotion time)

1. Take a fresh `taha_stage` dump (so any staging edit made before promotion is
   included) and restore it into a new `taha_prod` database on the staging host.
2. In `taha_prod`: delete landing `staging-acceptance-20260905` and user
   `staging-mfa-test`.
3. Keep the owner user `taha` (staff+superuser); the admin password is the one
   already used on the legacy site (and MFA state carries over from the seeded
   legacy user).
4. Verify counts against `R9-LEGACY-BACKUP-EVIDENCE.md`.
5. The legacy `taha_cms` database and stack stay untouched for rollback.

## Owner confirmation

The exclusion of the two test artifacts follows directly from the owner's
"controlled merge with conflict report" decision; no content conflict requires a
further owner choice. If the owner wants `staging-mfa-test` kept for later MFA
testing, say so before promotion — otherwise it is excluded from production.
