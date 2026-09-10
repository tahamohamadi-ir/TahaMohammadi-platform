# R7 CSRF Evidence (staging)

**Status: PARTIAL — enforcement and cookie flags proven live; the
authenticated-success leg is credential-gated** (owner decision 2026-09-10:
live admin journey deferred to R9, `COORD-080` F-05).

**Release:** `stage-601b2294-f1cfa37d-9c2c7045`
(PUBLIC `601b2294` / ADMIN `f1cfa37d` / BACKEND `9c2c7045`), 2026-09-10.

No credentials were sent; only unauthenticated probes were executed.

| Probe                                 | Command                                             | Result                                                                                      |
| ------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Login without CSRF                    | `POST /api/v1/admin/auth/login` (valid-shape body)  | **403** `{"code":"CSRF_FAILED","message":"CSRF token missing or invalid."}`                  |
| CSRF seed + cookie flags              | `GET /api/v1/admin/auth/csrf`                       | **200**; `Set-Cookie: csrftoken=…; HttpOnly; Max-Age=31449600; Path=/; SameSite=Lax; Secure` |
| Admin API unauthenticated             | `GET /api/v1/admin/content/schema`, `/auth/me`, `/dashboard/summary` | **401** x3                                                            |
| Internal API boundary                 | `GET /api/v1/internal/health`                       | **404**                                                                                     |
| Admin OpenAPI docs unauthenticated    | middleware gate                                     | **404**                                                                                     |

Proxy/TLS observations: `strict-transport-security: max-age=31536000;
includeSubDomains; preload`; the `Secure` cookie proves HTTPS was forwarded
through the proxy; `x-frame-options: DENY`, `x-content-type-options: nosniff`,
`referrer-policy: same-origin`, `cross-origin-opener-policy: same-origin`,
`x-robots-tag: noindex, nofollow, noarchive` all present.

**PASS assessment:** enforcement leg PASS (`403 CSRF_FAILED` without header;
cookie flags correct through the edge). The "success with header" leg requires a
staff session and is deferred with the owner decision. Server-side coverage:
`apps/api/admin_common.py::_check_csrf`, `tests/test_security.py`.
