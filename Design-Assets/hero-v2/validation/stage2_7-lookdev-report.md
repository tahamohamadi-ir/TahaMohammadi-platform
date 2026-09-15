# Hero v2 — Stage 2.7 look-dev report: material + relation polish (look lock)

**Status: complete. 18/18 validator checks pass, 11/11 builder checks pass, zero tracebacks.**
Stage 2.6's geometry language (four plain spheres, three real relations) is unchanged; this
stage replaces the physically dead surface of 2.6, thins the relations to hairlines, and adds
the web-scale previews the look had to be judged against.

## 1. Files created / updated

| file | what |
|---|---|
| `source/hero-v2-stage2_7.blend` | new scene (built by the script, reproducible) |
| `scripts/hero_v2_stage2_7.py` | material + relation library (423 → 489 lines) |
| `scripts/build_hero_v2_stage2_7.py` | pipeline: nodes, strokes, 2 rigs, 8 renders, reports |
| `scripts/composite_stage2_7.py` | light-page compositing + the four web-scale previews |
| `scripts/validate_hero_v2_stage2_7.py` | re-opens the shipped `.blend`, measures all 12 PNGs |
| `renders/stage2_7/*.png` | 12 outputs (see §7) |
| `validation/hero-v2-stage2_7-report.json` | builder report (checks, geometry, hashes) |
| `validation/hero-v2-stage2_7-validation.json` | validator report (18 checks with measurements) |
| `validation/hero-v2-stage2_7-composite.json` | compositing report (levels per frame) |
| `README.md` | Stage 2.7 section + commands |

Previous sources are byte-identical (recorded and re-verified): graybox `8dace2c240d4`,
lookdev `a440b085505c`, stage2_5 `5c2957d2ba2c`, stage2_6 `d5d7ae75f2da`.

## 2. Final shader architecture (the headline fix)

Stage 2.6 shipped **zero specular** on every role — it was the only way to stop the highlight
clipping inside the card's enforced roughness band. That is a physically dead material, and it
is why 2.6 read slightly flat. Stage 2.7 restores a real dielectric response and pays for it
with roughness, not with a cheat:

| role | base | roughness | IOR | specular | measured result |
|---|---|---|---|---|---|
| core_shell | `#27565A` | 0.62 | 1.46 | 0.50 | broad soft sheen, no hotspot |
| hcai_shell | `#6F8474` | 0.71 | 1.43 | 0.50 | |
| health_shell | `#877156` | 0.72 | 1.45 | 0.50 | |
| wearable_shell | `#6B6580` | 0.68 | 1.44 | 0.50 | |
| relation | `#C6B191` | 0.62 | 1.44 | 0.35 | hairline sheen, no sparkle |

`specular = 0.5` is Blender's physically-correct F0 for that IOR, not a tuned value; metallic is
0 everywhere. All four shells land inside the card's 0.58–0.76 band, at the matte end.

**Multi-scale system — three deliberately decorrelated fields** (so no scale reads as a pattern):
- **macro, tonal drift only**: Noise scale 1.6, detail 2.0 → ramp 0.42–0.58, mixes the base
  colour by ±3.5 % value. Barely visible; it stops the spheres from being mathematically flat.
- **meso, roughness variation**: Noise scale 6.5, detail 3.0 → roughness ±0.045–0.060. Broad
  irregular patches that only appear through the lighting response.
- **micro, tactile normal**: Noise scale 22, detail 2.5, bump strength 0.026–0.030, distance
  0.004. Perceivable at desktop close review, averaged away at web scale.

No scratches, pores, veins, grain maps, repeating patterns or sparkling highlights; all fields
are evaluated on world position so the texture scale is identical on the core and the
companions regardless of their size.

## 3. Relation curves — thickness before → after

| stroke | 2.6 tube | 2.7 tube | vs 2.6 | taper | curvature (dev/chord) | mid-path clearance |
|---|---|---|---|---|---|---|
| core → HCAI | 0.0075 | **0.0037** | 49 % | 1.00 → 0.68 | 0.0665 | +0.03939 |
| core → health | 0.0064 | **0.00315** | 49 % | 1.00 → 0.68 | 0.0406 | +0.02473 |
| core → wearable | 0.00525 | **0.00259** | 49 % | 1.00 → 0.68 | 0.0639 | +0.04247 |

Every stroke is 49 % of its Stage 2.6 weight — the top of the card's 35–50 % band, chosen after
43 % measured *below the visibility floor* at the real 686×600 footprint in light mode. The taper
(0.68 at the far end) keeps the drawn-gesture reading but stops the arrival from vanishing.
Bends, lifts and depths stay distinct (−0.07/+0.035/+0.035 … +0.05/−0.075/+0.045), so no two arcs
mirror each other and none is an orbit ring. A new `arrival_tangent` tilts each end handle
sideways so the stroke meets its sphere at a **grazing angle** — a bond is inserted radially into
a ball, a drawn line arrives at an angle.

**Endpoint accuracy (measured, not assumed):** each stroke's nearest vertex to each sphere is
compared against that sphere's own measured radius — core 0.7205/0.7219/0.7180 vs R 0.725 and
companions 0.4776/0.4965/0.5227 vs R 0.4800/0.5000/0.5250 (≤ 0.7 % off, tolerance 2 %).

**Occlusion without interpenetration:** the wearable stroke leaves from 14° round the far
hemisphere and bows +0.045 on +Y, so its first stretch is hidden behind the core — real depth
instead of a flat diagram. 38° was tried first and rejected: it pushes the anchor so far round
that the chord to the companion cuts *inside* the core (measured 3× its own tube radius deep).
The builder now carries a control-handle solver that pushes the path outward whenever even the
centreline would enter a sphere; after the fix every stroke reports `interpenetration_excess =
0.000` with zero correction needed.

## 4. Lighting (unchanged rigs, re-verified)

- **dark** — key 1050 W / size 6.4 / tint 1.0·0.985·0.96, fill 0.17×, separation 0.20×, ambient
  0.045, AgX + Medium High Contrast, exposure −0.55, navy gradient world, gain 6.0.
- **light** — key 980 W / size 4.4 / tint 1.0·0.99·0.97, fill 0.10×, separation 0.13×, ambient
  0.05, AgX, exposure −0.30, page composited from the alpha frame so the canvas is exactly the
  site token (measured 248 = token, delta 0).

Light mode is **not** a blanket darkening: pigment goes deeper only where a sphere read pastel
(sage 0.62, violet 0.60 vs 1.00 in dark), the whole set gains +0.045 roughness (flatter, more
mineral against a near-white page), the stroke pigment drops to 0.22, and the rig is steered
harder. No floor or ground plane is built in either theme.

## 5. Validation

`validate_hero_v2_stage2_7.py` re-opens the shipped `.blend` in a fresh process and measures the
files rather than trusting the builder. **18/18 pass** — including the two checks this stage
specifically needed:

- **`dielectric_response_plausible`** — metallic 0, IOR inside 1.42–1.50, non-zero specular,
  roughness inside 0.58–0.76 for every shell. This is the check that stops 2.6's dead material
  from ever coming back.
- **`no_clipping_anywhere`** — max level per frame: dark 202, 199 (desktop/mobile review),
  alphas 220/200/215/201, web-scale 200/248/191/248, **clipped pixels 0** in all twelve. The
  light frames' 248 is the page itself (no pixel above it).

Also measured: 4 nodes only; every node Euler 2, 0 boundary edges, 0 non-manifold edges, radial
variation 1.31–1.72 % (simple spheres); exactly 3 stroke meshes (156 faces each); no forbidden
feature geometry; no text or particles; both cameras independent (PERSP/ORTHO); safe margins
8.05 % desktop / 3.97 % mobile (49.7 px / 25.9 px gap on the real page); form/background
separation 0.36–0.61; alpha corners exactly 0.0 with 19.98 % / 24.10 % coverage; web-scale
previews at exactly 686×600 and 288×288; no GLB/glTF/WebP/AVIF anywhere; no frontend file touched.

## 6. Visual review — the card's ten questions

Answered from the rendered evidence (1600×1400 review frames, the 686×600 previews at real
size, and a 3× nearest-neighbour zoom used as an instrument):

- **A — molecule?** **Still the primary read.** It is a hub with three satellites; that *is* the
  structure the card mandates. Mitigated, not removed: the strokes are hairlines with no volume
  and no radial insertion, so it reads as a diagram of relations rather than a physical
  ball-and-stick model.
- **B — solar system?** No. No orbital logic, no glow, no rings.
- **C — physical rods?** No. At hairline weight with an oblique arrival they read as lines, not
  cylinders.
- **D — smooth CG or tactile?** Tactile: a broad soft sheen with a restrained unevenness, judged
  "powder/blasted, not vinyl".
- **E — restrained?** Yes; the tactility is low-contrast and quiet, and it disappears into clean
  gradients at web scale.
- **F — dark academic/premium?** Yes.
- **G — light mineral/editorial?** Yes; deeper pigments plus a matte response keep it off pastel.
- **H — core dominant without special geometry?** Yes, by scale and position only.
- **I — elegant hairlines, still connections?** Yes at real size on both themes (after the
  stroke weight was raised to the top of the allowed band).
- **J — decorative-only elements?** None.

## 7. The twelve review images

`renders/stage2_7/`: `01-desktop-dark.png`, `02-desktop-light.png`, `03-mobile-dark.png`,
`04-mobile-light.png` (review, 1600×1400 / 800×800) · `11-desktop-dark-alpha.png`,
`12-desktop-light-alpha.png`, `13-mobile-dark-alpha.png`, `14-mobile-light-alpha.png`
(alpha-ready for CSS compositing) · `21-desktop-dark-webscale.png`,
`22-desktop-light-webscale.png`, `23-mobile-dark-webscale.png`, `24-mobile-light-webscale.png`
(actual CSS footprint, 686×600 / 288×288).

Two bugs were found and fixed along the way, both from measurement rather than inspection:
LANCZOS downsampling put **223 pixels at 255** in the first light web-scale preview (ringing
overshoot from a source frame with none) — the previews now clamp to the source maximum; and
Studio lights are visible to a Cycles camera by default, which had been adding an unexplained
white streak since Stage 1 (`visible_camera = False`).

## 8. Remaining weaknesses (no self-congratulation)

1. **The molecular association survives.** The card's own structure (one dominant node, three
   companions, three connectors) cannot fully escape it at this scale; softness and hairlines
   reduce it, geometry cannot remove it without abandoning the brief.
2. **Sub-pixel stroke behaviour at fractional DPR.** A ~1.4 px hairline is crisp at 1× and 2×
   but can go soft at 1.25×/1.5×. The export stage must check those ratios, not just 1× and 2×.
3. **Light theme remains the weaker of the two.** Structurally sound and shippable, but a
   near-white page gives matte mineral tones less room than navy does.
4. **Banding risk unverified on hardware.** The teal core's long gradient is the most likely
   place for contour steps on an 8-bit panel; this was judged from rendered PNGs, not on a real
   display.
5. **Tactility is deliberately below the "look at the surface" threshold.** A viewer hunting for
   hand-made imperfections at review size will not find them — that is the brief, not a defect.
6. **Geometry density is ~55 k triangles**, ≈4× the GLB budget. The export stage must
   re-tessellate; stroke anchors are ray-cast at build time so they recompute, but sphere
   smoothness at lower density must be re-judged.
7. **Two review frames depend on the compositing step** (`composite_stage2_7.py`); this is
   documented here and recorded in the build report.

## 9. Explicit answers

**pushed? NO · deployed? NO · GLB created? NO · frontend touched? NO**

This stage stops here: no scroll frames, no animation, no WebP/AVIF, no `<picture>`, no
ScrollTrigger, no site wiring.
