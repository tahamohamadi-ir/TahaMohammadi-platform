# Deployment Topology

## Selected baseline

The pre-scaffold baseline is same-origin public delivery through a reverse proxy. This matches the migrated backend production model, which assumes Caddy terminates TLS and Django uses secure same-site session and CSRF cookies. A cross-origin SPA/API deployment is not accepted until a separate CORS, cookie, CSRF, proxy, and browser-test decision replaces this baseline.

```text
browser
  -> HTTPS reverse proxy
     -> public static site routes and assets
     -> admin static SPA routes and assets
     -> backend /api/, /api/v1/admin/, /health/, /media/, /preview/
        -> PostgreSQL and approved media storage
```

## Required rules

- The proxy owns public HTTPS termination and forwards the canonical host/proto to Django.
- Admin and public applications use the same site origin for cookie-authenticated API calls.
- State-changing admin calls include CSRF tokens and rely on server authorization.
- Public contact submissions use the backend’s same-origin policy; form and JSON responses are handled explicitly by the public client.
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, secure-cookie settings, proxy headers, media URL, rebuild callbacks, and preview URLs are configured from the accepted deployment host set.
- No CORS middleware is introduced merely to make an unplanned cross-origin setup work.

## Evidence required before staging

1. Exact host/path routing table and proxy configuration.
2. Browser tests for sign-in, MFA, session expiry, CSRF failure, admin mutation, public contact, preview, media, and logout.
3. Staging headers for canonical host, HTTPS, cookie `Secure`/`SameSite`, and proxy forwarding.
4. Explicit decision if public/admin are ever served from distinct origins.
