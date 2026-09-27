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
| DEBT-008 | **`RECONCILIATION-CHECK.json` is `STALE` — cause now established, not just noted.** `validate-plan.py` aborts at line 78 (accepted-HEAD), so the file-hash check never runs; re-running it manually shows **46 of 87 accepted files drifted** (0 missing), so the 10 `ACCEPTED_LOCAL` labels no longer describe the current trees. Also `ACCEPTED-LOCAL-2026-09-06.json` holds 68 entries vs 10 in the live queue. Re-baselining is an owner/coordinator decision | Owner (re-baseline) + Agent (validator fix) | Before PU-25-review |
| DEBT-009 | `public/research-universe/models/*.glb` — never promoted in the asset ledger, no runtime consumer, but **owner artwork**. Provenance is the tracked `.blend`, not the shipped GLB; left in place pending an owner keep-or-archive decision rather than deleted by an agent | Owner | Plan D Task 12 closeout |
| DEBT-010 | ~~`.ru-track` / `.ru-stage` / `.ru-scene` selectors~~ **CLOSED 2026-09-27** — all 10 references were inside one stylesheet with no emitter; removed in public-site `3294a7f` after proving the live Atlas scene's `.ru-label*`/`.ru-leaders` classes and the `--ru-*` custom properties are untouched. lint clean, 638 passed, build 46 pages | — | Closed |
