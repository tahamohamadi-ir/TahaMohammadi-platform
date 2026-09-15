# Hero v2 — Stage 2.6 report (PURE NODE LANGUAGE)

Review-only pass. No GLB, no glTF, no WebP/AVIF, no `<picture>`, no scroll states,
no frontend edit, no CMS change, no commit, no push, no deploy.

The stage's goal was to stop the hero reading as *objects* and start it reading as a
*connected system*. Every object-feature cue is gone, and the graph reading now comes
from three real relation curves.

## 1. Geometry

| Object | What it is now |
| --- | --- |
| `CORE_SPHERE` | one plain sphere, ⌀1.45, 10 240 faces, 1.72% radial variation |
| `HCAI_SPHERE` | one plain sphere, ⌀0.96 (scale hierarchy), 5 760 faces, 1.31% |
| `HHB_SPHERE` | one plain sphere, ⌀1.00, 5 760 faces, 1.31% |
| `WE_SPHERE` | one plain sphere, ⌀1.05, 5 760 faces, 1.31% |
| `REL_CORE_HUMAN_CENTERED_AI` | cubic Bézier rod, tube radius 0.0075 BU |
| `REL_CORE_HEALTH_BEHAVIOR` | cubic Bézier rod, tube radius 0.0075 BU |
| `REL_CORE_WEARABLE_EDGE` | cubic Bézier rod, tube radius 0.0075 BU |

Removed from Stage 2.5 in this pass: the core's diagonal seam, the gold inlay and
`DECOR_ARC_01` entirely. Nothing on the core tells a story any more; it is a node.

Every sphere is verified as a **single closed surface** — Euler characteristic 2,
zero boundary edges, zero non-manifold edges — and the companions stay under the
card's 1–2% radial-variation allowance. Node count is unchanged: four groups, one
core, three companions.

## 2. Relation curves

Each curve is anchored by **ray-casting the real deformed surface**, not by assuming
a radius, so the endpoints touch the geometry exactly and would keep touching after
any tweak to the deformation. Measured:

| Curve | Chord | Start dist. | Core radius | End dist. | Companion radius | Max deviation |
| --- | --- | --- | --- | --- | --- | --- |
| `REL_CORE_HUMAN_CENTERED_AI` | 0.5834 | 0.7216 | 0.725 | 0.4785 | 0.480 | 0.0388 |
| `REL_CORE_HEALTH_BEHAVIOR` | 0.3729 | 0.7241 | 0.725 | 0.4974 | 0.500 | 0.0206 |
| `REL_CORE_WEARABLE_EDGE` | 0.7286 | 0.7192 | 0.725 | 0.5233 | 0.525 | 0.0406 |

Every start lands within 0.5% of the core's surface radius and every end within
0.5% of its companion's (tolerance 2%). Three **distinct** deviations from their own
chords — 0.0206 / 0.0388 / 0.0406 — so no two curves share a curvature and none can
read as an orbit. They are open hub-and-spoke connectors, not rings, and they carry
no arrowheads.

Stroke: matte champagne, `#C6B191` at full strength in dark and 0.45 of it in light
(after review: the first light tone was too close in value to the off-white page and
to the sandstone sphere). Thinner than a hairline relative to the core: 0.5% of its
diameter.

## 3. Materials

Diffuse **pigmented plaster**: metallic 0 and dielectric specular 0 on every role, and
every shell sits at the matte end of the card's roughness band.

| Role | Hex (dark) | Roughness | Card band | Layers |
| --- | --- | --- | --- | --- |
| `core_shell` | `#27565A` | 0.62 | 0.52–0.62 ✓ | tonal, roughness, micro-normal |
| `hcai_shell` | `#6F8474` | 0.72 | 0.60–0.72 ✓ | same graph, own numbers |
| `health_shell` | `#877156` | 0.74 | 0.62–0.74 ✓ | same graph, own numbers |
| `wearable_shell` | `#6B6580` | 0.68 | 0.58–0.68 ✓ | same graph, own numbers |
| `relation` | `#C6B191` | 0.80 | stroke | matte, no glint by design |

Three restrained layers only, all driven by world position (so the grain scale is
identical on a ⌀1.45 core and a ⌀1.00 companion): a very soft low-frequency tonal
drift (noise scale 2.2, ±6%), a roughness breakup (±0.03–0.045), and an extremely
light micro-normal (scale 14, strength 0.032–0.036). Nothing tiled, nothing loud.

Per-theme presets (plan section 3: warm mineral in Light, deeper in Dark): dark
0.97–1.00, light 0.86 / 0.66 / 0.84 / 0.64 — the two lightest companions darkened
most, after the Stage 2.5 review called them pastel.

Why specular is exactly zero: grazing Fresnel glints on the spheres reached a raw
radiance many times the white point, so they stayed pinned at 255 through a 26% key
cut, a specular-level cut *and* a view-transform change. Pigmented plaster has no such
highlight, and the card asks for "non-metallic everywhere", "no glossy plastic" and
"surfaces should not look like CG toys". Shape now comes from the broad key, the tonal
drift and the relief.

## 4. Rendering

**Dark theme.** Key 1150 W / size 6.0 at `(-2.6,-3.2,3.0)`, fill 0.16×, separation
0.20×, world ambient 0.045 — all large area lights at low level. AgX with
`AgX - Medium High Contrast`, exposure −0.55. Background is a **world gradient**
(`#050D1C → #08142A`, gained 6.0 against the tone curve) with a Light-Path split that
keeps the ambient low while the camera sees the navy. Measured background 19/255
against the token's 17. Max pixel 210 — nothing clips.

**Light theme.** Key 1050 W / size 4.6, fill 0.14×, separation 0.16×, ambient 0.055,
AgX, exposure −0.30. The page is **composited from the alpha frame**, so it lands on
the token exactly (measured 248/255, delta 0, and only because the page is composited
can it be exact *and* unclipped). Max pixel 248 — i.e. the page itself; no pixel in
any frame exceeds it.

**No floor, no backdrop geometry, anywhere.** The card asked to minimise the
"standing on a floor" feeling, so the background is the world and the contact shadow
is gone with it: these are hero assets that composite into a page, and the alpha
frames need no clean-up as a result.

Eight outputs — four review frames plus four alpha-ready frames (RGBA, nodes and
curves only, all four corners fully transparent, 20.0% / 24.2% coverage).

## 5. Validation — 19/19 in a fresh Blender process

`source_opens_with_stage_tag` · `previous_sources_unchanged` (sha256 of Stage 1,
Stage 2 and Stage 2.5 files) · `node_count_preserved` ·
`only_spheres_and_relation_curves` · `all_nodes_are_simple_spheres` ·
`no_object_feature_geometry` · `relation_curves_surface_to_surface` ·
`relation_curves_not_one_orbit` · `no_metallic_materials` ·
`no_text_or_particles` · `no_glb_or_web_formats` · `frontend_untouched` ·
`all_eight_renders_exist_and_sized` · `no_clipped_or_blown_highlights`
(0.0% ≥254 on all four, max 210/248) · `alpha_frames_transparent_and_covered` ·
`theme_backgrounds_match_tokens` (Δ2 dark, Δ0 light) ·
`forms_separate_from_background` (0.35 dark, 0.61 light) · `safe_margins_kept`
(8.05% desktop, 3.97% mobile; silhouette gaps 49.7 px / 25.9 px on the real page) ·
`mobile_is_not_a_desktop_crop` (mean difference 0.1475 dark / 0.2548 light against a
0.010 floor, cameras PERSP vs ORTHO).

Measured totals: 55 132 triangles, one material slot per sphere plus one shared
stroke material.

## 6. Visual review answers (the card's nine criteria)

1. **Gadget / device / toy — no.** Nothing reads as a device or a toy in any panel.
2. **Planet reading weaker than Stage 2.5 — yes.** With the curves present the reading
   moves to a node-link system, and the dark panels most of all. The residual is a
   *molecule / hub-and-spoke* association, not a planetary one.
3. **Core important without object-like features — yes.** Scale, centrality, colour
   weight and hub position carry it; no seam or dot is needed.
4. **Companions premium and tactile — yes in dark, improved in light.** After the
   second light calibration the sage reads as a muted grey-green and the violet as a
   deeper aubergine rather than mint and lavender.
5. **One connected system — yes**, and strongest in dark. This was the weakest light
   criterion before the stroke was deepened, and the re-review confirmed the curves
   are now traceable and still restrained.
6. **Dark premium and believable — yes.** No neon, glow, fog or sci-fi tropes.
7. **Light premium and believable — yes, but it is the weaker theme.** A near-white
   page is simply a harder stage than a deep navy one.
8. **Curves support the graph without clutter — yes.** Thin, single-stroke, matte,
   unadorned, never competing with the nodes.
9. **Academic / HCI / research rather than sci-fi — yes.**

## 7. Remaining weaknesses

1. **The arrangement can still read as a molecule.** That is inherent to the card's
   own structure — one distinctive central node plus three companions with no
   decoration — and it is now the honest strongest association left.
2. **Light mode is the weaker theme.** It is believable and no longer pastel, but it
   does not carry the richness of the dark frames; a near-white page gives the matte
   mineral tones less to work with.
3. **Tactility is felt, not seen.** By instruction ("felt, not announced") the relief
   is subtle; a viewer looking for craft imperfections in the surface will not find
   them at review size.
4. **Review-resolution geometry.** ~55k triangles is roughly 4× the plan's GLB budget;
   the export pass must re-tessellate. The curve anchors are ray-cast at build time, so
   they recompute against whatever surface exists — but the smoothness of the spheres
   at lower density still has to be re-checked.
5. **The light review frames depend on the composite step.** Anyone re-rendering must
   run `composite_stage2_6.py` after the builder, or `02-`/`04-` will be stale. This is
   documented in the README and in the builder's own report (`produced_by`).

## 8. Scope statement

No frontend file was read, written or built; no GLB/glTF/WebP/AVIF exists anywhere
under `Design-Assets/hero-v2/`; nothing was written outside `Design-Assets/hero-v2/`;
the Stage 1, Stage 2 and Stage 2.5 source files are unchanged (hash-verified in the
validator); nothing was committed, pushed or deployed. No scroll states, no animation
frames, no About interaction, no motion implementation.
