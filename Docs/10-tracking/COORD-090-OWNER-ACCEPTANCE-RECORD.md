# COORD-090 — Owner Production Acceptance Record (Template)

Task: COORD-090 — "Owner production acceptance record".
Board deliverable: "Owner sign-off logged".
Created: 2026-09-02.

**Status: TEMPLATE ONLY — NOT EXECUTED. No sign-off recorded.** Production
deployment is not authorized until R8 passes
(`Docs/08-operations/DEPLOYMENT-RUNBOOK.md`), and R8 is not passed (see
`Docs/10-tracking/COORD-080-R8-SIGNOFF-PACKAGE.md`). Every value below is a
placeholder. This record is completed only after real production deployment and
smoke results exist; agents must not fill it.

Prerequisites per `Docs/05-delivery/RELEASE-GATES.md` R9: tagged artifacts are
immutable; deployment and rollback commands are verified; owner acceptance is
recorded; production smoke tests pass.

## 1. Release commits and hashes (3 repositories)

| Repository | Remote (PROJECT-MANIFEST)                    | Release tag | Commit SHA | Artifact hash | Recorded by |
| ---------- | -------------------------------------------- | ----------- | ---------- | ------------- | ----------- |
| PUBLIC     | `TahaMohammadi-platform-FrontEnd-publicSite` | ____        | ____       | ____          | ____        |
| ADMIN      | `TahaMohammadi-platform-FrontEnd-adminPanel` | ____        | ____       | ____          | ____        |
| BACKEND    | `TahaMohammadi-platform-backEnd`             | ____        | ____       | ____          | ____        |

Immutability confirmation: tags pushed and verified as immutable — [ ] Yes / [ ] No — verified by: ____

## 2. Production migration record

Deployment order per `Docs/08-operations/DEPLOYMENT-RUNBOOK.md`:

| Step                                           | Evidence               | Result   |
| ---------------------------------------------- | ---------------------- | -------- |
| Pre-deploy production DB + media backup taken  | backup id/stamp: ____  | [ ] done |
| Backward-compatible backend deployed           | commit: ____           | [ ] done |
| Reviewed migrations applied                    | migration list: ____   | [ ] done |
| `migrate --plan` reports no pending operations | output captured: ____  | [ ] done |
| Rollback command verified                      | command + result: ____ | [ ] done |

## 3. Production smoke results

Repeat the browser flows proven on staging (COORD-070 evidence set) against
production:

| Check                                         | Expected                             | Result |
| --------------------------------------------- | ------------------------------------ | ------ |
| `GET /health/`                                | 200, `status: ok`, `db: ok`          | ____   |
| Public home EN/FA over HTTPS                  | 200, correct `lang`/canonical        | ____   |
| Public contact submission                     | delivered, honest response           | ____   |
| Admin sign-in (+ MFA if enrolled)             | session + CSRF behavior per contract | ____   |
| Draft privacy (published-only public surface) | zero draft leak                      | ____   |
| `/media/` active-only boundary                | active 200 / inactive 404            | ____   |

Run by: ____ — Date: ____ — Raw output archived at: ____

## 4. Monitoring and backups confirmation

- [ ] Backup schedule active and matches the accepted retention plan — confirmed by: ____
- [ ] Restore capability proven in the R7 drill (`R7-backup-restore-EVIDENCE.md` exists) — confirmed by: ____
- [ ] Monitoring/health alerting in place — confirmed by: ____
- [ ] Rollback readiness recorded (DEPLOYMENT-RUNBOOK step 8) — recorded at: ____

## 5. Owner acceptance

I confirm the production deployment, smoke results, monitoring, and backup state
above have been reviewed and accepted.

- Owner name: ____
- Owner signature: ____
- Date: ____

**Bottom line:** COORD-090 remains OPEN. No owner sign-off is logged; nothing on
this page is evidence of a production deployment.
