# Coordinator verification, 2026-09-06

Scope: independently review OpenCode's A01–A10 remediation, repair the remaining WP-40 browser checks, reconcile dispatch state and accept only evidenced packets. No commit, push, deploy or production database change.

## Independent results

- BACKEND full suite: 885 passed; ruff passed.
- PUBLIC full unit suite: 353 passed in 61 files.
- ADMIN full suite: 121 passed; TypeScript/Vite build passed.
- ROOT runner: 27 passed, using isolated test fixtures/services.
- Original WP-40 browser suite: 11 passed, 4 failed, independently reproduced.

Three Home failures asserted the removed three-node separate graph. Replaced those assertions with integrated semantic graph checks: ready payload node count and visible labels, or truthful empty/error/unavailable content without fabricated links. Image-blocked and no-JS checks remain. The fourth failure was a real accessibility defect, not a stale assertion: gateway accessible heading was `TahaMohammadi`. Added the correct accessible name to the actual H1; preserved the existing strict browser assertion.

## Decisions

- CA-01: ACCEPTED_LOCAL for the versioned overlay and historical-reference validation only. Full unit suite verifies future Three.js allowance and historical constraints. No visual/deployment acceptance implied.
- PU-03-resolver: ACCEPTED_LOCAL for endpoint parsing, locale/privacy filtering and descriptor contract, with the full backend suite passing. This does not accept the broader publication-snapshot implementation in PU-07-revisions.
- PU-07-revisions: REVISE. A04 does not yet substantiate full parent/story/relation isolation. `materialize_published_item` restores scalar/FK fields but keeps live reverse/M2M relations. The public project collaborator resolver reads the live relation manager.
- PU-07-runner: REVISE. Both normal completion and resume paths ignore the Boolean result of `remove_revocations`; a failed removal/apply/probe can still produce a succeeded callback. Require failure propagation and regressions for both paths. Real ingress and rollback acceptance remain open.
- Other existing implementation handoffs: IMPLEMENTED_UNREVIEWED, not NOT_STARTED. Existing blocked admin editor/transport/host/family handoffs: BLOCKED. Sync handoffs superseded by the A07 report retain history and are IMPLEMENTED_UNREVIEWED.

### Reproduced project snapshot defect

An isolated Django test database was created and destroyed using setup_databases/teardown_databases. A synthetic draft Project with a ProjectCollaborator was passed to the actual `_build_full_content_snapshot(project, 'project')`. Result:

`AttributeError: 'ProjectCollaborator' object has no attribute 'affiliation'`

The serializer also references collaborator `url/is_approved/position`, funding `funding_entries`, and evidence fields that must be checked against the real models. Current collaborator model fields include `name`, `role`, `publication_approved`. This is independent evidence that green tests with empty project relations do not prove complete snapshot handling.

Required PU-07-revisions follow-up: regression with nonempty project evidence/collaborators/funding through HTTP publish/restore; correct field mapping from actual models; ensure public reads use frozen approved relations until republish; preserve historical records and explicit archive semantics. Add real nonempty relation fixtures, not just scalar article tests.

Required runner follow-up: failure tests for remove_revocations false in both fresh and resume paths; prevent succeeded report and preserve truthful removal/error state. Keep real ingress acceptance separate from localhost test success.

## Queue and ownership

The coordinator reconciles all existing handoffs, preserves original reports, and extends exact leaf-packet allowlists for already present audit fixes and the two current PUBLIC edits. This is explicit retrospective ownership classification, not proof that previous workers respected their original allowlists. No unrelated notebook, cache, media or foreign stash is adopted.

ACCEPTED_LOCAL requires a pinned file manifest and passing dependencies. Hash drift invalidates that acceptance. It permits local dependency use of this exact uncommitted snapshot, not deployment. BLOCKED/REVISE/IMPLEMENTED_UNREVIEWED do not satisfy dependencies. Already implemented eligible packets appear under ready_for_review, not as new implementation assignments.

The current validator report records counts, ready queues and open visual/publication gates. Historical source drift is reported independently of structural validation; it must not masquerade as a structural failure or a release PASS.

## Final verification and resume point

- WP-40 Home/gateway after repair: **15 passed, 0 failed, 0 skipped**. CA-07's 12 gateway checks also passed in the preceding combined run; no gateway runtime changes followed that run.
- Queue validator: **PASS**. 82 packets: 3 DOC_COMPLETE, 2 ACCEPTED_LOCAL, 27 IMPLEMENTED_UNREVIEWED, 2 REVISE, 5 BLOCKED, 43 NOT_STARTED. Checks include DAG/file-write ordering, local links, CA status/dependency mirror, exact accepted-file hashes and HEAD, tracked/untracked product change ownership, and diff whitespace.
- ready_for_review: PU-03-settings and PU-SYNC-graph. These are existing implementations to review, not instructions to rebuild them. ready_to_start is empty; accepting unrelated packets prematurely to unblock ADMIN would be inaccurate.
- Two trailing blank lines in BACKEND admin_api.py/services.py were normalized for diff-check only; backend runtime behavior was not changed in this coordinator pass.
- Acceptance manifest: [exact snapshots](ACCEPTED-LOCAL-2026-09-06.json). Any change to those bytes requires re-review before continuing dependent work.
- This pass does not close the new PU-07-revisions/runner findings, actual ingress testing, visual review or rollout gates. No commit/push/deploy performed.
