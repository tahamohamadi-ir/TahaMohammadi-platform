# COORD-060 — Staging Topology Checklist (Browser Smoke Plan)

Task: COORD-060 — "Staging topology checklist against `Docs/02-architecture/DEPLOYMENT-TOPOLOGY.md`".
Board deliverable: "Browser smoke plan written with owners".
Created: 2026-09-02.

**Status: checklist READY — execution BLOCKED.** No staging environment exists yet
(Docker daemon down; `PUBLIC_STAGING_SITE_URL` unset). This document is the written
plan; **no browser evidence has been captured**. Board dependencies `BACKEND-200`,
`PUBLIC-350`, `ADMIN-320` are not complete. `Owner: ____` placeholders are
intentional — assignment is an owner action, not an agent decision.

**Refreshed 2026-09-04:** `BACKEND-190` permission matrix is now CLOSED
(`tests/test_admin_permission_matrix.py`, 712 backend tests pass); the admin
browser matrix (ADMIN-290, mocked-API Playwright) now exists — the staging rows
below still need real-environment browser captures. Preconditions P1–P5 remain
unsatisfied.

## Topology under test

Normative baseline from `Docs/02-architecture/DEPLOYMENT-TOPOLOGY.md`
(same-origin reverse proxy; cross-origin deployment is not accepted without a
separate topology decision):

```text
browser
  -> HTTPS reverse proxy
     -> public static site routes and assets
     -> admin static SPA routes and assets
     -> backend /api/, /api/v1/admin/, /health/, /media/, /preview/
        -> PostgreSQL and approved media storage
```

## Preconditions (all must hold before any row below is executed)

| #   | Precondition                                                                                                                               | State @ 2026-09-02                                                                                              | Assignment  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------- |
| P1  | Staging-ready backend artifact + migration evidence (`BACKEND-200`)                                                                        | Open (`BACKEND-190` permission matrix closed 2026-09-04)                                                        | Owner: ____ |
| P2  | Staging stack running: Docker daemon up, proxy + TLS termination per topology                                                              | Blocked — Docker daemon currently down                                                                          | Owner: ____ |
| P3  | `PUBLIC_STAGING_SITE_URL` set for the public-site staging smoke                                                                            | Unset — `npm run test:smoke` reports skipped (`Front-End/public-site/docs/quality/PUBLIC-320-STAGING-SMOKE.md`) | Owner: ____ |
| P4  | Host/path routing table + proxy configuration accepted (DEPLOYMENT-TOPOLOGY evidence item 1)                                               | Template below, unfilled                                                                                        | Owner: ____ |
| P5  | Staging staff credentials / test fixtures for sign-in + MFA flows                                                                          | Not provided                                                                                                    | Owner: ____ |
| P6  | Same-origin rule holds (no distinct public/admin origins). If ever distinct, an explicit topology decision must replace the baseline first | Baseline unchanged                                                                                              | Owner: ____ |

## Browser-evidence matrix (DEPLOYMENT-TOPOLOGY evidence item 2)

Nine required flows. "Server-side smoke" = `Back-End/tests/test_staging_smoke.py`
(BACKEND-180: 3/3 pass on disposable settings; full backend suite 712 pass). Per
`Back-End/docs/quality/INTEGRATION-TEST-PLAN.md`, disposable-env tests do **not**
substitute for browser acceptance — each row still needs its browser capture.

| #   | Flow           | What to observe in the browser                                                                                                                                                         | Server-side smoke mapping                                                                                                                                                 | Browser smoke mapping                                                                                         | Owner       |
| --- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------- |
| 1   | Sign-in        | HTTPS on canonical host; session cookie carries `Secure`/`SameSite`/`HttpOnly`; bad credentials show an error and do not change the session; valid sign-in reaches the dashboard       | Chain steps 2–4 (`401 AUTH_REQUIRED`, `401 AUTH_FAILED`, `200 mfaEnrolled=false`)                                                                                         | ADMIN-300 (not yet scaffolded); ADMIN-080 browser test                                                        | Owner: ____ |
| 2   | MFA            | Enrollment via SPA API (`/auth/mfa/status` → `/auth/mfa/confirm`) issues recovery codes; OTP prompt shown; no dashboard access without OTP; valid OTP accepted                         | Chain steps 5, 6, 9 (recovery codes issued; `401` without token; `200 otpVerified=true`)                                                                                  | ADMIN-300; ADMIN-090 browser test                                                                             | Owner: ____ |
| 3   | Session expiry | Stale/expired session lands on sign-in; re-auth restores access                                                                                                                        | Chain step 8 (expired row → `401`)                                                                                                                                        | ADMIN-300; ADMIN-100 browser test                                                                             | Owner: ____ |
| 4   | CSRF failure   | State-changing call without `X-CSRFToken` rejected (`403 CSRF_FAILED`); `csrftoken` cookie carries `Secure`/`SameSite` through the proxy; safe call with header succeeds               | Chain step 7                                                                                                                                                              | ADMIN-300; ADMIN-110 browser test                                                                             | Owner: ____ |
| 5   | Admin mutation | Article create returns `201`; draft saved and listed; request carries session cookie + CSRF header; server authorization enforced                                                      | Chain step 10                                                                                                                                                             | ADMIN-300                                                                                                     | Owner: ____ |
| 6   | Public contact | Footer form (no-JS HTML path) and JSON path both deliver; foreign-origin POST rejected; entered values preserved on safe failure per `Docs/03-contracts/ERROR-COMPATIBILITY-MATRIX.md` | `test_contact_smoke_html_json_cross_origin_and_non_persistence` (HTML 200 + one email; JSON 200 `{ok:true}`; cross-origin 400, no email; nothing persisted in `AuditLog`) | PUBLIC-320 `npm run test:smoke` (status-only GETs; probe matrix has no POST) + manual browser form submission | Owner: ____ |
| 7   | Preview        | Valid share token opens a draft outside any session; expired token shows the expiry page; response carries `no-store`/`noindex`/`noarchive`                                            | Chain step 11 (200 + `no-store`, sanitized body) + `test_preview_share_expiry_smoke` (410)                                                                                | Manual browser capture (no public-side automated staging probe exists for preview)                            | Owner: ____ |
| 8   | Media          | `/media/` through the proxy serves active files only; inactive file returns 404; upload starts inactive by default                                                                     | Chain step 12 (201 inactive by default; active 200 / inactive 404)                                                                                                        | Manual browser check against the proxy path                                                                   | Owner: ____ |
| 9   | Logout         | Sign-out clears the session; a following `/auth/me` returns 401; signed-out admin shows sign-in                                                                                        | Chain step 13 (200 → 401 on `/auth/me`)                                                                                                                                   | ADMIN-300; ADMIN-100 browser test                                                                             | Owner: ____ |

## Host/path routing table (template — evidence item 1, must be accepted before execution)

| Path             | Serves                           | Upstream / target | Notes                                  |
| ---------------- | -------------------------------- | ----------------- | -------------------------------------- |
| `/`              | Public static site (Astro build) | ____              | Language gateway + `/{locale}/` routes |
| `/admin/`        | Admin static SPA (Vite build)    | ____              | SPA fallback routing                   |
| `/api/`          | Backend public API               | ____              | Published-only anonymous surface       |
| `/api/v1/admin/` | Backend admin API                | ____              | Session + CSRF protected               |
| `/health/`       | Backend health                   | ____              | 200 body `{status, db, contact}`       |
| `/media/`        | Backend media                    | ____              | Active files only                      |
| `/preview/`      | Backend preview share            | ____              | Token-gated draft access               |

## Header capture checklist (evidence item 3)

- [ ] Canonical host forwarded to Django (proxy `Host`/forwarding configuration) — observed value: ____
- [ ] `x-forwarded-proto` = `https` on every request — observed: ____
- [ ] Session cookie flags `Secure`, `SameSite`, `HttpOnly` — observed: ____
- [ ] `csrftoken` cookie flags `Secure`, `SameSite` — observed: ____
- [ ] `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` configured from the accepted staging host set — values: ____
- [ ] Media/preview/rebuild callback URLs match the accepted host set — observed: ____
- [ ] No CORS middleware present or needed (same-origin delivery) — confirmed: ____

## Execution status

| DEPLOYMENT-TOPOLOGY evidence item                                                        | State @ 2026-09-02               |
| ---------------------------------------------------------------------------------------- | -------------------------------- |
| 1. Exact host/path routing table and proxy configuration                                 | Template only — not accepted     |
| 2. Browser tests for the nine flows                                                      | Not run — blocked on P1–P5       |
| 3. Staging headers (canonical host, HTTPS, cookie `Secure`/`SameSite`, proxy forwarding) | Not captured                     |
| 4. Explicit decision if public/admin are ever served from distinct origins               | N/A — same-origin baseline holds |

## Related evidence

- `Docs/02-architecture/DEPLOYMENT-TOPOLOGY.md` — topology + evidence list
- `Docs/03-contracts/AUTH-CONTRACT.md` — same-origin session/CSRF contract
- `Back-End/docs/quality/INTEGRATION-TEST-PLAN.md` (BACKEND-170) — flow → smoke → browser-evidence mapping
- `Back-End/tests/test_staging_smoke.py` (BACKEND-180) — server-side smoke, 3/3 pass
- `Front-End/public-site/docs/quality/PUBLIC-320-STAGING-SMOKE.md` — public staging smoke harness (skip while `PUBLIC_STAGING_SITE_URL` unset)
- `Front-End/admin-panel/docs/operations/LOCAL-E2E.md` — admin E2E basis for ADMIN-290/300

**Bottom line:** the plan (this checklist) is READY for owner review; execution
remains BLOCKED until P1–P5 are satisfied. COORD-070 consumes this checklist and
is likewise not executable yet.
