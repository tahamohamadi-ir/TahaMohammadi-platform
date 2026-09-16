# Hero v2 — Production Final Closeout (2026-09-16)

**Status: COMPLETE.** Home ships the Hero v2 image sequence on the production platform; every
publication concern that was still open on 2026-09-15 (owner gate, promotion, fonts, DNS) is
resolved and verified. This is the authoritative final record; earlier intermediate findings are
preserved in place and marked superseded where they describe a state that no longer holds.

---

## 1. Release identity

| Item | Value |
| ---- | ----- |
| Frontend source commit | `457b7fe7d0d4ed8e3d1ae12774449c0b3f550d5f` (branch `feat/research-universe-prototype`) |
| Outer design authority commit | `176ce4a719624cdc927118c77af2d51653079216` |
| Staging release | `stage-457b7fe7-1ea469ae-6c0d3491` |
| **Production release / web image** | **`taha-web-prod:prod-457b7fe7`** (`sha256:ddf40316…`, 117 936 085 B, 71 pages) |
| Production sources at promotion | public `457b7fe7…` / admin `1ea469ae…` / backend `6c0d3491…` (`taha-*-prod:prod-507b4bb3` for cms/admin) |
| Production rollback target | `taha-web-prod:prod-7a5c495a` (`sha256:d7e2ffa1…`) + `env.prod.before-20260915T194439Z` |

## 2. Promotion status

- **Owner gate cleared.** R8/F-01 was `REVISE` and became **APPROVED** on 2026-09-15 by explicit
  owner sign-off: [`R8-F01-OWNER-SIGNOFF-2026-09-15.md`](./R8-F01-OWNER-SIGNOFF-2026-09-15.md).
  `COORD-080` carries the matching "owner gate PASSED, R8 CLOSED" update; `COORD-090` carries its
  own 2026-09-15 update note and its owner cells remain owner-only by design.
- **Production promotion completed** 2026-09-15 12:39–12:54 (−07:00) through the **existing
  documented host-side procedure** (the same one used for `prod-7a5c495a`; no new workflow was
  invented): fresh restore-verified backups first (`backups/promotion-20260915T194439Z`,
  prod dump `4bdee1b7…` restored into an isolated probe, 113 = 113 tables, no pending migrations),
  then build → volume sync (463 → 473 files) → `RELEASE_ID=prod-457b7fe7` → recreate **only the web
  service**; cms/admin/db/mailpit untouched.
- The promotion path that earlier blocked on R8 is therefore **historically obsolete** and is not a
  current blocker.

## 3. Runtime architecture (production, verified)

- **Home = Hero v2 image sequence.** Four authored states, desktop + mobile frame families, driven by
  scroll progress only: no autoplay, no idle loop, no video, and **no WebGL/canvas on Home** (0
  canvas measured).
- **About = the interactive graph**, unchanged: 1 canvas (834×718), 28 nodes, no Hero v2 present
  there (no migration regression).
- **Reduced motion** is locked to the authored **state 2**, held at progress **0.3333** with no
  scrub journey: the rendered hero crop is byte-identical to the normal-motion authored state 2 crop
  (`19331d98…`, 40 944 B) and differs from state 0 (`36adddde…`). No DOM-painted-frame claim is made
  — the earlier `visibleFrames = 5` metric remains retracted in
  [`CORRECTION.md`](../../Design-Assets/hero-v2/validation/production-2026-09-15/CORRECTION.md).
- Independent re-check on 2026-09-16: `/en/` and `/fa/` both serve the sequence
  (`data-hero-sequence-frame-count="4"`, `data-hero-layout="integrated"`), HTTP 200.

## 4. Font stabilization

- **Root cause (traced end-to-end):** the production apex block's `handle /fonts/*` served from the
  **Caddy container's own** `/var/www/html`, which held only ten flat `Vazirmatn-*.woff2` files — no
  `inter/`, `newsreader/`, `estedad/`, `vazirmatn/` subdirectories. The correct files were present
  in the image, in the `prod_public_html` volume, and served `200 font/woff2` by the web container
  all along; staging has no such handler, which is why staging never failed.
- **Fixed 2026-09-15:** that single route now `reverse_proxy taha-prod-web:8080` with the route's
  existing CORS headers preserved (`header` → `header_down`); backup sha256 `09ef66aa…`, applied
  sha256 `fa36068e…`, validated then `caddy reload` (no rollback needed).
- **Result: 10/10 referenced faces return `200 font/woff2`, zero 404s.** Independent spot-check on
  2026-09-16 confirmed `InterVariable.woff2`, `Newsreader-Variable.woff2` and
  `Vazirmatn-Variable.woff2` → `200 font/woff2`. Full evidence:
  [`PRODUCTION-STABILIZATION-2026-09-15.md`](./PRODUCTION-STABILIZATION-2026-09-15.md).

## 5. DNS final verdict

**Control plane (Cloudflare API)**

| Item | Value |
| ---- | ----- |
| Zone / account | `tahamohamadi.ir` · `e0fef33eace06b0a07ff42d42b3652f5` · account `f2103c21a3b995eb7aee49393a61e1be` |
| Status / type | `active` · `full` |
| Apex A records | **exactly 1** — `85.192.29.196`, `proxied: true`, id `f8921a153bd2b2c386fbf31fa1e481ff` |
| www | proxied CNAME → `tahamohamadi.ir` |
| `213.176.74.133` | **zero occurrences** in the active zone |
| Zone DNS settings | `nameservers.type = cloudflare.standard`, `secondary_overrides = false`, `ns_ttl = 86400`, not paused |
| Delegation | `dale.ns.cloudflare.com`, `harmony.ns.cloudflare.com` (assigned and published) |

**Data plane (direct authoritative, 2026-09-16T10:09:24Z / 10:32:48Z, from the authorized host
`taha-nl` — `deploy@85.192.29.196:2222`, dig 9.20.24, read-only)**

| Query | Transport | Status | AA | Answer | TTL | SOA serial |
| ----- | --------- | ------ | -- | ------ | --- | ---------- |
| `@dale` apex A `+norecurse` | UDP | NOERROR | present | `172.67.220.35`, `104.21.24.197` | 300 | 2414083257 |
| `@dale` apex A `+norecurse` | TCP | NOERROR | present | `172.67.220.35`, `104.21.24.197` | 300 | 2414083257 |
| `@harmony` apex A `+norecurse` | UDP | NOERROR | present | `172.67.220.35`, `104.21.24.197` | 300 | 2414083257 |
| `@harmony` apex A `+norecurse` | TCP | NOERROR | present | `172.67.220.35`, `104.21.24.197` | 300 | 2414083257 |

- AAAA (both servers): `2606:4700:3033::6815:18c5`, `2606:4700:3032::ac43:dc23` — the edge's
  synthesized IPv6 for the proxied hostname.
- `www` resolves through the same Cloudflare edge (both servers, TTL 300).
- **SOA serial 2414083257 identical from both nameservers, over UDP and TCP** — one zone version,
  no authoritative split.
- Recursive agreement: `1.1.1.1` and `8.8.8.8` both return the same two edge addresses (TTL 300).
- Public HTTPS: `https://tahamohamadi.ir/en/` → **HTTP/2 200** through Cloudflare
  (`server: cloudflare`, `cf-cache-status: DYNAMIC`, `last-modified: Tue, 15 Sep 2026 19:45:23 GMT`
  — matching the promotion), `/fa/` → 200.
- Hence: Cloudflare control plane and authoritative data plane agree; `dale` and `harmony` agree;
  public recursive DNS agrees; **`213.176.74.133` is not currently authoritative** and requires **no
  DNS mutation** and **no Cloudflare Support case**.

**Superseded finding (history preserved, not deleted):** on 2026-09-15 every authoritative
nameserver answered the apex A with the legacy DNS-only `213.176.74.133` (a host refusing TCP/443),
while `www` was proxied — root-caused in `PRODUCTION-STABILIZATION-2026-09-15.md`, which specified
the exact required mutation (apex A → `85.192.29.196`, **Proxied**, TTL Auto) instead of attempting
it, because no Cloudflare credentials exist on the host. That mutation was subsequently applied by
the owner. The 2026-09-16 direct authoritative verification above shows the specified state is now
live, so the `213.176.74.133` observation is classified as **historical/resolved**: it was accurate
for its date, is unreproducible now, and is not a current blocker. The same finding as recorded in
`R8-F01-OWNER-SIGNOFF-2026-09-15.md` §7 and in `PROJECT-STATUS.md` §2 has been annotated accordingly.

## 6. Remaining blockers

**NONE for Hero v2 production.** The release is complete and serving.

Unrelated or non-blocking items still recorded elsewhere, explicitly **not** release blockers:

- Frontend repository TypeScript baseline (140 pre-existing `tsc` errors) — repo hygiene, unrelated
  to this release; no new errors were introduced by Hero v2.
- Mailpit stands in for real SMTP on production contact delivery — owner input, unchanged from R9.
- Hero CTA CMS content is unpublished (pre-existing published-content state, identical before this
  work; not a Hero v2 regression) — a separate content task.
- Dual-theme frame fetch on Home is the documented non-blocker, not optimized in this release.
- The Stage 4.2 midpoint/motion browser recapture remains deferred (environment-dependent) — QA
  depth, not a release blocker; the delivered look was verified at the delivered browser box.
- `HeroGraph.astro` remains dead-but-undeletable (test-covered shared-path consumer) per the Stage 4
  audit.
- Server disk headroom continues to warrant monitoring.
- The manual production update path (rebuild + volume sync) is still not a repo workflow.

## 7. Final statement

**HERO V2 HOME — PRODUCTION COMPLETE.**
