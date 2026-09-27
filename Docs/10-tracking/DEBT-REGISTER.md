# Debt Register

| ID | Debt | Owner | Planned gate |
|---|---|---|---|
| DEBT-001 | Legacy backend route prefixes are inconsistent | Backend | R2 |
| DEBT-002 | Backend still contains legacy SPA-serving routes | Backend | R6 cutover |
| DEBT-003 | Legacy deployment files assume old paths | Backend/Operations | R1 |
| DEBT-004 | Root coordination repository has no remote | Owner | Before multi-machine work |
| DEBT-005 | **Staging environment deleted; every staging-anchored procedure, the `Deploy staging` workflow, and the credentialed `PU-25-admin-journey` route are stale.** Blocks R7 re-verification, R9 rollout and Plan D Task 13 | Owner | Before R9 |
| DEBT-006 | **Production Atlas renders `unavailable` despite a healthy API** — no runtime recovery path when the build-time snapshot is not `ready` | Agent | Immediate (tracked on `fix/atlas-runtime-availability`) |
| DEBT-007 | **68 execution-queue packets are `IMPLEMENTED_UNREVIEWED`** — implementation evidence exists but no independent review or owner acceptance. Not a completion count | Coordinator | Before PU-25-review |
| DEBT-008 | **`RECONCILIATION-CHECK.json` is `STALE`** with 20 drifted source hashes; queue bookkeeping no longer matches reality | Coordinator | Before PU-25-review |
| DEBT-009 | `public/research-universe/models/*.glb` — never promoted in the asset ledger, no runtime consumer, but **owner artwork**. Provenance is the tracked `.blend`, not the shipped GLB; left in place pending an owner keep-or-archive decision rather than deleted by an agent | Owner | Plan D Task 12 closeout |
| DEBT-010 | `.ru-track` / `.ru-stage` / `.ru-scene` selectors in `src/styles/research-universe.css` lost their only emitter when `HeroGraph.astro` was retired, but share a file with the live shared `.ru-*` base the Atlas scene still emits. Splitting it is out of scope for a retirement commit | Agent | Next CSS cleanup boundary |
