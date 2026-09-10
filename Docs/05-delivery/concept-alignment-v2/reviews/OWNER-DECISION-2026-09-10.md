# Owner decision record — 2026-09-10

Recorded from the platform owner's answer round during R8 closure. These are
owner decisions, not agent inferences.

| Item                                           | Decision                                                                                  |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- |
| F-02 — PF-02 creative detail                   | Current empty-shell captures accepted; published creative detail remains owner CMS content. |
| F-03 — production performance telemetry        | Accepted as a post-launch (non-blocking) field-measurement deferral.                        |
| F-05 — admin browser scope                     | Mocked-boundary matrix 5/5 + CI accepted; live PU-25 journey deferred to R9 with credentials. |
| Manual screen-reader spot check                | Automated axe/landmark coverage accepted; manual spot check non-blocking.                   |
| F-01 — PUBLIC-190 visual acceptance            | Owner is reviewing the served compare report; sign-off and §8 signature still pending.      |

## Effect on the execution queue

- `PU-25-admin-journey` remains `REVISE` in `execution-tasks.json`. The
  coordinator should re-disposition it toward R9 (credential-gated) with this
  record as the owner authority; agents must not flip the status by themselves.
- `PU-03-settings`, `PU-09-editor` and `PU-15-lessons` repairs need independent
  re-review to clear `REVISE`.
- R8 evidence package updated: `Docs/10-tracking/COORD-080-R8-SIGNOFF-PACKAGE.md`.

## Second owner round — same date (post-verification)

| Item                                        | Decision                                                                                              |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| F-01 visual review                          | **Revision required.** Owner feedback: icons are wrong; no image should sit below the graphs; graph text is messy; node/child-node hierarchy is unclear; the concepts are far more professional and beautiful across the board. Scope: Home EN/FA, Gateway, page families, shared chrome. |
| Capture-only Home rows (5)                  | Accepted as non-blocking capture-only rows.                                                            |
| Manual screen-reader (already recorded)     | Automated coverage accepted; manual spot check non-blocking.                                           |
| §8 signature                               | Owner approved recording with name `Taha Mohammadi`, date `2026-09-10` — **held** until F-01 revisions close. |
| PU-09-editor path                           | Agent builds admin browser evidence (RTL, focus, keyboard; CSRF/session expiry via server/mocked checks). |
| Queue status updates                        | Owner authorized: `PU-15-lessons` and `PU-03-settings` → `IMPLEMENTED_UNREVIEWED` (re-verified); `PU-25-admin-journey` → `BLOCKED` (R9 target). Applied 2026-09-10. |
| 66 `IMPLEMENTED_UNREVIEWED` campaign        | Start in dependency order (first ready packet `PU-26-seed-safety`).                                    |
| CI dependency + secret scans                | Add both to all three workflows (fail on high/critical dependencies; secret baseline gate).            |
| Node 20 actions deprecation                 | Upgrade actions and re-run CI.                                                                         |
| Contact delivery live test                  | Approved; send one real staging-form message to `taha95mohammadi@gmail.com`.                            |
| preview-token / MFA / session-expiry live   | Moved to R9 (consistent with F-05).                                                                    |
| CM-02 residual (brand mark from promoted registry, nav fallback only when data is absent) | Accepted as non-blocking.                                                        |
| Staging admin account                       | Add a manual `workflow_dispatch` bootstrap with owner-provided secrets.                                |
