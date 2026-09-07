# Acceptance verification — provenance split + PU-03-settings / PU-SYNC-graph local acceptance (2026-09-06)

Scope: mission verification + provenance repair + acceptance decisions for PU-03-settings and PU-SYNC-graph. Coordinator authority for ACCEPTED_LOCAL was granted by the mission for reviewed packets with accepted dependencies and sufficient evidence. Local acceptance only — not visual, content, or deployment acceptance. No commit/push/merge/deploy, no real-database change (disposable test DB only). Prior reports (`COORDINATOR-REVIEW-2026-09-06.md`, `EXECUTION-REVIEW-2026-09-06-PU04.md`) are preserved as history and treated as claims re-verified here against current code.

## 1. Baseline registration

- HEADs (branch `main`, all repos): ROOT `c69e339c8c26788467d29ad346fb7df99b1c2842`, BACKEND `bd6682ea9dae7e5bf6957c36691dc3a94a00ea37`, PUBLIC `b895b2cb9c6ad9519d55bd2663448461931c0a39`, ADMIN `ca4dd3d26484d4468465c756d302b8e3247a3cbe`.
- Queue at entry: PU-03-settings IMPLEMENTED_UNREVIEWED, PU-SYNC-graph IMPLEMENTED_UNREVIEWED, PU-07-revisions / PU-07-runner IMPLEMENTED_UNREVIEWED (ex-REVISE), PU-03-resolver + CA-01 ACCEPTED_LOCAL, ready_to_start empty.
- Arithmetic check on the disputed failure: coordinator suite 885 green + 8 tests added by the prior delivery (5 settings + 1 snapshot repro + 2 isolation) = 893 = current 892 passed + 1 failed. The single failure (`test_provenance_matches_accepted_record`) is unrelated to the 8 added tests. It was reproduced here BEFORE any edit in this session (PROVENANCE at hash `3469b4…`, status `source-generated-unaccepted`), so it is not an artifact of this session's probe runs.

## 2. Provenance failure — cause and principled fix

### 2.1 Independent reproduction

`uv run pytest tests/test_openapi_hash_drift.py::test_provenance_matches_accepted_record -q` → FAILED: `assert 'source-generated-unaccepted' == 'scaffold-accepted'`. Full suite before fix: 892 passed, 1 failed.

### 2.2 What the new export changes (measured, not assumed)

Ran `uv run python scripts/export_openapi.py` twice on the unchanged tree: `public-openapi.json` (`47980f…`), `admin-openapi.json` (`1176c0…`), `endpoint-inventory.md` (`154a…`) byte-identical across runs; only `PROVENANCE.json` changed (`3469b4…` → `d3e819…`), and only its `generatedAtUtc` field. Artifact content never drifted.

### 2.3 Origin (evidence, not labeling)

At coordinator time the full suite was green, so PROVENANCE then carried a promoted acceptance (`scaffold-accepted`). Every product packet's acceptance steps mandate running `scripts/export_openapi.py`, which unconditionally writes `status: source-generated-unaccepted` with pending evidence and no `acceptanceRecord`. Those mandated runs overwrote the promoted file while artifact bytes stayed identical. The prior report's "timestamp churn only" description missed that the test asserts exactly the clobbered fields (`status`, `acceptanceRecord`), and its "pre-existing / unrelated" label for the resulting failure was incorrect: the failure was introduced by its own export runs (885 + 8 = 892 + 1 accounts for every test). Stated plainly because the mission required checking the origin.

### 2.4 Semantics of the two statuses

- `source-generated-unaccepted` = machine generation evidence: bytes produced from source at time T on commit C, no human acceptance attached. The export tool MUST always write this (per `Docs/03-contracts/OPENAPI-ARTIFACT-CONTRACT.md`: "Their PROVENANCE.json must state source-generated-unaccepted"; also `Back-End/docs/contracts/API-INVENTORY.md`: snapshots are "explicitly unaccepted").
- `scaffold-accepted` (+ `acceptanceRecord` → `OPENAPI-ACCEPTANCE.md`) = human acceptance pointer for reviewed, hash-locked bytes. The drift test's expectation is legitimate in substance but was pointed at the wrong file.

### 2.5 Inconsistency map (test / tool / doc / consumers)

- Export tool: correct (always unaccepted). Left unchanged.
- `PROVENANCE.json`: conflated generation evidence with the acceptance pointer; every regeneration made identical-snapshot acceptance ambiguous. Now generation-evidence-only by design.
- Drift test: asserted acceptance from the mutable file — direct contradiction with the artifact contract (contract = authority level 4, test = level 8 per AUTHORITY-ORDER), so aligning it is a correction, not a weakening.
- `OPENAPI-ACCEPTANCE.md` (+ addendum 2026-09-06): hash lock (48/57 paths, `47980f…`/`1176c0…`/`154a…`, commit `bd6682ea…`) remains valid and is the grounding for everything below. Its one stale sentence ("PROVENANCE.json records scaffold-accepted") is left untouched as history; supersession is recorded here and in ACCEPTANCE.json.
- `scripts/verify_openapi_export.py`: expected acceptance inside PROVENANCE — same contradiction; retargeted (below).
- Consumers: PUBLIC `generate-api-types.mjs` and ADMIN contract test read hash pins only — unaffected (verified: no PROVENANCE reference in either consumer path).
- Queue manifest: pinned timestamped PROVENANCE — fragile by construction (see §5).

### 2.6 Fix (separation) + allowlist record

`ACCEPTANCE.json` (new stable hash-based acceptance record, BACKEND `docs/contracts/openapi/current/`): status `scaffold-accepted`, record pointer, source commit `bd6682ea…` (= HEAD, verified), settings module, exact CRLF artifact hashes/paths/versions, access evidence (`test_public_openapi.py` + `test_admin_openapi.py`, 9 passed re-run here). Every value verified against the acceptance doc, HEAD, and live test runs — nothing invented. Export never touches it (verified byte-identical across exports: `b3b5f6a4…` before and after).
- Drift test: first three test groups untouched; `test_provenance_matches_accepted_record` now asserts from the stable record (same strength: status, record pointer, hashes, paths/versions) plus sourceCommit↔HEAD linkage; new `test_provenance_is_generation_evidence_only` locks the split (PROVENANCE unaccepted, no record pointer, artifacts equal).
- Verify script: gates against ACCEPTANCE.json (same 3/3 MATCH semantics), still snapshot-restores export-touched files.
- Expansion recorded BEFORE executing (mission rule), BACKEND-only, no shared-file conflict: PU-03-settings allowlist += `ACCEPTANCE.json` (also proposed_new_files), += `scripts/verify_openapi_export.py`; drift test edited under its existing single PU-20-events ownership (no duplication — duplicating it into settings would trip the validator's unordered-write rule). Single writers everywhere: ACCEPTANCE.json (resolver+settings, ancestor-ordered), verify script (settings only).

### 2.7 Before/after + idempotence proof

- Before: drift file 10 tests with 1 failure; full backend 892+1.
- After: `tests/test_openapi_hash_drift.py` 11 passed; export re-run leaves ACCEPTANCE byte-identical (`b3b5f6a4…`) and drift still 11 green (re-export can no longer make identical-snapshot acceptance ambiguous — the mission's core demand, demonstrated not asserted).
- `uv run python scripts/verify_openapi_export.py` → exit 0, 3/3 MATCH ("matches the accepted record"). Note: must run under `uv run` (bare `python` lacks django) — invocation detail, not a defect.
- Full backend after fix: **894 passed, 0 failed** (893 + 1 new linkage test). Ruff clean. `makemigrations --check`: no changes.

## 3. Revisions / runner re-verification (claims vs current code)

- Backend targeted re-run: settings 17 + resolver 33 + revision_snapshot 6 + isolation 6 = **62 passed**. Collected test names confirm the repro (`test_project_snapshot_with_nonempty_relations_regression`, nonempty evidence/collaborators/funding) and the HTTP cycle (`test_project_publish_restore_cycle_serves_frozen_relations_a04`: publish → edit/restore draft → GET frozen → republish → GET new; archive/removal/ordering tests present).
- Runner re-run: `python -m unittest discover -s Infra/staging -p test_rebuild_product.py` → **29 passed**, including both `remove_revocations_failure_blocks_success_{normal,resume}_path` (REMOVAL_FAILED); propagation confirmed in code (`if not edge_mgr.remove_revocations`, rebuild-product.py lines 606/668).
- No new defects found; no additional code changes made in this mission to these two packets. Remaining gates (real ingress, visual, rollout) stay open as before.

## 4. Acceptance decisions

### PU-03-settings → ACCEPTED_LOCAL (BACKEND)

Per-dimension evidence: draft-only/absent/unsupported-locale → 404 NOT_FOUND envelope, no fallback (tests + `api.py` published-payload gate); FA/EN isolation (exact-locale test); admin OTP+CSRF on all mutations and If-Match on PUT with 409 semantics (code + 5 regression tests incl. CSRF_FAILED and 401/403 cases); nav (20, javascript:/data:/http:/unknown rejected, locale-prefixed accepted), audience (2, kind enum), presets (atlas-v2/arch-v2, motion/density enums); legacy `/api/site` + `/api/v1/admin/site` present and mounted, untouched; publish is atomic (select_for_update), snapshots payload, enqueues I06 job — enqueue proven by `test_localized_site_settings_publish_enqueues_publication_job` (locale `fa`, `removal_state not_requested`, paths `/fa/`, `/fa/site/`), 11/11 invalidation tests green. Publish POST has no If-Match by design: it carries no payload (intent is "publish current"), the snapshot is atomic, concurrent PUTs are If-Match-guarded, so last-writer-wins is benign; the contract does not require it. Migration `0005` is a pure CreateModel (inherently reversible, correct dependency on `0004`); forward application proven by every test-DB run, backward covered by the preserved handoff's disposable-DB evidence. Schema export deterministic (identical hashes across runs); no schema-shape change from this packet.

### PU-SYNC-graph → ACCEPTED_LOCAL (PUBLIC)

Types genuinely generated (`generate:api-types` re-ran here, `public-api.ts` byte-identical `70b247b2…`, no hand edits); fixture pin `47980f…` equals PUBLIC pin equals live backend schema; all records synthetic (reviewed full fixture, no persona claims); lesson honestly documented as resolver-400 (backend registry has 13 families, `lesson` absent → 400 INVALID_INPUT, `courseSlug` hardcoded `None` in both resolve paths — fixture's null-courseSlug and unsupported-lesson scenarios are truthful); 13 routeFamily mappings match the backend map exactly; consumer chain live (`hero-graph-content.ts` imports `WorkRefOut`; `hero-graph-content.test.ts` + `hero-graph-resolve.test.ts` green inside the full 354). Contract 9/9, prettier/eslint clean, full PUBLIC 61 files / 354 green, `astro build` complete (33 pages, Pagefind en/fa, sitemap). No frontend runtime change (only fixture/test/pinned types) → no browser retest required. Lesson *backend* support (I05 direction) is left as an explicit non-decision: inventing it in the fixture would be fabrication; it needs a backend packet and product decision (gate noted, not taken).

Both dependencies satisfied (PU-02 DOC_COMPLETE; PU-03-resolver ACCEPTED_LOCAL re-grounded in §5). Scope is local only in both pins.

## 5. Prior acceptances preserved

- CA-01: all 5 pinned files re-hashed — intact, untouched.
- PU-03-resolver: 7 unchanged pins re-verified byte-identical; `record_resolver.py` untouched; 33 resolver tests green (part of the 62). Shared-file change since its acceptance (`apps/api/api.py` project-detail resolvers, prior mission) does not touch the resolver endpoint; schema hashes unchanged. Manifest swap PROVENANCE→ACCEPTANCE (old pin `3469b4…` retired for the documented timestamp-fragility reason) with history kept here and in prior reports. Resolver stays ACCEPTED_LOCAL.
- No accepted file was edited to chase green; the only hand-authored acceptance bytes are the new stable record grounded in §2.6.

## 6. Queue synchronization

- `execution-tasks.json`: settings/sync → ACCEPTED_LOCAL + review_note → this report + handoff_state `accepted-local-uncommitted`; settings/resolver allowlist edits per §2.6 (PROVENANCE stays writable via 17 other packets; writers-overlap check holds: ACCEPTANCE shared only by ancestor-ordered resolver+settings).
- Packet specs: settings/sync status → ACCEPTED_LOCAL; coordinator notes added (settings: split + drop rationale; resolver: swap rationale).
- `EXECUTION.md`: 82 = 3 DOC + 4 ACCEPTED + 27 IMPLEMENTED + 0 REVISE + 5 BLOCKED + 43 NOT_STARTED; table rows updated; banner points here with history links.
- `Back-End/TASK-LIST.md`, `public-site/TASK-LIST.md`: rows → ACCEPTED_LOCAL. CA mirror (`tasks.json`) untouched — no CA status changed.
- Manifest `ACCEPTED-LOCAL-2026-09-06.json`: resolver swap + new settings (12 files) + sync (4 files) entries; history (old pins, reasons) in this report; prior review files untouched.

## 7. Final validation (real runs, no skips)

- BACKEND full: **894 passed, 0 failed, 0 skipped**; ruff clean; `makemigrations --check` clean.
- Runner: **29 passed** (unittest OK).
- PUBLIC: contract 9/9; full **354 passed / 61 files**; prettier+eslint clean; generate deterministic; build complete (33 pages + Pagefind + sitemap; one pre-existing chunk-size advisory, not a failure).
- Invalidation (enqueue evidence): 11/11. Verify gate: exit 0, 3/3 MATCH. ADMIN tree untouched by this mission (status identical to baseline) — not re-run; it is not the affected consumer.
- `validate-plan.py`: **PASS** (counts 4/27/0 as above; ready_for_review now empty since both eligible packets accepted; ready_to_start empty; source drift reported separately as before; publication/visual acceptance OPEN).
- `git diff --check`: PASS in all four repos (CRLF advisory warnings only).
- No test deleted, skipped, or weakened to pass a gate (the drift-test change is a contract-grounded correction plus one added linkage test).

## 8. Ready queues and still-open gates

- Newly accepted: PU-03-settings, PU-SYNC-graph (dependents such as PU-04-catalog/PU-SYNC-public/admin may now legitimately consume them; enactment is for future workers, not this mission).
- ready_for_review / ready_to_start recomputed by the validator run (see RECONCILIATION-CHECK.json).
- Still open (explicit, not hidden): real-ingress edge verification, visual/content acceptance, deployment/rollout, lesson-resolver backend support decision, ADMIN editor chain (BLOCKED), and any future schema change follows OPENAPI-ACCEPTANCE change control. Operating rule going forward: export freely (only PROVENANCE timestamp moves); acceptance is decided via ACCEPTANCE.json + drift tests + verify script; manifest refresh is required only when artifact bytes change, and then with full re-review.
