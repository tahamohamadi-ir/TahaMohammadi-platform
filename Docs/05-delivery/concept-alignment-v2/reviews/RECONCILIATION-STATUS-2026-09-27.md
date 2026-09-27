# Reconciliation check — 2026-09-27 coordinator re-verification

**Narrative companion to `RECONCILIATION-CHECK.json`.** That file remains the
machine record and keeps its JSON schema; this file explains what the
coordinator found by actually running the validator.

**This supersedes the `STALE` 2026-09-08 note.** The prior note blamed
"pre-existing accepted-head assertions" without ever saying whether the accepted
*content* still holds. That question is now answered, and the answer matters:
**the drift is real content drift, not cosmetic bookkeeping.**

## Root cause, established by actually running the validator

```
$ python Docs/05-delivery/concept-alignment-v2/validate-plan.py
AssertionError at validate-plan.py:78
  assert git -C <repo> rev-parse HEAD == evidence['head']
```

All 10 `ACCEPTED_LOCAL` packets pin a commit that is no longer any repository's
HEAD:

| Repository | Pinned by acceptance | Actual HEAD now |
|---|---|---|
| ROOT | `48a6bc6` | `fe62e26` |
| PUBLIC | `aa06bdd` / `a033a73` | `5863f17` (checkout; `main` = `bddcebe`) |
| ADMIN | `7bcd412` | `e50fdce` |
| BACKEND | `4cc39cc` / `a48a6bd` | `e999737` |

## The finding that actually matters: content drift, not just HEAD drift

`validate-plan.py` aborts at the HEAD assertion (line 78), so the **file-hash
assertion one line later never runs**. Re-running the same SHA-256 comparison
the validator would have performed, across every accepted file:

| Packet | files unchanged | files **drifted** | files missing |
|---|---|---|---|
| PU-03-resolver | 3 | **5** | 0 |
| PU-SYNC-graph | 2 | **2** | 0 |
| CA-01 | 5 | 0 | 0 |
| CA-02 | 4 | 0 | 0 |
| CA-03 | 3 | **11** | 0 |
| CA-04 | 5 | **4** | 0 |
| CA-05 | 5 | **3** | 0 |
| CA-06 | 1 | **5** | 0 |
| CA-07 | 1 | **7** | 0 |
| CA-08 | 12 | **9** | 0 |
| **TOTAL** | 41 | **46** | **0** |

**Nothing is missing** — every accepted file still exists. But **46 of 87
accepted files have changed content** (44 unique paths; two files appear in two
packets), so the `ACCEPTED_LOCAL` label is no longer a truthful statement about
the current trees. Representative paths:

- `Back-End/apps/api/api.py`, both OpenAPI snapshots, `ACCEPTANCE.json`,
  `endpoint-inventory.md`
- `Front-End/public-site/src/generated/public-api.ts`
- `Front-End/public-site/src/components/hero/{HeroGraph,GraphNodeList}.astro`
- `Front-End/public-site/src/components/home/{HomeHero,HomeResearchGraph}.astro`
- `Front-End/public-site/tests/fixtures/contracts/product-record-resolver.json`

Some of this drift is **expected and good**: the Knowledge Atlas program merged
into `main` after the acceptance was recorded, and `HeroGraph.astro` was since

## Fix applied to the validator (agent-owned part of DEBT-008)

`validate-plan.py` could not report any of this, so the defect was fixed in the
tool itself rather than only described:

| Change | Why |
|---|---|
| Acceptance checks now **collect** defects instead of asserting in sequence | The old HEAD -> allowlist -> hash chain meant a stale HEAD masked the hash check. All 18 defects are now reported in one run. |
| A defectful queue reports `status: STALE`, not `PASS` | `status: PASS` reads as a completion signal. The plan *structure* is still validated; only the acceptance claim is withdrawn. |
| Human-readable defect list on stderr | `ACCEPTANCE DEFECTS: 18 across 10 packet(s); 44 file(s) drifted` plus one line per packet. |
| Untracked files no longer count as "unassigned product change" | Agent tooling blocks and local QA captures made the validator crash, so it went unrun — which is *how* the drift stayed hidden. Only tracked modifications are a product change now. |

Result after the fix — the validator runs to completion and self-reports:

```
ACCEPTANCE DEFECTS: 18 across 10 packet(s); 44 file(s) drifted
  PU-03-resolver   stale-head    pinned 4cc39cc, repository is at e999737
  PU-03-resolver   content-drift 5 of 8 files changed
  PU-SYNC-graph    stale-head    pinned aa06bdd, repository is at 5863f17
  PU-SYNC-graph    content-drift 2 of 4 files changed
  CA-01            stale-head    pinned aa06bdd, repository is at 5863f17
  CA-02            stale-head    pinned aa06bdd, repository is at 5863f17
  CA-03            content-drift 11 of 14 files changed
  ... (18 lines total)
```

`RECONCILIATION-CHECK.json` now carries `status: STALE`, `acceptance_status:
STALE`, `accepted_content_intact: false`, `accepted_files_drifted: 44`,
`accepted_files_missing: 0` and the full `accepted_defects` array. **CA-01 and
CA-02 have no content drift** — only a stale HEAD — so the honest verdict is
"8 of 10 packets have drifted content", not "all 10".

Re-baselining remains an owner/coordinator decision and **was not performed**.

## Required before the queue can be trusted

deliberately retired (Plan D Task 11, public-site `034b73a`). Some of it may be
unreviewed change. **The acceptance manifest cannot tell the two apart** — that
is exactly the gap, and it is why the queue cannot currently be trusted.

## A second, separate inconsistency

`execution-tasks.json` carries **10** `ACCEPTED_LOCAL` packets.
`reviews/ACCEPTED-LOCAL-2026-09-06.json` carries **68** entries — including
`PU-09-editor`, `PU-25-admin-journey` and every `PU-10-*` family, all of which
the live queue now marks `IMPLEMENTED_UNREVIEWED`, `REVISE` or `BLOCKED`. The
acceptance file is a **2026-09-06 artifact the queue has since moved past**; it
is not a second, wider acceptance.

## What the coordinator ran, separately from the validator

The validator runs no product tests. These were run directly:

| Suite | Result |
|---|---|
| Back-End Atlas projection + migration | 30 passed |
| public-site full vitest | 731 passed / 4 skipped / 121 files |
| admin-panel full vitest | 344 passed / 61 files |
| admin-panel hermetic journey | 4 passed |

## Required before the queue can be trusted

Re-baselining is a **coordinator/owner decision, not an agent's**, because
`ACCEPTED_LOCAL` grants dependency satisfaction. Coordinator recommendation,
stated as a recommendation:

1. Re-baseline the 10 `ACCEPTED_LOCAL` packets against the current trees by
   re-running **each packet's own verification** — not re-hashing alone, which
   would re-bless whatever happens to be there now.
2. Reconcile or retire the 68-entry acceptance file so it matches the queue.
3. Fix the validator to **report all** assertion classes (HEAD, file hash,
   allowlist coverage) instead of aborting at the first. Aborting at the HEAD
   check is precisely what hid the 46-file content drift for weeks.
4. Re-run the validator and let its result become the machine record.

**No packet status was changed. No product code was touched.**