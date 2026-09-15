# Hero v2 — Stage 3 report: scroll keyframe authoring (four static states)

**Status: complete. Final validator 22/22 pass, builder checks all green, every hard
constraint in the card's section 8 green.** Stage 2.7 is untouched and is still the look lock.

## 1. Winning method

**Pivot offset** (the card's primary method). The authored angles were *not* weakened, and
fallback A was not needed. The rotation pivot on `RIG_ROOT` is offset from the core's centre
along the direction **derived programmatically** from the core → HEALTH vector in the rig's
horizontal (XY) rotation plane — never eyeballed. Mechanically the offset enters the
projection as `d = (I − R)·P`, which is zero at rest (so FRAME_01 *is* the approved Stage 2.7
composition, by construction) and grows with the rotation, pushing the HEALTH companion
outward in projected space exactly as the card asked.

## 2. Winning pivot offset vector

| quantity | value |
|---|---|
| offset magnitude | **0.20** scene units (sign +1) |
| direction (unit, world XY) | **(0.97904, 0.20365, 0.0)** |
| core centre (world) | (−0.06, −0.22, −0.04) |
| RIG_ROOT origin (world) | **(0.13581, −0.17927, −0.04)** |

## 3. Authored states (exact values)

| frame | key | yaw° | pitch° | desktop parallax | rig rotation_euler° | intent |
|---|---|---|---|---|---|---|
| 1 | FRAME_01_REST | 0 | 0 | 0.00 | (0, 0, 0) | rest — the approved Stage 2.7 composition |
| 2 | FRAME_02_EARLY_ROTATION | 10 | 3 | 0.05 | (3, 0, 10) | small but visible depth change |
| 3 | FRAME_03_MID_STRONGEST_DEPTH | 26 | 10 | 0.11 | (10, 0, 26) | strongest depth, still calm |
| 4 | FRAME_04_SETTLED_REVEAL | 36 | 7 | 0.07 | (7, 0, 36) | another meaningful viewing angle |

Total yaw 36° (card band 22–38), total pitch 10° (band 4–12). Desktop camera: PERSP, 70 mm,
sequence fit at distance **10.5014**; mobile: ORTHO, `ortho_scale` **4.2943**, no parallax
(an ortho lateral move would slide the composition instead of creating parallax).

## 4. Candidate table (pivot-offset sweep, real scene builds, no render time)

| offset | min gap px | clearance desktop/mobile % | 01→04 movement % | continuity | core drift % | hard |
|---|---|---|---|---|---|---|
| 0.00 (baseline) | 1.00 | 8.62 / 4.39 | 8.38 | 0.590 | 1.33 | FAIL (gap) |
| 0.04 | 2.10 | 8.62 / 4.39 | 8.21 | 0.596 | 1.33 | FAIL (gap) |
| 0.06 | 2.60 | 8.62 / 4.39 | 8.12 | 0.602 | 1.32 | FAIL (gap) |
| 0.08 | 3.10 | 8.62 / 4.39 | 8.04 | 0.608 | 1.32 | FAIL (gap) |
| 0.10 | 3.70 | 8.62 / 4.39 | 7.95 | 0.615 | 1.32 | FAIL (gap) |
| 0.12 | 4.20 | 8.62 / 4.39 | 7.87 | 0.622 | 1.32 | FAIL (gap) |
| 0.14 | 4.80 | 8.62 / 4.39 | 7.78 | 0.629 | 1.32 | FAIL (gap) |
| 0.16 | 5.30 | 8.61 / 4.39 | 7.70 | 0.637 | 1.32 | PASS |
| **0.20 (WINNER)** | **6.10** | **8.61 / 4.39** | **7.53** | **0.652** | **1.32** | **PASS** |
| 0.22 | 6.40 | 8.60 / 4.39 | 7.44 | 0.660 | 1.32 | PASS |
| 0.24 | 6.70 | 8.60 / 4.39 | 7.36 | 0.668 | 1.32 | PASS |
| 0.26 | 7.00 | 8.60 / 4.39 | 7.28 | 0.677 | 1.32 | PASS |
| 0.28 | 7.30 | 8.60 / 4.39 | 7.19 | 0.686 | 1.31 | PASS |

Ranking, exactly as defined: hard constraints → the card's 8 px preference → a 6 px **safety
gap** → weighted movement 0.35 / continuity 0.30 / gap 0.20 / drift 0.15. The 8 px preference
is unreachable on this rig without an offset so large that the companions read as translated
rather than rotated (which the card forbids), so the safety rank decides against a candidate
that clears the 5 px floor by only 6% — the final validator measures the gap from *rendered
pixels*, not projections. Winner 0.20 costs 2.2% of movement against 0.16 and pays for it with
a 22%-over-floor gap.

## 5. Final minimum silhouette gap, every frame and device

| state | desktop px | mobile px |
|---|---|---|
| FRAME_01_REST | 45.9 | 24.8 |
| FRAME_02_EARLY_ROTATION | 39.6 | 22.5 |
| FRAME_03_MID_STRONGEST_DEPTH | 24.0 | 15.0 |
| FRAME_04_SETTLED_REVEAL | **6.4** | **6.1** |

Worst case 6.1 px (floor 5, safety target 6). Edge clearance: desktop 8.61–11.21 %, mobile
4.39–6.52 % — both margin contracts hold on every frame.

## 6. Final render paths

`renders/stage3/desktop/dark/frame-01..04.png` · `renders/stage3/desktop/light/frame-01..04.png`
· `renders/stage3/mobile/dark/frame-01..04.png` · `renders/stage3/mobile/light/frame-01..04.png`
(16 review frames) plus 16 transparent masters in `renders/stage3/alpha/`
(`desktop-dark-01..04`, `desktop-light-01..04`, `mobile-dark-01..04`, `mobile-light-01..04`).
Blender source: `source/hero-v2-stage3.blend` (959,151 bytes). Production quality: Cycles,
160 samples, denoise, Stage 2.7 colour management — the look was not touched while solving
motion.

## 7. Contact sheets and motion review

`renders/stage3/contact-desktop-dark.png` · `contact-desktop-light.png` ·
`contact-mobile-dark.png` · `contact-mobile-light.png` ·
`contact-motion-difference-desktop-dark.png` · `contact-motion-difference-mobile-dark.png`.
Quick review sheets for the three leading candidates: `validation/stage3-optimizer/candidate-01..03/`.
Motion review (design review only, not a web asset): **`validation/stage3-motion-review.gif`**
— 32 frames, 110 ms per frame, 880 ms hold per keyframe, simple cross-dissolve, 672×588.

## 8. Continuity measurements (card section 13 A–I)

| test | measurement | verdict |
|---|---|---|
| A core centroid | desktop 0.94 / 1.13 / 0.75 %, 01→04 1.32 %; **mobile 0.00 %** (ortho, fixed camera) | PASS (band ≤2.5) |
| B companion displacement | steps 0.86–5.21 % desktop, 0.37–5.44 % mobile; 01→04 5.05–8.88 % desktop, 1.09–8.87 % mobile | PASS (see note) |
| C node identity | min projected separation 29.19 % of frame width; each node keeps its own locked material | PASS |
| D scale delta | companions ≤5.73 % per step, core ≤0.11 % | PASS (band ≤12 / ≤1) |
| E relation endpoints | all 12 strokes surface-anchored on both ends, every state | PASS (tol 2%) |
| F safe region | 0 form pixels in the desktop text strip and the mobile margin strips, all 16 masters | PASS |
| G frame bounds | 0 form pixels inside a 1 % border band, all 16 masters | PASS |
| H 04 ≠ 01 | silhouette IoU 0.5195 desktop / 0.6831 mobile; mean Δalpha 0.101 / 0.083 | PASS (≤0.97) |
| I step < whole | desktop steps IoU 0.760 / 0.692 / 0.844 vs 0.520 direct; mobile 0.870 / 0.819 / 0.875 vs 0.683 | PASS |

**Test B note (measured, not hidden):** on the orthographic mobile camera one companion
(human-centered AI) moves only 1.09 % across the whole sequence, because its arc runs mostly
along that camera's view axis — an orthographic camera cannot show motion in depth. The
desktop (perspective) view shows 5.05 % for the same node, and the other two companions move
7.60 % and 8.87 % on mobile. The card anticipates this: mobile frames must correspond
*semantically*, not in exact screen coordinates.

Silhouette metrics were also re-measured at the **real display footprint** (686×600 and
288×288): mobile steps 0.872 / 0.820 / 0.876, 01→04 0.684 — i.e. the mobile motion survives
downscaling rather than being a review-scale illusion. Max pixel level in any review frame is
248 (the page itself), with 0 pixels at 255.

## 9. Final validator count

**22 checks, 22 passed, 0 failed** (`validation/hero-v2-stage3-validation.json`), including
every hard requirement: 4 nodes · 3 visible relations per state · surface-anchored endpoints ·
no clipping · both margin contracts · text-safe region · gap ≥5 px on every frame and device ·
core drift · bounded scale delta · semantic identity · each step smaller than the 01→04 change ·
04 differs from 01 · no GLB · no frontend files · no WebP · no AVIF. The validator fails loudly
on any gap violation (`gap_every_frame_device`), and the builder re-reads the keyed rig poses
out of the animation system so a silent zero-degree bake cannot ship.

## 10. Visual review (A–J)

- **A. One object reorienting?** Yes on the evidence that matters: the core is grey (unmoved)
  in every panel of the motion diagnostic while both companions and all three connectors carry
  coherent red/blue fringes, the per-step deltas build toward FRAME_03 and settle, and every
  step changes the silhouette less than the 01→04 span. Note that four still frames *are* four
  discrete keyframes by design — the tweening is the frontend's job, which is why this stage
  authors four poses rather than a baked animation.
- **B. FRAME_04 meaningfully different from FRAME_01?** Yes — IoU 0.52 desktop / 0.68 mobile.
- **C. HEALTH breathing room?** Yes: its worst-case projected gap went 0.9 px → 6.4 px while
  every other frame kept 24–46 px.
- **D. More molecule/planetary than Stage 2.7?** Slightly more system-like because the
  companions now visibly orbit a stable core, but the locked material language, muted palette
  and absence of orbit rings keep it an editorial knowledge object.
- **E. Any relation curve reading as an orbit?** No — three straight-ish strokes with distinct
  curvatures (0.041 / 0.067 / 0.064 deviation-over-chord); none closes an arc.
- **F. Core stability preserved?** Yes: ≤1.32 % desktop drift (all of it the authored camera
  parallax) and exactly 0.00 % on mobile, with apparent diameter moving ≤0.11 %.
- **G. FRAME_03 still the strongest depth state?** Yes — largest per-step silhouette change
  (mean Δalpha 0.058 desktop, 0.044 mobile) and the largest apparent-diameter spread.
- **H. Mobile equivalent but independently composed?** Yes: same semantic states, ORTHO
  camera, no parallax, mobile-only margins — and the review confirms it is not a crop of the
  desktop layout.
- **I. Dark and light the same geometry?** Yes by construction: one scene, one rig, one
  animation; the two themes differ only in materials, lights and canvas, and both were
  validated frame by frame.
- **J. Visible discontinuity in a four-frame preview?** No discontinuity in the measurements
  (each step < the whole, mid step largest). What a reviewer *can* see on a small contact sheet
  is that thin hairlines and 20 px displacements compress at sheet scale — the diagnostic sheet
  and the GIF exist precisely because a still comparison under-reports motion.

## 11. Remaining visual risks

1. **Frame-rate continuity is unverified by this stage.** Four keyframes cannot prove how a
   scroll tween looks; that is the frontend stage's job and its own review.
2. **Sub-pixel hairlines at fractional DPR** (inherited from the Stage 2.7 lock, which requires
   the edge weight to stay identical): ~1.4 px strokes are crisp at 1× and 2× but can soften at
   1.25×/1.5×, and at phone scale they are the least legible element of the composition.
3. **One companion's mobile screen motion is small** (1.09 %, measured above) because of the
   ortho view axis; the geometry is correct, the camera simply cannot show that depth.
4. **Camera parallax shows as 1.32 % core drift on desktop** — intentional (it is the depth
   cue) but it is motion of the anchored object, so a frontend that also moves the container
   could compound it.
5. **Banding on the teal core** remains unverified on physical 8-bit displays.
6. **Geometry density ≈59k triangles**, still ~4× the GLB budget; the export stage must
   re-tessellate and re-judge sphere smoothness, though curve anchors are recomputed at build
   time so they survive it.

## 12. Explicit answers

**pushed = NO · deployed = NO · frontend touched = NO · GLB created = NO · WebP/AVIF created = NO**

No frontend integration, no ScrollTrigger, no `<picture>` markup, no CSS, no About WebGL, no
deployment. The next stage owns web export and frontend delivery.
