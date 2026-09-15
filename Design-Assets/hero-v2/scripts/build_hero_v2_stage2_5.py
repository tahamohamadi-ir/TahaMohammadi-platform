"""Hero v2 — Stage 2.5 builder: simplified geometry, calibrated materials, both themes.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_5.py -- \
      --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_5.blend \
      --renders   Design-Assets/hero-v2/renders/stage2_5 \
      --report    Design-Assets/hero-v2/validation/hero-v2-stage2_5-report.json

Flags: --quick (half res, 24 samples), --no-gpu, --exposure <override>,
       --dark-exposure / --light-exposure, --skip-renders.

The composition is not re-authored here: LAYOUT, LAYOUT_ROT_DEG, the diameters,
the view directions, the margin contract and the resolutions are imported from
`build_hero_v2_graybox.py`, so Stage 2.5 inherits the approved Stage 1 composition
by construction. Only the *forms* change: the three companions become single
spheres and the core's seam becomes a procedural recess instead of a boolean.

Sources are hashed before anything else happens, and those hashes go into the
report, so the validator can prove that Stage 1 and Stage 2 stayed untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import build_hero_v2_graybox as s1     # noqa: E402  (import is side-effect free)
import hero_v2_common as hv            # noqa: E402
import hero_v2_stage2_5 as lk          # noqa: E402

STAGE = "2.5 - geometry simplification + material calibration"
SAMPLES = 160
SAMPLES_QUICK = 24
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
ENV_COLLECTION = "Rig_ReviewEnv_2_5"
FORMS_COLLECTION = "HERO_V2_FORMS"
SOURCE_FILES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend")

README_TEXT = """HERO V2 -- STAGE 2.5 (simplified geometry + calibrated materials)

Review-only pass. No GLB, no web asset, no frontend link.

Scene:
  HERO_V2_ROOT
    GRP_CORE                 CORE_SPHERE (procedural seam recess) + CORE_ACCENT
    GRP_HUMAN_CENTERED_AI    HCAI_SPHERE   -- one plain sphere
    GRP_HEALTH_BEHAVIOR      HHB_SPHERE    -- one plain sphere
    GRP_WEARABLE_EDGE        WE_SPHERE     -- one plain sphere
    DECOR_ARC_01             kept for provenance, hide_render = True

The three companions are single closed spheres with <=1.2% radial variation: no
aperture, no inner ball, no bands, no grooves. The core keeps its sphere identity,
its tilted seam and its warm inlay, but the seam is now a raised-cosine radial
recess instead of a boolean cut, so there is no stepped edge to see.

Materials (M2_*): matte mineral ceramic. Metallic 0 everywhere; the accent is a
warm stone inlay. One broad field drives a roughness band and a slight tonal
mottle; the bump is 0.010-0.014 strong, felt rather than seen.

Two authoring environments, only one visible per render:
  dark  -> BACKDROP2_DARK  on the plan's Dark page canvas #071225
  light -> BACKDROP2_LIGHT on the Light page canvas #f7f8f5
Each has its own rig (LG2_5_Dark_*/Light_*) and its own exposure; the light rig is
calibrated independently (stronger key direction, less fill) rather than being the
dark rig on a pale background.

Renders (renders/stage2_5/): 01-desktop-dark, 02-desktop-light, 03-mobile-dark,
04-mobile-light.
"""


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-out", required=True)
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--no-gpu", action="store_true")
    parser.add_argument("--skip-renders", action="store_true")
    parser.add_argument("--exposure", type=float, default=None)
    parser.add_argument("--dark-exposure", type=float, default=None)
    parser.add_argument("--light-exposure", type=float, default=None)
    return parser.parse_args(argv)


def sha256(path):
    if not os.path.exists(path):
        return None
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes(root):
    out = {}
    for relative in SOURCE_FILES:
        path = os.path.join(root, relative)
        out[relative] = dict(sha256=sha256(path), bytes=os.path.getsize(path)
                             if os.path.exists(path) else None)
    return out


# ------------------------------------------------------------------- form builders
def build_core(collection, root):
    sphere = hv.new_uv_sphere("CORE_SPHERE", s1.CORE_RADIUS,
                              segments=lk.CORE_SEGMENTS, rings=lk.CORE_RINGS)
    hv.link_to(sphere, collection)
    touched = lk.recess_seam(sphere, s1.CORE_SEAM_TILT,
                             lk.SEAM_HALF_WIDTH_DEG, lk.SEAM_DEPTH_FRACTION)
    hv.radial_harmonic_deform(sphere, *lk.CORE_DEFORM)
    hv.scale_verts(sphere, *lk.CORE_FLATTEN)
    hv.shade_smooth_by_angle(sphere, lk.SMOOTH_ANGLE_DEG)
    hv.normalize_group([sphere], s1.CORE_DIAMETER)

    # The inlay is anchored to the seam so it interrupts that line deliberately.
    direction = s1.seam_direction(s1.CORE_SEAM_TILT, s1.CORE_ACCENT_PARAM)
    hit, location, _normal, _index = sphere.ray_cast(Vector((0.0, 0.0, 0.0)), direction)
    if not hit:
        raise RuntimeError("core accent ray-cast missed the recessed surface")
    bead = hv.new_uv_sphere("CORE_ACCENT", s1.CORE_ACCENT_RADIUS, segments=64, rings=38)
    hv.link_to(bead, collection)
    hv.scale_verts(bead, 1.0, 1.0, 0.22)
    hv.shade_smooth_by_angle(bead, 55.0)
    bead.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    hv.deselect_all()
    hv.set_active(bead)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    # The ray hit is the FLOOR of the recess, so lift by a fraction of the seam
    # depth: the stone sits flush-to-slightly-proud instead of floating.
    hv.translate_verts(bead, location + direction * lk.ACCENT_PROUD)
    return [sphere, bead], dict(seam_vertices=touched,
                                seam_half_width_deg=lk.SEAM_HALF_WIDTH_DEG,
                                seam_depth_fraction=lk.SEAM_DEPTH_FRACTION,
                                accent_lift=lk.ACCENT_PROUD)


def build_companion(name, collection, scale=1.0):
    sphere = hv.new_uv_sphere(name, s1.DOMAIN_RADIUS,
                              segments=lk.COMPANION_SEGMENTS,
                              rings=lk.COMPANION_RINGS)
    hv.link_to(sphere, collection)
    hv.radial_harmonic_deform(sphere, *lk.COMPANION_DEFORM)
    hv.shade_smooth_by_angle(sphere, lk.SMOOTH_ANGLE_DEG)
    # A shallow scale hierarchy, not a rank change: +/-5% at most, which is what
    # the card's "subtle spatial hierarchy" asks for.
    hv.normalize_group([sphere], s1.DOMAIN_DIAMETER * scale)
    return [sphere]


def build_forms(collection):
    """Same four semantic groups, same layout, simplified forms."""
    groups, empties = {}, {}
    builders = (
        ("GRP_CORE", lambda: build_core(collection, None), "core_shell"),
        ("GRP_HUMAN_CENTERED_AI",
         lambda: build_companion("HCAI_SPHERE", collection,
                                 lk.COMPANION_SCALE["GRP_HUMAN_CENTERED_AI"]),
         "hcai_shell"),
        ("GRP_HEALTH_BEHAVIOR",
         lambda: build_companion("HHB_SPHERE", collection,
                                 lk.COMPANION_SCALE["GRP_HEALTH_BEHAVIOR"]),
         "health_shell"),
        ("GRP_WEARABLE_EDGE",
         lambda: build_companion("WE_SPHERE", collection,
                                 lk.COMPANION_SCALE["GRP_WEARABLE_EDGE"]),
         "wearable_shell"),
    )
    detail = {}
    for group_name, builder, shell_role in builders:
        built = builder()
        objs, info = built if isinstance(built, tuple) else (built, {})
        empty = hv.make_empty(group_name)
        hv.link_to(empty, collection)
        # Stage 1's direction and quadrant, Stage 2.5's radial rhythm. The card
        # forbids an atom/solar-system read; equal radii is what produced it.
        rhythm = lk.COMPANION_RHYTHM.get(group_name, 1.0)
        empty.location = Vector(s1.LAYOUT[group_name]) * rhythm
        empty.rotation_euler = tuple(
            __import__("math").radians(a) for a in s1.LAYOUT_ROT_DEG[group_name])
        for obj in objs:
            obj.parent = empty
        groups[group_name] = objs
        empties[group_name] = empty
        for obj in objs:
            role = "core_accent" if obj.name == "CORE_ACCENT" else shell_role
            lk.assign(obj, role)
            detail[obj.name] = dict(group=group_name, role=role,
                                    **hv.mesh_stats(obj))
        if info:
            detail["_core_seam"] = info
    return groups, empties, detail


def mesh_flags(objs):
    """Structural facts a validator can trust: closed surface, radial variation."""
    out = {}
    for obj in objs:
        mesh = obj.data
        edge_use = {}
        for poly in mesh.polygons:
            for key in poly.edge_keys:
                edge_use[key] = edge_use.get(key, 0) + 1
        boundary = sum(1 for count in edge_use.values() if count == 1)
        nonmanifold = sum(1 for count in edge_use.values() if count > 2)
        euler = len(mesh.vertices) - len(edge_use) + len(mesh.polygons)
        radii = [Vector(vertex.co).length for vertex in mesh.vertices]
        out[obj.name] = dict(
            euler_characteristic=euler, boundary_edges=boundary,
            nonmanifold_edges=nonmanifold,
            radial_variation_pct=round(100.0 * (max(radii) / min(radii) - 1.0), 2)
            if radii and min(radii) > 0 else None)
    return out


def relative_to(path, root):
    """Repo-relative when possible; absolute when the path is on another drive
    (Blender renders into scratch dirs on C: while the repo lives on D:)."""
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return os.path.abspath(path)


def theme_exposure(args, theme):
    """Per-theme exposure: explicit theme flag wins, then the global flag."""
    if theme == "dark" and args.dark_exposure is not None:
        return args.dark_exposure
    if theme == "light" and args.light_exposure is not None:
        return args.light_exposure
    if args.exposure is not None:
        return args.exposure
    return lk.RIGS[theme]["exposure"]


# ---------------------------------------------------------------------------- main
def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(os.path.join(HERE, ".."))
    before = source_hashes(root)
    hv.log("blender %s" % bpy.app.version_string)
    for name, entry in before.items():
        hv.log("source %-36s sha256=%s" % (name, (entry["sha256"] or "MISSING")[:16]))
    hv.clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    forms_coll = hv.ensure_collection(FORMS_COLLECTION)
    materials = lk.build_all_materials()
    groups, empties, detail = build_forms(forms_coll)
    root_empty = hv.make_empty("HERO_V2_ROOT")
    hv.link_to(root_empty, forms_coll)
    for empty in empties.values():
        empty.parent = root_empty

    # Provenance only: the card requires the arc off in every Stage 2.5 render.
    arc = hv.new_torus("DECOR_ARC_01", s1.ARC_RADIUS, s1.ARC_TUBE_MAX,
                       location=s1.ARC_CENTER, rotation=tuple(
                           __import__("math").radians(a) for a in s1.ARC_ROT_DEG))
    hv.link_to(arc, forms_coll)
    arc.hide_render = True

    all_forms = [obj for objs in groups.values() for obj in objs]
    lo, hi = hv.world_bounds(all_forms)
    centre = (lo + hi) * 0.5
    bpy.context.view_layer.update()

    materials = sorted(mat.name for mat in bpy.data.materials
                       if mat.name.startswith("M2_"))
    env_coll = hv.ensure_collection(ENV_COLLECTION)
    backdrop_by_theme = {"dark": lk.build_environment(env_coll, "dark", centre),
                         "light": lk.build_environment(env_coll, "light", centre)}
    rig_by_theme = {"dark": lk.build_rig(env_coll, "dark", centre, "LG2_5_Dark"),
                    "light": lk.build_rig(env_coll, "light", centre, "LG2_5_Light")}
    scene.world = scene.world or bpy.data.worlds.new("HERO_V2_World_2_5")
    scene.world.use_nodes = True

    cam_coll = hv.ensure_collection(s1.CAM_COLLECTION)
    res_desktop = RES_DESKTOP_QUICK if args.quick else s1.RES_DESKTOP
    res_mobile = RES_MOBILE_QUICK if args.quick else s1.RES_MOBILE
    cam_desktop = hv.make_camera("CAM_DESKTOP", s1.VIEW_DIR_DESKTOP, 9.0, centre,
                                 "PERSP", lens=70.0)
    hv.link_to(cam_desktop, cam_coll)
    cam_mobile = hv.make_camera("CAM_MOBILE", s1.VIEW_DIR_MOBILE, 12.0, centre, "ORTHO")
    hv.link_to(cam_mobile, cam_coll)
    desktop_fit = hv.fit_camera(cam_desktop, groups, s1.VIEW_DIR_DESKTOP, centre,
                                s1.MARGIN_DESKTOP, *res_desktop)
    mobile_fit = hv.fit_camera(cam_mobile, groups, s1.VIEW_DIR_MOBILE, centre,
                               s1.MARGIN_MOBILE, *res_mobile)
    hv.log("desktop fit %s" % desktop_fit)
    hv.log("mobile  fit %s" % mobile_fit)
    composition = {
        "desktop": hv.composition_report(cam_desktop, groups, *res_desktop),
        "mobile": hv.composition_report(cam_mobile, groups, *res_mobile)}
    for key, slot in (("desktop", s1.DESKTOP_SLOT_HEIGHT_PX),
                      ("mobile", s1.MOBILE_SLOT_HEIGHT_PX)):
        composition[key]["min_gap_scaled_to_page_px"] = round(
            composition[key]["min_silhouette_gap_px"] *
            (slot / composition[key]["resolution"][1]), 1)
        composition[key]["slot_height_px"] = slot

    flags = mesh_flags(all_forms)
    total_triangles = sum(entry["triangles"] for entry in detail.values()
                          if isinstance(entry, dict) and "triangles" in entry)

    renders, theme_settings = {}, {}
    if not args.skip_renders:
        device = hv.setup_cycles(SAMPLES_QUICK if args.quick else SAMPLES,
                                 lk.RIGS["dark"]["exposure"], gpu=not args.no_gpu)
        hv.log("cycles device: %s" % device)
        scene.use_nodes = False
        scene.render.film_transparent = False
        scene.render.image_settings.color_mode = "RGB"
        out_dir = os.path.abspath(args.renders)
        os.makedirs(out_dir, exist_ok=True)
        for label, camera, theme in lk.RENDERS:
            cam = cam_desktop if camera == "desktop" else cam_mobile
            res = res_desktop if camera == "desktop" else res_mobile
            exposure = theme_exposure(args, theme)
            theme_settings[theme] = lk.apply_theme(theme, backdrop_by_theme,
                                                   rig_by_theme, exposure)
            # Plan section 3: theme-specific material preset, not an inverted render.
            theme_settings[theme]["material_preset"] = lk.apply_theme_tint(
                lk.THEME_TINT[theme])
            hv.set_resolution(int(res[0]), int(res[1]))
            path = os.path.join(out_dir, "%s.png" % label)
            scene.camera = cam
            scene.render.filepath = path
            bpy.ops.render.render(write_still=True)
            hv.log("rendered %s" % path)
            renders[label] = dict(path=relative_to(path, root), camera=cam.name,
                                  theme=theme, resolution=[int(res[0]), int(res[1])],
                                  bytes=os.path.getsize(path)
                                  if os.path.exists(path) else 0)
        # Leave the file in the dark theme: it is the primary review state.
        lk.apply_theme("dark", backdrop_by_theme, rig_by_theme,
                       lk.RIGS["dark"]["exposure"])
        lk.apply_theme_tint(lk.THEME_TINT["dark"])

    hv.write_text_block("README_HERO_V2_STAGE2_5", README_TEXT)
    hv.purge_orphans()
    scene["hero_v2_stage"] = STAGE
    scene["hero_v2_plan"] = "HERO_PRODUCTION_PLAN_v2.md section 3"
    scene["hero_v2_note"] = (
        "Simplified geometry and calibrated matte-mineral materials, both page "
        "canvases. Review-only: no GLB, no web asset, no frontend link.")
    scene["hero_v2_sources"] = json.dumps(before)

    checks = {
        "four_semantic_groups": dict(pass_=sorted(groups) == sorted([
            "GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
            "GRP_WEARABLE_EDGE"]), groups=sorted(groups)),
        "core_plus_three_single_spheres": dict(
            pass_=len(groups["GRP_CORE"]) == 2 and
                  all(len(groups[name]) == 1 for name in groups if name != "GRP_CORE"),
            counts={name: len(objs) for name, objs in groups.items()}),
        "companions_are_closed_single_surfaces": dict(
            pass_=all(flags[obj.name]["euler_characteristic"] == 2 and
                      flags[obj.name]["boundary_edges"] == 0 and
                      flags[obj.name]["nonmanifold_edges"] == 0
                      for name in groups if name != "GRP_CORE"
                      for obj in groups[name]),
            flags={name: flags[name] for name in flags if name != "CORE_ACCENT"}),
        "companion_variation_within_2pct": dict(
            pass_=all(flags[obj.name]["radial_variation_pct"] <= 2.0
                      for name in groups if name != "GRP_CORE"
                      for obj in groups[name]),
            measured={obj.name: flags[obj.name]["radial_variation_pct"]
                      for name in groups if name != "GRP_CORE"
                      for obj in groups[name]}),
        "arc_hidden_from_render": dict(pass_=arc.hide_render is True,
                                       hide_render=arc.hide_render),
        "no_metallic_roles": dict(
            pass_=all(bpy.data.materials["M2_%s" % role.upper()]
                      .node_tree.nodes.get("Principled BSDF")
                      .inputs["Metallic"].default_value == 0.0 for role in lk.ROLES)),
        "no_text_or_particles": dict(
            pass_=not any(obj.type in {"FONT", "CURVE"} for obj in bpy.data.objects)
            and len(bpy.data.particles) == 0),
        "sources_recorded": dict(
            pass_=all(entry["sha256"] for entry in before.values()), sources=before),
        # The layout was re-spaced radially, so the Stage 1 framing contract has to
        # be re-asserted rather than assumed: safe edge margin AND enough silhouette
        # separation once scaled to the real page slots.
        "framing_contract": dict(
            pass_=all(
                min(composition[key]["edge_clearance_pct"].values()) >=
                (s1.MARGIN_DESKTOP if key == "desktop" else s1.MARGIN_MOBILE) * 100.0 - 0.5
                and composition[key]["min_gap_scaled_to_page_px"] >= s1.MIN_GAP_ON_PAGE_PX
                for key in ("desktop", "mobile")),
            edge_clearance_pct={key: composition[key]["edge_clearance_pct"]
                                for key in ("desktop", "mobile")},
            gap_on_page_px={key: composition[key]["min_gap_scaled_to_page_px"]
                            for key in ("desktop", "mobile")},
            required_gap_px=s1.MIN_GAP_ON_PAGE_PX),
    }
    report = dict(
        stage=STAGE, blender=bpy.app.version_string, quick=bool(args.quick),
        samples=SAMPLES_QUICK if args.quick else SAMPLES, render_device=None,
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile)),
        canvases=dict(dark=lk.CANVAS_DARK, light=lk.CANVAS_LIGHT,
                      source="HERO_PRODUCTION_PLAN_v2.md section 3"),
        materials={role: dict(hex=lk.ROLES[role][0], roughness=lk.ROLES[role][1],
                              spread=lk.ROLES[role][2], mottle=lk.ROLES[role][3],
                              bump=lk.ROLES[role][4], metallic=0.0,
                              note=lk.ROLES[role][5]) for role in lk.ROLES},
        material_list=materials,
        geometry_detail=detail, mesh_flags=flags,
        total_triangles=total_triangles,
        composition_adjustments=dict(
            rhythm=lk.COMPANION_RHYTHM, scale=lk.COMPANION_SCALE,
            note="Stage 1 directions and quadrants kept. Radial distances were "
                 "re-spaced outward only (1.62/1.56/1.66 -> 1.72/1.50/1.90) and the "
                 "companions given a shallow +/-5% scale hierarchy, because equal "
                 "radii at equal size read as an atom/solar system, which the card "
                 "forbids. The first attempt pulled one companion inward, shortened "
                 "its chord to a neighbour and broke the 12 px silhouette-gap "
                 "contract on mobile; the framing_contract check caught it.",
            core_position="unchanged"),
        composition=composition, fits=dict(desktop=desktop_fit, mobile=mobile_fit),
        themes=theme_settings, rigs=lk.RIGS, renders=renders,
        sources=before, checks=checks,
        checks_all_pass=all(item["pass_"] for item in checks.values()),
    )
    if not args.skip_renders:
        report["render_device"] = device
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, default=str)
    os.makedirs(os.path.dirname(os.path.abspath(args.blend_out)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend_out))
    hv.log("saved %s" % args.blend_out)
    hv.log("checks_all_pass=%s total_triangles=%d"
           % (report["checks_all_pass"], total_triangles))
    return report


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
