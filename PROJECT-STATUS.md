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
- Disk: 30 GB total, ~6.6 GB free (77% used). On 2026-09-13 it hit 99% (421 MB) and blocked a deploy; reclaimed to 9.7 GB by pruning only unused buildx cache + unused staging image tags, then ~6.6 GB after the release builds. ~11 GB of images remain reclaimable if it tightens again — monitor.
- Backups: `/home/deploy/taha-cms-stage/backups/` — per-release deploy backups,
  `legacy-20260911-165545` (old DB/media/static) and
  `promotion-20260911-191139` (pre-promotion DBs + Caddy snapshot + checksums).

## 4. Status by area (2026-09-12 23:49)

| Area            | State | Notes |
| --------------- | ----- | ----- |
| Backend         | ✅ | 952 tests, Ruff clean, migrations applied; `9c2c704` (+ CI-only `6c0d349`) |
| Public site     | ✅ live | `f23deec`: graph clarity, authored prose, journey icons, project metadata, About from live API, full-card links + pointer-follow glow; local (unpushed): portal world integrated + frozen `79a15f1` |
| Admin panel     | ✅ | 197 unit tests, browser matrix 5/5, CI green; `1ea469a` |
| CI/CD           | ✅ | CI in all three repos with dependency + secret scans; deploy-staging workflow; production updates still manual |
| R7 staging      | ✅ mostly | live smoke 10/10, backup/restore proven, security probes; credential-gated families deferred to R9 |
| R8 quality      | ◐ | all agent gates green; F-01 owner visual review returned revisions — 4 remediation slices shipped; owner re-review pending |
| R9 production   | ◐ | production live on the apex with migrated data; SMTP + owner acceptance remain |

## 5. Current releases

| Repo | `main` (local = remote) | Deployed |
| ---- | ----------------------- | -------- |
| PUBLIC | `7a5c495` | staging `stage-7a5c495a-1ea469ae-6c0d3491`; **production `prod-7a5c495a`** (PW-1 portal world + PW-2 language entry); previous production `prod-507b4bb3` preserved as rollback (`taha-rollback-web:20260913T111001Z`) |
| ADMIN | `1ea469a` | staging + production image `prod-507b4bb3` (admin code `f1cfa37` equivalent; also tagged `prod-7a5c495a` for release-id alignment) |
| BACKEND | `6c0d349` | staging + production image `prod-507b4bb3` (app code `9c2c704`; also tagged `prod-7a5c495a` for release-id alignment) |

## 6. Changelog

### 2026-09-13

| Time (−07:00) | Event |
| ------------- | ----- |
| 02:00–10:08 | PUBLIC — **PW-2 language-entry transition** implemented and released. Two blockers found and fixed before the release gate could pass: (1) a real race where `data-gateway-state="ready"` was published before the entry listeners existed — proven on a cold cache, a `pointerenter` right after `ready` was lost 5 of 6 times, which is what made PW-2 e2e test 11 flaky (the window itself was benign: a click there is a plain native navigation), fixed by publishing `ready` only once the controller and listeners are wired; (2) CI `Format check` failed on the first push because hand-edited files were never run through prettier (the documented pitfall) — fixed format-only in `7a5c495`. `window.__tmStallGatewayEntry` kept as the one documented test seam but hardened to `writable:false, enumerable:false, configurable:true`. Gates: ESLint 0; `tsc` 0 new errors in PW-2 files; vitest 482/482; build 42 pages; PW-2 e2e 11/11; scene-polish 9/9; ca07 9/12 (its 3 documented `.gw__title` failures); wp40-gateway 2/5 — **proven pre-existing** by running the same spec against the clean PW-1 baseline worktree `79a15f1` (identical 3 failures) |
| 09:52 | Git: PW-2 committed `0188e79` + format fix `7a5c495`, pushed to PUBLIC `main` (`f23deec..7a5c495`); this also carried the previously-unpushed frozen PW-1 `79a15f1`. CI on `7a5c495`: **success** |
| 10:00 | **DEPLOYMENT BLOCKED (server disk).** Root `/` was at 99% (554 MB free, later 421 MB). The staging deploy failed with CI's own evidence: `failed to update builder last activity time: write /home/deploy/.docker/buildx/activity/…: no space left on device`. No production change was made. Also discovered: production was still **pre-PW-1** (`portal-centered-*` fingerprints, `/portal/tahamohammadi-portal-v1.4.glb` → 404), so a deploy would land PW-1 + PW-2 together |
| 11:00–11:12 | **Disk recovery (owner-authorized: disposable Docker build/staging space only).** `docker buildx prune -f` freed 641.5 MB (421 MB → 929 MB). Then 126 unused images removed explicitly by tag with an in-use guard — 41 `taha-web-stage:*` + 85 `taha-cms-stage:*`/`taha-admin-stage:*` — 0 skipped, 0 failed → **9.7 GB free (66%)**. KEEP SET verified intact: all running-container images, `taha-web-prod:prod-507b4bb3`, caddy/postgres/redis/mailpit, phd-radar runtime images, legacy `taha-release-*`; all 20 containers untouched; prod/stage web restarts=0. No `docker system prune`, no volume prune, no rollback artifact or unrelated data touched |
| 11:12–11:19 | **Staging deploy PASSED** (re-ran the existing "Deploy staging" workflow on `7a5c495`) → `taha-web-stage:stage-7a5c495a-1ea469ae-6c0d3491`. Staging verified externally: `/`, `/en/`, `/fa/` 200; frozen GLB byte-identical (`b4c11427…`, 1,588,376 B); fingerprint `portal-world-*` with no `portal-centered-*`; Playwright on staging 6/6 — one canvas + zero console errors, desktop dark EN navigation, 390×844 FA, 430×932 EN, reduced motion (travel 0), no-WebGL native fallback. Disk after staging 7.7 GB |
| 11:19–11:26 | **Production deployed and verified.** Backup first: `.env.prod` copy + 74 MB `public_html` volume tarball (`sha256 21961a9f…`) + rollback images tagged `taha-rollback-{web,cms,admin}:20260913T111001Z`; `prod-507b4bb3` left untouched. Built `taha-web-prod:prod-7a5c495a` from the verified `7a5c495` source tree (`sha256:d7e2ffa1…`), **only the `web` service recreated** — cms/admin/db/mailpit untouched. External: `/` 200, `/en/` 200, `/fa/` 200, `www` 301 unchanged, TLS valid, **GLB MATCH** (1,588,376 B, `b4c11427…`), fingerprint `portal-world-*`; Playwright on production **6/6 passed**. Disk after deploy 6.6 GB free |
| — | Rollback target (no build required): `RELEASE_ID=prod-507b4bb3` in `.env.prod` + re-sync the volume from `taha-web-prod:prod-507b4bb3` + `up -d --force-recreate web` |

### 2026-09-12

| Time (UTC+07:00) | Event |
| ------------- | ----- |
| 03:30–04:16 | PUBLIC (local, uncommitted) — Portal Web Integration Phase 1: approved v1.3.1 portal GLB integrated into the language gateway (`src/lib/visual/portal-scene.ts`, rewritten `GatewayPortal.astro`, assets under `public/portal/`); dark/light runtime themes, runtime floor + light rig + restrained glow (no post-processing), on-demand rendering with offscreen suspension and frame-budget fallback; semantic language links unchanged; no language-entry transition yet (Phase 2) |
| 04:16 | Gates: ESLint clean; 478 unit tests pass across 89 files (incl. new `portal-scene.test.ts`); `astro build` 42 pages; gateway Playwright specs 20/23 (3 failures are a pre-existing backend-settings dependency: `.gw__title` requires live site settings, reproduced on the pre-change tree); web screenshots (desktop/tablet/mobile, both themes) in `Design-Assets/portal/validation/web/` |
| 09:50 | PUBLIC (local, uncommitted) — Portal Web Integration Phase 1.1: full-viewport environment; removed the hero-slot framing/mask (layered gateway composition: fixed full-viewport canvas + raster fallback below, atmosphere overlays, brand layer, language controls embedded over the floor, floating theme toggle); CSS page background matched to the WebGL world color per theme; composition-aware camera (portal ≈50% viewport width desktop, threshold anchored ≈72%, height clamps, mobile near-full width) with floor/backdrop extending to every viewport edge; full-viewport fallback cover; GSAP lag-smoothing disabled so the bounded arrival settles in wall time on slow renderers |
| 09:52 | Gates: ESLint clean; 479 unit tests pass (89 files); `astro build` 42 pages; gateway Playwright specs 18/21 (same 3 pre-existing settings-dependent failures); screenshots `portal_fullviewport_*` (desktop/tablet/mobile × dark/light) + full-viewport fallback in `Design-Assets/portal/validation/web/` |
| 10:07 | PUBLIC (local, uncommitted) — hardening: removed the global `gsap.ticker.lagSmoothing(0)` side effect; the bounded arrival now enforces a scoped 4.2s wall-clock deadline inside `gateway-motion.ts` (kills the tween, snaps to settled state, clears on dispose); measured software-GL settle 4.4s after ready; gateway specs 18/21 again (same 3 pre-existing); lint + visual unit tests + build green; no visual change |
| 12:38 | PUBLIC (local, uncommitted) — PW-1.2 material polish + fallback parity: v1.4 stone re-bake (bake-time meso contrast ×1.2, bump ×0.7; normal/roughness 2048) exported as `tahamohammadi-portal-v1.4-preview.glb` (948,252 B; WIP blend `portal-export-source-v1.4-wip.blend`); frozen master, v1.3.1 GLB and v1.3.1 textures untouched; web runtime adopts the v1.4-preview GLB; fallback parity via new `portal-world-dark/light.png` (1920×1080 renders of the same world; promoted-asset registry + ledger rows added; `GATEWAY_ATMOSPHERE_ASSETS` remapped); light threshold halo restrained; gates: lint clean, 479 unit tests (89 files), build 42 pages, gateway e2e 18/21 (3 pre-existing settings failures) |
| 22:10 | PUBLIC (local, uncommitted) - pre-freeze audit: exported `tahamohammadi-portal-v1.4-preview2.glb` (1,588,376 B) with per-image formats (basecolor JPEG 2048 sRGB; normal PNG 1024 lossless; roughness PNG 1024 lossless as metallicRoughness; identical structure to v1.3.1). Audit correction: stone normal/roughness maps are 1024, not 2048, and v1.3.1/v1.4-preview embedded them as heavily compressed JPEG (normal 31 KB) - to be fixed by adopting preview2 at freeze. One targeted environment refinement applied (dark floor/fog/backdrop horizon: floor 0.0125, roughness 0.30, fog 0.0058, atmosphere 0.42) plus brand-mark clearance fix (tablet node collision); 8 versioned finalcheck screenshots captured; gates: lint clean, 479 unit tests, build 42 pages, gateway e2e 18/21 (same 3 pre-existing) |
| 22:55 | PUBLIC (local, uncommitted) - PW-1 PORTAL WORLD INTEGRATION = FROZEN: runtime asset frozen as `public/portal/tahamohammadi-portal-v1.4.glb` (1,588,376 B, SHA-256 B4C11427..., byte-identical to the audited v1.4-preview2; basecolor JPEG 2048 sRGB + normal/roughness PNG 1024 lossless; 22 meshes/32 nodes/19 mats/13,888 unique-mesh tris); v1.3.1, v1.4-preview and v1.4-preview2 retained; accepted performance tradeoff (0.95 -> 1.59 MB, lossless non-color maps); freeze screenshots `portal_freeze_*` (6 web + 2 fallback) in Design-Assets/portal/validation/web; gates: lint clean, 479 unit tests, build 42 pages, gateway e2e 18/21 (3 documented pre-existing settings failures); docs updated (portal README + export manifest pw1_freeze) |
| 23:49 | PUBLIC — PW-1 COMMITTED: frontend `79a15f1` (portal scene module + full-viewport gateway, frozen `tahamohammadi-portal-v1.4.glb` with retained versions, fallback-parity stills, gateway spec updates; 21 files) and workspace `1ca22dd` (status + promotion ledger); both unpushed. Independent re-verification (23:30–23:49): ESLint clean; 479/479 unit tests (89 files); `astro build` 42 pages; gateway e2e 18/21 reproduced — the 3 failures are `.gw__title`/“Taha” assertions, and the mechanism is now recorded (`src/pages/index.astro:82` renders the title only when the API site name exists, so builds without live settings cannot satisfy them; `index.astro` is unchanged from `f23deec`); fresh 1440×900 dark+light captures against the running preview (PID 22324, untouched) match the freeze evidence within raster noise (mean abs diff <= 0.28/255) and the served GLB hashes to B4C11427... |

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

- **Light-theme pier seam (severity unverified)**: a ~2 px near-black vertical
  line (luminance ~34 on a ~200 field) at x≈833–834, y≈473–608 in the 1440×900
  light capture, on the right pier only (the mirrored position is clean). It is
  present in the PW-1.1 and pre-freeze captures and reproduces in the live build,
  so it is not a freeze regression; most likely a panel-joint/geometry seam
  throwing a hard shadow under the raking light-theme sun. Evidence:
  `Design-Assets/portal/validation/web/portal_freeze_light_desktop.png`.
- **Prod web image tag**: `taha-web-prod:prod-507b4bb3` now contains the
  `f23deec` build; the tag label lags the content. Next promotion should use a
  fresh `RELEASE_ID` across all three images (or retag) for clarity.
- **Contact mail in production** goes to Mailpit until SMTP is set (no real
  delivery).
- **Cloudflare** is proxied although DNS-only was chosen; origin certificate is
  valid, but renewal behind the proxy needs care.
- **Server disk**: hit 99% on 2026-09-13 and blocked deploy (ENOSPC in buildx). Reclaimed by removing only disposable buildx cache and unused staging image tags — never `docker system prune`, volumes, rollback artifacts or unrelated stacks. Check `docker system df` before large operations.
- `www.tahamohammadi.ir` redirects to the apex; `http(s)://85.192.29.196`
  also redirects to the apex.
