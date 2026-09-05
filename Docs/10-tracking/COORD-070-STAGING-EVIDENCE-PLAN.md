# COORD-070 — Staging Evidence Collection Plan (R7)

Task: COORD-070 — "Run draft-leak + CSRF + MFA staging evidence collection".
Board deliverable: "Evidence files in `Docs/10-tracking/`".
Created: 2026-09-02.

**Status: PLAN ONLY — NOT EXECUTED.** No staging environment exists yet
(Docker daemon down; `PUBLIC_STAGING_SITE_URL` unset; `BACKEND-200` staging
artifact open). None of the `R7-<family>-EVIDENCE.md` files named below exist
yet. **Do not mark COORD-070 done.** This document is the collection harness:
probes, PASS criteria, and evidence file names, ready to run once COORD-060's
preconditions (`Docs/10-tracking/COORD-060-STAGING-TOPOLOGY-CHECKLIST.md`, P1–P5)
are satisfied.

**Refreshed 2026-09-04:** `BACKEND-190` closed (712 backend tests pass); admin
browser matrix (ADMIN-290) shipped — but the staging _live_ rows below still
require the deployed environment.

## Evidence layers

| Layer                              | Environment                                                          | What it proves                                                   | Status                  |
| ---------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------- |
| Disposable-env smoke (BACKEND-180) | Django test client on `config.settings.test` / disposable PostgreSQL | Server-side boundaries only                                      | 3/3 pass — exists today |
| Staging evidence (this plan)       | Deployed staging stack behind the reverse proxy                      | Real cookie flags, proxy headers, host routing, browser behavior | Not executed            |

Per `Back-End/docs/quality/INTEGRATION-TEST-PLAN.md`: disposable-env tests do
**not** substitute for browser acceptance.

## Automated smoke commands available today

| Repo                  | Command                                        | Gated on                                                                                 |
| --------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Back-End              | `uv run pytest tests/test_staging_smoke.py -v` | Runs on disposable settings; backend `tests/test_staging_smoke.py`                       |
| Front-End/public-site | `npm run test:smoke`                           | `PUBLIC_STAGING_SITE_URL` set; otherwise reports skipped (`PUBLIC-320-STAGING-SMOKE.md`) |
| Front-End/admin-panel | ADMIN-300 integrated staging smoke             | Not yet scaffolded (open in `Front-End/admin-panel/TASK-LIST.md`)                        |

## Evidence families

Each family: the exact probe, the PASS criterion, and the evidence file to
produce under `Docs/10-tracking/`.

### 1. Draft-leak privacy — `R7-draft-leak-EVIDENCE.md`

- Probe: on staging, unauthenticated requests against every public API family;
  confirm records in `draft`/`not-public` state never appear on the public
  surface (seed guarantee from BACKEND-070: 85 records, zero published leak).
  Valid preview-share token must open a draft outside any session; the public
  surface must not expose the same draft.
- Map: backend chain step 11 (200 + `no-store`, sanitized body) + PUBLIC-320
  `npm run test:smoke` + manual browser check.
- PASS: zero draft/not-public records in any public response; preview reachable
  only via a valid unexpired token; browser captures attached.
- Evidence file: `Docs/10-tracking/R7-draft-leak-EVIDENCE.md`.

### 2. CSRF — `R7-csrf-EVIDENCE.md`

- Probe: state-changing admin call without `X-CSRFToken` from the deployed
  staging origin; then a call with the header.
- Map: backend chain step 7 (`403 CSRF_FAILED`; enforcement in
  `apps/api/admin_common.py::_check_csrf`) + ADMIN-300 when scaffolded.
- PASS: `403 CSRF_FAILED` without header; success with header; `csrftoken`
  cookie observed with `Secure`/`SameSite` through the proxy (header capture per
  COORD-060 checklist).
- Evidence file: `Docs/10-tracking/R7-csrf-EVIDENCE.md`.

### 3. MFA — `R7-mfa-EVIDENCE.md`

- Probe: enrollment via SPA API (`/auth/mfa/status` → `/auth/mfa/confirm`),
  sign-in with enrolled MFA without OTP, then with a valid OTP.
- Map: backend chain steps 5, 6, 9 + ADMIN-300 / ADMIN-090 browser flow.
- PASS: recovery codes issued (hashed at rest, shown only during generation per
  `Docs/03-contracts/AUTH-CONTRACT.md`); `401` without OTP; `200 otpVerified=true`
  with OTP; browser shows the OTP prompt and then the dashboard.
- Evidence file: `Docs/10-tracking/R7-mfa-EVIDENCE.md`.

### 4. Session expiry — `R7-session-expiry-EVIDENCE.md`

- Probe: sign in, force/await session expiry, then call `/auth/me` and load an
  admin route with the stale session.
- Map: backend chain step 8 (expired row → `401`) + ADMIN-300 / ADMIN-100.
- PASS: stale session returns `401` and the SPA lands on sign-in; re-auth works;
  no privileged action succeeds on the stale session.
- Evidence file: `Docs/10-tracking/R7-session-expiry-EVIDENCE.md`.

### 5. Contact delivery — `R7-contact-delivery-EVIDENCE.md`

- Probe: submit the public contact form via the no-JS HTML path and via the JSON
  path on staging; repeat with a foreign `Origin`/`Referer`.
- Map: `test_contact_smoke_html_json_cross_origin_and_non_persistence` (HTML 200
  - one email; JSON 200 `{ok:true}`; cross-origin 400 with no email; no message
    body in `AuditLog`) + manual browser submission against the proxy.
- PASS: both paths deliver exactly one message through the staging-configured
  transport (delivery confirmed by the transport owner); foreign-origin POST
  rejected with no delivery; nothing persisted.
- Evidence file: `Docs/10-tracking/R7-contact-delivery-EVIDENCE.md`.

### 6. Preview expiry — `R7-preview-expiry-EVIDENCE.md`

- Probe: request a preview share URL after its token expires.
- Map: `test_preview_share_expiry_smoke` (410) + browser capture.
- PASS: expired token shows the expiry page (410); response carries
  `noindex`/`noarchive`/`no-store` (`apps/content/views_preview.py`); no draft
  body leaks.
- Evidence file: `Docs/10-tracking/R7-preview-expiry-EVIDENCE.md`.

### 7. Media boundary — `R7-media-boundary-EVIDENCE.md`

- Probe: upload via the admin API, then fetch the file via the `/media/` proxy
  path in its inactive and active states.
- Map: backend chain step 12 (201, inactive by default; active 200 / inactive 404) + browser check.
- PASS: inactive file returns 404 through `/media/`; activating it yields 200;
  upload starts inactive by default; no inactive file is publicly reachable.
- Evidence file: `Docs/10-tracking/R7-media-boundary-EVIDENCE.md`.

### 8. Backup/restore drill — `R7-backup-restore-EVIDENCE.md`

- Probe: execute the restore-drill checklist in
  `Back-End/docs/operations/BACKUP-RESTORE.md` ("Restore-drill checklist — NOT
  yet drilled"; R7-gated): dump with recorded size → restore into a freshly
  recreated disposable `taha_platform_dev` → `pg_restore --exit-on-error` →
  media copy with matching file count → `migrate --plan` reports no planned
  operations → `/health/` returns `"status": "ok"` and `"db": "ok"`.
- Map: the drill checklist itself (BACKEND-160 documented commands); no
  frontend smoke involved.
- PASS: every checklist checkbox checked with commands + output recorded against
  R7, per the workspace rule that a backup is accepted only when it restores
  into an isolated environment (`Docs/08-operations/BACKUP-RESTORE-RUNBOOK.md`).
- Evidence file: `Docs/10-tracking/R7-backup-restore-EVIDENCE.md`.

## Execution order

1. COORD-060 preconditions P1–P5 satisfied; routing table + proxy config accepted.
2. Families 1–7 on the deployed staging stack (backend smoke first, then browser
   captures); family 8 may run against the disposable profile once Docker is up.
3. Record each `R7-<family>-EVIDENCE.md` with exact commands, outputs, commits,
   and observed headers; link the set from this file's index below.

## Evidence index (empty — none executed)

| Family               | Evidence file                     | Status       |
| -------------------- | --------------------------------- | ------------ |
| Draft-leak           | `R7-draft-leak-EVIDENCE.md`       | not produced |
| CSRF                 | `R7-csrf-EVIDENCE.md`             | not produced |
| MFA                  | `R7-mfa-EVIDENCE.md`              | not produced |
| Session expiry       | `R7-session-expiry-EVIDENCE.md`   | not produced |
| Contact delivery     | `R7-contact-delivery-EVIDENCE.md` | not produced |
| Preview expiry       | `R7-preview-expiry-EVIDENCE.md`   | not produced |
| Media boundary       | `R7-media-boundary-EVIDENCE.md`   | not produced |
| Backup/restore drill | `R7-backup-restore-EVIDENCE.md`   | not produced |

**Bottom line:** COORD-070 remains OPEN. R7 ("Integrated deployment and smoke
tests pass; drafts remain private; backup and restore are proven on staging")
cannot be claimed from disposable-env evidence alone.
