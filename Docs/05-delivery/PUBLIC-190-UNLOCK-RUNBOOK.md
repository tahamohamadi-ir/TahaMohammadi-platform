# PUBLIC-190 Post-PASS Unlock Runbook

**Trigger:** `Docs/10-tracking/PUBLIC-190-VISUAL-QA.md` records verdict `PASS` with §4 sign-off evidence filled and explicit owner approval.

**Agents must not set PASS.** Owner only.

---

## 1. Coordination repository

```powershell
cd D:\Project\tahamohammadi-platform
git pull
# Verify PUBLIC-190-VISUAL-QA.md shows Result: PASS and §4 Accepted rows checked
```

Edit and commit (coordination repo only):

- `Docs/10-tracking/PUBLIC-190-VISUAL-QA.md` — owner already set PASS
- `Docs/05-delivery/MULTI-AGENT-TASK-BOARD.md` — PUBLIC-190 → Done
- `Docs/05-delivery/MASTER-TASK-LIST.md` — advance R4/R8 items per release gates

```powershell
git add Docs/10-tracking/PUBLIC-190-VISUAL-QA.md Docs/05-delivery/MULTI-AGENT-TASK-BOARD.md Docs/05-delivery/MASTER-TASK-LIST.md
git commit -m "$( @'
Record PUBLIC-190 visual QA PASS and unfreeze page-family recovery.

'@ )"
git push
```

Record coordination SHA in unlock handoff.

---

## 2. Public-site repository

```powershell
cd Front-End\public-site
git pull
npm run build
npm test
npm run test:foundation
npm run test:performance
npm run test:visual -- --grep PUBLIC-270
npm run test:visual -- --grep PUBLIC-280
npm run test:nojs
npm run test:a11y
npm run report:visual-compare
```

Edit and commit (public-site repo only):

- `TASK-LIST.md` — PUBLIC-190 → `[x]`; lift freeze note on PUBLIC-201..PUBLIC-221
- `docs/quality/PUBLIC-350-RELEASE-EVIDENCE.md` — update gate-sweep SHA; note owner blocker cleared
- `src/test-harness/release-evidence.ts` — update `PUBLIC_RELEASE_GATE_SWEEP_SHA`; adjust R8 owner-acceptance slice if spec allows

```powershell
git add TASK-LIST.md docs/quality/PUBLIC-350-RELEASE-EVIDENCE.md src/test-harness/release-evidence.ts
git commit -m "$( @'
Unfreeze page families after PUBLIC-190 owner visual PASS.

'@ )"
git push
```

---

## 3. Still blocked after PASS

| Item | Owner | Notes |
| ---- | ----- | ----- |
| PF-02 creative detail | Public | Needs published API slug in static build |
| PUBLIC-320 staging smoke | Ops | `PUBLIC_STAGING_SITE_URL` + BACKEND-180 |
| PUBLIC-290 production telemetry | Platform | 75th-percentile field data |
| R7 integrated staging | All repos | Required before R9 |

---

## 4. Handoff evidence

Return both repository SHAs, gate command summary, and confirmation that `summarizeReleaseEvidence().ready` is still **false** until staging + remaining R8 slices close.
