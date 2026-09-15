"""Hero v2 — Stage 2.7 builder: final look lock (materials + relations).

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/build_hero_v2_stage2_7.py -- \
      --blend-out Design-Assets/hero-v2/source/hero-v2-stage2_7.blend \
      --renders   Design-Assets/hero-v2/renders/stage2_7 \
      --report    Design-Assets/hero-v2/validation/hero-v2-stage2_7-report.json

Then (Pillow, system python) to composite the light page and make the web-scale
previews:  python .../composite_stage2_7.py --renders .../renders/stage2_7

Geometry is not rebuilt here in any meaningful sense: the spheres are built by Stage
2.6's own `build_sphere` helper with Stage 2.6's own constants, so the approved
silhouettes are identical by construction, and only the material assignment differs.
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

import build_hero_v2_graybox as s1                       # noqa: E402
import build_hero_v2_stage2_6 as builder26              # noqa: E402
import hero_v2_common as hv                             # noqa: E402
import hero_v2_stage2_7 as lk                           # noqa: E402

STAGE = "2.7 - material + relation polish (final look lock)"
SAMPLES = 160
SAMPLES_QUICK = 24
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
FORMS_COLLECTION = "HERO_V2_FORMS"
RIG_COLLECTION = "Rig_ReviewEnv_2_7"
DARK_REVIEW = (("01-desktop-dark", "desktop", "dark"),
               ("03-mobile-dark", "mobile", "dark"))
ALPHA_RENDERS = (("11-desktop-dark-alpha", "desktop", "dark"),
                 ("12-desktop-light-alpha", "desktop", "light"),
                 ("13-mobile-dark-alpha", "mobile", "dark"),
                 ("14-mobile-light-alpha", "mobile", "light"))
LIGHT_REVIEW = (("02-desktop-light", "12-desktop-light-alpha"),
                ("04-mobile-light", "14-mobile-light-alpha"))
WEBSCALE = (("21-desktop-dark-webscale", "01-desktop-dark", "desktop"),
            ("22-desktop-light-webscale", "02-desktop-light", "desktop"),
            ("23-mobile-dark-webscale", "03-mobile-dark", "mobile"),
            ("24-mobile-light-webscale", "04-mobile-light", "mobile"))
SOURCE_FILES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend",
                "source/hero-v2-stage2_5.blend", "source/hero-v2-stage2_6.blend")
GROUP_ORDER = ("GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
               "GRP_WEARABLE_EDGE")
SHELL_ROLE = {"GRP_CORE": "core_shell", "GRP_HUMAN_CENTERED_AI": "hcai_shell",
              "GRP_HEALTH_BEHAVIOR": "health_shell",
              "GRP_WEARABLE_EDGE": "wearable_shell"}
COMPANION_MESH = {"GRP_HUMAN_CENTERED_AI": "HCAI_SPHERE",
                  "GRP_HEALTH_BEHAVIOR": "HHB_SPHERE",
                  "GRP_WEARABLE_EDGE": "WE_SPHERE"}
FORBIDDEN_TOKENS = ("SHELL", "INSET", "INNER", "BAND", "RING", "APERTURE", "ARC",
                    "SEAM", "GROOVE", "ACCENT", "BUTTON")
ANCHOR_TOLERANCE = 0.02

README_TEXT = """HERO V2 -- STAGE 2.7 (material + relation polish, look lock)

Stage 2.6's geometry language is approved and unchanged: four plain spheres and
three real relation curves. This file changes only how they are made.

  HERO_V2_ROOT
    GRP_CORE                CORE_SPHERE   one plain sphere (identical geometry)
    GRP_HUMAN_CENTERED_AI   HCAI_SPHERE   one plain sphere
    GRP_HEALTH_BEHAVIOR     HHB_SPHERE    one plain sphere
    GRP_WEARABLE_EDGE       WE_SPHERE     one plain sphere
    REL_CORE_*              three hairline strokes, ray-cast onto both surfaces

Materials (M2_7_*): pigmented mineral plaster with a real dielectric response --
metallic 0, IOR 1.43-1.46, specular level 0.5 (Blender's physical F0 for that IOR),
roughness 0.62-0.72 for the shells. Three decorrelated scales: macro tonal drift,
meso roughness patches, micro tactile normal. Per-theme presets change pigment AND
roughness AND rig - light mode is not a blanket darkening.

Relations: bevel radius 0.0032 (43% of Stage 2.6), tapered 1.00 -> 0.55 so the
stroke has no uniform weight, per-curve curvature, and one stroke's core-side anchor
is swung 38 degrees so it leaves from behind the core (real occlusion, no tangled
graph). One stroke is 0.85 and one is 0.70 of the base radius.

Renders: renders/stage2_7/ 01..04 review, 11..14 alpha, 21..24 web-scale previews at
the real CSS footprint (desktop 686x600, mobile 288x288).

No GLB, no web export, no frontend link, no scroll frames.
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
    edge_use = {}
    for poly in obj.data.polygons:
        for key in poly.edge_keys:
            edge_use[key] = edge_use.get(key, 0) + 1
    radii = [vertex.co.length for vertex in obj.data.vertices]
    return dict(faces=len(obj.data.polygons),
                euler=len(obj.data.vertices) - len(edge_use) + len(obj.data.polygons),
                boundary_edges=sum(1 for count in edge_use.values() if count == 1),
                nonmanifold_edges=sum(1 for count in edge_use.values() if count > 2),
                radial_variation_pct=round(100.0 * (max(radii) / min(radii) - 1.0), 2)
                if radii and min(radii) > 0 else None)


def build_nodes(collection):
    """Same four spheres, built by Stage 2.6's helper with Stage 2.6's constants."""
    core = builder26.build_sphere(
        "CORE_SPHERE", s1.CORE_RADIUS, collection, lk.CORE_SEGMENTS, lk.CORE_RINGS,
        lk.CORE_DEFORM, lk.CORE_FLATTEN, diameter=s1.CORE_DIAMETER)
    companions = {}
    for group in GROUP_ORDER[1:]:
        companions[group] = builder26.build_sphere(
            COMPANION_MESH[group], s1.DOMAIN_RADIUS, collection,
            lk.COMPANION_SEGMENTS, lk.COMPANION_RINGS, lk.COMPANION_DEFORM, None,
            diameter=s1.DOMAIN_DIAMETER, scale=lk.COMPANION_SCALE[group])
    groups, empties = {"GRP_CORE": [core]}, {}
    for index, group in enumerate(GROUP_ORDER):
        empty = hv.make_empty(group)
        hv.link_to(empty, collection)
        empty.location = Vector(s1.LAYOUT[group]) * lk.COMPANION_RHYTHM.get(group, 1.0)
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
            obj.data.materials.clear()
            obj.data.materials.append(
                bpy.data.materials["M2_7_%s" % SHELL_ROLE[group].upper()])

    relations, curves = {}, []
    for group in GROUP_ORDER[1:]:
        curve, info = lk.build_relation_curve(
            "REL_CORE_%s" % group.replace("GRP_", ""), groups["GRP_CORE"][0],
            groups[group][0], lk.RELATIONS[group], forms_coll)
        curve.parent = forms_root
        curves.append(curve)
        relations[group] = info
        hv.log("relation %s len=%.3f dev=%.3f signed=%.4f excess=%.5f swing=%.0f"
               % (curve.name, info["chord_length"], info["max_deviation_fraction"],
                  info["min_signed_clearance"], info["interpenetration_excess"],
                  info["swing_deg"]))

    all_forms = [obj for objs in groups.values() for obj in objs] + curves
    lo, hi = hv.world_bounds([obj for objs in groups.values() for obj in objs])
    centre = (lo + hi) * 0.5
    bpy.context.view_layer.update()

    rig_coll = hv.ensure_collection(RIG_COLLECTION)
    rigs = {"dark": lk.build_rig(rig_coll, "dark", centre, "LG2_7_Dark"),
            "light": lk.build_rig(rig_coll, "light", centre, "LG2_7_Light")}
    base = lk.base
    base.ensure_world()

    cam_coll = hv.ensure_collection(s1.CAM_COLLECTION)
    res_desktop = RES_DESKTOP_QUICK if args.quick else s1.RES_DESKTOP
    res_mobile = RES_MOBILE_QUICK if args.quick else s1.RES_MOBILE
    cam_desktop = hv.make_camera("CAM_DESKTOP", s1.VIEW_DIR_DESKTOP, 9.0, centre,
                                 "PERSP", lens=70.0)
    hv.link_to(cam_desktop, cam_coll)
    cam_mobile = hv.make_camera("CAM_MOBILE", s1.VIEW_DIR_MOBILE, 12.0, centre, "ORTHO")
    hv.link_to(cam_mobile, cam_coll)
    fit_payload = {"forms": all_forms}
    desktop_fit = hv.fit_camera(cam_desktop, fit_payload, s1.VIEW_DIR_DESKTOP, centre,
                               s1.MARGIN_DESKTOP, *res_desktop)
    mobile_fit = hv.fit_camera(cam_mobile, fit_payload, s1.VIEW_DIR_MOBILE, centre,
                              s1.MARGIN_MOBILE, *res_mobile)
    composition = {"desktop": hv.composition_report(cam_desktop, groups, *res_desktop),
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
        out_dir = os.path.abspath(args.renders)
        os.makedirs(out_dir, exist_ok=True)

        def shoot(label, camera, theme, alpha):
            cam = cam_desktop if camera == "desktop" else cam_mobile
            res = res_desktop if camera == "desktop" else res_mobile
            hv.set_resolution(int(res[0]), int(res[1]))
            path = os.path.join(out_dir, "%s.png" % label)
            scene.camera = cam
            scene.render.filepath = path
            bpy.ops.render.render(write_still=True)
            hv.log("rendered %s" % path)
            renders[label] = dict(path=relative_to(path, root), camera=cam.name,
                                  theme=theme, alpha=alpha,
                                  resolution=[int(res[0]), int(res[1])],
                                  bytes=(os.path.getsize(path)
                                         if os.path.exists(path) else 0))

        for label, camera, theme in DARK_REVIEW:
            themes[theme] = lk.apply_theme(theme, rigs, theme_exposure(args, theme))
            lk.base.configure_output(scene, theme, alpha=False)
            shoot(label, camera, theme, False)
        for label, camera, theme in ALPHA_RENDERS:
            themes[theme] = lk.apply_theme(theme, rigs, theme_exposure(args, theme))
            lk.base.configure_output(scene, theme, alpha=True)
            shoot(label, camera, theme, True)
        for label, source in LIGHT_REVIEW:
            target = os.path.join(out_dir, "%s.png" % label)
            renders[label] = dict(path=relative_to(target, root), theme="light",
                                  camera="desktop" if label.startswith("02") else "mobile",
                                  resolution=list(res_desktop if label.startswith("02")
                                                  else res_mobile),
                                  alpha=False, bytes=(os.path.getsize(target)
                                                      if os.path.exists(target) else 0),
                                  produced_by="composite_stage2_7.py",
                                  source_alpha=source)
        for label, source, breakpoint in WEBSCALE:
            target = os.path.join(out_dir, "%s.png" % label)
            renders[label] = dict(path=relative_to(target, root),
                                  camera=breakpoint,
                                  theme="dark" if "-dark-" in label else "light",
                                  resolution=list(lk.WEB_SCALE[breakpoint]),
                                  alpha=False, bytes=(os.path.getsize(target)
                                                      if os.path.exists(target) else 0),
                                  produced_by="composite_stage2_7.py",
                                  source_review=source)
        lk.apply_theme("dark", rigs, lk.RIGS["dark"]["exposure"])
        lk.base.configure_output(scene, "dark", alpha=False)

    hv.write_text_block("README_HERO_V2_STAGE2_7", README_TEXT)
    hv.purge_orphans()
    scene["hero_v2_stage"] = STAGE
    scene["hero_v2_plan"] = "HERO_PRODUCTION_PLAN_v2.md section 3"
    scene["hero_v2_note"] = (
        "Look lock: dielectric plaster materials, hairline relation strokes, "
        "per-theme pigment+roughness presets. Geometry unchanged from stage 2.6. "
        "No GLB, no web export, no frontend link, no scroll frames.")
    scene["hero_v2_relations"] = json.dumps(relations)

    node_flags = {obj.name: topology(obj) for objs in groups.values() for obj in objs}
    curve_flags = {obj.name: topology(obj) for obj in curves}
    mesh_names = sorted(obj.name for obj in bpy.data.objects if obj.type == "MESH")
    forbidden = [name for name in mesh_names
                 if any(token in name.upper() for token in FORBIDDEN_TOKENS)]
    dielectric = {}
    for role in lk.ROLES:
        mat = bpy.data.materials["M2_7_%s" % role.upper()]
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        dielectric[role] = dict(
            metallic=round(float(bsdf.inputs["Metallic"].default_value), 3),
            ior=round(float(bsdf.inputs["IOR"].default_value), 3),
            specular=round(float(bsdf.inputs["Specular IOR Level"].default_value
                                 if "Specular IOR Level" in bsdf.inputs
                                 else bsdf.inputs["Specular"].default_value), 3),
            roughness=round(float(bsdf.inputs["Roughness"].default_value), 3))
    anchors = {}
    for group, info in relations.items():
        core = groups["GRP_CORE"][0]
        companion = groups[group][0]
        core_radius = max(vertex.co.length for vertex in core.data.vertices)
        companion_radius = max(vertex.co.length for vertex in companion.data.vertices)
        anchors[group] = dict(
            start_ok=abs(info["start_distance_from_core_centre"] - core_radius) <=
            ANCHOR_TOLERANCE * core_radius,
            end_ok=abs(info["end_distance_from_companion_centre"] - companion_radius)
            <= ANCHOR_TOLERANCE * companion_radius,
            core_radius=round(core_radius, 4),
            companion_radius=round(companion_radius, 4))
    deviations = [info["max_deviation_fraction"] for info in relations.values()]
    checks = {
        "sources_recorded": dict(pass_=all(e["sha256"] for e in sources.values()),
                                 sources=sources),
        "node_count_preserved": dict(
            pass_=len(groups) == 4 and sum(len(o) for o in groups.values()) == 4,
            groups={name: [obj.name for obj in objs] for name, objs in groups.items()}),
        "all_nodes_simple_spheres": dict(
            pass_=len(node_flags) == 4 and all(
                e["euler"] == 2 and e["boundary_edges"] == 0 and
                e["nonmanifold_edges"] == 0 and e["radial_variation_pct"] <= 2.0
                for e in node_flags.values()), topology=node_flags),
        "exactly_three_relations": dict(pass_=len(curves) == 3,
                                        curves=[obj.name for obj in curves]),
        "relations_surface_to_surface": dict(
            pass_=all(e["start_ok"] and e["end_ok"] for e in anchors.values()),
            per_relation=anchors, tolerance_fraction=ANCHOR_TOLERANCE),
        "relations_asymmetric": dict(
            pass_=len(set(round(v, 4) for v in deviations)) == 3,
            deviations=[round(v, 4) for v in deviations]),
        "relations_clear_the_core": dict(
            pass_=all(info["interpenetration_excess"] <= 0.001
                      for info in relations.values()),
            measured={name: dict(mid_path=info["mid_path_signed_clearance"],
                                 anchor=info["min_signed_clearance"],
                                 centreline_min_radius=info["centreline_min_radius"],
                                 core_radius=info["core_radius"],
                                 excess=info["interpenetration_excess"],
                                 correction=info["outward_correction"])
                      for name, info in relations.items()},
            note="mid-path burial is the failure mode (a stroke cutting through the "
                 "sphere); burial at the anchor is attachment and is reported "
                 "separately. A control-handle solver pushes the path outward by "
                 "(correction) whenever even the centreline would enter the sphere"),
        "relation_hairlines": dict(
            pass_=all(info["bevel_radius"] <= 0.5 * 0.0075 for info in relations.values()),
            bevel_radius={name: info["bevel_radius"] for name, info in relations.items()},
            stage26_radius=0.0075),
        "no_forbidden_feature_geometry": dict(pass_=not forbidden, offenders=forbidden),
        "dielectric_response_present": dict(
            pass_=all(e["metallic"] == 0.0 and e["ior"] >= 1.42 and e["ior"] <= 1.50
                      and e["specular"] > 0.0 and 0.58 <= e["roughness"] <= 0.76
                      for role, e in dielectric.items() if role != "relation"),
            measured=dielectric,
            note="metallic 0 with a plausible IOR and a broad, rough specular lobe"),
        "framing_contract": dict(
            pass_=all(
                min(composition[key]["edge_clearance_pct"].values()) >=
                (s1.MARGIN_DESKTOP if key == "desktop" else s1.MARGIN_MOBILE) * 100.0 - 0.5
                and composition[key]["min_gap_scaled_to_page_px"] >= s1.MIN_GAP_ON_PAGE_PX
                for key in ("desktop", "mobile")),
            edge_clearance_pct={key: composition[key]["edge_clearance_pct"]
                                for key in ("desktop", "mobile")},
            gap_on_page_px={key: composition[key]["min_gap_scaled_to_page_px"]
                            for key in ("desktop", "mobile")}),
    }
    report = dict(
        stage=STAGE, blender=bpy.app.version_string, quick=bool(args.quick),
        samples=SAMPLES_QUICK if args.quick else SAMPLES,
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile),
                        webscale=lk.WEB_SCALE),
        canvases=dict(dark=list(lk.CANVAS_DARK_GRADIENT), light=lk.CANVAS_LIGHT),
        shader_architecture=dict(
            model="Principled BSDF, metallic 0, physical dielectric F0 (specular "
                  "level 0.5) with IOR 1.43-1.46, roughness 0.62-0.72 for shells",
            scales=dict(macro=dict(scale=lk.MACRO_SCALE, detail=lk.MACRO_DETAIL,
                                   effect="tonal drift, +/-3.5%"),
                        meso=dict(scale=lk.MESO_SCALE, detail=lk.MESO_DETAIL,
                                  effect="roughness patches"),
                        micro=dict(scale=lk.MICRO_SCALE, detail=lk.MICRO_DETAIL,
                                   bump_distance=lk.MICRO_DISTANCE,
                                   effect="tactile normal")),
            roles={role: dict(hex=lk.ROLES[role][0], roughness=lk.ROLES[role][1],
                              spread=lk.ROLES[role][2], tonal=lk.ROLES[role][3],
                              bump=lk.ROLES[role][4], ior=lk.ROLES[role][5],
                              specular=lk.ROLES[role][6], note=lk.ROLES[role][7])
                   for role in lk.ROLES},
            presets=lk.THEME_PRESET),
        relations=relations, relation_topology=curve_flags, node_topology=node_flags,
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
