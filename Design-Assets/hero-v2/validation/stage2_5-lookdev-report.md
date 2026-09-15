# Hero v2 — Stage 2.5 report (geometry simplification + material calibration)

Review-only pass. No GLB, no glTF, no WebP/AVIF, no `<picture>`, no scroll states,
no frontend edit, no CMS change, no commit, no push, no deploy.

## 1. Geometry — exactly what changed

Semantic node count is untouched: four groups, and the core is still the only
object with a distinct silhouette.

| Object | Stage 2 | Stage 2.5 |
| --- | --- | --- |
| `GRP_CORE` / `CORE_SPHERE` | torus-boolean seam (stepped edge) | **procedural raised-cosine recess**: every vertex inside the seam's angular band is pushed inward along its own radius (7.4° half-width, 2.8% depth). No cut edge exists, so nothing can staircase; the profile is C1-continuous at the centre and the rim. |
| `GRP_CORE` / `CORE_ACCENT` | flattened bead, lifted 0.010 | same inlay, lifted **0.004** (flush): the review read the old lift as a button |
| `GRP_HUMAN_CENTERED_AI` | aperture shell + inner ball | **one plain sphere**, 1.31% radial variation |
| `GRP_HEALTH_BEHAVIOR` | sphere + two contours | **one plain sphere**, 1.31% |
| `GRP_WEARABLE_EDGE` | sphere + two grooves | **one plain sphere**, 1.31% |
| `DECOR_ARC_01` | rendered in the `-arc` pair | present for provenance, **`hide_render = True`** |

Topology is the evidence, not adjectives: each companion is read back from the
saved file as **Euler characteristic 2, zero boundary edges, zero non-manifold
edges** — which a cavity, an inner ball, a solidified shell, a ring, a band or a
silhouette groove could not be. Radial variation is **1.31%** against the card's
1–2% allowance. `CORE_SPHERE` is deliberately excluded from that test: its seam is
the one incision this stage keeps.

Triangle counts: `CORE_SPHERE` 20 224 · `CORE_ACCENT` 4 736 · each companion
11 328 → **58 944 for the family** (plus two 30-triangle backdrops and the hidden
4 480-triangle arc). That is *review* resolution, far above the plan's ≤15 000
triangle GLB budget: the export stage must re-tessellate.

## 2. Composition — small adjustments, and why

The card forbids an atom / solar-system read, and the Stage 2.5 review confirmed
that Stage 1's layout produced exactly that: one big sphere with three similar
spheres at **similar distances** (radii 1.56–1.66) and equal diameter.

* Radical distances re-spaced **outward only**: 1.72 / 1.50 / 1.90 (directions,
  quadrants and the core's position are Stage 1's).
* A ±5% scale hierarchy on the companions (0.96 / 1.00 / 1.05) — the card names
  scale as a legitimate lever.

The first attempt pulled one companion *inward* to 1.39. That shortened the chord
between two companions on the same side and dropped the mobile silhouette gap to
**10.5 px against the 12 px floor**; the framing-contract check caught it before
it reached a render review. The shipped layout measures **50.3 px desktop /
26.3 px mobile**, with edge clearance **8.05% desktop / 3.97% mobile** (contract:
≥8% and ≥4%).

## 3. Materials

Five roles, all **metallic 0** (the accent is a warm *stone* inlay, not metal), all
inside the card's roughness bands, and one shared node graph so the family holds:
one broad field (scale 3.6) drives a roughness band *and* a slight tonal mottle;
one broad bump (scale 9.0, strength 0.018–0.024) gives soft undulation rather than
a visible texture pattern.

| Role | Hex | Roughness | Band | Card range |
| --- | --- | --- | --- | --- |
| `core_shell` | `#27565A` | 0.56 | ±0.045 | 0.52–0.62 ✓ |
| `core_accent` | `#8E7854` | 0.58 | ±0.030 | restrained warm stone |
| `hcai_shell` | `#6F8474` | 0.66 | ±0.030 | 0.60–0.72 ✓ |
| `health_shell` | `#877156` | 0.68 | ±0.045 | 0.62–0.74 ✓ |
| `wearable_shell` | `#6B6580` | 0.63 | ±0.050 | 0.58–0.68 ✓ |

Per-theme preset (plan section 3, "warm mineral shells in Light, navy shells in
Dark: change the preset, do not invert"): the light pass multiplies every shell
and accent colour by **0.86** and uses its own rig and exposure.

## 4. Dark environment

Backdrop `#0A1730` (a hair lifted from the plan's Dark canvas `#071225` so the rig
has a surface to model) with a separate floor tone; cyclorama, no horizon line.
Rig: key 1100 W / size 6.0 at `(-2.6, -3.2, 3.0)`, fill 0.18× (size 7.5),
separation 0.22× — every source a large, low-level area light. World ambient 0.05,
faintly cool. AgX + `AgX - Medium High Contrast`, exposure −0.55.
Measured canvas: **25/255** against the token's 17 (Δ8).

## 5. Light environment

Backdrop `#F2F3EE` with a bounded emission (0.62 on the `#f7f8f5` canvas) and a
slightly dropped floor tone; rig **independently calibrated**: key **1900 W /
size 4.2** (tighter, steeper, stronger direction), fill **0.075×**, separation
0.10×, ambient 0.06 — less fill and more direction than the dark rig, per the
card. Exposure −0.30 under AgX.
Measured canvas: **236/255** against the token's 248 (Δ12).

The light pass was tried with a **Standard** transform, which does land the canvas
on the token exactly — and clips it to pure 255, which the card forbids ("no
clipped highlights"). Reverted to AgX and reported as a deviation instead of
shipping a clipped page.

## 6. Cameras

`CAM_DESKTOP` (perspective, 70 mm on a 36 mm sensor, 1600×1400) and `CAM_MOBILE`
(orthographic, 800×800) are kept, re-fitted with the same Stage 1 margin contract
(8% / 4%) because the silhouettes changed. No 26 views, no animation, no scroll
frames; mobile remains an authored orthographic composition, not a crop. Fits:
desktop distance 9.35, fill 0.78×0.84; mobile distance 10.0, fill 0.92×0.91.

## 7. Validation — 19/19 in a fresh Blender process

Re-opened `hero-v2-stage2_5.blend` and measured the four PNGs on disk:

`sources_unchanged` (sha256 of both inputs matches the build-time record) ·
`exactly_four_semantic_groups` · `one_core_plus_three_single_spheres` ·
`no_cavity_or_inner_ball_geometry` · `no_ring_band_or_groove_companions` ·
`arc_hidden` · `no_text_or_particles` · `no_glb_or_web_export` ·
`no_frontend_export` · `no_metallic_shells` · `triangle_counts_reported` ·
`camera_framing_safe_margin` · `four_renders_exist_and_sized` ·
`no_clipped_highlights` (**0.0%** on all four) · `no_excessive_crushed_blacks`
(0.0 / 0.0 / 0.007 / 0.0 %) · `theme_canvases_match_tokens` ·
`forms_readable_in_both_themes` (dark forms 0.41 against a 0.10 field; light forms
0.72 against a 0.92 page) · `stage_tag` · `dark_and_light_are_different_renders`.

The readability metric was fixed during this pass: its first version only looked
for pixels *darker* than the page field, which is right for light mode and wrong
for dark mode (the forms are brighter there) — it now measures separation in
either direction.

## 8. Visual review answers (A–J)

A. **Eye — faintly yes, all four panels.** The cavity/ball geometry is gone, so it
   is no longer a structural eye, but the core's tilted seam plus its small warm
   inlay can still suggest an eyelid crease and a pupil. Companions: no.
B. **Planet — yes, all four panels**, and it is the strongest remaining association:
   a large featured sphere with smaller plain spheres reads planetary, more so on
   the navy canvas. Companions also read as moons.
C. **Gadget — mildly, all four panels**, only for the core (seam + inlay as a
   button/indicator). Not a strong read; companions: no.
D. **Atom / solar system — yes, more solar system than atom.** Removing the arc
   weakened the atom reading; the varied distances and sizes did not remove the
   planetary association.
E. **Core distinctiveness — yes**, in every panel: size, centrality, colour, the
   only seam and the only inlay.
F. **Tactile / mineral / human — partially.** Matte and muted, clearly unglazed
   ceramic or mineral rather than gloss; dark panels read best. The light panels
   and the companions still read smooth and slightly CGI-perfect: no pores,
   imperfection or unevenness at review size.
G. **Dark elegance — yes**; no neon, glow, fog or HUD. The planetary association
   remains, but it reads abstract rather than sci-fi.
H. **Light premium — mostly.** Off-white page, soft contact shadows and the teal /
   bronze anchors read editorial; the mint and lavender companions risk pastel on
   a near-white field.
I. **Companion differentiation — by colour, not yet by material.** Three distinct
   hues; finish is nearly identical. Size/spacing hierarchy is subtle.
J. **Hierarchy — core over companions is immediate.** The exact ranking among the
   three companions is not readable at a glance.

## 9. Remaining weaknesses

1. **Planetary / solar-system association persists (B, D).** It follows from the
   prescribed structure — one distinctive central sphere plus three restrained
   companions with no decoration. Breaking it further means either a non-spherical
   core silhouette or deliberate asymmetry between companions, both of which are
   Stage 1 contract questions, not material ones.
2. **Tactility is the weakest axis (F).** Broad undulation and tonal mottle are
   present but too fine to read at review size; the surfaces still look perfect.
   The next lever is low-frequency imperfection (a faint asymmetric value drift,
   or a real micro-displacement), not more noise.
3. **Light panels lean pastel for the two lightest companions (H).** Their albedo
   is high enough that a near-white page pulls them toward chalk; the per-theme
   preset could go further than 0.86 for those two roles specifically.
4. **Light canvas is 12 levels below the token** because AgX rolls the top end off.
   Fixes exist (a Standard-transform light pass, or Stage 1's transparent-film
   composite onto the canvas) and each has a cost: the first clips, the second
   needs a shadow-catcher pass.
5. **Review-resolution geometry** — 58 944 triangles is ~4× the plan's GLB budget;
   an export pass must re-tessellate and re-verify the seam's smoothness at the
   lower density (the procedural recess is resolution-independent, so it should
   survive, but it must be re-measured).

## 10. Scope statement

No frontend file was read, written or built for this pass; no GLB/glTF, WebP or
AVIF exists anywhere under `Design-Assets/hero-v2/` (validator check:
`no_glb_or_web_export`); nothing was written outside `Design-Assets/hero-v2/`;
Stage 1 and Stage 2 sources are unchanged (hash-verified); nothing was committed,
pushed or deployed. Deliverables: `source/hero-v2-stage2_5.blend`, the four
`renders/stage2_5/*.png`, `scripts/{hero_v2_stage2_5,build_hero_v2_stage2_5,
validate_hero_v2_stage2_5}.py`, and the two JSON reports in `validation/`.
