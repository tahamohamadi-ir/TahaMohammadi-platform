"""Hero v2 — Stage 2.6 builder: pure node language.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_6.py -- \
      --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_6.blend \
      --renders   Design-Assets/hero-v2/renders/stage2_6 \
      --report    Design-Assets/hero-v2/validation/hero-v2-stage2_6-report.json

Flags: --quick, --no-gpu, --exposure, --dark-exposure, --light-exposure,
       --skip-renders.

Eight renders: four review frames (opaque, on each theme's background) and four
alpha-ready frames (`film_transparent`, nodes + curves only) for later compositing
over CSS backgrounds.

Composition, diameters, view directions, margins and resolutions are imported from
`build_hero_v2_graybox.py`, and the relation curves are anchored by ray-casting
the real surfaces, so nothing here restates a number that Stage 1 already owns.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import build_hero_v2_graybox as s1     # noqa: E402  (side-effect free import)
import hero_v2_common as hv            # noqa: E402
import hero_v2_stage2_6 as lk          # noqa: E402

STAGE = "2.6 - pure node language (spheres + relation curves)"
SAMPLES = 160
SAMPLES_QUICK = 24
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
FORMS_COLLECTION = "HERO_V2_FORMS"
RIG_COLLECTION = "Rig_ReviewEnv_2_6"
REVIEW_RENDERS = (("01-desktop-dark", "desktop", "dark"),
                  ("03-mobile-dark", "mobile", "dark"))
# The two light review frames are composited from their alpha frames by
# composite_stage2_6.py (page background, exact token, no denoiser overshoot).
COMPOSITE_RENDERS = (("02-desktop-light", "12-desktop-light-alpha", "light"),
                     ("04-mobile-light", "14-mobile-light-alpha", "light"))
ALPHA_RENDERS = (("11-desktop-dark-alpha", "desktop", "dark"),
                 ("12-desktop-light-alpha", "desktop", "light"),
                 ("13-mobile-dark-alpha", "mobile", "dark"),
                 ("14-mobile-light-alpha", "mobile", "light"))
SOURCE_FILES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend",
                "source/hero-v2-stage2_5.blend")
GROUP_ORDER = ("GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
               "GRP_WEARABLE_EDGE")
SHELL_ROLE = {"GRP_CORE": "core_shell", "GRP_HUMAN_CENTERED_AI": "hcai_shell",
              "GRP_HEALTH_BEHAVIOR": "health_shell",
              "GRP_WEARABLE_EDGE": "wearable_shell"}

README_TEXT = """HERO V2 -- STAGE 2.6 (pure node language)

Four plain spheres and three real relation curves. No shell, cavity, aperture,
band, ring, seam, inlay or decorative arc exists in this file.

Scene:
  HERO_V2_ROOT
    GRP_CORE                 CORE_SPHERE     -- one plain sphere
    GRP_HUMAN_CENTERED_AI    HCAI_SPHERE     -- one plain sphere
    GRP_HEALTH_BEHAVIOR      HHB_SPHERE      -- one plain sphere
    GRP_WEARABLE_EDGE        WE_SPHERE       -- one plain sphere
    REL_CORE_HCAI / REL_CORE_HHB / REL_CORE_WE
                             cubic Bezier rods, one per real relation, each
                             anchored by ray-cast on the core's surface and on the
                             companion's surface. Asymmetric curvature per curve.

Materials (M2_6_*): pigmented mineral plaster. Metallic 0 everywhere. Three
restrained layers only -- a very soft low-frequency tonal drift, a roughness
breakup, and an extremely light micro-normal. The relation strokes are a champagne
non-metallic tone, thicker than a hairline but thin enough to stay supporting.

No floor and no backdrop geometry: the background for camera rays comes from the
world (a light-path split), so nothing can look like a studio stage and the alpha
frames need no clean-up.

Renders: renders/stage2_6/01..04 review frames (opaque) and 11..14 alpha frames
(transparent, nodes + curves only).

No GLB, no web export, no frontend link, no motion.
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
        out[relative] = dict(sha256=sha256(path),
                             bytes=(os.path.getsize(path)
                                    if os.path.exists(path) else None))
    return out


def relative_to(path, root):
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return os.path.abspath(path)


def theme_exposure(args, theme):
    if theme == "dark" and args.dark_exposure is not None:
        return args.dark_exposure
    if theme == "light" and args.light_exposure is not None:
        return args.light_exposure
    if args.exposure is not None:
        return args.exposure
    return lk.RIGS[theme]["exposure"]


def topology(obj):
    """Closed surface? Radial variation? Read off the mesh, not assumed."""
    edge_use = {}
    for poly in obj.data.polygons:
        for key in poly.edge_keys:
            edge_use[key] = edge_use.get(key, 0) + 1
    radii = [vertex.co.length for vertex in obj.data.vertices]
    return dict(faces=len(obj.data.polygons), vertices=len(obj.data.vertices),
                euler=len(obj.data.vertices) - len(edge_use) + len(obj.data.polygons),
                boundary_edges=sum(1 for count in edge_use.values() if count == 1),
                nonmanifold_edges=sum(1 for count in edge_use.values() if count > 2),
                radial_variation_pct=round(100.0 * (max(radii) / min(radii) - 1.0), 2)
                if radii and min(radii) > 0 else None)


def build_sphere(name, radius, collection, segments, rings, deform, flatten=None,
                 diameter=None, scale=1.0):
    sphere = hv.new_uv_sphere(name, radius, segments=segments, rings=rings)
    hv.link_to(sphere, collection)
    hv.radial_harmonic_deform(sphere, *deform)
    if flatten:
        hv.scale_verts(sphere, *flatten)
    hv.shade_smooth_by_angle(sphere, lk.SMOOTH_ANGLE_DEG)
    hv.normalize_group([sphere], (diameter or radius * 2.0) * scale)
    return sphere


def build_nodes(collection):
    core = build_sphere("CORE_SPHERE", s1.CORE_RADIUS, collection,
                        lk.CORE_SEGMENTS, lk.CORE_RINGS, lk.CORE_DEFORM,
                        lk.CORE_FLATTEN, diameter=s1.CORE_DIAMETER)
    companions = {}
    for group in GROUP_ORDER[1:]:
        name = {"GRP_HUMAN_CENTERED_AI": "HCAI_SPHERE",
                "GRP_HEALTH_BEHAVIOR": "HHB_SPHERE",
                "GRP_WEARABLE_EDGE": "WE_SPHERE"}[group]
        companions[group] = build_sphere(
            name, s1.DOMAIN_RADIUS, collection, lk.COMPANION_SEGMENTS,
            lk.COMPANION_RINGS, lk.COMPANION_DEFORM, None,
            diameter=s1.DOMAIN_DIAMETER, scale=lk.COMPANION_SCALE[group])
    groups, empties = {"GRP_CORE": [core]}, {}
    for index, group in enumerate(GROUP_ORDER):
        empty = hv.make_empty(group)
        hv.link_to(empty, collection)
        rhythm = lk.COMPANION_RHYTHM.get(group, 1.0)
        empty.location = Vector(s1.LAYOUT[group]) * rhythm
        empty.rotation_euler = tuple(math.radians(angle)
                                     for angle in s1.LAYOUT_ROT_DEG[group])
        if index:
            groups[group] = [companions[group]]
        for obj in groups[group]:
            obj.parent = empty
        empties[group] = empty
    bpy.context.view_layer.update()
    return groups, empties


def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(os.path.join(HERE, ".."))
    sources = source_hashes(root)
    hv.log("blender %s" % bpy.app.version_string)
    for name, entry in sources.items():
        hv.log("source %-38s sha256=%s" % (name, (entry["sha256"] or "MISSING")[:16]))
    hv.clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    forms_coll = hv.ensure_collection(FORMS_COLLECTION)
    materials = lk.build_all_materials()
    groups, empties = build_nodes(forms_coll)
    forms_root = hv.make_empty("HERO_V2_ROOT")
    hv.link_to(forms_root, forms_coll)
    for empty in empties.values():
        empty.parent = forms_root

    for group in GROUP_ORDER:
        for obj in groups[group]:
            lk_role = SHELL_ROLE[group]
            obj.data.materials.clear()
            obj.data.materials.append(bpy.data.materials[
                "M2_6_%s" % lk_role.upper()])

    relations = {}
    curve_objects = []
    for group in GROUP_ORDER[1:]:
        spec = lk.RELATIONS[group]
        curve, info = lk.build_relation_curve(
            "REL_CORE_%s" % group.replace("GRP_", ""), groups["GRP_CORE"][0],
            groups[group][0], spec["bend"], spec["lift"], forms_coll)
        curve.parent = forms_root
        curve_objects.append(curve)
        relations[group] = info
        hv.log("relation %s len=%.3f dev=%.3f start=%.3f end=%.3f"
               % (curve.name, info["chord_length"], info["max_deviation_fraction"],
                  info["start_distance_from_core_centre"],
                  info["end_distance_from_companion_centre"]))

    all_forms = [obj for objs in groups.values() for obj in objs] + curve_objects
    lo, hi = hv.world_bounds([obj for objs in groups.values() for obj in objs])
    centre = (lo + hi) * 0.5
    bpy.context.view_layer.update()

    rig_coll = hv.ensure_collection(RIG_COLLECTION)
    rigs = {"dark": lk.build_rig(rig_coll, "dark", centre, "LG2_6_Dark"),
            "light": lk.build_rig(rig_coll, "light", centre, "LG2_6_Light")}
    lk.ensure_world()

    cam_coll = hv.ensure_collection(s1.CAM_COLLECTION)
    res_desktop = RES_DESKTOP_QUICK if args.quick else s1.RES_DESKTOP
    res_mobile = RES_MOBILE_QUICK if args.quick else s1.RES_MOBILE
    cam_desktop = hv.make_camera("CAM_DESKTOP", s1.VIEW_DIR_DESKTOP, 9.0, centre,
                                 "PERSP", lens=70.0)
    hv.link_to(cam_desktop, cam_coll)
    cam_mobile = hv.make_camera("CAM_MOBILE", s1.VIEW_DIR_MOBILE, 12.0, centre,
                                "ORTHO")
    hv.link_to(cam_mobile, cam_coll)
    # Fit against nodes AND curves, so a bulging relation can never leave the frame.
    fit_payload = {"forms": all_forms}
    desktop_fit = hv.fit_camera(cam_desktop, fit_payload, s1.VIEW_DIR_DESKTOP,
                                centre, s1.MARGIN_DESKTOP, *res_desktop)
    mobile_fit = hv.fit_camera(cam_mobile, fit_payload, s1.VIEW_DIR_MOBILE, centre,
                               s1.MARGIN_MOBILE, *res_mobile)
    composition = {"desktop": hv.composition_report(cam_desktop, groups,
                                                    *res_desktop),
                   "mobile": hv.composition_report(cam_mobile, groups, *res_mobile)}
    for key, slot in (("desktop", s1.DESKTOP_SLOT_HEIGHT_PX),
                      ("mobile", s1.MOBILE_SLOT_HEIGHT_PX)):
        composition[key]["min_gap_scaled_to_page_px"] = round(
            composition[key]["min_silhouette_gap_px"] *
            (slot / composition[key]["resolution"][1]), 1)

    renders, themes = {}, {}
    if not args.skip_renders:
        device = hv.setup_cycles(SAMPLES_QUICK if args.quick else SAMPLES,
                                 lk.RIGS["dark"]["exposure"], gpu=not args.no_gpu)
        hv.log("cycles device: %s" % device)
        scene.use_nodes = False
        out_dir = os.path.abspath(args.renders)
        os.makedirs(out_dir, exist_ok=True)

        def shoot(label, camera, theme):
            cam = cam_desktop if camera == "desktop" else cam_mobile
            res = res_desktop if camera == "desktop" else res_mobile
            hv.set_resolution(int(res[0]), int(res[1]))
            path = os.path.join(out_dir, "%s.png" % label)
            scene.camera = cam
            scene.render.filepath = path
            bpy.ops.render.render(write_still=True)
            hv.log("rendered %s" % path)
            renders[label] = dict(path=relative_to(path, root), camera=cam.name,
                                  theme=theme, resolution=[int(res[0]), int(res[1])],
                                  alpha=label.endswith("-alpha"),
                                  bytes=(os.path.getsize(path)
                                         if os.path.exists(path) else 0))

        for label, camera, theme in REVIEW_RENDERS:
            themes[theme] = lk.apply_theme(theme, rigs, theme_exposure(args, theme))
            background = lk.configure_output(scene, theme, alpha=False)
            shoot(label, camera, theme)
            renders[label]["background"] = background
        for label, camera, theme in ALPHA_RENDERS:
            themes[theme] = lk.apply_theme(theme, rigs, theme_exposure(args, theme))
            background = lk.configure_output(scene, theme, alpha=True)
            shoot(label, camera, theme)
            renders[label]["background"] = background
        for label, source, theme in COMPOSITE_RENDERS:
            target = os.path.join(out_dir, "%s.png" % label)
            renders[label] = dict(path=relative_to(target, root), theme=theme,
                                  camera="desktop" if label.startswith("02")
                                  else "mobile",
                                  resolution=list(res_desktop if label.startswith("02")
                                                  else res_mobile),
                                  alpha=False, bytes=(os.path.getsize(target)
                                                      if os.path.exists(target) else 0),
                                  background="composited_page",
                                  produced_by="composite_stage2_6.py",
                                  source_alpha=source)
        # Leave the file ready for the next dark review frame.
        lk.apply_theme("dark", rigs, lk.RIGS["dark"]["exposure"])
        lk.configure_output(scene, "dark", alpha=False)

    hv.write_text_block("README_HERO_V2_STAGE2_6", README_TEXT)
    hv.purge_orphans()
    scene["hero_v2_stage"] = STAGE
    scene["hero_v2_plan"] = "HERO_PRODUCTION_PLAN_v2.md section 3"
    scene["hero_v2_note"] = (
        "Pure node language: four plain spheres plus three surface-anchored relation "
        "curves. No seam, inlay, cavity, band, ring or decorative arc exists. No "
        "GLB, no web export, no frontend link, no motion.")
    scene["hero_v2_relations"] = json.dumps(relations)

    node_flags = {obj.name: topology(obj) for obj in
                  [o for objs in groups.values() for o in objs]}
    curve_flags = {obj.name: topology(obj) for obj in curve_objects}
    forbidden = sorted(
        obj.name for obj in bpy.data.objects
        if obj.type == "MESH" and any(token in obj.name.upper() for token in
                                      ("SHELL", "INSET", "INNER", "BAND", "RING",
                                       "Aperture".upper(), "ARC", "SEAM", "GROOVE",
                                       "ACCENT")))
    anchor_tolerance = 0.02     # 2% of the node's own radius
    curves_ok = {}
    for group, info in relations.items():
        companion = groups[group][0]
        core = groups["GRP_CORE"][0]
        core_radius = max(Vector(vertex.co).length for vertex in core.data.vertices)
        companion_radius = max(Vector(vertex.co).length
                               for vertex in companion.data.vertices)
        curves_ok[group] = dict(
            start_ok=abs(info["start_distance_from_core_centre"] - core_radius) <=
            anchor_tolerance * core_radius,
            end_ok=abs(info["end_distance_from_companion_centre"] - companion_radius)
            <= anchor_tolerance * companion_radius,
            core_radius=round(core_radius, 4),
            companion_radius=round(companion_radius, 4))
    deviations = [info["max_deviation_fraction"] for info in relations.values()]
    checks = {
        "sources_recorded": dict(
            pass_=all(entry["sha256"] for entry in sources.values()),
            sources=sources),
        "node_count_preserved": dict(
            pass_=len(groups) == 4 and
                  sum(len(objs) for objs in groups.values()) == 4,
            groups={name: [obj.name for obj in objs]
                    for name, objs in groups.items()}),
        "all_nodes_simple_spheres": dict(
            pass_=all(entry["euler"] == 2 and entry["boundary_edges"] == 0 and
                      entry["nonmanifold_edges"] == 0 and
                      entry["radial_variation_pct"] <= 2.0
                      for entry in node_flags.values()),
            topology=node_flags),
        "no_object_feature_geometry": dict(
            pass_=not forbidden, offenders=forbidden,
            note="no shell, cavity, inner ball, band, ring, seam, inlay or arc "
                 "object exists in this scene (DECOR_ARC_01 is gone entirely)"),
        "relation_curves_surface_to_surface": dict(
            pass_=len(curve_objects) == 3 and
                  all(entry["start_ok"] and entry["end_ok"]
                      for entry in curves_ok.values()),
            per_relation=curves_ok, tolerance_fraction=anchor_tolerance),
        "relation_curves_asymmetric": dict(
            pass_=len(set(round(value, 4) for value in deviations)) == 3 and
                  len(set(round(abs(value), 4) for value in deviations)) == 3,
            deviations=[round(value, 4) for value in deviations],
            note="three distinct deviations from their own chords, so no two curves "
                 "share a curvature and none reads as an orbit"),
        "no_metallic_materials": dict(
            pass_=all(float(bpy.data.materials[name].node_tree.nodes.get(
                "Principled BSDF").inputs["Metallic"].default_value) == 0.0
                for name in materials)),
        "no_text_or_particles": dict(
            pass_=not any(obj.type in {"FONT", "CURVE"} for obj in bpy.data.objects)
            and len(bpy.data.particles) == 0,
            types=sorted({obj.type for obj in bpy.data.objects})),
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
            fit_bbox=dict(desktop=desktop_fit.get("projected_bbox"),
                          mobile=mobile_fit.get("projected_bbox"))),
    }
    report = dict(
        stage=STAGE, blender=bpy.app.version_string, quick=bool(args.quick),
        samples=SAMPLES_QUICK if args.quick else SAMPLES,
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile)),
        canvases=dict(dark=[lk.CANVAS_DARK_BOTTOM, lk.CANVAS_DARK_TOP],
                      light=lk.CANVAS_LIGHT,
                      source="HERO_PRODUCTION_PLAN_v2.md section 3"),
        materials={role: dict(hex=lk.role_hex(role),
                              roughness=lk.role_roughness(role),
                              metallic=0.0, note=lk.ROLES[role][5])
                   for role in lk.ROLES},
        material_list=materials,
        theme_presets=lk.THEME_TINT,
        relations=relations, relation_topology=curve_flags,
        node_topology=node_flags,
        total_triangles=sum(entry["faces"] * 2 for entry in
                            list(node_flags.values()) + list(curve_flags.values())),
        composition=composition, fits=dict(desktop=desktop_fit, mobile=mobile_fit),
        themes=themes, rigs=lk.RIGS, renders=renders, sources=sources,
        checks=checks, checks_all_pass=all(item["pass_"] for item in checks.values()),
    )
    if not args.skip_renders:
        report["render_device"] = device
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, default=str)
    os.makedirs(os.path.dirname(os.path.abspath(args.blend_out)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend_out))
    hv.log("saved %s" % args.blend_out)
    hv.log("checks_all_pass=%s" % report["checks_all_pass"])
    return report


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
