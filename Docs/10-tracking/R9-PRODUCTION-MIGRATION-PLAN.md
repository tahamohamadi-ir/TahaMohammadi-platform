# R9 Production Migration Plan — tahamohammadi.ir

Owner decisions recorded 2026-09-10 (`Docs/05-delivery/concept-alignment-v2/reviews/OWNER-DECISION-2026-09-10.md`):

- Full migration of the old production database into the new platform database.
- Controlled merge with a conflict report (old content + new CMS settings/Home/graph preserved where compatible).
- Production target: the current staging server; the `tahamohammadi.ir` domain moves to it.
- Timing: test the migration first; promote only after R8 passes (F-01 revisions + owner sign-off).
- End state: `tahamohammadi.ir` is the production surface; `staging.tahamohamadi.ir` remains the future-changes environment; the old stack is retired after owner confirmation.
- DNS for both domains is managed in Cloudflare.

## Progress (2026-09-11)

| Phase | State | Evidence |
| ----- | ----- | -------- |
| 0 — Access + inventory | **COMPLETE** | Legacy stack found on the *same* server as staging (`taha-nl`): project `taha-cms` from `/home/deploy/cms-repo`, DB `taha_cms`, containers `taha-cms-{cms,web,admin,caddy,db}`. Apex DNS `213.176.74.133` is unreachable; the domain record must be replaced at promotion. |
| 1 — Backup | **COMPLETE** | `R9-LEGACY-BACKUP-EVIDENCE.md`: DB dump (543K, SHA-256 pinned), media, 91M old static build, image tags, repo HEAD. |
| 2 — Isolated restore rehearsal | **COMPLETE** | `taha_prod_migration_probe` restored with 0 errors; new migrations report **no pending operations**; `manage.py check` clean. |
| 3 — Controlled merge + conflicts | **COMPLETE** | `R9-MERGE-CONFLICTS.md`: content rows identical; only two staging test artifacts to exclude. |
| 4 — Validation on merged data | **IN PROGRESS** | Owner authorized promotion 2026-09-11; origin built and verified (`R9-PRODUCTION-ORIGIN-EVIDENCE.md`); waiting for the Cloudflare DNS switch. |
| 5 — Promotion | pending | DNS switch + public smoke |
| 6 — Post-promotion | pending | second staging stack on the same host |

## Phase 0 — Access and inventory (owner + agent)

1. Owner provides old-server access (SSH or panel) and confirms how the legacy stack runs.
2. Inventory on the old host: running containers/processes, PostgreSQL database name/user, media/uploads path, sizes.
3. Confirm the old stack is reachable for a dump; if the host stays unreachable from the agent network, the owner runs the provided commands.

## Phase 1 — Backup (both sides, checksummed)

1. `pg_dump -Fc` of the old production database; `tar` of the media directory.
2. Record SHA-256 for both artifacts and the source commit/code state of the running old stack.
3. Store the backup on the old host and transfer a copy to the staging server backup area (never only one location).

## Phase 2 — Isolated restore rehearsal

1. Create an isolated database (`taha_prod_migration_probe`) on the new stack.
2. Restore the old dump there and run `manage.py migrate`; `migrate --plan` must report no pending operations.
3. Verify `manage.py check`, `/health/` with the probe DB, and compare record counts, identifiers, locales, and media hashes against the source export.

## Phase 3 — Controlled merge + conflict report

1. Export counts by model and lifecycle state from both databases.
2. Rules: old published records are the content source of truth; new CMS settings, Home composition, and graph versions are preserved unless the owner decides otherwise per conflict.
3. Produce `R9-MERGE-CONFLICTS.md` listing every conflict (slug, locale, model, old vs new) for owner decisions.
4. Apply the merge into a single production database copy; rerun count comparisons.

## Phase 4 — Validation on the merged data

1. Build the public site and admin against the merged database.
2. Run the staging smoke, the browser matrix, and a focused visual capture.
3. Owner reviews the migrated production candidate and records acceptance.

## Phase 5 — Promotion (only after R8 passes)

1. Tag exact release commits in all three repositories; record artifact hashes.
2. Final pre-promotion backup of both databases and media (old and new).
3. Point `tahamohammadi.ir` in Cloudflare to the production stack (low TTL first); keep the old stack untouched and running.
4. Production smoke tests: public EN/FA, admin sign-in, draft privacy, media boundary, contact, health.
5. Record rollback readiness (old stack intact; DNS revert path documented).

## Phase 6 — Post-promotion

1. Owner confirms; old stack is archived/retired (owner action).
2. Re-create a separate staging stack for future changes if promotion reuses the staging host (topology decision pending).
3. Update `COORD-090` with release tags, hashes, migration record, smoke results, and acceptance.

## Gates

- Production promotion is blocked until R8 passes (`DEPLOYMENT-RUNBOOK.md`).
- Every phase records evidence under `Docs/10-tracking/` and updates the task registers.
