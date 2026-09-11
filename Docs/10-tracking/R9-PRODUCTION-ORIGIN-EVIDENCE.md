# R9 Production Origin Evidence — tahamohammadi.ir

**Status: ORIGIN READY — WAITING FOR CLOUDFLARE DNS SWITCH (owner action).**
Owner decision 2026-09-11: promote now (fresh backups required, second staging
stack afterwards).

## 1. Fresh backups (pre-promotion)

Directory on the staging host:
`/home/deploy/taha-cms-stage/backups/promotion-20260911-191139/`

| Artifact                    | Size | SHA-256                                                          |
| --------------------------- | ---- | ---------------------------------------------------------------- |
| `legacy-taha_cms.dump`      | 543K | `171aad0b8d3c0acc63fcdc7b425a80c7e06e2d6c4013bfc1b7794347c223cf3d` |
| `stage-taha_stage.dump`     | 549K | `3d25676fc1ed53dc6cc6738c48c301e91deb92991f2f547ff311d366c2de8e7d` |
| `legacy-media.tar`          | 10K  | `6e72972c27ca8452af3131e7145ab0f45c17567fb72b18a07be375a904eee2ce` |
| `stage-media.tar`           | 57B… | recorded in `SHA256SUMS.txt`                                      |

The legacy `taha_cms` database and the old stack remain untouched.

## 2. Production database (`taha_prod`)

- Restored from the fresh `stage-taha_stage` dump (pg_restore, 0 errors).
- Test artifacts excluded: landing `staging-acceptance-20260905` and user
  `staging-mfa-test` (+ its OTP device and audit rows).
- Final counts: articles 4, projects 6, publications 6, landings 2, users 1
  (owner `taha`).

## 3. Production stack (`taha-cms-prod`)

- Compose: `/home/deploy/taha-cms-stage/deploy/docker-compose.prod.yml`
- Env: `/home/deploy/taha-cms-stage/.env.prod` (600; copied from staging with
  production hosts and canonical URLs).
- Images: `taha-cms-prod:prod-507b4bb3`, `taha-web-prod:prod-507b4bb3`
  (built with `PUBLIC_SITE_URL`/`PUBLIC_API_BASE_URL=https://tahamohamadi.ir`),
  `taha-admin-prod:prod-507b4bb3`.
- Containers healthy: `taha-cms-prod-{db,cms,web,admin,mailpit}`; migrations
  report no pending operations; `manage.py check` clean.
- Note: email delivery still uses Mailpit (no SMTP provider configured yet);
  `CONTACT_FORM_TO=taha95mohammadi@gmail.com`. Real SMTP is an owner input.

## 4. Ingress cutover (apex)

- Apex block in the active Compose edge replaced with the managed production
  fragment (`deploy/Caddyfile.prod.fragment`) routing to `taha-prod-*`;
  security headers, cache policies and internal-API 404 preserved.
- Pre-cutover backup:
  `backups/promotion-20260911-191139/Caddyfile.compose.before-prod-cutover`.
- Validation inside the edge container passed; `caddy reload` returned OK.
- Staging ingress re-verified after the reload: `staging.tahamohamadi.ir`
  smoke **10/10**.

## 5. Origin verification (apex SNI via 127.0.0.1)

| Check                          | Result |
| ------------------------------ | ------ |
| `/health/`                     | 200 `{"status":"ok","db":"ok","contact":"ok"}` |
| `/en/`                         | 200, title "Taha Mohammadi — Human-Centered Intelligent Systems", hero + journey present |
| `/fa/`                         | 200, Persian title, hero present |
| `/en/about/`, `/en/projects/`, `/en/research/` | 200 |
| `/api/site`                    | 200 |
| `/admin/`                      | 200 |
| `/api/v1/internal/health`      | 404 |
| Canonical                      | `https://tahamohamadi.ir/en/` |
| Security headers               | HSTS, nosniff, X-Frame-Options DENY present |
| Public pages accidental noindex| none |

## 6. Pending (owner)

1. **Cloudflare DNS switch for the apex:** point `tahamohamadi.ir` (A) and
   `www.tahamohamadi.ir` to `85.192.29.196` (the staging host). The Caddy TLS
   store already holds valid certificates for both names, so HTTPS starts
   working as soon as DNS resolves here. DNS-only (grey) is safest for
   certificate renewal; proxied works with the existing origin certificate.
2. Real SMTP credentials for production contact delivery.
3. After DNS propagates: agent runs the public production smoke, records
   `COORD-090` numbers, then creates the separate staging stack.

## 7. Rollback

- Ingress: restore `Caddyfile.compose.before-prod-cutover` to
  `/home/deploy/cms-repo/infra/caddy/Caddyfile.compose` and
  `caddy reload` inside `taha-cms-caddy-1`.
- DNS: point the apex back to `213.176.74.133`.
- The legacy `taha-cms` stack and `taha_cms` database were never modified; the
  production stack is additive (`taha-cms-prod`).
