# Hero v2 — Home hero asset family (Stage 1: graybox · Stage 2: look development)

Home hero artwork for [HERO_PRODUCTION_PLAN_v2.md](../../HERO_PRODUCTION_PLAN_v2.md).

Stage 1 is the approved graybox composition. **Stage 2 adds materials, a studio
rig and a review backdrop to that geometry and changes nothing else** — the four
group transforms, the layout and the two authored cameras are identical, and the
validator re-checks that against the Stage 1 report on the shipped file.

The plan supersedes `HERO_VISUAL_SPEC_v1.md`. The retired Research Universe
signature family under `Design-Assets/research-universe/` is a different asset
set for a different surface and is not read or written by anything here.

## Stage 3 at a glance

Stage 3 turns the Stage 2.7 look into four authored states of one reorientation, on the way
to scroll. Geometry, materials, palette, lighting, relation character and node count are all
inherited from the look lock: only the rig pose changes. `RIG_ROOT` sits at the core's own
centre (offset by the closure-pass pivot below) and the three companion groups are parented
to it, so yaw about world Z and pitch about world X swing them through real depth; the core
is deliberately NOT a child of the rig, which makes its stability structural rather than
tuned. The four poses are baked as CONSTANT keyframes on scene frames 1-4, so the whole
sequence replays from the saved .blend with no viewport state, and each state carries its own
three relation strokes (`REL_CORE_*_F01..F04`, visible only on its own frame) because the
anchors are ray-cast on the surfaces as they stand in that state.

| Piece | Where |
| --- | --- |
| Stage 3 scene (open this one) | `Design-Assets/hero-v2/source/hero-v2-stage3.blend` |
| Builder | `Design-Assets/hero-v2/scripts/build_hero_v2_stage3.py` |
| State / rig / band library | `Design-Assets/hero-v2/scripts/hero_v2_stage3.py` |
| Page composite for the light frames | `Design-Assets/hero-v2/scripts/composite_stage3.py` |
| Contact sheets, motion diagnostic, review GIF | `Design-Assets/hero-v2/scripts/contact_sheet_stage3.py` |
| Validator (22 checks, fresh process) | `Design-Assets/hero-v2/scripts/validate_hero_v2_stage3.py` |
| Pivot-offset sweep + winner selection | `Design-Assets/hero-v2/scripts/optimize_stage3_pivot.py` |
| Renders | `Design-Assets/hero-v2/renders/stage3/{desktop,mobile}/{dark,light}/frame-0N.png` + `alpha/` |
| Reports | `Design-Assets/hero-v2/validation/{stage3-report.md,hero-v2-stage3-report.json,hero-v2-stage3-validation.json,hero-v2-stage3-composite.json,hero-v2-stage3-sheets.json}` |
| Closure sweep | `Design-Assets/hero-v2/validation/stage3-optimizer/` |

The authored states: yaw 0 / 10 / 26 / 36 degrees with pitch 0 / 3 / 10 / 7 and desktop
parallax 0.00 / 0.05 / 0.11 / 0.07 scene units. Total yaw 36 (card band 22-38), total pitch 10
(band 4-12), and the middle step is the largest because that is where the depth has to read.
Mobile is an independently composed ORTHO camera with no parallax: an orthographic camera
cannot show motion along its own view axis, so there the depth reads from the layout's
foreshortening and occlusion instead of from perspective scale.

A closure pass fixed FRAME_04 crowding (the HEALTH companion's projected disc closing to
0.9 px on the desktop frame) without weakening the motion: the rotation pivot moves 0.20 scene
units along the direction derived from the core->HEALTH vector, which took the worst-case gap
to 6.4 px desktop / 6.1 px mobile while giving up 2% of total movement. The sweep, its
rejections and the winner are in `validation/stage3-optimizer/`, and the builder's default
`--pivot-scale 0.20` encodes the winning configuration so the pipeline stays reproducible.

Build note for anyone touching the rig: `frame_set` re-evaluates the animation, so a pose must
be applied AFTER stepping the frame, never before - the wrong order silently keyed all four
states at zero degrees once. The builder now reads the keyed poses back out of the animation
system (`rig_keys_carry_the_states`) and the validator reads animated visibility from the
evaluated depsgraph, so that class of bug cannot pass unnoticed again.

## Stage 2.7 at a glance

Stage 2.7 is the LOOK LOCK on 2.6's geometry: same four plain spheres, same three real
relations, and the same absence of every object-feature read. What changes is the surface
and the curves. 2.6 had to ship zero specular to stay inside the card's roughness band -
a physically dead material. 2.7 puts a real dielectric response back (metallic 0, IOR
1.42-1.50, specular 0.5 = Blender's physical F0 for that IOR, roughness at the matte end
of 0.58-0.76) and pays for it with roughness instead of a cheat. The surface is a
restrained multi-scale system - macro tonal drift, meso roughness patches, micro tactile
normal, three decorrelated fields - with no scratches, pores, grain maps or sparkle. The
relation curves drop to 49% of their 2.6 weight (the top of the card's 35-50% band) with
a 0.68 taper and a grazing arrival tangent, and one leaves from 14 degrees round the far
hemisphere so its first stretch is occluded by the core.

The card required the look to be judged at the real CSS footprint, so this stage adds
four web-scale previews (686x600 desktop, 288x288 mobile) and validates them too:
resampling can invent values a render never had - LANCZOS ringing put 223 pixels at 255
in the first light preview, from a source frame with none.

| Piece | Where |
| --- | --- |
| Stage 2.7 scene (open this one) | `Design-Assets/hero-v2/source/hero-v2-stage2_7.blend` |
| Builder | `Design-Assets/hero-v2/scripts/build_hero_v2_stage2_7.py` |
| Material / curve library | `Design-Assets/hero-v2/scripts/hero_v2_stage2_7.py` |
| Page composite + web-scale previews | `Design-Assets/hero-v2/scripts/composite_stage2_7.py` |
| Validator (18 checks, fresh process) | `Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_7.py` |
| Renders | `Design-Assets/hero-v2/renders/stage2_7/` |
| Reports | `Design-Assets/hero-v2/validation/{stage2_7-lookdev-report.md,hero-v2-stage2_7-report.json,hero-v2-stage2_7-validation.json,hero-v2-stage2_7-composite.json}` |

Review renders: `01-desktop-dark.png`, `02-desktop-light.png`, `03-mobile-dark.png`,
`04-mobile-light.png` (opaque) · alpha-ready: `11-desktop-dark-alpha.png`,
`12-desktop-light-alpha.png`, `13-mobile-dark-alpha.png`, `14-mobile-light-alpha.png` ·
web-scale: `21-desktop-dark-webscale.png`, `22-desktop-light-webscale.png`,
`23-mobile-dark-webscale.png`, `24-mobile-light-webscale.png`.

Build note: the builder carries a control-handle solver. If a stroke's sampled centreline
would enter the core or a companion, the handles are pushed outward until it clears - a
38-degree anchor swing was measured cutting 3x its own tube radius deep into the core, so
the swing is 14 degrees plus a deeper +Y bow. The correction applied is reported in the
builder JSON rather than hidden.

## Stage 2.6 at a glance

Stage 2.6 is PURE NODE LANGUAGE: four plain spheres and three real relation curves.
Every object-feature read is gone (no seam, inlay, cavity, aperture, band, ring or
decorative arc), and the graph reading comes from the curves themselves - each one
anchored by ray-cast on the core's surface and on a companion's surface.

| Piece | Where |
| --- | --- |
| Stage 2.6 scene (open this one) | `Design-Assets/hero-v2/source/hero-v2-stage2_6.blend` |
| Builder | `Design-Assets/hero-v2/scripts/build_hero_v2_stage2_6.py` |
| Geometry / material / rig / curve library | `Design-Assets/hero-v2/scripts/hero_v2_stage2_6.py` |
| Page composite for the light review frames | `Design-Assets/hero-v2/scripts/composite_stage2_6.py` |
| Validator (19 checks, fresh process) | `Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_6.py` |
| Renders | `Design-Assets/hero-v2/renders/stage2_6/` |
| Reports | `Design-Assets/hero-v2/validation/{stage2_6-lookdev-report.md,hero-v2-stage2_6-report.json,hero-v2-stage2_6-validation.json,hero-v2-stage2_6-composite.json}` |

Review renders (opaque): `01-desktop-dark.png`, `02-desktop-light.png`,
`03-mobile-dark.png`, `04-mobile-light.png`.
Alpha-ready renders (transparent, nodes + curves only): `11-desktop-dark-alpha.png`,
`12-desktop-light-alpha.png`, `13-mobile-dark-alpha.png`,
`14-mobile-light-alpha.png`.

Two build notes worth knowing before touching this stage:

* The **light review frames are composited**, not rendered: a flat near-white page is
  exactly what Cycles' denoiser overshoots, and the alpha frame is the source of
  truth for the nodes. `composite_stage2_6.py` (system python + Pillow) puts the page
  under `12-/14-...-alpha.png` and writes `02-/04-...png`. This is the same pattern
  Stage 1 used for its page-canvas previews.
* **Studio lights are `visible_camera = False`.** Cycles renders area lights visible
  to camera rays by default, and a white sliver inside the frame clips at 255 in a
  way that no material or exposure change can fix.

```bash
# build (dark review frames + all four alpha frames), then composite, then validate
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_6.py -- \
  --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_6.blend \
  --renders   Design-Assets/hero-v2/renders/stage2_6 \
  --report    Design-Assets/hero-v2/validation/hero-v2-stage2_6-report.json

python Design-Assets/hero-v2/scripts/composite_stage2_6.py \
  --renders Design-Assets/hero-v2/renders/stage2_6 \
  --report  Design-Assets/hero-v2/validation/hero-v2-stage2_6-composite.json

"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_6.py -- \
  --blend  Design-Assets/hero-v2/source/hero-v2-stage2_6.blend \
  --report Design-Assets/hero-v2/validation/hero-v2-stage2_6-report.json \
  --out    Design-Assets/hero-v2/validation/hero-v2-stage2_6-validation.json
```

## Stage 2.5 at a glance

Stage 2.5 is the simplification + calibration pass on top of Stage 2: the three
companions became single closed spheres, the core's seam became a procedural
recess (no boolean edge), the materials were re-calibrated to matte mineral, and
the review set gained a **required light-canvas environment**.

| Piece | Where |
| --- | --- |
| Stage 2.5 scene (open this one) | `Design-Assets/hero-v2/source/hero-v2-stage2_5.blend` |
| Builder | `Design-Assets/hero-v2/scripts/build_hero_v2_stage2_5.py` |
| Geometry / material / rig library | `Design-Assets/hero-v2/scripts/hero_v2_stage2_5.py` |
| Validator (19 checks, fresh process) | `Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_5.py` |
| Review renders | `Design-Assets/hero-v2/renders/stage2_5/` |
| Report / validation | `Design-Assets/hero-v2/validation/{stage2_5-lookdev-report.md,hero-v2-stage2_5-report.json,hero-v2-stage2_5-validation.json}` |

Renders: `01-desktop-dark.png`, `02-desktop-light.png`, `03-mobile-dark.png`,
`04-mobile-light.png`. `DECOR_ARC_01` is `hide_render = True` in this stage.
Dark mode sits on the plan's Dark canvas (`#071225`), light mode on the Light
canvas (`#f7f8f5`), each with its own rig and exposure.

```bash
# build + render the four Stage 2.5 frames
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_5.py -- \
  --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_5.blend \
  --renders   Design-Assets/hero-v2/renders/stage2_5 \
  --report    Design-Assets/hero-v2/validation/hero-v2-stage2_5-report.json

# validate it
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_5.py -- \
  --blend  Design-Assets/hero-v2/source/hero-v2-stage2_5.blend \
  --report Design-Assets/hero-v2/validation/hero-v2-stage2_5-report.json \
  --out    Design-Assets/hero-v2/validation/hero-v2-stage2_5-validation.json
```

## Stage 2 at a glance

| Piece | Where |
| --- | --- |
| Look-dev scene (open this one) | `Design-Assets/hero-v2/source/hero-v2-lookdev.blend` |
| Builder | `Design-Assets/hero-v2/scripts/build_hero_v2_lookdev.py` |
| Material / rig / environment library | `Design-Assets/hero-v2/scripts/hero_v2_lookdev.py` |
| Validator (re-opens the shipped `.blend`, measures the PNGs) | `Design-Assets/hero-v2/scripts/validate_hero_v2_lookdev.py` |
| Review renders | `Design-Assets/hero-v2/renders/stage2/` |
| Report / validation | `Design-Assets/hero-v2/validation/hero-v2-lookdev-*.json` |

Four material roles in one mineral-ceramic family: **core** deep mineral teal
(the anchor), **Human-Centered AI** muted eucalyptus, **AI for Health** deep
mineral bronze-clay (the warm contrast role), **Wearable / Edge** deep
stone-violet (the cool support role). Grooves, seams and the shell's inner wall
carry a *slightly darker and flatter* inset of their own shell colour — the
recesses are recovered geometrically from the Stage 1 cutter parameters, because
Stage 1 baked those booleans away. One restrained warm bronze-stone inlay sits on
the core seam. Everything shares one node graph (world-position mineral grain +
micro-relief + a satin roughness band) so the four read as one family; only the
colour and three per-role character numbers differ.

`DECOR_ARC_01` is on with a faint matte grey. `hide_render` is toggled per
render, so every camera is captured both **without** (`-clean`) and **with**
(`-arc`) the arc — the two compositions the review asks to compare.

`BACKDROP` plus `LG2_Key` / `LG2_Fill` / `LG2_Sep` are review furniture in the
`Rig_ReviewEnv` collection: a seamless cyclorama (no horizon line) lit by a soft
key, a gentle fill and one restrained top-back separation. The Stage 1 neutral
rig is kept in the file with `hide_render=True` as evidence, not as lighting.

```bash
BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"

# build + render the four review frames (add --quick for a half-res iteration pass)
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_lookdev.py -- \
  --blend-in  Design-Assets/hero-v2/source/hero-v2-graybox.blend \
  --blend-out Design-Assets/hero-v2/source/hero-v2-lookdev.blend \
  --renders   Design-Assets/hero-v2/renders \
  --report    Design-Assets/hero-v2/validation/hero-v2-lookdev-report.json \
  --stage1-report Design-Assets/hero-v2/validation/hero-v2-graybox-report.json
# add --debug-mask to paint the recovered groove faces magenta (coverage check)

# validate what actually shipped
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_lookdev.py -- \
  --blend     Design-Assets/hero-v2/source/hero-v2-lookdev.blend \
  --stage1-report Design-Assets/hero-v2/validation/hero-v2-graybox-report.json \
  --renders   Design-Assets/hero-v2/renders/stage2 \
  --report    Design-Assets/hero-v2/validation/hero-v2-lookdev-validation.json
```

No GLB, no web runtime asset and no frontend connection comes out of Stage 2.

## Stage 1 at a glance

| Artefact | Path |
| --- | --- |
| Source `.blend` | `Design-Assets/hero-v2/source/hero-v2-graybox.blend` |
| Builder (Blender 5.2.1 LTS, headless) | `Design-Assets/hero-v2/scripts/build_hero_v2_graybox.py` |
| Shared helpers | `Design-Assets/hero-v2/scripts/hero_v2_common.py` |
| Validator (re-opens the shipped `.blend`) | `Design-Assets/hero-v2/scripts/validate_hero_v2_graybox.py` |
| Page-canvas previews + metrics (system Python + Pillow) | `Design-Assets/hero-v2/scripts/composite_previews.py` |
| Preview renders | `Design-Assets/hero-v2/renders/` |
| Build report / validation / preview metrics | `Design-Assets/hero-v2/validation/` |

## Build

Run from the repository root. Native forward-slash paths: MSYS does not convert
arguments for native tools, so `/c/...` paths fail.

```bash
BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"

# Stage 3 (current): four authored states -> renders -> sheets -> validation
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_stage3.py -- \
  --blend-out Design-Assets/hero-v2/source/hero-v2-stage3.blend \
  --renders   Design-Assets/hero-v2/renders/stage3 \
  --report    Design-Assets/hero-v2/validation/hero-v2-stage3-report.json
# add --quick for the low-res iteration pass; --skip-renders to measure only
# add --pivot-scale <world units> / --pivot-sign -1 to move the rotation pivot
python Design-Assets/hero-v2/scripts/composite_stage3.py \
  --renders Design-Assets/hero-v2/renders/stage3 \
  --report  Design-Assets/hero-v2/validation/hero-v2-stage3-composite.json
python Design-Assets/hero-v2/scripts/contact_sheet_stage3.py \
  --renders    Design-Assets/hero-v2/renders/stage3 \
  --validation Design-Assets/hero-v2/validation \
  --report     Design-Assets/hero-v2/validation/hero-v2-stage3-sheets.json
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage3.py -- \
  --blend  Design-Assets/hero-v2/source/hero-v2-stage3.blend \
  --report Design-Assets/hero-v2/validation/hero-v2-stage3-report.json \
  --out    Design-Assets/hero-v2/validation/hero-v2-stage3-validation.json

# the pivot-offset sweep behind the FRAME_04 gap (no render time, real scene builds)
python Design-Assets/hero-v2/scripts/optimize_stage3_pivot.py \
  --root Design-Assets/hero-v2 \
  --out  Design-Assets/hero-v2/validation/stage3-optimizer \
  --blender "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" \
  --phase sweep --scales 0.00,0.16,0.20,0.22,0.24,0.26,0.28 --signs 1
# --phase rescore re-ranks the reports already on disk; --phase sheets renders
# quick contact sheets for the leading candidates into candidate-01..03

# Stage 2.7 (look lock, unchanged)
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_7.py -- \
  --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_7.blend \
  --renders   Design-Assets/hero-v2/renders/stage2_7 \
  --report    Design-Assets/hero-v2/validation/hero-v2-stage2_7-report.json
python Design-Assets/hero-v2/scripts/composite_stage2_7.py \
  --renders Design-Assets/hero-v2/renders/stage2_7 \
  --report  Design-Assets/hero-v2/validation/hero-v2-stage2_7-composite.json
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_7.py -- \
  --blend  Design-Assets/hero-v2/source/hero-v2-stage2_7.blend \
  --report Design-Assets/hero-v2/validation/hero-v2-stage2_7-report.json \
  --out    Design-Assets/hero-v2/validation/hero-v2-stage2_7-validation.json

"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/build_hero_v2_graybox.py -- \
  --blend   Design-Assets/hero-v2/source/hero-v2-graybox.blend \
  --renders Design-Assets/hero-v2/renders \
  --report  Design-Assets/hero-v2/validation/hero-v2-graybox-report.json
# add --quick for a low-res 24-sample iteration pass
# add --skip-renders to build + measure only
# add --exposure <float> to look-dev the preview exposure
```

Compositing is a separate step because Blender's bundled Python has no Pillow,
and because the composite wants to be the browser's own arithmetic
(`fg*a + bg*(1-a)` on the sRGB bytes):

```bash
python Design-Assets/hero-v2/scripts/composite_previews.py \
  --renders Design-Assets/hero-v2/renders --hex "#f7f8f5" \
  --metrics Design-Assets/hero-v2/validation/hero-v2-graybox-preview-metrics.json
```

Validate what is actually on disk — a green build is not evidence, because
Blender exits 0 even when a `--background --python` script raises:

```bash
"$BLENDER" --background --factory-startup \
  --python Design-Assets/hero-v2/scripts/validate_hero_v2_graybox.py -- \
  --blend   Design-Assets/hero-v2/source/hero-v2-graybox.blend \
  --report  Design-Assets/hero-v2/validation/hero-v2-graybox-validation.json
```

**Safety.** No script calls `bpy.ops.wm.read_factory_settings()` (it has
previously unloaded the owner's Blender MCP addon). `--factory-startup` is passed
on the command line instead, which loads no user addons at all — the owner's
interactive Blender session is untouched. The builder empties the scene object by
object and writes a **new** `.blend`; the validator opens that file in a fresh
process. Nothing outside `Design-Assets/hero-v2/` is written.

## Scene

```
HERO_V2_ROOT
  GRP_CORE                 CORE_SPHERE, CORE_ACCENT
  GRP_HUMAN_CENTERED_AI    HCAI_SHELL, HCAI_INSET
  GRP_HEALTH_BEHAVIOR      HHB_SPHERE
  GRP_WEARABLE_EDGE        WE_SPHERE
  DECOR_ARC_01             authored, hide_render = True (see below)
Cameras/    CAM_DESKTOP, CAM_MOBILE
Rig_PreviewNeutral   LG_Key, LG_Fill, LG_Rim
```

Group empties carry the composition; the meshes themselves are centred on the
world origin, so moving a group moves its whole form.

## Design intent

| Form | Plan reading | Built as |
| --- | --- | --- |
| Core | soft mineral sphere, one recessed seam, restrained warm-metal detail | ⌀1.45 sphere, one tilted recessed seam (22°/−34°, deliberately not equatorial), broad 2–4% radial deformation, plus a wide flat inlay **straddling the seam** so the detail reads as intentional |
| Human-Centered AI | rounded shell with one generous opening around an inset form | bisected shell (rim radius 80% of the sphere), 0.052 wall, aperture axis 61° off-camera so the opening **breaks the outline**, inset form slid off the aperture axis so it cannot read as an iris |
| AI for Health & Human Behavior | smooth sphere with two shallow contours following its volume | one swept near-great circle + one tilted crown ring; the two groove planes differ by ~29° so they cannot read as planetary latitude lines |
| Wearable / Edge Intelligence | compact sphere with three broad, rounded segments | two grooves with **different** tilts, deep enough to notch the silhouette; flattens to 0.978/0.962 for the "compact" read |

`DECOR_ARC_01` is the single decorative arc the plan allows ("at most one faint,
incomplete orbital arc … without endpoints or arrowheads"). It is built as a
tapered tube — the taper is what lets an arc read as a drawn gesture rather than
a solid ring — and its clearance to every form is verified. It is **excluded from
the Stage 1 renders**: "faint" is a material property and this stage has no
materials. Give it a faint material and clear `hide_render` in Stage 2, or delete
it. The plan intends it as the compositional thread between the four forms, which
is also the honest answer to the "loose cluster" reading in review.

## Contract and gates

Enforced by the builder, re-asserted on the shipped file by the validator
(21 checks), and measured in pixels rather than asserted:

- core ⌀1.45 BU, every companion ⌀1.00 BU, companions equal in rank
- desktop: 1600×1400, perspective, 70 mm on a 36 mm sensor, **≥8% clear space**
  at all four edges (measured 8.0–8.4%)
- mobile: 800×800, orthographic, tighter diamond (4% side margins)
- silhouette separation, scaled to the real page slots (600 px desktop /
  288 px mobile), ≥12 px. Measured 27.7 px desktop, 22.8 px mobile
- every groove keeps ≥100° camera-facing span **and** ≥1.10 sphere-radii of
  *projected* length. Span alone is not legibility: a contour high on the sphere
  scored 199° visible and was invisible in the render
- previews must separate tonally from the `#f7f8f5` page canvas. Measured form
  median Δ63.4 desktop / Δ64.4 mobile against a Δ45 floor
- no text, labels, particles, UI panels, unapplied modifiers, or zero-area faces

## Not in this stage

Final materials, image or procedural textures, the four material roles, theme
lighting for Light and Dark, the four final PNGs, and the six WebP derivatives.
`PREVIEW_CLAY` is a single neutral placeholder — a mid-grey chosen so the forms
separate from the Light page canvas, **not** an art decision about final colour.
