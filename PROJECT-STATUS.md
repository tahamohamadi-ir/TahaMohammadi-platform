# PROJECT STATUS — tahamohammadi-platform

Living status document for the whole platform: repositories, environments,
server, gates, and a dated changelog of everything done.
**Last updated: 2026-09-11 15:20 −07:00 (server 22:20 UTC).**

> **Update convention (every session):**
>
> 1. Append a new dated entry to §7 (date + hour:minute) for every meaningful
>    change, deploy, decision, or incident.
> 2. Refresh the affected tables in §2/§4/§5/§6 (statuses, releases, containers).
> 3. Never write secret values — record locations only (§9).
> 4. Times use the workspace timezone (−07:00) unless marked UTC; server logs are
>    UTC.

---

## 1. Project map

| Part          | Path                              | Remote (GitHub, org `tahamohamadi-ir`)          | Role |
| ------------- | --------------------------------- | ----------------------------------------------- | ---- |
| Coordination  | `D:\Project\tahamohammadi-platform` | `TahaMohammadi-platform`                      | Docs, governance, infra, task registers |
| Public site   | `Front-End\public-site`           | `TahaMohammadi-platform-FrontEnd-publicSite`    | Astro 7 public experience |
| Admin panel   | `Front-End\admin-panel`           | `TahaMohammadi-platform-FrontEnd-adminPanel`    | React 19 CMS admin |
| Backend       | `Back-End`                        | `TahaMohammadi-platform-backEnd`                | Django 5.2 + Ninja CMS/API |

## 2. Environments

### Local development
- Public: Astro dev/build; Admin: Vite; Backend: `uv run` + Django.
- Local gate commands: `npm test`, `npm run test:a11y|visual|performance|nojs|smoke`,
  `uv run pytest`, `uv run ruff check .`.

### Staging — `https://staging.tahamohamadi.ir`
- Stack: compose project `taha-cms-stage` (`/home/deploy/taha-cms-stage`).
- Database: `taha_stage` (container `taha-cms-stage-db-1`).
- Deploy: push to PUBLIC `main` → workflow **Deploy staging** (build + migrate +
  backup + isolated restore + ingress + smoke).
- Current release: `stage-f23deecd-1ea469ae-6c0d3491` (2026-09-11 14:5x).
- Mail: Mailpit (`taha-cms-stage-mailpit-1`).

### Production — `https://tahamohamadi.ir`
- Stack: compose project `taha-cms-prod`
  (`/home/deploy/taha-cms-stage/deploy/docker-compose.prod.yml`, env `.env.prod`).
- Database: `taha_prod` (container `taha-cms-prod-db-1`) — migrated from the
  legacy production data; test artifacts removed.
- Ingress: managed apex block in the host Compose edge
  (`/home/deploy/cms-repo/infra/caddy/Caddyfile.compose`), upstreams
  `taha-prod-*`; TLS certificates already in the Caddy store.
- DNS: Cloudflare (currently proxied); canonical `https://tahamohammadi.ir`.
- Mail: Mailpit until real SMTP is configured (§8).
- Web content refresh: rebuild `taha-web-prod` + sync the
  `taha-cms-prod_prod_public_html` volume (see §10 commands).

### Legacy (rollback only)
- Stack `taha-cms` from `/home/deploy/cms-repo` (old monorepo), DB `taha_cms`,
  containers `taha-cms-{cms,web,admin,caddy,db}` — untouched since the
  promotion; kept for rollback.

## 3. Server inventory (`taha-nl`)

- SSH: `85.192.29.196:2222`, user `deploy` (key on this machine, see §9).
- Running stacks: `taha-cms` (legacy), `taha-cms-stage`, `taha-cms-prod`,
  `phd-radar`.
- Disk: 30 GB total, ~3.8 GB free (87% used) — monitor.
- Backups: `/home/deploy/taha-cms-stage/backups/` — per-release deploy backups,
  `legacy-20260911-165545` (old DB/media/static) and
  `promotion-20260911-191139` (pre-promotion DBs + Caddy snapshot + checksums).

## 4. Status by area (2026-09-11 15:20)

| Area            | State | Notes |
| --------------- | ----- | ----- |
| Backend         | ✅ | 952 tests, Ruff clean, migrations applied; `9c2c704` (+ CI-only `6c0d349`) |
| Public site     | ✅ live | `f23deec`: graph clarity, authored prose, journey icons, project metadata, About from live API, full-card links + pointer-follow glow |
| Admin panel     | ✅ | 197 unit tests, browser matrix 5/5, CI green; `1ea469a` |
| CI/CD           | ✅ | CI in all three repos with dependency + secret scans; deploy-staging workflow; production updates still manual |
| R7 staging      | ✅ mostly | live smoke 10/10, backup/restore proven, security probes; credential-gated families deferred to R9 |
| R8 quality      | ◐ | all agent gates green; F-01 owner visual review returned revisions — 4 remediation slices shipped; owner re-review pending |
| R9 production   | ◐ | production live on the apex with migrated data; SMTP + owner acceptance remain |

## 5. Current releases

| Repo | `main` (local = remote) | Deployed |
| ---- | ----------------------- | -------- |
| PUBLIC | `f23deec` | staging `stage-f23deecd-…`; production web image tag `prod-507b4bb3` (contains the `f23deec` build — see §11) |
| ADMIN | `1ea469a` | staging + production image `prod-507b4bb3` (admin code `f1cfa37` equivalent) |
| BACKEND | `6c0d349` | staging + production image `prod-507b4bb3` (app code `9c2c704`) |

## 6. Changelog

### 2026-09-11

| Time (−07:00) | Event |
| ------------- | ----- |
| 15:00–15:16 | PUBLIC `f23deec` — full-card stretched links + pointer-follow glow (projects/research/featured); staging deploy green; production web rebuilt + volume synced + verified live (glow vars set, body click navigates) |
| 14:5x | Staging deploy `stage-f23deecd-1ea469ae-6c0d3491` completed; staging smoke registry release |
| 13:43 | Apex Caddy cutover to the production stack (`taha-prod-*`) after fixing the domain spelling (`tahamohamadi.ir`, one “m”); validate + reload OK; staging re-verified 10/10 |
| 12:15–13:00 | Production stack created: `taha_prod` restored from the staging dump (test user/landing removed), images `taha-{cms,web,admin}-prod:prod-507b4bb3` built, `taha-cms-prod` containers healthy, migrations no-op, health/API/pages verified via apex SNI |
| 12:11 | Pre-promotion backups: `promotion-20260911-191139` (legacy + staging DB dumps, media, SHA-256) |
| 11:46 | PUBLIC `507b4bb` — About page now renders the published profile (camelCase API mapping fix; real bio, 2 education + 5 experience entries) |
| 11:11 | PUBLIC `e35f43b` — humanized/localized project metadata (no raw enums), hero media fills its card |
| 10:29 | PUBLIC `53baeba` — journey icons (experience/education) + graph presentation polish |
| 10:19 | PUBLIC `d79391a` — authored prose rendering fix, constellation raster backplate removed, graph labels wrap + hub/child hierarchy |
| 09:55 | Legacy backup (`legacy-20260911-165545`) + migration rehearsal into `taha_prod_migration_probe` (0 errors, no pending migrations); row-level comparison: staging content identical to legacy |
| 08:55 | R9 production migration plan documented (owner decisions: full data migration, controlled merge, same server, promote after testing) |
| morning | README/coordination updates; owner decisions recorded (F-02/F-03/F-05 accepted, screen-reader deferral, queue dispositions) |

### 2026-09-10

| Time (−07:00) | Event |
| ------------- | ----- |
| 12:54 | CI workflows: `setup-uv` major-tag fix; no more Node 20 warnings (PUBLIC `cdd6cf5`, ADMIN `1ea469a`, BACKEND `6c0d349`) |
| 12:48 | Dependency + secret scans added to all three CI workflows (PUBLIC `da0faac`, ADMIN `58ec81c`, BACKEND `b7bfccb`); baselines committed |
| 12:44 | Owner revision round recorded; V2 queue updated (PU-15/PU-03 → IMPLEMENTED_UNREVIEWED, PU-25 → BLOCKED to R9) |
| 12:23 | R7 live evidence files (CSRF, draft-leak, media boundary, contact, backup/restore) + stale registers reconciled |
| 12:11 | Contact delivery probe: `POST /api/contact` → `{ok:true}`, foreign origin 400 (staging Mailpit) |
| 11:02 | Owner deferral decisions recorded (F-02/F-03/F-05 + manual SR non-blocking; §8 signature instructions) |
| 10:23 | R8 live security probes on staging (CSRF 403, admin 401, internal 404) |
| 10:21 | R8 evidence package complete on release set `f3e9032`/`f1cfa37`/`9c2c704`; PUBLIC `601b229` staging smoke pin |
| 09:25 | BACKEND `9c2c704` — Django 5.2.17 + pytest 9.0.3 advisories patched |
| 09:19 | Vitest 4.1.11 upgrade (PUBLIC `6f44298`, ADMIN `f1cfa37`); `npm audit` clean |
| 09:13 | ADMIN `3d42995` / PUBLIC `ddbcef6` — js-yaml advisory patched |
| 08:25 | BACKEND `4e508a8` graph identity + PUBLIC `0a72b7a` desktop graph composition / hero copy |
| 07:52 | BACKEND `9d66096` graph seeded from published research; earlier `f68adfb` home-composition safety seed |
| morning | R8 browser matrix alignment (PUBLIC `f3e9032`), staging deployment green (platform `642de92`, previous day’s ingress fixes) |

### 2026-09-09 and earlier

See git history; highlights: staging ingress isolation (`bead720`, `818f8f5`,
`642de92`), staging deploy pipeline (`507058a`), admin R8 file normalization
(`4c3042b`), content-completion merges (PR #3/#4).

## 7. Pending / next actions

| # | Item | Owner |
| - | ---- | ----- |
| 1 | Real SMTP for production contact delivery (`.env.prod` + recreate `cms`) | Owner (+ agent on request) |
| 2 | F-01 visual review of the four remediation slices; then accepted hashes + §8 signature | Owner |
| 3 | Production deploy workflow (today promotions are manual rebuild + volume sync) | Agent |
| 4 | Remaining visual polish: blog/gallery cards, section spacing on `/fa`, broader concept alignment | Agent (on direction) |
| 5 | Rotate `PREVIEW_SHARE_SECRET` (a value was echoed during server recon) | Owner |
| 6 | Optional: `STAGING_ADMIN_*` secrets + dispatch **Bootstrap staging admin** workflow | Owner |
| 7 | Monitor server disk (87% used) and Cloudflare certificate renewal behind the proxy | Owner |

## 8. Common operations

```bash
# Staging deploy
#   push to PUBLIC main; watch: gh run list (Deploy staging)

# Production web refresh after a verified staging deploy (on taha-nl)
cd /home/deploy/taha-cms-stage
docker build -q --network=host --add-host=tahamohamadi.ir:127.0.0.1 \
  -f deploy/Dockerfile.public \
  --build-arg PUBLIC_SITE_URL=https://tahamohamadi.ir \
  --build-arg PUBLIC_API_BASE_URL=https://tahamohamadi.ir \
  -t taha-web-prod:prod-507b4bb3 .
docker run --rm -v taha-cms-prod_prod_public_html:/target \
  taha-web-prod:prod-507b4bb3 sh -c 'cp -a /usr/share/nginx/html/. /target/'
docker compose -p taha-cms-prod --env-file .env.prod \
  -f deploy/docker-compose.prod.yml up -d --force-recreate web

# Production rollback (ingress)
cp /home/deploy/taha-cms-stage/backups/promotion-20260911-191139/Caddyfile.compose.before-prod-cutover \
   /home/deploy/cms-repo/infra/caddy/Caddyfile.compose
docker exec taha-cms-caddy-1 caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
```

## 9. Access & secret locations (no values)

| Thing | Location |
| ----- | -------- |
| Server SSH | `~/.ssh/config` host `taha-nl` (85.192.29.196:2222, user `deploy`) |
| Staging env | `/home/deploy/taha-cms-stage/.env.stage` (600) |
| Production env | `/home/deploy/taha-cms-stage/.env.prod` (600) |
| GitHub deploy secrets | `STAGING_SSH_*`, `STAGING_APP_DIR` in the PUBLIC repo |
| Admin bootstrap (pending) | `STAGING_ADMIN_EMAIL/USERNAME/PASSWORD` + workflow `Bootstrap staging admin` |
| DB users | `taha_stage`, `taha_prod`, legacy `taha_cms` |
| Owner admin login | user `taha` (legacy password/MFA carry over) |

## 10. Known quirks / risks

- **Prod web image tag**: `taha-web-prod:prod-507b4bb3` now contains the
  `f23deec` build; the tag label lags the content. Next promotion should use a
  fresh `RELEASE_ID` across all three images (or retag) for clarity.
- **Contact mail in production** goes to Mailpit until SMTP is set (no real
  delivery).
- **Cloudflare** is proxied although DNS-only was chosen; origin certificate is
  valid, but renewal behind the proxy needs care.
- **Server disk** at 87%; clean old images/backups before large operations.
- `www.tahamohammadi.ir` redirects to the apex; `http(s)://85.192.29.196`
  also redirects to the apex.
