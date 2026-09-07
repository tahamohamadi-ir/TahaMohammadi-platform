# Audit fix report — A01–A10 implementation (2026-09-06)

Mission: implement (not just propose) the fixes for
`reviews/IMPLEMENTATION-AUDIT-2026-09-06.md`, integrate in-flight agent work
without resets, verify by execution, and align documents/queue with real
outcomes. No commit, push, merge, deploy, or real-database change was made.
No content, API, link, or acceptance claim was invented. New unrelated
features (full admin editors, page families) remain next-phase work.

Review inputs were treated as leads, not truth: every finding was re-checked
against current code. All ten findings were confirmed as written (details in
`AUDIT-FIX-STATE-2026-09-06.md`), except scope notes recorded per item below.

Heads (unchanged by this mission): ROOT `c69e339c`, BACKEND `bd6682e`,
PUBLIC `b895b2c`, ADMIN `ca4dd3d`. All agent working-tree changes preserved.
One self-caused incident (accidental `git stash pop` of a foreign stash in
public-site) was fully recovered; foreign stash left intact, HEADs unchanged
(see the state file).

Result codes used below: **FIXED** (implemented + locally verified),
**FIXED with open gate** (implemented + verified within reach, external gate
remains), **PROCESS** (queue/process alignment, no product-code claim).

---

## A01 — rebuild/revoke split — FIXED

Cause: `compute_affected_paths` (home + list + detail for every entity) doubled
as the edge-deny list, so archiving one article could 404 home/blog, and the
deny persisted after a successful removal job.

Changes:
- BACKEND `apps/rebuild/models.py`: new `revoked_paths` JSONField +
  `to_dict()["revokedPaths"]`; migration `apps/rebuild/migrations/0002`.
- BACKEND `apps/rebuild/services.py`: new `compute_revoked_paths` (own
  detail/file URLs only; shared pages never; unknown/empty → deny nothing);
  `enqueue_*` carry both sets (revoked only when removal is pending).
- BACKEND `apps/api/admin_publication_jobs.py`: schema + retry carry
  `revokedPaths`.
- BACKEND `apps/content/services/lifecycle.py`: bulk jobs carry per-locale
  revoked sets.
- ROOT `Infra/staging/rebuild-product.py`: `job_revoke_paths` (legacy payloads
  without the key fall back to `affectedPaths`); deny uses revoked only;
  republish clears via revoked-else-affected.
- Contract `Docs/03-contracts/PRODUCT-INTERFACES-V2.md` §I06 wire shape.

Failing before: `test_archive_splits_rebuild_and_revoke_paths_a01`
(`KeyError: 'revokedPaths'`).
After: backend A01 test green; 4 new runner tests green (deny-only-detail,
legacy fallback, publish-clears); 12/12 runner green at the time.
Remaining limit: pre-A01 jobs without `revokedPaths` still deny the rebuild
set (documented compatibility fallback).

## A02 — real edge verification — FIXED with open gate

Cause: `verify_effective` re-read the manifest file; no config apply/reload or
HTTP probe existed, yet callbacks reported `effective`.

Changes (ROOT runner only):
- `EdgeDenyManager` split into stages: `write_manifest` → file check →
  `apply_configuration` (optional validate + reload commands) →
  `probe_paths_blocked` (optional ingress base URL; every revoked path and its
  slash twin must answer HTTP 404). Any configured stage failure is
  fail-closed (never `effective`). Unconfigured stages are skipped, as before.
- CLI/env: `--edge-validate-cmd`, `--edge-reload-cmd`,
  `--edge-probe-base-url`, `--edge-probe-timeout` (`EDGE_*`).
- Runbook §4 + contract §I06 record the staged semantics.

Failing before: no coverage existed (the 8-test suite never proved effect).
After: 7 new tests against an isolated localhost edge (real HTTP) green —
file→404 chain, stale-edge fail-closed (the audit's exact scenario),
reload/validate failure fail-closed, unreachable probe fail-closed,
unblock-on-republish; 27/27 runner green.
Open gate: **real-ingress integration** (no deployed Caddy/Nginx exists here).
Without a configured probe the report is file-local only; mock results are
not declared operational acceptance.

## A03 — publication job lifecycle — FIXED

Cause: dispatch fired synchronously inside the request transaction without a
job ID (legacy bash path; Compose has `REBUILD_TRIGGER_ENABLED=false`);
runner ignored claim failures and kept building; empty revisions accepted;
`index.html`-only pre-swap check; callback loss could strand or fake state.

Changes:
- BACKEND `apps/rebuild/services.py`: `enqueue_publication_job` auto-issues a
  non-empty opaque revision, dispatches via `transaction.on_commit` with the
  job UUID (rollback dispatches nothing); `invoke_static_rebuild` prefers
  `PUBLICATION_RUNNER_ARGV` + job ID, keeps the legacy script as fallback;
  `record_job_result` enforces exclusive claim (second `running` → 409),
  claim-before-terminal (queued→terminal → 409), non-empty matching
  `artifactRevision` for `succeeded`, and `effective/failed` removal only for
  pending removals.
- BACKEND callers: removed the redundant synchronous trigger
  (`admin_content` transition, scheduled command — both covered by on-commit);
  scheduled publish now records publication snapshots (A04 link);
  `PUBLICATION_RUNNER_ARGV` added to base/production settings.
- ROOT runner: terminal jobs are no-ops; rejected claims stop silently (no
  build/swap/callbacks); worker-cut-after-swap resumes (re-verify + re-report)
  instead of rebuilding; revision/path validation before any write; pre-swap
  artifact set (`index.html`, `sitemap.xml`, `pagefind/pagefind.js`,
  overridable) with `SITEMAP_FAILED`/`PAGEFIND_FAILED` mapping; rollback
  preserved.
- Runbook §3/§5 + contract §I06 record claim discipline, resume/retry
  recovery, and dispatch wiring.

Failing before: 7 new `test_product_publication_lifecycle_a03.py` tests
(dispatch timing, rollback silence, exclusivity, terminal-from-queued,
revision discipline, removal guard).
After: 8/8 new + 16/16 jobs green; 8 new runner tests green (claim stop,
empty/traversal revision, sitemap/pagefind gaps, terminal no-op, resume,
held-elsewhere stop); 20/20 runner green at the time.
Affected existing tests were updated to the corrected contract (workflow job
now pending-removal; dispatch assertions via `captureOnCommitCallbacks`).
Remaining limits: mid-build worker-cut recovery is a fresh admin retry job
(documented); legacy signed-trigger endpoint kept for compatibility.
Migration `0002` proven forward→row-write→backout→re-apply on a throwaway DB.

## A04 — draft/published isolation — FIXED

Cause: public detail reads used the live row (`Article.objects.public()`),
while restore-as-draft flips that row to draft (and even enqueued a removal),
so the published document 404'd until republication. Snapshots existed but
no parent read consulted them.

Changes:
- BACKEND `apps/content/published.py` (new): latest-snapshot resolution,
  in-memory materialization (snapshot scalars/FKs over the live row; relations
  keep working; never saves), detail/list/target/extras helpers, Django-like
  in-memory ordering, archive invalidation (belt-and-braces with the delete).
- Public reads fall back to the snapshot while the live row is a non-archived
  draft: all 15 detail endpoints, all list endpoints (merged + re-sorted,
  pagination-safe), related records, collection/series members, lesson
  neighbors + parent guard, alternates, record resolver, download file
  endpoint. Explicit archive invalidates snapshots (transition, admin PUT,
  bulk) and stays removing. Restore-as-draft enqueues **no** removal.
- Scheduled publish records the same snapshots as admin publish.
- Contract §I03 enforcement note.

Failing before: 3 new HTTP tests (`test_product_draft_published_isolation.py`:
restore cycle, draft edit, scheduled-then-draft — all 404'd).
After: 4/4 green, including publish→restore→GET-old→republish→GET-new plus
list/resolver/story/scheduled/archive-contrast coverage.
Remaining limit (documented): nested project case-study *row* content across
restore follows the live DB (single-row storage); the published parent
document, story, ID-reference relations, and presence are preserved. Full
dual-workspace storage is future work, not this mission.

## A05 — resolver wired to Home — FIXED

Cause: both Home pages called `loadHeroGraph(locale)` with no resolver; no
runtime fetch of `/api/v1/records/{locale}/resolve` existed anywhere in
`src` (only generated types + type-level contract tests referenced it).

Changes (PUBLIC): `collectRelatedRefs` (dedupe, eligible + well-formed only),
`fetchRecordResolutions` (≤50 batches, order-preserving, failed batches stay
unresolved without failing the graph), `workRefToHref` (exact-locale
published hits → canonical hrefs; lesson/landing rules; nothing guessed),
`createRecordResolver`, and real wiring inside `loadHeroGraph` for fa+en
(index.astro call sites unchanged).

Failing before: proven by absence (zero runtime references pre-change).
After: 10/10 new `hero-graph-resolve.test.ts` green — dedupe/skip, 50+5
batching, partial failure, wrong-locale/bad-slug non-links, and
**fetch→rendered-link**: stubbed graph + resolver → `loadHeroGraph` →
`HeroGraph.astro` rendered via the Astro container asserts the canonical href
in HTML for **en and fa**, with unresolved IDs producing no link.
Remaining limit: PU-SYNC-graph packet itself (generated resolver
types/fixture from the accepted schema) is still NOT_STARTED; href rules
mirror the backend route maps.

## A06 — CA-01 historical guards — FIXED

Cause: one test banned Three.js from the live tree forever (breaking the
legitimate CA-04 adoption), another attributed the whole-checkout `git status`
diff to CA-01 (breaking every later packet).

Changes (PUBLIC `src/foundation.contract.test.ts` only): the dependency
invariance is now checked against the CA-01 delivery artifact
(`v2-overlay.json`: `runtimeChange.* == false`, bounded Three.js allowance
credited to CA-04, handoff preserved); the checkout scan is replaced by a
delivery-evidence reproducibility check (manifest↔overlay consistency,
pinned-snapshot presence). Isolated-fixture Three.js accept/reject tests,
snapshot/order/portal/negative validator scenarios untouched; Three.js stays
installed.

Failing before: baseline PUBLIC failures at foundation:435 (three absence)
and :590 (checkout diff) plus the OpenAPI pin.
After: foundation 16/16 green (includes the production `astro build` with
Three.js installed).

## A07 — contracts and consumer sync — FIXED

Cause: 14 backend drift failures + 1 public pin failure: 16 additive packet
endpoints plus audit-fix schema deltas with no new acceptance; fixtures and
pins stale.

Changes:
- Exported from source (`scripts/export_openapi.py`); semantic diff HEAD vs
  fresh: **+16 paths, 0 removed, 0 changed pre-existing operations**
  (public +8: resolver, localized site, collections×2, series detail,
  lessons×2, analytics; admin +8: analytics, case-study, revision detail,
  jobs×3, localized site×2). Additive schema deltas only on the new paths
  (`revokedPaths`, analytics I08 error responses).
- New scaffold acceptance addendum in `OPENAPI-ACCEPTANCE.md` (history
  preserved): CRLF `47980f8f…` (48 paths, v0.4.0) / `1176c069…` (57 paths,
  v0.1.0) / `154a2c1b…` (124 ops); `PROVENANCE.json` re-locked;
  `test_openapi_hash_drift.py` re-pinned (LF hashes alongside);
  `verify_openapi_export.py` 3/3 MATCH; access evidence
  (`test_public_openapi` + `test_admin_openapi`) 9/9 green.
- Fixtures from real responses (`CONTRACT_FIXTURES_WRITE=1`, synthetic seed):
  only the reviewed additive I03 metadata changed; component validation kept.
  `ARTICLE_DETAIL_FIELDS` and admin schema entity set extended to the reviewed
  shapes (sets stay exact; nothing deleted to force green).
- PU-SYNC-public: pins moved, `generate:api-types` re-ran, 3 consumer
  fixtures byte-aligned, public-310 6/6 green.
- PU-SYNC-admin: pin moved, `generate:api-types` re-ran, new
  `product-contract.test.ts` (3/3, written failing first), full admin suite
  + typecheck build green.
- `OPENAPI-TYPESCRIPT-GENERATION.md` hash/count/pin rows updated (admin pin
  row corrected to the real `src/generated/openapi-hash.json` mechanism).

Failing before: 14 backend drift + 1 public pin.
After: backend suite fully green (see counts); both consumer lanes green.
Remaining limits: the suggested ADMIN `generate:api-types` pin guard was not
added (outside this scope, still recommended); visual acceptance, deploy, and
owner review are untouched (local acceptance only).

## A08 — multilingual bulk archive — FIXED

Cause: one job tagged with the last item's locale carried all paths.

Changes: `bulk_archive_items` groups by locale and enqueues one pending-removal
job per locale (with per-locale revoked sets after A01).

Failing before: `test_bulk_archive_mixed_locales…` (0 fa jobs).
After: fa+en jobs asserted path-exact with no cross-locale leakage and no
null-locale catch-all; existing bulk tests green.

## A09 — analytics validation — FIXED

Cause: generic shape checks admitted any well-formed target/path; legacy
`HttpError` shapes on a new endpoint.

Changes (BACKEND): per-event registered-target registry grounded in shipped
surfaces (`cv_download → {academic_cv, industry_resume}`; every other event
requires an empty target until its sender registers real IDs); canonical
route-structure validation with locale consistency (locale-neutral gateway
`/` allowed); 4096-byte limit → 413; same-origin/rate-limit kept; **all**
ingest rejections use the I08 envelope (including a route-scoped 422 envelope
for schema-shape failures — legacy routes byte-identical); aggregate,
identifier-free storage untouched. Contract §I07 enforcement note.

Failing before: 5 new tests (unregistered target, page_view target, unknown
route/locale mismatch, oversized body, 422 envelope).
After: 16/16 analytics green. One existing ingest test moved to the
registered `academic_cv` target (intended behavior change).
Remaining limit: the registry grows only with shipped senders (PU-21); demo/
contact/research-profile targets stay empty-only until then — fail-closed by
design.

## A10 — machine-auth nonce — FIXED

Cause: `validate_machine_request` persisted the nonce before the HMAC check,
letting forged requests pollute/burn nonce state.

Changes: verify timestamp → nonce shape → **HMAC first**, then atomically
claim the nonce (replay → 401). Empty nonces rejected.

Failing before: `test_invalid_signature_consumes_no_nonce_a10` (forged nonce
row existed).
After: 8/8 jobs tests green (forged leaves zero state; same nonce reusable
once legitimately; replay still 401; stale timestamps consume nothing).

---

## Verification totals (final, this mission)

| Lane | Command | Passed | Failed | Skipped |
|---|---|---|---|---|
| BACKEND | `uv run pytest -q` | 885 | 0 | 0 |
| BACKEND | `uv run ruff check .` | clean | — | — |
| BACKEND | `makemigrations --check` | clean | — | — |
| BACKEND | migration 0002 fwd/back/fwd (throwaway DB) | OK | — | — |
| ROOT runner | `python Infra/staging/test_rebuild_product.py` | 27 | 0 | 0 |
| ROOT | `validate-plan.py` | 1 structural rule red (pre-existing PUBLIC dispatch gap, see gates) | — | — |
| PUBLIC unit | `npm.cmd test` | 353 (61 files) | 0 | 0 |
| PUBLIC | `lint` / `validate:design` / `build` | pass / pass / 33 pages + pagefind en+fa + sitemap | — | — |
| PUBLIC e2e (seeded ready graph) | ca03 + ca05 | 12 | 0 | 1 (gated atlas specimen, legitimate) |
| PUBLIC e2e (seeded) | ca06 + ca07 | 21 | 0 | 0 |
| PUBLIC e2e (seeded) | public-150-shell | 7 | 0 | 0 |
| PUBLIC e2e (clean build) | wp40-home + wp40-gateway (+wp10 acceptance in run 1) | 11 (+15 in run 1) | 4 stale (pre-existing, evidenced below) | 0 |
| ADMIN | `npm.cmd test` | 121 (29 files) | 0 | 0 |
| ADMIN | `lint` / `build` (tsc+vite) | 0 errors (5 pre-existing warnings) / pass | — | — |

Audit baselines for comparison: backend was 848+14 failed; public unit was
340+3 failed; runner was 8 passed. The 4 wp40 e2e failures are pre-existing
stale specs: they assert `[data-graph-state="unavailable-route"]` from the
pre-CA-03 separate graph section, which CA-03 removed from the pages (the
component still exists, hence the passing unit behavior test). They fail
identically on the clean unseeded build, predate this mission (stale at first
read), and were neither deleted nor skipped. The previously-skipped
resize/theme ready-data test now runs and passes.

Browser matrix covered (existing specs, synthetic ready data where noted):
Home FA/EN, gateway, 320/390/768/1440, light/dark (portal + home theme
toggle), mobile/desktop resize, no-JS (home+gateway), reduced-motion
(home+gateway), WebGL/chunk failure fallbacks, keyboard/focus, 200% zoom,
graph selection/interaction en+fa without skips. Synthetic records were
explicitly labeled, localhost-only, and never committed or presented as real;
the final `dist/` is a clean unseeded build (ignored build output).

## Schema hashes and consumer sync

- Accepted (addendum 2026-09-06, history preserved): public CRLF
  `47980f8f…` (48 paths, v0.4.0; LF `1efc7313…`); admin CRLF `1176c069…`
  (57 paths, v0.1.0; LF `046bef5a…`); inventory CRLF `154a2c1b…` (124 ops).
- PU-SYNC-public: pins moved (`contracts/openapi.public.sha256`,
  `src/generated/openapi-hash.json` @ `bd6682e`/48 paths), types regenerated
  from the accepted snapshot, 3 fixtures byte-aligned, public-310 6/6.
- PU-SYNC-admin: pin moved (`src/generated/openapi-hash.json` @ `bd6682e`/
  57 paths), types regenerated, new `product-contract.test.ts` 3/3.
- Local acceptance only: no visual acceptance, no deploy, no owner review.

## Exact per-repository changes and uncommitted state

- BACKEND (`bd6682e`, all uncommitted, no reset/clean): edited
  `apps/rebuild/services.py`, `apps/rebuild/models.py`,
  `apps/content/services/lifecycle.py`, `apps/content/published.py` (new),
  `apps/rebuild/migrations/0002_*` (new), `apps/api/{api,admin_content,
  admin_publication_jobs,record_resolver}.py`, `apps/analytics/api.py`,
  `apps/content/management/commands/publish_scheduled_content.py`,
  `config/settings/{base,production}.py`, regenerated OpenAPI snapshots +
  `PROVENANCE.json`, 3 fixtures, 6 existing test files; new tests
  (`draft_published_isolation`, `publication_lifecycle_a03`, A08/A09/A10
  additions); drift pins re-pinned. Plus all pre-existing agent work,
  untouched.
- ROOT (`c69e339c`): edited `Infra/staging/rebuild-product.py`,
  `Infra/staging/test_rebuild_product.py`, `Docs/03-contracts/
  {PRODUCT-INTERFACES-V2,OPENAPI-ACCEPTANCE,OPENAPI-TYPESCRIPT-GENERATION}.md`,
  `Docs/08-operations/PRODUCT-PUBLISHING-RUNBOOK.md`,
  `Docs/05-delivery/{EXECUTION,queue,validator,tasks,board,task-lists}.md`
  (queue dir untracked), new `reviews/AUDIT-FIX-{STATE,REPORT}-2026-09-06.md`.
  Pre-existing agent doc/infra modifications untouched.
- PUBLIC (`b895b2c`): edited `src/lib/hero-graph-content.ts`,
  `src/pages/{fa,en}/index.astro` (comments), `src/foundation.contract.test.ts`,
  pins/harness/generated-types/fixtures; new `hero-graph-resolve.test.ts`.
  Pre-existing agent work untouched (including the recovered `parallel-wip`
  incident — foreign stash left intact).
- ADMIN (`ca4dd3d`): regenerated `src/generated/admin-api.ts`, moved pin,
  new `src/lib/api/product-contract.test.ts`. Nothing else touched.

## Open gates (with reason)

1. **A02 real-ingress integration** — no deployed Caddy/Nginx exists in this
   environment; file-local + isolated-server evidence only.
2. **Visual acceptance** (CA-17 / PU-25-review) — owner/design review open by
   program design.
3. **Rollout/deploy/operation** — no deploy performed; staging Compose keeps
   the legacy trigger off; runner dispatch is explicit until secrets and
   `PUBLICATION_RUNNER_ARGV` are provisioned.
4. **Queue validator** — structurally valid; still red on the pre-existing
   PUBLIC dispatch gap (tracked implementation files inside NOT_STARTED
   packets), which predates this mission and is coordinator business. The new
   status is fully supported (rule + review_note enforcement + ROOT runner
   topology rule).
5. **4 stale wp40 e2e specs** — pre-existing, evidenced above; left failing
   rather than deleted/skipped.
6. **Owner content/credential/product decisions** — none encountered as
   blockers; none invented.

## Next packets actually unblocked

No packet's dependency set is fully DOC_COMPLETE/accepted yet, so under the
dispatch rule **no new packet is selectable today** — this is reported
honestly rather than papered over. The concrete unblock path:

1. Review + accept the 9 IMPLEMENTED_UNREVIEWED packets, starting with the
   two ex-REVISE ones (CA-01, PU-03-resolver) against this report.
2. Accepting PU-03-resolver makes **PU-SYNC-graph** selectable (its only
   dependency), which then unblocks CA-02 → CA-03 → CA-04… in dependency
   order.
3. Accepting PU-SYNC-public / PU-SYNC-admin unblocks the PUBLIC family track
   (PU-13-*) and the ADMIN editor track (PU-09-transport → editor → host →
   family editors) respectively.
4. PU-25-review / CA-17 remain the visual-acceptance close-out after
   implementation packets land.
