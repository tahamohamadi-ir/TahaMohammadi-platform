# PUBLIC-190 Visual and Accessibility QA Report

**Packet:** WP-50  
**Tool:** Cursor (substituting Hermes automated matrix)  
**Public-site commit:** `ea70e7b` (`main`)  
**Coordination commit:** `1edd30c` (`main`)  
**Run date:** 2026-09-01  
**Result:** `REVISE`

---

## Automated gate summary

| Command | Exit | Summary |
|---|---:|---|
| `npm test` (Vitest) | 0 | 99 passed |
| `npm run validate:design` | 0 | 24 components, 6 templates; central hash match |
| `npm run build` | 0 | 15 static pages; no `/_design` leak |
| `npm run build:atlas` | 0 | 16 pages including `/_design`; positive Atlas gate |
| `npx playwright test` | 0 | 41 passed (foundation, a11y, visual, WP-40 gateway/home/media, shell, atlas gate) |
| `npm run test:foundation` | 0 | 2 passed |
| `npm run test:a11y` | 0 | 6 passed |
| `npm run test:visual` | 0 | 1 passed (token snapshot); full suite green via unfiltered run |

**Evidence note:** Playwright required `npx playwright install chromium` and a clean `dist/` rebuild before the webServer harness succeeded. Stale `dist/` manifests caused an initial `@visual` failure (`TypeError` in base64 decode during prerender).

---

## Automated matrix coverage (WP-50 Section 5)

| Check | Status | Evidence |
|---|---|---|
| `lang`, `dir`, one H1 | pass | `wp40-home.e2e.ts`, screenshot-discovery tests |
| No horizontal overflow | pass | Gateway + Home @390/1440/768, 200% zoom tests |
| Keyboard / skip / theme | pass | `wp10-foundation.*`, `public-150-shell.e2e.ts` |
| axe serious/critical on theme control | pass | `wp10-foundation.accessibility.e2e.ts` |
| No-JS readability | pass | `wp40-home.e2e.ts` JS-disabled test |
| Images blocked readability | pass | `wp40-home.e2e.ts` |
| Single theme variant per slot | pass | `wp40-media.e2e.ts`, `wp40-gateway.e2e.ts` |
| AVIF/WebP `currentSrc` at suitable width | pass | `wp40-media.e2e.ts` |
| No raw `/media/` art URLs | pass | `wp40-gateway.e2e.ts`, `wp40-media.e2e.ts` |
| No deferred assets in runtime | pass | `promoted-media.test.ts` |
| Graph semantic list, non-interactive unavailable | pass | `wp40-home.e2e.ts` |
| Atlas excluded from production | pass | `public-170-atlas-gate.e2e.ts`, Vitest foundation contract |

Screenshot SHA-256 baselines were **not** captured to `test-results/visual/` in this run; automated discovery tests assert matrix eligibility only (`@later-packet-acceptance`).

---

## Manual matrix (WP-50 Section 5) — not closed

| Target | Locale | Theme | Viewport | Status |
|---|---|---|---:|---|
| Gateway | neutral | Light/Dark | 1440 | **pending owner/manual** |
| Gateway | neutral | Light/Dark | 390 | **pending owner/manual** |
| Home | EN | Light/Dark | 1440 | **pending owner/manual** |
| Home | FA | Light/Dark | 390 | **pending owner/manual** |
| Home | EN/FA | Light/Dark | 768 | automated reflow only |
| Home + Gateway | applicable | Light/Dark | 200% zoom | automated composition only |

Manual checks still required per `VISUAL-QA-CONTRACT.md`: concept parity review, screen-reader walkthrough, crop/focal review, and owner sign-off.

---

## Findings

### F-01 — PUBLIC-180 content-state components not closed (blocking)

| Field | Value |
|---|---|
| Severity | **blocking** |
| Route | design system / page families |
| Contract | `CONTENT-STATE-MATRIX.md`; `PUBLIC-180` |
| Expected | Shared `loading`, `empty`, `unavailable`, `error`, `untranslated` (and matrix-aligned `no-results`) primitives with state tests |
| Observed | Per-component flags (`unavailable`, `inactive`, `loading`) exist; no dedicated content-state module or matrix tests |
| Owning packet | **PUBLIC-180** (new implementation slice; prerequisite for closing `PUBLIC-190`) |

### F-02 — Manual visual acceptance not recorded (blocking)

| Field | Value |
|---|---|
| Severity | **blocking** |
| Route | `/`, `/en/`, `/fa/` |
| Contract | `VISUAL-QA-CONTRACT.md`; execution authority WP-50 manual matrix |
| Expected | Side-by-side concept comparison with documented acceptable deviations and screenshot SHA-256 hashes |
| Observed | Automated structural gates only; no committed manual evidence |
| Owning packet | **WP-50 manual / WP-60 owner** |

### F-03 — TASK-LIST status drift (informational)

| Field | Value |
|---|---|
| Severity | informational |
| Contract | `TASK-LIST.md` |
| Expected | `PUBLIC-140`–`PUBLIC-170` marked complete when integrated evidence exists |
| Observed | Tasks remain `[ ]` / `[~]` despite Vitest/Playwright/Atlas gates on `main` |
| Owning packet | **WP-60 / coordination status commit** |

---

## Verdict

**`REVISE`** — automated implementation gates are green on `ea70e7b`, but `PUBLIC-180` and manual visual acceptance remain open. Do not mark `PUBLIC-190` Done until F-01 and F-02 close and the owner explicitly accepts (WP-60).

---

## Resume instruction

1. Implement **PUBLIC-180** on `Front-End/public-site`.
2. Re-run the command table above from a clean `dist/`.
3. Capture manual matrix screenshots under ignored `test-results/visual/` with SHA-256 hashes.
4. Update this report to `PASS` or a revised `REVISE` list.
5. Present acceptance dossier to owner (WP-60).
