# Production Stabilization Pass — DNS apex + `/fonts/*` 404s (2026-09-15)

> **UPDATE 2026-09-16 — DNS ITEM RESOLVED; this record is the historical root-cause analysis.**
> The apex `A` finding below was accurate for 2026-09-15: every authoritative nameserver then
> answered the legacy DNS-only `213.176.74.133`. The required mutation specified in PHASE 2 was
> subsequently applied by the owner, and direct authoritative verification on 2026-09-16 from the
> authorized host (`dale` + `harmony`, UDP **and** TCP, `+norecurse`) now returns the Cloudflare
> edge with the AA flag, TTL 300 and the identical SOA serial `2414083257` — `213.176.74.133` is
> **no longer authoritative** and occurs zero times in the zone. The font section (PHASE 3/4) was
> applied and verified as recorded. Final authoritative record:
> [`HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](./HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md).

**Scope:** exactly two objectives, per owner authorization — stabilize the apex DNS path, resolve
the production `/fonts/*` 404s. No Hero / design / CMS / CTA change. Prior reduced-motion
correction preserved (see `Design-Assets/hero-v2/validation/production-2026-09-15/CORRECTION.md`);
the retracted `visibleFrames = 5` metric is not repeated anywhere in this record.

**Production revision at the time of this pass (unchanged by it):** web `taha-web-prod:prod-457b7fe7`,
cms/admin `taha-*-prod:prod-507b4bb3`, sources public `457b7fe7…` / admin `1ea469ae…` / backend `6c0d3491…`.

---

## PHASE 0/1 — Current truth and DNS root cause

### Zone identity

| Item | Value |
| ---- | ----- |
| Registrant NS RRset (as published by every name server) | `dale.ns.cloudflare.com`, `harmony.ns.cloudflare.com` |
| Previously observed pair (earlier today) | `johnathan.ns.cloudflare.com`, `candy.ns.cloudflare.com` — **still answering authoritatively with identical records** |
| SoA | `candy.ns.cloudflare.com. dns.cloudflare.com. 2410061025 …` |
| `.ir` TLD delegation query | **not verifiable from here** — `a/b/c.nic.ir` returned no answer for this network (IPv6 unreachable, IPv4 no reply) |
| Cloudflare credentials on the host | **none** — no `CF_*`/`CLOUDFLARE_*` env in any env file, no `dns.providers` plugin in the Caddy build; the edge obtains public certs via ACME |

### Record-level answers

| Resolver / NS | Record | Returned value | TTL | Expected | Match |
| ------------- | ------ | -------------- | --- | -------- | ----- |
| `dale.ns.cloudflare.com` (auth) | apex A | `213.176.74.133` | 300 | production origin | **NO** |
| `dale.ns.cloudflare.com` (auth) | apex AAAA | *(none)* | — | — | n/a |
| `dale.ns.cloudflare.com` (auth) | www A | `172.67.220.35`, `104.21.24.197` | 300 | — | ✅ (Cloudflare proxy) |
| `harmony.ns.cloudflare.com` (auth) | apex A | `213.176.74.133` | 300 | production origin | **NO** |
| `harmony.ns.cloudflare.com` (auth) | www A | `172.67.220.35`, `104.21.24.197` | 300 | — | ✅ |
| `johnathan.ns.cloudflare.com` (old pair) | apex A | `213.176.74.133` | 300 | production origin | **NO** |
| `candy.ns.cloudflare.com` (old pair) | apex A | `213.176.74.133` | 300 | production origin | **NO** |
| `1.1.1.1` (recursive) | apex A | `213.176.74.133` | — | production origin | **NO** |
| `8.8.8.8` (recursive) | apex A | `213.176.74.133` | — | production origin | **NO** |
| Cloudflare DoH / Google DoH | apex A | `213.176.74.133` | 300 | production origin | **NO** |
| Origin edge itself (`--resolve apex:443:127.0.0.1`) | apex HTTPS | **200** | — | 200 | ✅ |

### Root cause

**The apex `A` record is a DNS-only record pointing at the legacy host `213.176.74.133`, which
refuses TCP/443.** Every authoritative name server agrees on it, so this is *not* split-brain,
stale zone data, or an inconsistent NS set — it is a single wrong record value that was never
replaced when the platform moved to the production host.

Consequences, both observed:

- A client whose resolver returns that record cannot reach the site at all (`curl` → connect error).
- A client whose resolver returns Cloudflare edge addresses for the same name reaches the promoted
  application normally (`200`, `server: cloudflare`, post-promotion `last-modified`) — because
  `www` **is** proxied and the edge serves the apex block from the production host.

That mixture is exactly the flapping observed in the previous pass. The proxied path works; the
authoritative apex record does not.

Derived intended target (from existing infrastructure, not guessed): the production host
**`85.192.29.196`** — the `taha-nl` host holding the `taha-cms-prod` stack whose Caddy serves the
`tahamohamadi.ir` block (verified 200 locally) and whose `www` sibling already resolves through
Cloudflare.

## PHASE 2 — DNS change

**No mutation performed.** The provider integration is absent on the host (no Cloudflare
credentials, no DNS plugin), and Cloudflare is the owner's. Per instruction, the required mutation
is specified instead of worked around:

```
Record:       apex A (replace existing; do not add a second)
Name:         tahamohamadi.ir
Type:         A
Current:      213.176.74.133   (DNS only / grey cloud — legacy host, refuses :443)
Required:     85.192.29.196    (production host running taha-cms-prod)
TTL:          Auto (300)
Proxy state:  Proxied (orange cloud) — same state as the working www record
Reason:       The apex must reach the production stack. The current DNS-only value points at a
              host that is not serving HTTPS, so any resolver returning it makes the site
              unreachable, while proxied clients reach it fine — the exact instability reported.
```

Second, unverified item needing an owner check (could not be read from here): **the registrar
delegation**. The zone’s published NS set is `dale`/`harmony`, while the previous pair
`johnathan`/`candy` still answers with identical data. If the `.ir` registrar still delegates to
the old pair, the domain will fail when Cloudflare retires it. Confirm the set in the registrar
panel matches the NS Cloudflare currently assigns for the zone.

## PHASE 3 — Font 404 root cause (traced end-to-end)

| URL (as referenced by the built site) | Referenced by | Exists in build/image | In `prod_public_html` | In container | Via edge before | Via edge now | MIME |
| ------------------------------------- | ------------- | --------------------- | --------------------- | ------------ | --------------- | ------------ | ---- |
| `/fonts/inter/InterVariable.woff2` | built CSS (global font stack) | yes | yes | yes (200, 352 240 B) | **404** | **200** | `font/woff2` |
| `/fonts/inter/InterVariable-latin.woff2` | built CSS | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/newsreader/Newsreader-Variable.woff2` | built CSS | yes | yes | yes (214 880 B) | **404** | **200** | `font/woff2` |
| `/fonts/newsreader/Newsreader-Variable-latin.woff2` | built CSS | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/estedad/Estedad-Variable.woff2` | `:lang(fa)` stack | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/estedad/Estedad-Variable-arabic.woff2` | `:lang(fa)` stack | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/estedad/Estedad-Variable-latin.woff2` | built CSS | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/vazirmatn/Vazirmatn-Variable.woff2` | `:lang(fa)` stack | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/vazirmatn/Vazirmatn-Variable-arabic.woff2` | `:lang(fa)` stack | yes | yes | yes | **404** | **200** | `font/woff2` |
| `/fonts/vazirmatn/Vazirmatn-Variable-latin.woff2` | `:lang(fa)` stack | yes | yes | yes | **404** | **200** | `font/woff2` |

**Cause: Caddy, not the build and not the sync.** The prod apex block intercepted
`handle /fonts/*` and served it from the Caddy container's own `/var/www/html`, which holds only
ten flat `Vazirmatn-*.woff2` files — no `inter/`, `newsreader/`, `estedad/`, `vazirmatn/`
subdirectories. The files were always present in the image, in the volume (verified by listing),
and served correctly by the web container (`200 font/woff2` on `127.0.0.1:8080`). Staging has no
such handler, which is precisely why staging never showed the failure.

## PHASE 4 — Font fix applied

One route corrected, inside the `# BEGIN TAHA PROD MANAGED` section only — the CORS headers the
route already carried were preserved (`header` → `header_down`):

```diff
 	handle /fonts/* {
-		root * /var/www/html
-		file_server
-		header Access-Control-Allow-Origin *
-		header Access-Control-Allow-Methods "GET, OPTIONS"
+		reverse_proxy taha-prod-web:8080 {
+			header_down Access-Control-Allow-Origin *
+			header_down Access-Control-Allow-Methods "GET, OPTIONS"
+		}
 	}
```

Applied to `/home/deploy/cms-repo/infra/caddy/Caddyfile.compose` using the deployment pattern the
staging workflow already uses: backup → candidate → `caddy validate` (`Valid configuration`) →
swap → `caddy reload` → automatic rollback if the reload failed (it did not).

| Item | Value |
| ---- | ----- |
| Backup | `backups/font-fix-20260915/Caddyfile.compose.before` — sha256 `09ef66aa9e6f459684dc3ab3ed45e403da759e96f037e91721b820818d59c0c8` |
| Applied | sha256 `fa36068e1041aee995792a35d65094ec09e418d221e955f14a380b392af5f857` |
| Scripts | `scripts/font-route-fix.sh`, `scripts/font-verify.sh` |
| Evidence | `evidence/font-route-fix-20260915.txt`, `evidence/font-verify-20260915.txt` |

Not changed: font families, font declarations, typography, any other route, `tls` config, the
`www` redirect block, the staging block, or any container.

**One behavior consequence, verified inert:** the ten flat `Vazirmatn-*.woff2` files under Caddy's
`/var/www/html/fonts` are no longer reachable on the apex (`/fonts/Vazirmatn-Regular.woff2` now 404,
was 200). Nothing references them: the built platform site references only the
`<family>/<file>` paths above, and neither legacy container's served HTML references any
`/fonts/*.woff2` at all. The files remain on disk, so a revert is a one-line change.

## PHASE 5 — Regression smoke (production edge, all green)

HTTP: `/` 200 · `/en/` 200 · `/fa/` 200 · `/api/site` 200 (`application/json`, 443 B).
Fonts: **all ten referenced faces 200 `font/woff2`, zero 404s**, zero failed responses during page loads.

| Check | desktop-dark | desktop-light | mobile-dark | mobile-light |
| ----- | ------------ | ------------- | ----------- | ------------ |
| Hero v2 present | ✅ (1 sequence) | ✅ | ✅ | ✅ |
| Home canvas/WebGL | 0 | 0 | 0 | 0 |
| States reached | 0 → 0.363 → 0.626 → 1 | same | 0 → 0.300 → 0.624 → 1 | same |
| Horizontal overflow | 0 px | 0 px | 0 px | 0 px |
| Page errors | 0 | 0 | 0 | 0 |

Reduced motion (accepted statement only — no DOM-paint claim): progress **fixed at 0.3333** before
and after scrubbing, and the rendered Hero crop is **byte-identical** to the authored state 2 crop
(`19331d989e63aee7`); no scroll-driven progression occurs.

About: 1 canvas (interactive graph present), no Hero v2, 0 px overflow.
Smoke problems array: **empty**. Machine reports:
`evidence/smoke-report.json` (browser) and `evidence/font-verify-20260915.txt`.

## PHASE 6 — Evidence hygiene

The reduced-motion correction stands: progress frozen at 0.3333, visual output matches authored
state 2, no scroll-driven progression. No DOM-painted-frame claim is made, and the invalid
`visibleFrames = 5` metric is not resurrected.

## Remaining blocker

**One, and it is not fixable from here:** the apex `A` record still returns `213.176.74.133`, so the
public path is only stable for clients that resolve through Cloudflare. Everything on the
application side — fonts, Hero, About, HTTP routes — is green and verified against the production
origin.

> **UPDATE 2026-09-16 — this remaining blocker is CLOSED.** The apex `A` record no longer returns
> `213.176.74.133`; it is the single proxied `85.192.29.196` record and the authoritative path
> serves the Cloudflare edge consistently (direct `dale`/`harmony`, UDP+TCP, `+norecurse`, AA
> present, TTL 300, SOA serial `2414083257`). See the banner at the top of this file and
> [`HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md`](./HERO-V2-PRODUCTION-FINAL-CLOSEOUT-2026-09-16.md).