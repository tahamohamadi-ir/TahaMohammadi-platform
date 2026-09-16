# PROJECT STATUS — tahamohammadi-platform

Living status document for the whole platform: repositories, environments,
server, gates, and a dated changelog of everything done.
**Last updated: 2026-09-16 03:35 −07:00 (DNS closeout: apex record verified healthy from the authoritative path; Hero v2 production complete).**

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
- Current release: **`prod-457b7fe7`** (Hero v2, promoted 2026-09-15 — only the web
  service was recreated; previous `prod-7a5c495a` kept as rollback).
- DNS: **resolved and verified (2026-09-16).** The apex `A` record is the single proxied record
  `85.192.29.196` (id `f8921a153bd2b2c386fbf31fa1e481ff`) and the authoritative path now serves the
  Cloudflare edge exactly as `proxied: true` implies: `dale` and `harmony`, over **UDP and TCP**
  with `+norecurse`, return `172.67.220.35` / `104.21.24.197` with the AA flag, TTL 300, and the
  identical SOA serial `2414083257`; `1.1.1.1` and `8.8.8.8` agree; `https://tahamohamadi.ir/en/`
  and `/fa/` return HTTP/2 200. `213.176.74.133` occurs **zero** times in the zone and is no longer
  authoritative (the 2026-09-15 finding was accurate for its date and is now historical/resolved).
  Final record:
  [`Docs/10-tracking/HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](Docs/10-tracking/HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md);
  the original root-cause analysis stays as history in
  [`Docs/10-tracking/PRODUCTION-STABILIZATION-2026-09-15.md`](Docs/10-tracking/PRODUCTION-STABILIZATION-2026-09-15.md).
- Fonts in production are served by the **web container** (`/fonts/<family>/<file>.woff2`) after the
  2026-09-15 route correction; all ten referenced faces return `200 font/woff2`.

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
| R8 quality      | ✅ PASSED | Owner sign-off 2026-09-15 approved R8/F-01 for the Hero v2 revision `457b7fe7…`; all agent gates were already green ([`R8-F01-OWNER-SIGNOFF-2026-09-15.md`](Docs/10-tracking/R8-F01-OWNER-SIGNOFF-2026-09-15.md)) |
| R9 production   | ✅ | Hero v2 promoted to the production stack (`taha-web-prod:prod-457b7fe7`, web only) with restore-verified backups + public smoke green; **apex DNS now verified healthy** from the authoritative path (2026-09-16, direct dale/harmony UDP+TCP, one SOA serial) — see the final closeout; real SMTP remains an owner input |
| Home hero production plan | **Shipped** | 2026-09-15: Hero v2 (four authored stills, static-first Home) is live in the production build; About keeps the interactive graph. Witnesses: [`Design-Assets/hero-v2/validation/production-2026-09-15/`](Design-Assets/hero-v2/validation/production-2026-09-15/README.md) |

## 5. Current releases

| Repo | `main` (local = remote) | Deployed |
| ---- | ----------------------- | -------- |
| PUBLIC | `feat/research-universe-prototype` @ `457b7fe` (7 ahead of `main` `7a5c495`) | staging `stage-457b7fe7-1ea469ae-6c0d3491`; **production `prod-457b7fe7`** (Hero v2 — four authored scroll states, desktop + mobile frame families); previous production `prod-7a5c495a` preserved as rollback (`sha256:d7e2ffa1…`, env snapshot `env.prod.before-20260915T194439Z`) |
| ADMIN | `1ea469a` | staging + production image `prod-507b4bb3` (admin code `f1cfa37` equivalent; also tagged `prod-7a5c495a` for release-id alignment) |
| BACKEND | `6c0d349` | staging + production image `prod-507b4bb3` (app code `9c2c704`; also tagged `prod-7a5c495a` for release-id alignment) |

## 6. Changelog

### 2026-09-16

| Time (−07:00) | Event |
| ------------- | ----- |
| 03:30–03:35 | **DNS CLOSEOUT — apex record verified healthy; Hero v2 production complete.** The last open publication concern (the 2026-09-15 finding that every authoritative nameserver answered the apex `A` with the legacy DNS-only `213.176.74.133`) is resolved by the owner-applied mutation that the stabilization pass specified: the zone now holds exactly **one** apex `A` — `85.192.29.196`, `proxied: true`, id `f8921a15…`, zone `e0fef33e…` — and **zero** occurrences of `213.176.74.133`. Verification from the authorized host (`taha-nl`, read-only, `dig` 9.20.24): `@dale` and `@harmony`, both **UDP and TCP**, `+norecurse` → `NOERROR`, **AA present**, `172.67.220.35` + `104.21.24.197`, TTL 300, and the **identical SOA serial `2414083257`** from both servers (one zone version, no split); AAAA synthesized as `2606:4700:3033::6815:18c5` / `2606:4700:3032::ac43:dc23`; `www` resolves through the same edge; `1.1.1.1` and `8.8.8.8` agree. Public HTTPS: `/en/` 200 (Hero v2 present — `data-hero-sequence-frame-count="4"`), `/fa/` 200, `last-modified: Tue, 15 Sep 2026 19:45:23 GMT` matching the promotion; the ten `/fonts/*.woff2` faces spot-checked `200 font/woff2`. **No DNS mutation, no Cloudflare mutation, no Caddy edit, no deploy/restart/reload, no code change** in this pass. Final record: [`Docs/10-tracking/HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](Docs/10-tracking/HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md) |

### 2026-09-15

| Time (−07:00) | Event |
| ------------- | ----- |
| 13:19–13:29 | **PRODUCTION STABILIZATION — fonts FIXED, DNS root-caused (owner-authorized two-objective pass; no Hero/design/CMS change).** *Fonts:* traced end-to-end — the files were always present in the image, the `prod_public_html` volume, and served `200 font/woff2` by `taha-prod-web`; the prod apex block's `handle /fonts/*` was serving from the Caddy container's own `/var/www/html` (ten flat Vazirmatn files only), so all ten referenced faces 404'd. One route corrected inside the `# BEGIN TAHA PROD MANAGED` section (`root`/`file_server` → `reverse_proxy taha-prod-web:8080` with the existing CORS headers preserved as `header_down`), applied with the deploy workflow's own pattern: backup (`sha256 09ef66aa…`) → candidate → `caddy validate` → swap → `caddy reload` (no rollback needed), applied file `sha256 fa36068e…`. Result: **all ten `/fonts/*.woff2` → 200 `font/woff2`**, zero 404s, zero failed responses. Consequence verified inert: the ten legacy flat `Vazirmatn-*.woff2` in Caddy's dir are no longer apex-reachable, and nothing references them (platform CSS uses only `<family>/<file>`; neither legacy container references any `/fonts/*.woff2`). *DNS:* root cause is **not** split-brain or stale zone data — every authoritative NS (`dale`/`harmony`, and the still-answering old pair `johnathan`/`candy`), both recursives, and both DoH providers agree the apex A = `213.176.74.133`, a DNS-only record pointing at a host that refuses TCP/443, while `www` is proxied and works. No Cloudflare credentials exist on the host (no `CF_*` env, no `dns.providers` plugin), so per authorization the **exact mutation is specified instead of attempted**: apex A → `85.192.29.196` (the `taha-cms-prod` host), **Proxied**, TTL Auto, mirroring `www`. Second owner check: the registrar delegation NS set (zone publishes `dale`/`harmony`; the old pair still answers). Record: [`Docs/10-tracking/PRODUCTION-STABILIZATION-2026-09-15.md`](Docs/10-tracking/PRODUCTION-STABILIZATION-2026-09-15.md) |
| 13:29–13:36 | **Short regression smoke (production edge, DNS-independent, real Chromium).** HTTP `/`, `/en/`, `/fa/`, `/api/site` all 200. Home across desktop-dark / desktop-light / mobile-dark / mobile-light: Hero v2 present (1 sequence), **0 canvas**, all four authored states reached (0 → 0.363 → 0.626 → 1 desktop; 0 → 0.300 → 0.624 → 1 mobile), 0 px horizontal overflow, 0 page errors. Reduced motion: progress fixed at `0.3333` and the rendered crop byte-identical to authored state 2 (`19331d98…`) — no DOM-paint claim made. About: 1 canvas, no Hero v2, 0 px overflow. Smoke `problems` array empty; machine report in `Design-Assets/hero-v2/validation/production-2026-09-15/smoke-report.json`. No commit, push, container or CMS change in this pass |
| 12:39–12:54 | **HERO V2 → PRODUCTION (owner-authorized).** Owner sign-off received for R8/F-01 on the accepted revision (frontend `457b7fe7d0d4ed8e3d1ae12774449c0b3f550d5f`, staging release `stage-457b7fe7-1ea469ae-6c0d3491`, design authority `176ce4a`); recorded in [`Docs/10-tracking/R8-F01-OWNER-SIGNOFF-2026-09-15.md`](Docs/10-tracking/R8-F01-OWNER-SIGNOFF-2026-09-15.md) with R8 → **PASSED** and the promotion gate **OPEN**. Backups first (`backups/promotion-20260915T194439Z`): prod DB `560 501 B` `4bdee1b7…`, media `29972152…`, pre-promotion served payload `103 826 944 B` `75b77dd0…`, legacy `taha_cms` dump `555 112 B` `66a98953…`; the prod dump was **restore-verified** into an isolated probe (113 = 113 tables, `migrate --plan` → no pending operations), then dropped. Promoted with the existing host-side procedure (no new workflow): built `taha-web-prod:prod-457b7fe7` (`sha256:ddf40316…`, 117.9 MB, 71 pages) from the accepted revision with the canonical production build args, replaced the `prod_public_html` payload (463 → 473 files), set `RELEASE_ID=prod-457b7fe7`, and recreated **only the web service** — cms/admin/db/mailpit untouched (`Up 3 days`) |
| 12:50 | **Production verification (browser + network).** Real-browser witnesses against the live site: 4 frames per sequence, all four authored states reached (desktop progress 0 → 0.446 → 0.844 → 1; mobile 0 → 0.346 → 0.642 → 1), hero asset requests **AVIF only** (0 PNG, 0 WebP), desktop receives the desktop family / mobile the mobile family, horizontal overflow **0 px** at desktop + mobile + RTL `/fa/`, sticky journey releases cleanly (desktop 1069 → bottom 1316 of 2216), `prefers-reduced-motion` performs **no scrub journey** (progress frozen at 0.3333 and the held hero crop byte-identical to authored state 2, `19331d98…`; differs from state 0 `36adddde…`), Home has **0** canvas, About keeps **1** canvas (834×718, 28 nodes) with no Hero v2, `/api/site` 200. Public HTTP: `/`, `/en/`, `/fa/` 200 via the Cloudflare edge with `last-modified` matching the promotion. Witnesses + machine report: [`Design-Assets/hero-v2/validation/production-2026-09-15/`](Design-Assets/hero-v2/validation/production-2026-09-15/README.md) (host copy in `/home/deploy/taha-cms-stage/evidence/hero-v2-*`). **Correction applied the same session:** the first reduced-motion screenshot was captured after the script had scrolled (wrong region) and its `visibleFrames` count double-counted `<picture>` wrappers — both retracted, superseded by element-level hero crops and `rm-check.json` ([`CORRECTION.md`](Design-Assets/hero-v2/validation/production-2026-09-15/CORRECTION.md)) |
| 12:54 | **Two findings recorded, deliberately not fixed (owner change freeze).** (1) **Apex DNS is still the legacy record:** authoritative A = `213.176.74.133` (TCP 443 refuses connections) with no AAAA, while the production host's resolver answers with Cloudflare edge addresses — i.e. the domain reaches the new stack only over the proxied path, and the R9 Phase 5 "replace the apex record" step is still open (owner/Cloudflare action). (2) **Fonts 404 on the apex:** the prod Caddy fragment's `handle /fonts/*` serves from `/var/www/html` (Vazirmatn only), so the app's `/fonts/inter/InterVariable*.woff2` and `/fonts/newsreader/Newsreader-Variable*.woff2` requests 404 and typography falls back to system faces — the pre-promotion build referenced the same URLs, the fragment is unchanged since 2026-09-11, and staging serves them fine from its container, so this predates Hero v2 and is **not** attributable to the promotion. Rollback path (no build needed): restore `env.prod.before-20260915T194439Z`, re-sync the volume from `taha-web-prod:prod-7a5c495a`, `up -d --force-recreate web` |

### 2026-09-13

| Time (−07:00) | Event |
| ------------- | ----- |
| (QA-03) | POST-PW2 QA follow-up — `8590642` `test(gateway): provide deterministic site settings for e2e`. Closes the last four environment-dependent gateway failures without touching an assertion. Root cause read from code: `src/pages/index.astro` does `await fetchLocalizedSiteSettings('en')` in its frontmatter (**build time**) and derives the title from `settings?.brandName ?? ''`, while the loader only fetches when `PUBLIC_API_BASE_URL` is set (`canFetchPublicApi()`); a local `astro build` has no `.env`, so `brandName` was empty and `.gw__title` never rendered — while production/staging builds pass `PUBLIC_API_BASE_URL` and reach the CMS, which is why the same assertions passed live. No fixture mechanism existed for the build (the vitest `vi.mock('site-settings-content')` seam only covers unit rendering), so the fix uses the **existing config seam**: `scripts/e2e-site-settings-fixture.mjs` serves only `/api/v1/site/<locale>` from a minimal committed fixture (`tests/fixtures/site-settings/localized-site-settings.fixture.json`, `brandName` taken from the canonical `site.get.200.json`, empty `contentCopy` so every copy fallback stays byte-identical), and `scripts/playwright-web-server.mjs` starts it and passes `PUBLIC_API_BASE_URL` **to the E2E build only**. Nothing in product source changed — `src/lib/site-settings-content.ts` and `index.astro` are untouched and carry no test branch. New `src/gateway-title.contract.test.ts` pins both contract directions (name present → title renders that name; name absent → title omitted and the prompt stays the h1) and forbids hardcoding the personal name or growing a fixture branch. Results: **ca07 12/12** and **wp40-gateway 5/5** (were 9/12 and 4/5), wp40-media 3/3, PW-2 11/11, scene-polish 9/9, a11y 4/4 + 23/23, no-JS 23/23, unit 503/503 (91 files), lint/format 0, build 42 pages, tsc 138 pre-existing with none in changed files. Build parity proven: fixture build emits `<h1 id="gateway-name" class="gw__title">Taha Mohammadi`, normal build emits **0** `gw__title` and keeps `<h1 class="gw__prompt">Choose your language` — the fixture cannot leak. Also corrected the stale `portal-centered-*` fallback comment in `ca07-gateway-scene.e2e.ts` (comment only) |
| (QA) | POST-PW2 QA maintenance — two test-harness cards, **no production change, no deploy**. **CARD-QA-02** `5e5e274` `test(playwright): avoid unsafe ephemeral ports`. Root cause measured, not assumed: this machine's Windows dynamic port range is `Start Port 1024 / 13977 ports`, so the OS `listen(0)` allocation draws from 1024–15000 — which straddles Chromium's restricted list (1723, 2049, 3659, 4045, 4190, 5060/5061, 6000, 6566, 6665–6669, 6679, 6697). One run really did get 1723 and produced 12 bogus `ERR_UNSAFE_PORT` failures that looked like product regressions. Fix extracts `src/test-harness/playwright-port.ts`: candidates come from 20000–59999, Chromium-restricted and reserved (4321) ports are rejected, bindability is proven with `exclusive: true` (on Windows SO_REUSEADDR would otherwise report a busy port as free), attempts are bounded at 30 with an actionable error, and an unsafe `TM_E2E_PORT` pin is refused rather than silently accepted. 17 new unit tests (unit 482→499); three real Playwright startups landed on 35697/56269/47716, all green. **CARD-QA-01** `0de753d` `test(gateway): align wp40 assertions with portal-world assets`. Stale assertions repaired against the frozen PW-1 contract read from the registry (`GATEWAY_ATMOSPHERE_ASSETS` = `portal-world-light/dark`, `intrinsic` 1920×1080), keeping independent literal pins plus an anti-resurrection check and an explicit theme pin so the assertion no longer inherits the system colour scheme. The QA-01D sweep showed the card under-described the blast radius: `wp40-media` also expected `portal-centered-*` (2 tests) and is now fixed; `1672` is still a legitimate emitted width, so `ATMOSPHERE_WIDTHS` was left alone. Result: wp40-media 3/3 (was 1/3), wp40-gateway 4/5 locally — the remaining failure is the documented `.gw__title` build-settings dependency, **proven environmental by running the repaired spec against production: 5/5** |
| 02:00–10:08 | PUBLIC — **PW-2 language-entry transition** implemented and released. Two blockers found and fixed before the release gate could pass: (1) a real race where `data-gateway-state="ready"` was published before the entry listeners existed — proven on a cold cache, a `pointerenter` right after `ready` was lost 5 of 6 times, which is what made PW-2 e2e test 11 flaky (the window itself was benign: a click there is a plain native navigation), fixed by publishing `ready` only once the controller and listeners are wired; (2) CI `Format check` failed on the first push because hand-edited files were never run through prettier (the documented pitfall) — fixed format-only in `7a5c495`. `window.__tmStallGatewayEntry` kept as the one documented test seam but hardened to `writable:false, enumerable:false, configurable:true`. Gates: ESLint 0; `tsc` 0 new errors in PW-2 files; vitest 482/482; build 42 pages; PW-2 e2e 11/11; scene-polish 9/9; ca07 9/12 (its 3 documented `.gw__title` failures); wp40-gateway 2/5 — **proven pre-existing** by running the same spec against the clean PW-1 baseline worktree `79a15f1` (identical 3 failures) |
| 09:52 | Git: PW-2 committed `0188e79` + format fix `7a5c495`, pushed to PUBLIC `main` (`f23deec..7a5c495`); this also carried the previously-unpushed frozen PW-1 `79a15f1`. CI on `7a5c495`: **success** |
| 10:00 | **DEPLOYMENT BLOCKED (server disk).** Root `/` was at 99% (554 MB free, later 421 MB). The staging deploy failed with CI's own evidence: `failed to update builder last activity time: write /home/deploy/.docker/buildx/activity/…: no space left on device`. No production change was made. Also discovered: production was still **pre-PW-1** (`portal-centered-*` fingerprints, `/portal/tahamohammadi-portal-v1.4.glb` → 404), so a deploy would land PW-1 + PW-2 together |
| 11:00–11:12 | **Disk recovery (owner-authorized: disposable Docker build/staging space only).** `docker buildx prune -f` freed 641.5 MB (421 MB → 929 MB). Then 126 unused images removed explicitly by tag with an in-use guard — 41 `taha-web-stage:*` + 85 `taha-cms-stage:*`/`taha-admin-stage:*` — 0 skipped, 0 failed → **9.7 GB free (66%)**. KEEP SET verified intact: all running-container images, `taha-web-prod:prod-507b4bb3`, caddy/postgres/redis/mailpit, phd-radar runtime images, legacy `taha-release-*`; all 20 containers untouched; prod/stage web restarts=0. No `docker system prune`, no volume prune, no rollback artifact or unrelated data touched |
| 11:12–11:19 | **Staging deploy PASSED** (re-ran the existing "Deploy staging" workflow on `7a5c495`) → `taha-web-stage:stage-7a5c495a-1ea469ae-6c0d3491`. Staging verified externally: `/`, `/en/`, `/fa/` 200; frozen GLB byte-identical (`b4c11427…`, 1,588,376 B); fingerprint `portal-world-*` with no `portal-centered-*`; Playwright on staging 6/6 — one canvas + zero console errors, desktop dark EN navigation, 390×844 FA, 430×932 EN, reduced motion (travel 0), no-WebGL native fallback. Disk after staging 7.7 GB |
| 11:19–11:26 | **Production deployed and verified.** Backup first: `.env.prod` copy + 74 MB `public_html` volume tarball (`sha256 21961a9f…`) + rollback images tagged `taha-rollback-{web,cms,admin}:20260913T111001Z`; `prod-507b4bb3` left untouched. Built `taha-web-prod:prod-7a5c495a` from the verified `7a5c495` source tree (`sha256:d7e2ffa1…`), **only the `web` service recreated** — cms/admin/db/mailpit untouched. External: `/` 200, `/en/` 200, `/fa/` 200, `www` 301 unchanged, TLS valid, **GLB MATCH** (1,588,376 B, `b4c11427…`), fingerprint `portal-world-*`; Playwright on production **6/6 passed**. Disk after deploy 6.6 GB free |
| — | Rollback target (no build required): `RELEASE_ID=prod-507b4bb3` in `.env.prod` + re-sync the volume from `taha-web-prod:prod-507b4bb3` + `up -d --force-recreate web` |
| 13:31–13:45 | **RESEARCH UNIVERSE (local prototype) — frontend `924e782` on branch `feat/research-universe-prototype`** (from `f658726`): RU-2C closure, About pointer interaction repaired. Root cause: `stage.setPointerCapture()` was taken on *every* pointerdown inside the interactive stage, so the browser dispatched `click` to the stage instead of the toolbar button underneath — zoom in/out, focus, reset and clear were dead to mouse input in the About region while still working from the keyboard; a drag now starts only from a bare surface, never from a native control. Two WCAG 2.2 AA contrast failures on the universe pages also fixed (`.ru-edge__button` 4.23:1, `.ru-node__kind` 3.49:1), both caught by the existing public-080 crawl once it ran against a published-API build, plus a `details.open = false` force-close that fought the native disclosure. Most of the red in the card was the spec's, not the product's: the About stage sits below the fold, so unscrolled coordinates delivered no pointer events at all. Browser evidence with real pointer input: **About 14/14, Home 11/11**, accessibility crawl **23/23**, no idle render loop (**0 draw calls over 1500 ms**), unit 552/552, lint/format/validate:design green, published-API build 72 pages. Fresh post-fix captures + measurements: `Front-End/public-site/.evidence/research-universe/` (regenerate with `PUBLIC_API_BASE_URL=https://tahamohamadi.ir npm run build && node scripts/capture-research-universe.mjs`), written up in `Front-End/public-site/docs/quality/RESEARCH-UNIVERSE-RU2-EVIDENCE.md`. Reverted the `f658726` E2E fixture-server broadening (it made the hermetic build serve a ready graph and broke 21 unrelated hero specs). **Local only — not pushed, not deployed; visual sign-off pending; Blender decision still pending visual review.** Separate debt, deliberately untouched here: legacy `ca03`/`ca05`/`ca06` `details[open]` failures on the Home hero |
| 14:09–14:40 | **RESEARCH UNIVERSE — RU-3M mobile containment (frontend, local) + RU-3 Blender signature assets (local).** **RU-3M**: the card's `1951×768` canvas is not a cold-load state (a fresh 390×844 load measured `scrollWidth` 375 = viewport, stage 308×623). The reproducible defect is a **viewport change**: shrinking in place left the stage at its desktop width (measured 927px at a 390px viewport, `scrollWidth` 985) and one synthetic `resize` event then grew the canvas to 1390×934. Root cause read from code: a canvas with no CSS size takes its used width from its `width` attribute, and `enhancement.ts applySize()` → `scene-core.ts resize()` → `renderer.setSize(w, h, false)` writes that attribute from `stage.clientWidth` without ever touching styles — so the old width became an intrinsic min-content floor for every ancestor track (stage grid → `.ru-about` → page-family grid → template flex rows → `body`) and the next event re-read the inflated width. `.ru-labels`/`.ru-leaders` were already absolute; only the canvas was exposed. Fix makes CSS own the canvas box (`.ru-about__stage > .ru-canvas` absolute, inset 0, 100%×100%), verified by injecting the same rule and repeating the shrink (485→375 scroll, 927→293 stage). Two more mobile defects fixed: the section repeated the template's page gutter (stage 293–310px against the card's 320–360px target → 340px now) and the canonical view pushed a chip to `left = -18px` inside the stage's `overflow: hidden` (mobile fit padding 1.14 → 1.34, chips capped at 9rem; all four chips inside). Evidence: **About 16/16** (new tests 15/15b/15c: stage 320–360px band, `canvas ≤ stage`, `scrollWidth ≤ innerWidth+2`, every node projecting inside the stage, centroid within 16% of centre, every chip intersecting with text, plus a 1024→390 shrink regression guard), **Home 11/11**, desktop tests 1–14/16/17 unchanged, captures `about-mobile-{dark,light}-fixed.png`, written up in `docs/quality/RESEARCH-UNIVERSE-RU3M-MOBILE-EVIDENCE.md`. **RU-3**: the previous pass left only an unrun builder script (no `.blend`, no GLB, no renders) and two real defects — per-**mesh** normalisation (which would push every internal part out through its own shell) and three fully occluded shells, i.e. the exact "same sphere in three colours" failure the card exists to fix. Rebuilt with authored negative space (segmented housing + lattice; open frame cage + information slabs + 205° arc; split lens + aperture ring + framing fins), group-level normalisation, `hide_render` isolation (the earlier `hide_viewport` isolation made two domain close-ups byte-identical), a render-only floor, and a final mesh-hygiene pass. Measured on a fresh import of the shipped GLB: 14 meshes, **15,914 triangles**, node diameters `CORE` 1.4399 / each domain 1.0, exactly the four `RU_*` material slots, `RU_SIGNATURE_ROOT` hierarchy, and every validation check true (zero-area 191→0, coincident faces 72→0, winding-consistent, no inverted closed normals, no lights/cameras/helpers, scale applied). GLB **847,500 B (828 KiB)**. **Local only — not pushed, not deployed; RU-3 not integrated into Three.js and visual sign-off pending** (documented as `Design-Assets/research-universe/README.md`) |

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
| 2 | ~~F-01 visual review of the four remediation slices; then accepted hashes + §8 signature~~ **COMPLETED 2026-09-15** — owner sign-off recorded, R8 closed, production promoted ([`R8-F01-OWNER-SIGNOFF-2026-09-15.md`](Docs/10-tracking/R8-F01-OWNER-SIGNOFF-2026-09-15.md)) | Owner |
| 3 | Production deploy workflow (today promotions are manual rebuild + volume sync) | Agent |
| 4 | Remaining visual polish: blog/gallery cards, section spacing on `/fa`, broader concept alignment | Agent (on direction) |
| 5 | Rotate `PREVIEW_SHARE_SECRET` (a value was echoed during server recon) | Owner |
| 6 | Optional: `STAGING_ADMIN_*` secrets + dispatch **Bootstrap staging admin** workflow | Owner |
| 7 | Monitor server disk (87% used) and Cloudflare certificate renewal behind the proxy | Owner |
| 8 | ~~Execute the v2 Home plan when assigned~~ **SHIPPED 2026-09-15** — Hero v2 is live in the production build (`prod-457b7fe7`); About keeps the interactive graph | Developer / Blender workflow |

### Documentation changelog — 2026-09-14

| Time (−07:00) | Event |
| --- | --- |
| 10:46 | Created [HERO_PRODUCTION_PLAN_v2.md](HERO_PRODUCTION_PLAN_v2.md) under the owner's revised direction. Replaces v1's mandatory live-3D Home, 26-view render package, EXR/multilayer pipeline, and extensive handoff requirements with one Blender file, four stills, six WebP derivatives, and one focused integration review. Preserves material/light direction, responsive behavior, content boundaries, and web budgets; deeper interaction belongs to About. Verified nine requested sections and local links. v1 preserved; no code, artwork, commit, or deployment produced. |
| 10:38 | Created [HERO_VISUAL_SPEC_v1.md](HERO_VISUAL_SPEC_v1.md) for the owner's document-only request: four-form composition using the three product-authorized research axes, materials, lighting, responsive cameras, 26 rendered review views, export/naming rules, and web budgets. Verified all 17 numbered sections, local document links, and absence of code blocks. This is a separate proposed sphere family, not a relabeling of RU-3 assets. No art generated, product code changed, task acceptance advanced, commit made, or deployment performed. |

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
