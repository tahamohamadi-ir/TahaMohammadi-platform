# R8 / F-01 — Owner Sign-Off Record and Production Promotion (Hero v2)

**Date:** 2026-09-15 (−07:00; server/UTC 2026-09-15T19:4x)
**Owner decision:** **APPROVED** — owner sign-off given, superseding the prior F-01 `REVISE`
status for the accepted Hero v2 state.
**Accepted release:** frontend `457b7fe7d0d4ed8e3d1ae12774449c0b3f550d5f`
(branch `feat/research-universe-prototype`), outer design authority `176ce4a719624cdc927118c77af2d51653079216`,
staging release `stage-457b7fe7-1ea469ae-6c0d3491`.
**Promotion gate:** **OPEN** (owner gate passed; all other executable R8 gates were already green — see `COORD-080-R8-SIGNOFF-PACKAGE.md`).

This record exists because the owner's sign-off arrived as an explicit written authorization
(OWNER SIGN-OFF + PRODUCTION AUTHORIZATION, 2026-09-15) rather than through the pre-printed
§8 acceptance block in `COORD-080`. Historical evidence in that package is preserved unchanged;
`COORD-080` §8 owner cells remain unfilled by agents, as its own rule requires.

## 1. Owner decision (verbatim scope, condensed)

- R8 / F-01: **APPROVED** — the previous `REVISE` status is superseded for the current accepted
  Hero v2 state.
- Authorized: record the sign-off; update the R8/R9 gate/status documents; run the documented
  production promotion; take fresh pre-cutover backups; promote the accepted frontend revision;
  rebuild/recreate only through the documented host-side mechanism; run the production smoke;
  stop after verification.
- **Strict change freeze**: no design/feature changes, no Blender work, no animation/scroll
  tuning, no CMS CTA edits, no unrelated refactors or infrastructure invention.
- "If a real production blocker appears, STOP and report it."

## 2. Gate verification before promotion

| Gate | Requirement | State at 2026-09-15 |
| ---- | ----------- | ------------------- |
| R8 visual | Automated captures, responsive matrix | Green (39/39 + matrix; §1 `COORD-080`) |
| R8 a11y | Automated 31/31, keyboard/zoom/reduced-motion | Green; manual SR owner-accepted non-blocking |
| R8 browser | Live staging smoke, admin matrix, CI | Green (§6) |
| R8 performance | Local budget probes | Green; production field data owner-accepted post-launch |
| R8 security | `npm audit` 0 / `pip-audit` 0 / secret scan | Green (§5) |
| R8 deferrals | Named, owned, non-blocking | F-02/F-03/F-05 + manual SR accepted 2026-09-10 |
| **F-01 owner visual** | Owner compare + accepted state + sign-off | **APPROVED 2026-09-15 (this record)** |

No unresolved HARD R8 gate other than the owner sign-off was found, so promotion proceeded.

## 3. Pre-production safety (R9 Phase 5)

- Source revisions on the production host matched the accepted release set:
  public `457b7fe7…`, admin `1ea469ae…`, backend `6c0d3491…`; all three trees clean.
- Accepted frontend commit verified present on the remote (`origin/feat/research-universe-prototype` = `457b7fe7…`).
- Current production revision before the change: web `taha-web-prod:prod-7a5c495a`,
  cms/admin `taha-*-prod:prod-507b4bb3` (untouched by this promotion).
- Staging health at promotion time: `{"status": "ok", "db": "ok", "contact": "ok"}`,
  web image `taha-web-stage:stage-457b7fe7-1ea469ae-6c0d3491`.
- No force push, no history rewrite, no `git add -A`; the local coordination working tree was
  not committed during promotion (unrelated pre-existing changes remain local).

## 4. Backups (fresh, before cutover)

Directory: `/home/deploy/taha-cms-stage/backups/promotion-20260915T194439Z/`

| Artifact | Size | SHA-256 |
| -------- | ---- | ------- |
| `prod-taha_prod.dump` (production DB, `pg_dump -Fc`) | 560 501 B | `4bdee1b750d1bf338ff3718f19ad823a9be81ae5767c33cd7b43d01a73c43da2` |
| `prod-media.tar` (production media volume) | 10 240 B | `299721523b1fe6a0640ba04fe18ebdc5a0d7a226e6d1b2df0cce7d75fe8f224a` |
| `prod-public-html.tar` (pre-promotion served payload) | 103 826 944 B | `75b77dd01a122a0c986ccc458f65edee647e778e3ef5447e0495d5d4a1318e02` |
| `legacy-taha_cms.dump` (legacy stack, rollback reference) | 555 112 B | `66a989531570e788355dae7f415bb37127ecebda7355959d79308d970a522f81` |
| `env.prod.before-20260915T194439Z`, `public-image-before.id`, `release-before.txt` | — | minor state |

Verification (not just exit 0): the production dump was restored into an isolated probe database
on the same server — `pg_restore --exit-on-error --no-owner` completed, table counts matched
(**113 = 113**), and `manage.py migrate --plan` against the restored copy reported
**no planned migration operations**; the probe database was then dropped.
Previous image `sha256:d7e2ffa1…` (`taha-web-prod:prod-7a5c495a`) remains on the host as the
immediate rollback target.

## 5. Frontend promotion (R9 Phase 4/5)

Mechanism: the **existing documented host-side procedure** — the one actually used for the
previous production update (`Design-Assets/portal/validation/release-pw2/.tmp-prod-deploy.sh`,
run 2026-09-13 for `prod-7a5c495a`). No new workflow was created.

Source SHA → destination:

```
source SHA (frontend)   457b7fe7d0d4ed8e3d1ae12774449c0b3f550d5f  (feat/research-universe-prototype)
destination branch      production host-side release, tag/target prod-457b7fe7
commit range            origin/main..457b7fe7  = 7 commits
file summary            Hero v2 sequence + research-universe art direction + tests/evidence
                        (95 files, +16 769 / −449 in the public-site repo)
```

Executed steps (host scripts kept as evidence):
`/home/deploy/taha-cms-stage/scripts/hero-v2-preflight-build.sh` and
`/home/deploy/taha-cms-stage/scripts/hero-v2-promote.sh`

1. Built `taha-web-prod:prod-457b7fe7` from the accepted revision with the canonical production
   build arguments (`PUBLIC_SITE_URL=https://tahamohamadi.ir`,
   `PUBLIC_API_BASE_URL=https://tahamohamadi.ir`) via `deploy/Dockerfile.public`.
   Image `sha256:ddf40316681bad9dfe88181d8402b4218c470f0e18b0084ed40b065ab4de6aed`, 117 936 085 B, 71 pages.
2. Replaced the static payload in the `taha-cms-prod_prod_public_html` volume from that image
   (463 → 473 files, 71 pages, 80 hero-v2 assets).
3. Pointed `RELEASE_ID=prod-457b7fe7` in `.env.prod` (previous value `prod-7a5c495a`, snapshot kept).
4. Recreated **only** the web service (`docker compose … up -d --force-recreate web`).
   cms / admin / db / mailpit untouched and still `Up`.

## 6. Production smoke (post-cutover)

Public apex `https://tahamohamadi.ir` (served through the existing Cloudflare edge,
`cf-cache-status: DYNAMIC`, `last-modified` matching this promotion):

| Check | Result |
| ----- | ------ |
| `/` , `/en/`, `/fa/` | 200 |
| `/api/site` | 200, real payload |
| `/en/about/` | 200, `<canvas>` present, hero-v2 absent (no About regression) |
| Host-edge direct (bypassing DNS) | `/en/`, `/fa/`, `/en/about/`, `/health/`, `/api/site` all 200 |
| Hero v2 on Home | present in both locales; all 9 `data-hero-*` sequence attributes; 4 authored frames × 4 families |
| Reduced motion | no scrub journey — progress frozen at 0.3333; the held still is byte-identical to authored state 2 |
| Overflow | none at desktop 1440 / mobile 430 / RTL `/fa/` |
| Home WebGL | 0 canvas / 0 research-universe references on Home |

Full machine-readable witness output: `evidence/hero-v2-*` on the host plus the browser witness
run recorded in §7 of this file's accompanying session evidence.

### 6.1 Real-browser verification (Playwright 1.62.1 / Chromium, live site)

| Check (per authorization Phase 6/7/9) | Result |
| ------------------------------------- | ------ |
| Hero v2 present, desktop + mobile, both themes | 4 frames per sequence, 8 `<img>` in the sequence |
| 4 authored states reachable | desktop progress 0 → 0.446 → 0.844 → 1; mobile 0 → 0.346 → 0.642 → 1 |
| Sticky/pinned journey releases, scrolling continues | yes (desktop 1069 → bottom 1316 of 2216; mobile 857 → 2425 of 3357) |
| Horizontal overflow | **0 px** desktop 1440, mobile 430, `/fa/` (RTL) |
| Home canvas/WebGL | **0** — no WebGL on Home |
| Hero console errors | none attributable to Hero (only the pre-existing font 404s of §7) |
| AVIF where supported | **AVIF only**: 8 desktop / 8 mobile AVIF requests, **0 PNG**, **0 WebP** in the graph |
| Device families | desktop receives `hero-v2-desktop-*`, mobile `hero-v2-mobile-*` |
| No PNG source masters / candidate or sweep assets | confirmed (0 PNG masters requested; 0 candidate/sweep/blend files in the image) |
| Reduced motion | **verified as: no scrub journey** — progress frozen (0.3333 before and after scroll), and the held hero crop is **byte-identical** to the normal-motion authored state 2 crop (sha `19331d98…`, 40 944 B), differing from state 0 (`36adddde…`); visual inspection shows one coherent composition with no ghosting. An opacity-level "exactly one painted frame" assertion is **not** made — the frames are absolutely stacked with `will-change: opacity` and all report computed `opacity: 1`, so the metric is not separable; the first run's `visibleFrames = 5` number is retracted in [`CORRECTION.md`](../../Design-Assets/hero-v2/validation/production-2026-09-15/CORRECTION.md) |
| About | interactive graph intact — 1 canvas 834×718, 28 nodes, **no** Hero v2 migration regression |
| RTL `/fa/` | `dir="rtl"`, `lang="fa"`, Hero present, 0 overflow |

Witnesses: [`Design-Assets/hero-v2/validation/production-2026-09-15/`](../../Design-Assets/hero-v2/validation/production-2026-09-15/README.md)
(desktop/mobile × dark/light four-state captures, reduced-motion still, About, `/fa/`, `report.json`).
Host copy: `/home/deploy/taha-cms-stage/evidence/hero-v2-production-witnesses/`.

## 7. Known non-blockers recorded (not fixed — freeze respected)

- **Dual-theme fetch** on the Hero images is the documented non-blocker; not optimized in this release.
- **Hero CTA CMS content** is currently unpublished / pre-existing CMS state. It is **not** a
  Hero v2 deployment regression. (Recorded as the owner authorization states it; the promotion
  did not touch CMS content. Independent read-only corroboration on 2026-09-15: `/api/site`
  exposes `primaryColor, downloads, contact, brandName, tagline, footerText, seoDefaultTitle,
  seoDefaultDescription` and `/api/v1/site/en` exposes `locale, revision, brandName, contentCopy,
  featuredRecords, brandMedia, tagline, footerText, seo, navLinks, audienceLinks, scene, updatedAt`
  — zero CTA keys in either payload.)
- **Font delivery on the apex — FIXED 2026-09-15** (a later, narrowly-scoped owner pass lifted the
  freeze for this one objective). Cause, traced end-to-end: the prod Caddy block intercepted
  `handle /fonts/*` and served it from the Caddy container's own `/var/www/html` (ten flat
  `Vazirmatn-*.woff2`, no family subdirectories), while the correct files were present in the image,
  in `prod_public_html`, and served `200 font/woff2` by the web container all along — which is why
  staging (no such handler) never failed. Fix: that single route now proxies `taha-prod-web:8080`
  with the route's existing CORS headers preserved; backup `sha256 09ef66aa…`, applied
  `sha256 fa36068e…`. Result: **all ten referenced faces return `200 font/woff2`, zero 404s**.
  Full evidence: [`PRODUCTION-STABILIZATION-2026-09-15.md`](./PRODUCTION-STABILIZATION-2026-09-15.md).
- **Apex DNS record (pre-existing, owner action):** the authoritative A record answers
  `213.176.74.133` (TCP 443 refuses connections) with **no AAAA**, while the production host's
  resolver answers with Cloudflare edge addresses. The promoted revision is therefore served over
  the proxied path (verified 200 with the post-promotion payload), but the R9 Phase 5
  "replace the apex record" step is still open. **Not changed** — Cloudflare is the owner's.
  **UPDATE 2026-09-16 — RESOLVED.** The specified mutation was applied by the owner; the apex `A` is
  now the single proxied `85.192.29.196` record (id `f8921a15…`, zone `e0fef33e…`), and
  `213.176.74.133` occurs zero times in the zone. Direct authoritative queries from the authorized
  host (`dale` and `harmony`, UDP+TCP, `+norecurse`) return the Cloudflare edge with the AA flag,
  TTL 300, and the identical SOA serial `2414083257`. Record:
  [`HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](./HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md).
- Mailpit stands in for real SMTP (unchanged from the R9 plan).
- `HeroGraph.astro` remains dead-but-undeletable per the Stage 4 closeout audit (unchanged).

## 8. Rollback readiness

- Previous web image preserved: `taha-web-prod:prod-7a5c495a` (`sha256:d7e2ffa1…`).
- Rollback = restore `RELEASE_ID=prod-7a5c495a` in `.env.prod` (snapshot
  `env.prod.before-20260915T194439Z`) + `up -d --force-recreate web`, plus the pre-promotion
  static payload archive if the volume must be reverted.
- Legacy stack (`taha-cms`, `/home/deploy/cms-repo`) untouched and running.
