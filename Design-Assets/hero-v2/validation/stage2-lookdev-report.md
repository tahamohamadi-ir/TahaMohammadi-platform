# Hero v2 — Stage 2 look development report

Stage: **2 — materials + light** (on the approved Stage 1 graybox geometry).
Scope held: no frontend, no GLB, no web runtime asset, no animation, no particles,
no text or UI, no node-count change, no new hero object, no geometry redesign.

## 1. What changed

| Area | Change |
| --- | --- |
| Materials | The single `PREVIEW_CLAY` placeholder is replaced by 12 authored roles (4 shells, 5 insets, 1 accent, 1 arc, 1 backdrop). Every role shares one node graph: world-position mineral grain + micro-relief, a satin roughness band, and a small roughness variation. |
| Groove / inset treatment | Grooves, the core seam and the shell's inner wall now carry a *slightly darker and flatter* inset of their own shell colour. Recovered geometrically (see §2) because Stage 1 baked its boolean cutters away. |
| Light | The Stage 1 `Rig_PreviewNeutral` is retired (`hide_render=True`, kept as evidence) and replaced by `LG2_Key` / `LG2_Fill` / `LG2_Sep`. World ambient dropped to a faint cool 0.06. |
| Environment | New `BACKDROP`: a seamless matte cyclorama in `Rig_ReviewEnv`. `film_transparent` off, film RGB — the backdrop is the background. Review furniture only; it is never exported and no form was moved for it. |
| `DECOR_ARC_01` | Kept. Turned on with a faint matte grey and toggled per render, so every camera is captured without (`-clean`) and with (`-arc`) the arc. |

**Geometry, layout and cameras: untouched, and verified rather than assumed.**
The builder measures every mesh's triangle count, each group transform and both
camera matrices before and after the look pass and compares them against
`hero-v2-graybox-report.json`. Builder drift report: `{}` (no triangle, layout or
camera drift). `CAM_DESKTOP` (1600×1400, 70 mm) and `CAM_MOBILE` (800×800,
orthographic) are the Stage 1 cameras, unfitted.

## 2. Material roles

Colours are sRGB hex; Blender sockets get linear values. `character` = the three
numbers that make the roles four *materials* rather than four colours of one
shader (spread = satin band width, grain/micro = relief multipliers).

| Role | Hex | Rough | Metal | Character | Where |
| --- | --- | --- | --- | --- | --- |
| `core_shell` | `#27565A` | 0.40 | 0.0 | 0.050 / 1.15 / 1.0 | the anchor: deep mineral teal satin ceramic |
| `core_inset` | `#1E4347` | 0.58 | 0.0 | 0.045 / 1.10 / 0.9 | the tilted seam |
| `core_accent` | `#8A6C48` | 0.55 | 0.25 | 0.040 / 0.85 / 1.2 | the wide inlay straddling the seam — the only metallic, deliberately stone-like |
| `hcai_shell` | `#6E8B72` | 0.58 | 0.0 | 0.025 / 0.70 / 0.8 | muted eucalyptus; softer and more diffuse than the core |
| `hcai_inset` | `#63766A` | 0.60 | 0.0 | 0.030 / 0.80 / 0.9 | the aperture's inner wall and rim |
| `hcai_inner` | `#6A8070` | 0.56 | 0.0 | 0.025 / 0.75 / 0.9 | the inset form inside the cavity |
| `health_shell` | `#8C7050` | 0.60 | 0.0 | 0.050 / 1.30 / 1.1 | deep mineral bronze-clay — the warm contrast role, the most tactile surface |
| `health_inset` | `#775F45` | 0.66 | 0.0 | 0.045 / 1.25 / 1.0 | the two contours |
| `wearable_shell` | `#6A6383` | 0.48 | 0.0 | 0.060 / 1.00 / 1.0 | deep stone-violet; the tightest satin band |
| `wearable_inset` | `#5A5474` | 0.62 | 0.0 | 0.050 / 1.05 / 1.0 | the two grooves |
| `arc` | `#55595D` | 0.70 | 0.0 | default | `DECOR_ARC_01`: matte, close to the backdrop |
| `backdrop` | `#23262A` | 0.85 | 0.0 | default | review environment only |

**Inset recovery.** Stage 1 cut the grooves with real booleans, so the recessed
faces cannot be found by material slot. They are recovered from the same tool
parameters the Stage 1 builder used: a torus whose tube-centre circle lies on the
sphere removes everything inside its tube, so the surviving groove surface is
exactly the set of points at distance `width` from that circle. Marked faces:

| Object | Groove faces | % of faces | % of area |
| --- | --- | --- | --- |
| `CORE_SPHERE` (seam) | 2 718 | 32.8% | **9.9%** |
| `HCAI_SHELL` (inner wall + rim) | 5 641 | 51.1% | **46.0%** |
| `HHB_SPHERE` (two contours) | 4 728 | 48.3% | **19.3%** |
| `WE_SPHERE` (two grooves) | 6 073 | 57.5% | **34.0%** |

Face counts and area shares disagree on purpose: the boolean tessellates the
groove floor into many small faces. The area share is the number a reviewer
means, and the `HCAI_SHELL` share is large simply because a 0.052-thick hollow
shell's inner wall is roughly half of its total surface.

Recovery was verified the only way that settles it: a `--debug-mask` pass paints
every recovered face magenta and renders one desktop frame. Measured from that
render, the magenta covers **6.07% of the object pixels**, and inspection confirms
it traces the core seam, both contours, both grooves and the shell's inner cavity
and rim — with no magenta on any broad surface.

## 3. Lighting setup

| Source | Energy | Position (relative to the composition centre) | Size |
| --- | --- | --- | --- |
| `LG2_Key` | 1200 W | `(-3.0, -3.4, 3.1)` — above/front-left, barely warm | 4.0 |
| `LG2_Fill` | 264 W (0.22×) | `(3.8, -2.6, 0.4)` — broad, barely cool | 5.0 |
| `LG2_Sep` | 360 W (0.30×) | `(1.5, 3.4, 3.2)` — one restrained top-back separation | 2.6 |

World ambient 0.06, faintly cool — the rig does the work. Every source is a large
area light at a low level, so the falloff stays elegant: no rim-heavy lighting, no
coloured light, no fog, no HDRI. Cycles, 160 samples, OpenImageDenoise, AgX with
the medium-high-contrast look, exposure `-0.7`.

## 4. `DECOR_ARC_01` — kept, and how strongly

Kept, as a faint matte grey (`#55595D`, roughness 0.70) on the existing tapered
tube. Strength is *measured* from the delivered frames rather than asserted: the
arc changes a small number of pixels strongly (max local change 0.359 desktop /
0.174 mobile) but affects a tiny share of the frame (0.168% / 0.044% of sampled
pixels changed by more than 0.06). It is visible enough to evaluate the two
compositions and never dominates. It does not read as a thick sci-fi tube, and
because it is a matte near-neutral rather than a bright line, a viewer looking
for a planetary ring does not find one.

## 5. Composition adjustments

**None.** No form was moved, rescaled or rotated; both cameras keep the Stage 1
framing (desktop ≥8% edge clearance, mobile's tighter diamond) and were not
re-fitted. The only addition in frame is the review backdrop, which sits behind
and below the composition.

## 6. Remaining weaknesses and risks

1. **The open shell still leans "eye"** to a fresh viewer, though much less than in
   the first look-dev pass ("reads strongly like an eye" → "an abstract hollow
   shell with a ball inside"). What remains is geometric: a circle aperture with a
   ball inside it is an eye until something else breaks the read. Materials closed
   most of the gap (the cavity and the inner form now sit within a few percent of
   the shell in value, so there is no iris/pupil contrast). Fixing the rest means
   touching Stage 1 geometry, which this stage is not allowed to do — it belongs
   in the next pass, and it is the single most valuable thing to fix.
2. **The banded bronze form can read as a ringed planet** rather than a burger.
   Stage 1 already gave the two contours different tilts; at review size the
   material made the recesses quieter, which helped, but a sphere with two
   horizontal-ish bands has a planetary reading available. Also geometry-driven.
3. **This look is tuned for the dark review backdrop only.** The card's optional
   light-background validation render was not produced, so nothing here proves how
   these four roles behave on the Light page canvas (`#f7f8f5`). That is the next
   thing worth measuring before any export.
4. **The backdrop is review furniture.** If these frames are ever reproduced, the
   environment must not be mistaken for part of the artwork: it is not exported
   and it is not the planned page background.
5. **The inset area shares are load-bearing information.** If the Stage 1
   geometry is ever re-tessellated or re-cut, the recovered masks must be
   recomputed — they are derived from the cutter parameters, not stored in the
   mesh.

## 7. No frontend or GLB work

No GLB or glTF file exists anywhere under `Design-Assets/hero-v2/` (count: 0); no
web runtime asset was produced; nothing was written outside
`Design-Assets/hero-v2/`; the frontend was not opened, built or otherwise
touched; and the Stage 1 graybox `.blend` was not modified (Stage 2 writes a new
file). Only review PNGs and JSON/Markdown reports came out of this stage.

## Verification

| Gate | Result |
| --- | --- |
| Builder checks (8) | all pass — geometry/layout/cameras unchanged, four distinct roles, every groove recovered, arc material present, no GLB, no text/particles |
| Validator checks (17) | **all pass, 0 failed** — re-opened the shipped `.blend`; inspected all four PNGs on disk |
| Renders | `desktop-clean/arc` 1600×1400, `mobile-clean/arc` 800×800, all four present and pairwise distinct |
| Exposure | no clipped highlights (0.0%); crushed shadows 0.009% desktop / 0.015% mobile; p2 0.11/0.13, p50 0.17/0.18, p98 0.68/0.70 |
| Blender | 5.2.1 LTS, Cycles on CUDA, 160 samples, denoised |

Reports: `hero-v2-lookdev-report.json` (build facts),
`hero-v2-lookdev-validation.json` (independent re-check).
