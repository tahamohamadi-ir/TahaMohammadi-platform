# Audit fix execution state — 2026-09-06

Mission: fix A01–A10 from IMPLEMENTATION-AUDIT-2026-09-06.md. No commit/push/deploy/real-DB.

## Repos (HEAD unchanged since audit)
- ROOT `c69e339c8c26788467d29ad346fb7df99b1c2842`
- BACKEND `bd6682ea9dae7e5bf6957c36691dc3a94a00ea37`
- PUBLIC `b895b2cb9c6ad9519d55bd2663448461931c0a39`
- ADMIN `ca4dd3d26484d4468465c756d302b8e3247a3cbe`
- All agent working-tree changes preserved; no reset/clean.

## Baselines reproduced (match audit)
- BACKEND `uv run pytest -q`: 848 passed, 14 failed (test_admin_content_write, test_api detail article, 3 contract fixtures, 9 openapi drift).
- PUBLIC `npm.cmd test`: 340 passed, 3 failed, 60 files (foundation CA-01 guards + public-310 OpenAPI pin).
- ROOT `python Infra/staging/test_rebuild_product.py`: 8 passed.

## Verification vs audit (code as of HEAD)
- A01 CONFIRMED: `Back-End/apps/rebuild/services.py:292-376` puts `/fa|en/` home + list + detail into
  affectedPaths for every entity; `Infra/staging/rebuild-product.py:382` denies all affectedPaths on
  `removal_state==pending`. Archive of one article would 404 home/blog until manual un-deny.
- A02 CONFIRMED: `EdgeDenyManager.verify_effective` (rebuild-product.py:191) only re-reads the manifest
  file; no config-apply/reload or HTTP probe exists; callback reports `effective` from that.
- A03 CONFIRMED: `enqueue_publication_job` (services.py:209) calls `invoke_static_rebuild()` synchronously
  inside the transaction, no job_id passed; runner (rebuild-product.py:375-378) ignores non-200 on
  queued→running and continues; empty revision accepted; `build_site` only checks index.html
  (no Pagefind/sitemap/artifact checks).
- A04 CONFIRMED: public detail (`apps/api/api.py:608` etc.) reads `Article.objects.public()` live row;
  restore (`apps/api/admin_content.py:1622-1796` + `apps/content/revisions.py:93-107`) flips the live row
  to draft, so GET after restore 404s instead of serving the last published snapshot (snapshot exists in
  `PublicationSnapshot` but parents don't fall back to it). Restore also enqueues removal pending (A01 link).
- A05 CONFIRMED: `Front-End/public-site/src/pages/{fa,en}/index.astro:20` calls `loadHeroGraph(locale)` with
  no resolver; `hero-graph-content.ts:539` supports optional resolver but nothing calls the
  `/api/v1/records/{locale}/resolve` endpoint at runtime.
- A06 CONFIRMED: `src/foundation.contract.test.ts:429-443` asserts live package.json has no `three`
  (fails now that CA-04 legitimately added `three@^0.173.0`); `542-603` scans whole-checkout `git status`.
- A07 CONFIRMED: 14 backend drift failures + 1 public pin failure; snapshots need source regeneration.
- A08 CONFIRMED: `apps/content/services/lifecycle.py:183-193` single job, `target_locale` = last item's locale.
- A09 CONFIRMED: `apps/analytics/api.py:158-171` generic path/target shape checks only; any well-formed target
  accepted; no canonical-route registry, no locale-path consistency; errors via `HttpError` (legacy shape).
- A10 CONFIRMED: `apps/rebuild/services.py:164-181` creates `PublicationMachineNonce` BEFORE HMAC check.

## Order (shared files serialized)
1. A10 (services.py auth) → 2. A08 (lifecycle.py) → 3. A01 (services.compute + runner deny split + contract/schema)
   → 4. A04 (admin_content/api public fallback) → 5. A03 (jobs commit/claim/revision + runner) →
   6. A09 (analytics) → 7. A05+A06 (PUBLIC) → 8. A07 (contracts regen + syncs).
   services.py is shared by A10/A01/A03: strictly sequential.

## Status
- [x] baselines + verification

## Incident 2026-09-06 (public-site): accidental `git stash pop` recovered

A `git stash push -- <paths>` (intended to prove A05 pre-change failure) failed
because the target file is untracked, and the following `git stash pop` applied
a pre-existing foreign stash (`parallel-wip`) onto the working tree, producing
merge conflicts in 21 page-family files plus one clean auto-merge
(`template-base.css`). No commit/push/reset/clean was run. Recovery, verified
against the mission-start status record: conflicted/touched paths restored to
HEAD bytes (they were clean before the pop; merge "ours" equaled HEAD), the two
add/add files restored byte-exact from index stage 2 back to untracked, the
staged auto-merge unstaged, and the foreign stash entry left intact for its
owner. Final `git status` matches the pre-pop state plus only this mission's
intended changes; HEAD unchanged in all four repos. Lesson: never use
stash push/pop in this shared workspace; prove pre-change failure by code
evidence instead.
- [x] A10 (nonce after HMAC; 8/8 jobs tests green; ruff clean)
- [x] A08 (per-locale bulk jobs; 13/13 invalidation+bulk green)
- [x] A01 (revokedPaths split: model+0002 migration, services, admin schema+retry,
      lifecycle bulk, runner job_revoke_paths+deny/clear, contract §I06;
      backend A01 test + 4 runner tests green, 12/12 runner green)
- [x] A04 (apps/content/published.py snapshot fallback for ALL public detail/list/
      related/alternates/series-members/lesson-neighbors/resolver reads; restore
      enqueues no removal; archive invalidates snapshots in transition/PUT/bulk;
      scheduled publish records snapshots; contract §I03 note;
      4/4 new HTTP isolation tests green; full backend 856 passed + same 14 A07 failures)
- [x] A03 (dispatch on_commit+job_id, PUBLICATION_RUNNER_ARGV, auto revision,
      exclusive claim, revision/removal guards, runner resume/validation/artifacts,
      runbook+contract §I06; 8/8 new backend lifecycle green, 16/16 jobs green;
      20/20 runner green; ruff clean; migration 0002 fwd/back/fwd proven on
      throwaway DB; full backend 864 passed + same 14 A07 failures)
- [x] A02 (staged write/validate+reload/HTTP-probe, fail-closed; 7/7 isolated
      localhost-edge tests green; 27/27 runner green; runbook+contract §I06;
      real-ingress integration gate stays OPEN — no deployed Caddy/Nginx here)
- [x] A09 (target registry {cv slots}+empty-only, canonical+locale pagePath,
      413 limit, I08 envelope incl. scoped 422, contract §I07 note;
      16/16 analytics green; full backend 871 passed + same 14 A07 failures;
      ruff clean)
- [x] A05 (collect/dedupe/≤50-batch resolve, exact-locale canonical hrefs, wired
      into loadHeroGraph for fa+en Home; 10/10 new tests incl. fetch→rendered-link
      via astro container en+fa; PUBLIC 353 green)
- [x] A06 (CA-01 guards check delivery artifact only; three stays installed;
      historical validations kept; foundation 16/16 green)
- [x] A07 (fresh source export, additive-only semantic diff 16+/0-, new scaffold
      acceptance addendum w/ history, fixtures from real responses, pins+types+
      contract tests in BOTH lanes; backend 885 green; PUBLIC 353 green + build;
      ADMIN 121 green + build; runner verify 3/3 MATCH)
- [ ] final validation + report + queue sync
