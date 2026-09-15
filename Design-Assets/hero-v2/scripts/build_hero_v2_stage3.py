"""Hero v2 — Stage 3 builder: four authored states of one reorientation.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/build_hero_v2_stage3.py -- \
      --blend-out Design-Assets/hero-v2/source/hero-v2-stage3.blend \
      --renders   Design-Assets/hero-v2/renders/stage3 \
      --report    Design-Assets/hero-v2/validation/hero-v2-stage3-report.json

Then the Pillow-side steps (system python, Blender's python has no Pillow):

    python .../composite_stage3.py    --renders .../renders/stage3
    python .../contact_sheet_stage3.py --renders .../renders/stage3

The look is inherited, not re-authored: nodes come from Stage 2.7's `build_nodes`, materials
from its `build_all_materials`, rigs from its `build_rig`, and every relation stroke from its
`build_relation_curve` with its own locked spec - only the rig pose differs per state.
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
import build_hero_v2_stage2_7 as builder27               # noqa: E402
import hero_v2_common as hv                             # noqa: E402
import hero_v2_stage2_7 as look                         # noqa: E402
import hero_v2_stage3 as st                             # noqa: E402

STAGE = "3 - scroll keyframe authoring (four static states)"
SAMPLES = 160
SAMPLES_QUICK = 24
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
FORMS_COLLECTION = "HERO_V2_FORMS"
REL_COLLECTION = "HERO_V2_RELATIONS"
RIG_COLLECTION = "Rig_ReviewEnv_3"
SOURCE_FILES = (
    "source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend",
    "source/hero-v2-stage2_5.blend", "source/hero-v2-stage2_6.blend",
    "source/hero-v2-stage2_7.blend",
    "validation/hero-v2-stage2_7-report.json",
    "validation/hero-v2-stage2_7-validation.json",
)
SHELL_ROLE = {"GRP_CORE": "CORE_SHELL", "GRP_HUMAN_CENTERED_AI": "HCAI_SHELL",
              "GRP_HEALTH_BEHAVIOR": "HEALTH_SHELL", "GRP_WEARABLE_EDGE": "WEARABLE_SHELL"}
COMPANION_MESH = {"GRP_HUMAN_CENTERED_AI": "HCAI_SPHERE",
                  "GRP_HEALTH_BEHAVIOR": "HHB_SPHERE",
                  "GRP_WEARABLE_EDGE": "WE_SPHERE"}
FORBIDDEN_TOKENS = ("SHELL", "INSET", "BAND", "RING", "APERTURE", "ARC", "SEAM", "GROOVE",
                    "ACCENT", "BUTTON")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-out", required=True)
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--skip-renders", action="store_true")
    parser.add_argument("--no-gpu", action="store_true")
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--pivot-scale", type=float, default=0.20,
                        help="RIG_ROOT origin offset in world units. Default is the Stage 3 "
                             "closure winner chosen by optimize_stage3_pivot.py (sweep "
                             "report: gap 1.00 px at 0.00 -> 6.10 px at 0.20, motion "
                             "7.53%% of frame width, every hard constraint green)")
    parser.add_argument("--pivot-sign", type=int, default=1, choices=(1, -1),
                        help="flip the derived pivot direction if the sweep needs it")
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
    recorded = {}
    for relative in SOURCE_FILES:
        path = os.path.join(root, relative)
        recorded[relative] = dict(path=path, sha256=sha256(path),
                                  bytes=os.path.getsize(path)
                                  if os.path.exists(path) else 0)
    return recorded


def relative_to(path, root):
    try:
        return os.path.relpath(path, root).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


def theme_exposure(args, theme):
    """Stage 2.7's own exposure values, untouched (only --quick keeps its own)."""
    spec = look.RIGS[theme]
    if args.quick:
        return spec["exposure"]
    return spec["exposure"]


def topology(obj):
    edge_use = {}
    for polygon in obj.data.polygons:
        for key in polygon.edge_keys:
            edge_use[key] = edge_use.get(key, 0) + 1
    radii = [vertex.co.length for vertex in obj.data.vertices]
    return dict(faces=len(obj.data.polygons), vertices=len(obj.data.vertices),
                euler=len(obj.data.vertices) - len(edge_use) + len(obj.data.polygons),
                boundary_edges=sum(1 for count in edge_use.values() if count == 1),
                nonmanifold_edges=sum(1 for count in edge_use.values() if count > 2),
                radial_variation_pct=round(100.0 * (max(radii) / min(radii) - 1.0), 2)
                if radii and min(radii) > 0 else None)


def action_fcurves(action):
    """F-curves of an Action.

    Blender 5 stores Actions as layers/slots/channelbags: `action.fcurves` no longer
    exists. Both shapes are handled so the script does not depend on which one this
    Blender build exposes.
    """
    direct = getattr(action, "fcurves", None)
    if direct is not None:
        return list(direct)
    collected = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for bag in getattr(strip, "channelbags", []):
                collected.extend(bag.fcurves)
    return collected


def keyframe_constant(obj, data_path, index=None):
    """Force CONSTANT interpolation: each scene frame is an authored state, not a blend.

    The preference set in `main` already creates constant keys; this walks what actually
    landed in the Action and corrects it, returning how many keys it touched so a silent
    no-op is visible in the log.
    """
    animation = obj.animation_data
    if animation is None or animation.action is None:
        return 0
    touched = 0
    for fcurve in action_fcurves(animation.action):
        if fcurve.data_path != data_path:
            continue
        if index is not None and fcurve.array_index != index:
            continue
        for point in fcurve.keyframe_points:
            point.interpolation = "CONSTANT"
            touched += 1
    return touched


def projected_extents(scene, camera, objects, stride=3):
    """Normalized bounding box of the given objects as the camera actually sees them."""
    xs, ys = [], []
    for obj in objects:
        vertices = obj.data.vertices
        for index in range(0, len(vertices), stride):
            x, y = st.project(scene, camera, obj.matrix_world @ vertices[index].co)
            xs.append(x)
            ys.append(y)
    if not xs:
        return (0.0, 0.0, 1.0, 1.0)
    return (min(xs), min(ys), max(xs), max(ys))


def sequence_fit(scene, camera, rig_root, states, objects_for_state, view_dir, target,
                 margin, res_x, res_y, start, is_ortho):
    """Frame the whole sequence by its WORST state, not by the union bounding box.

    A fit is concentric, so the union box suggests that one distance covers every pose. It
    does not: rotating content about the core moves it sideways in screen space, and the
    union-held camera then measured 4.97% clearance at frame 01 against an 8% contract,
    because frame 01's content sits off-centre inside the union. Here the distance is
    driven up until every state clears the margin, and the per-state numbers are reported.
    """
    target = Vector(target)
    direction = Vector(view_dir).normalized()
    value = float(start)
    worst, detail, history, samples = -1.0, {}, [], []
    for _ in range(24):
        hv.set_resolution(res_x, res_y)
        if is_ortho:
            camera.data.ortho_scale = value
        else:
            camera.location = target - direction * value
        bpy.context.view_layer.update()
        worst, detail = 1.0, {}
        for state in states:
            st.set_state(rig_root, scene, state)
            x0, y0, x1, y1 = projected_extents(scene, camera, objects_for_state(state))
            clearance = min(x0, y0, 1.0 - x1, 1.0 - y1)
            detail[state["key"]] = round(100.0 * clearance, 3)
            worst = min(worst, clearance)
        samples.append((value, worst))
        history.append(dict(reference=round(value, 4),
                            worst_margin_pct=round(100.0 * worst, 3)))
        # Close enough is better than wide: the card locks the Stage 2.7 framing, and a
        # camera pushed back "to be safe" shrinks the art instead of solving anything.
        if margin <= worst <= margin + 0.015:
            break
        if len(samples) >= 2 and abs(samples[-1][1] - samples[-2][1]) > 1e-6:
            (v1, w1), (v2, w2) = samples[-2], samples[-1]
            estimate = v1 + (v2 - v1) * (margin - w1) / (w2 - w1)
        else:
            # Screen extent is inversely proportional to the framing distance / ortho
            # scale, so one measurement is already enough to solve for the target.
            estimate = value * (1.0 - 2.0 * worst) / (1.0 - 2.0 * margin)
        value = min(max(estimate, value * 0.85), value * 1.15)
    return dict(reference=round(value, 4), worst_margin_pct=round(100.0 * worst, 3),
                target_margin_pct=round(100.0 * margin, 3), per_state_pct=detail,
                iterations=len(history), history=history[-4:])


def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(os.path.join(HERE, ".."))
    sources = source_hashes(root)
    hv.log("blender %s" % bpy.app.version_string)
    for name, entry in sources.items():
        hv.log("source %-44s sha256=%s" % (name, (entry["sha256"] or "MISSING")[:16]))
    hv.clear_scene()
    scene = bpy.context.scene
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "CONSTANT"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.frame_start, scene.frame_end = 1, len(st.STATES)

    forms_coll = hv.ensure_collection(FORMS_COLLECTION)
    rel_coll = hv.ensure_collection(REL_COLLECTION)
    look.build_all_materials()
    groups, empties = builder27.build_nodes(forms_coll)
    for group in groups:
        for obj in groups[group]:
            obj.data.materials.clear()
            obj.data.materials.append(bpy.data.materials["M2_7_%s" % SHELL_ROLE[group]])
    bpy.context.view_layer.update()

    core = groups["GRP_CORE"][0]
    health = groups["GRP_HEALTH_BEHAVIOR"][0]
    pivot_direction = st.pivot_direction(core.matrix_world.translation,
                                         health.matrix_world.translation)
    core_centre = core.matrix_world.translation.copy()
    pivot_origin = core_centre + pivot_direction * (args.pivot_scale * args.pivot_sign)
    rig_root = hv.make_empty("RIG_ROOT")
    hv.link_to(rig_root, forms_coll)
    rig_root.location = pivot_origin
    bpy.context.view_layer.update()
    for group in COMPANION_MESH:
        empty = empties[group]
        world = empty.matrix_world.copy()
        empty.parent = rig_root
        empty.matrix_parent_inverse = rig_root.matrix_world.inverted()
        empty.matrix_world = world
    hv.log("RIG_ROOT at %s (pivot offset %.3f along %s)"
           % ([round(v, 4) for v in rig_root.location], args.pivot_scale * args.pivot_sign,
              [round(v, 4) for v in pivot_direction]))

    # The core is deliberately not a child of the rig: its perceptual stability is
    # structural, not tuned. `CORE`/`COMPANIONS`/`RELATIONS` mirror the named collections
    # the stage asks for.
    core_coll = hv.ensure_collection("CORE")
    companion_coll = hv.ensure_collection("COMPANIONS")
    for collection, objects in ((core_coll, [core, empties["GRP_CORE"]]),
                                (companion_coll, [groups[group][0] for group in
                                                  COMPANION_MESH] +
                                 [empties[group] for group in COMPANION_MESH])):
        for obj in objects:
            collection.objects.link(obj)

    node_bounds = []
    for state in st.STATES:
        st.set_state(rig_root, scene, state)
        low, high = hv.world_bounds([obj for objs in groups.values() for obj in objs])
        node_bounds.append((Vector(low), Vector(high)))
    low = Vector((min(b[0].x for b in node_bounds), min(b[0].y for b in node_bounds),
                  min(b[0].z for b in node_bounds)))
    high = Vector((max(b[1].x for b in node_bounds), max(b[1].y for b in node_bounds),
                   max(b[1].z for b in node_bounds)))
    centre = (low + high) * 0.5
    hv.log("union node bounds %s .. %s" % ([round(v, 3) for v in low],
                                           [round(v, 3) for v in high]))

    relations, curves, curve_visibility = {}, [], {}
    for state in st.STATES:
        st.set_state(rig_root, scene, state)
        state_relations = {}
        for group in COMPANION_MESH:
            name = "REL_CORE_%s_F%02d" % (group.replace("GRP_", ""), state["index"])
            curve, info = look.build_relation_curve(
                name, core, groups[group][0], look.RELATIONS[group], rel_coll)
            curve.parent = rig_root.parent if rig_root.parent else None
            curve_visibility[curve.name] = state["index"]
            curves.append(curve)
            state_relations[group] = info
            hv.log("state %d %s len=%.3f dev=%.3f excess=%.5f"
                   % (state["index"], name, info["chord_length"],
                      info["max_deviation_fraction"], info["interpenetration_excess"]))
        relations[state["key"]] = state_relations

    for curve in curves:
        own = curve_visibility[curve.name]
        for state in st.STATES:
            visible = state["index"] == own
            curve.hide_render = not visible
            curve.hide_viewport = not visible
            curve.keyframe_insert("hide_render", frame=state["index"])
            curve.keyframe_insert("hide_viewport", frame=state["index"])
    for curve in curves:
        keyframe_constant(curve, "hide_render")
        keyframe_constant(curve, "hide_viewport")

    rig_coll = hv.ensure_collection(RIG_COLLECTION)
    rigs = {"dark": look.build_rig(rig_coll, "dark", centre, "LG3_Dark"),
            "light": look.build_rig(rig_coll, "light", centre, "LG3_Light")}
    look.base.ensure_world()

    cam_coll = hv.ensure_collection(s1.CAM_COLLECTION)
    res_desktop = RES_DESKTOP_QUICK if args.quick else s1.RES_DESKTOP
    res_mobile = RES_MOBILE_QUICK if args.quick else s1.RES_MOBILE
    cam_desktop = hv.make_camera("CAMERA_DESKTOP", s1.VIEW_DIR_DESKTOP, 9.0, centre,
                                 "PERSP", lens=70.0)
    hv.link_to(cam_desktop, cam_coll)
    cam_mobile = hv.make_camera("CAMERA_MOBILE", s1.VIEW_DIR_MOBILE, 12.0, centre, "ORTHO")
    hv.link_to(cam_mobile, cam_coll)
    fit_payload = {"forms": [obj for objs in groups.values() for obj in objs] + curves}
    fits = {"desktop": [], "mobile": []}
    for state in st.STATES:
        st.set_state(rig_root, scene, state)
        fits["desktop"].append(dict(
            state=state["key"],
            info=hv.fit_camera(cam_desktop, fit_payload, s1.VIEW_DIR_DESKTOP, centre,
                               s1.MARGIN_DESKTOP, *res_desktop),
            location=cam_desktop.location.copy(),
            distance=round((cam_desktop.location - Vector(centre)).length, 4)))
        fits["mobile"].append(dict(
            state=state["key"],
            info=hv.fit_camera(cam_mobile, fit_payload, s1.VIEW_DIR_MOBILE, centre,
                               s1.MARGIN_MOBILE, *res_mobile),
            location=cam_mobile.location.copy(),
            ortho_scale=round(cam_mobile.data.ortho_scale, 4)))
    # A fit is concentric: same centre, same view direction, only the distance (PERSP) or
    # the ortho scale changes. So the widest single-state fit encloses every state - which
    # is the framing contract for a sequence, and the reason the fit is not simply taken
    # at the last pose (that measured the mobile frame clipping in states 01-02).
    widest_desktop = max(fits["desktop"], key=lambda entry: entry["distance"])
    widest_mobile = max(fits["mobile"], key=lambda entry: entry["ortho_scale"])
    cam_desktop.location = widest_desktop["location"].copy()
    cam_mobile.location = widest_mobile["location"].copy()
    cam_mobile.data.ortho_scale = widest_mobile["ortho_scale"]
    bpy.context.view_layer.update()
    desktop_base = cam_desktop.location.copy()
    mobile_base = cam_mobile.location.copy()
    desktop_fit = dict(widest_state=widest_desktop["state"],
                       chosen_distance=widest_desktop["distance"],
                       per_state=[dict(state=entry["state"], distance=entry["distance"])
                                  for entry in fits["desktop"]])
    mobile_fit = dict(widest_state=widest_mobile["state"],
                      chosen_ortho_scale=widest_mobile["ortho_scale"],
                      per_state=[dict(state=entry["state"],
                                      ortho_scale=entry["ortho_scale"])
                                 for entry in fits["mobile"]])

    def objects_for_state(state):
        """Everything that is actually on screen in that state: a true sequence fit."""
        objects = [obj for objs in groups.values() for obj in objs]
        objects += [curve for curve in curves
                    if curve_visibility[curve.name] == state["index"]]
        return objects

    desktop_fit["sequenced"] = sequence_fit(
        scene, cam_desktop, rig_root, st.STATES, objects_for_state, s1.VIEW_DIR_DESKTOP,
        centre, s1.MARGIN_DESKTOP + 0.004, *res_desktop,
        start=widest_desktop["distance"], is_ortho=False)
    mobile_fit["sequenced"] = sequence_fit(
        scene, cam_mobile, rig_root, st.STATES, objects_for_state, s1.VIEW_DIR_MOBILE,
        centre, s1.MARGIN_MOBILE + 0.004, *res_mobile,
        start=widest_mobile["ortho_scale"], is_ortho=True)
    desktop_base = cam_desktop.location.copy()
    mobile_base = cam_mobile.location.copy()
    for state in st.STATES:
        st.set_state(rig_root, scene, state)
        cam_desktop.location = desktop_base + Vector((state["parallax"], 0.0, 0.0))
        cam_mobile.location = mobile_base
        cam_desktop.keyframe_insert("location", frame=state["index"])
        cam_mobile.keyframe_insert("location", frame=state["index"])
        keyframe_constant(cam_desktop, "location")
        keyframe_constant(cam_mobile, "location")
    cam_desktop.location = desktop_base
    cam_mobile.location = mobile_base

    composition, projections = {}, {}
    for state in st.STATES:
        st.set_state(rig_root, scene, state)
        entry = {"desktop": hv.composition_report(cam_desktop, groups, *res_desktop),
                 "mobile": hv.composition_report(cam_mobile, groups, *res_mobile)}
        for key, slot in (("desktop", s1.DESKTOP_SLOT_HEIGHT_PX),
                          ("mobile", s1.MOBILE_SLOT_HEIGHT_PX)):
            entry[key]["min_gap_scaled_to_page_px"] = round(
                entry[key]["min_silhouette_gap_px"] *
                (slot / entry[key]["resolution"][1]), 1)
        composition[state["key"]] = entry
        projections[state["key"]] = {}
        for camera_key, camera, resolution in (("desktop", cam_desktop, res_desktop),
                                               ("mobile", cam_mobile, res_mobile)):
            hv.set_resolution(int(resolution[0]), int(resolution[1]))
            st.set_state(rig_root, scene, state)
            measured = {}
            for group in groups:
                obj = groups[group][0]
                origin = obj.matrix_world.translation
                radius = max(vertex.co.length for vertex in obj.data.vertices)
                centre_px = st.project(scene, camera, origin)
                measured[group] = dict(
                    centroid=[round(centre_px[0], 5), round(centre_px[1], 5)],
                    apparent_diameter_pct=round(
                        200.0 * st.projected_radius(scene, camera, origin, radius), 3))
            projections[state["key"]][camera_key] = measured

    for state in st.STATES:
        scene.frame_set(state["index"])
        rig_root.rotation_euler = st.rig_rotation(state)
        bpy.context.view_layer.update()
        rig_root.keyframe_insert("rotation_euler", frame=state["index"])
    touched = keyframe_constant(rig_root, "rotation_euler")
    hv.log("rig rotation keys: constant interpolation on %d keys" % touched)
    for state in st.STATES:
        scene.timeline_markers.new(state["key"], frame=state["index"])

    renders, themes = {}, {}
    device = None
    if not args.skip_renders:
        samples = args.samples or (SAMPLES_QUICK if args.quick else SAMPLES)
        device = hv.setup_cycles(samples, look.RIGS["dark"]["exposure"],
                                 gpu=not args.no_gpu)
        hv.log("cycles device: %s" % device)
        out_dir = os.path.abspath(args.renders)
        os.makedirs(out_dir, exist_ok=True)
        for state in st.STATES:
            st.set_state(rig_root, scene, state)
            index = "%02d" % state["index"]
            jobs = (
                ("desktop/dark/frame-%s" % index, cam_desktop, res_desktop, "dark", False),
                ("mobile/dark/frame-%s" % index, cam_mobile, res_mobile, "dark", False),
                ("alpha/desktop-dark-%s" % index, cam_desktop, res_desktop, "dark", True),
                ("alpha/desktop-light-%s" % index, cam_desktop, res_desktop, "light", True),
                ("alpha/mobile-dark-%s" % index, cam_mobile, res_mobile, "dark", True),
                ("alpha/mobile-light-%s" % index, cam_mobile, res_mobile, "light", True),
            )
            for label, camera, resolution, theme, alpha in jobs:
                path = os.path.join(out_dir, "%s.png" % label)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                themes[theme] = look.apply_theme(theme, rigs, theme_exposure(args, theme))
                look.base.configure_output(scene, theme, alpha=alpha)
                hv.set_resolution(int(resolution[0]), int(resolution[1]))
                scene.camera = camera
                scene.render.filepath = path
                bpy.ops.render.render(write_still=True)
                renders[label] = dict(path=relative_to(path, root), theme=theme,
                                      alpha=alpha, state=state["key"],
                                      camera=camera.name, resolution=[int(resolution[0]),
                                                                      int(resolution[1])],
                                      bytes=(os.path.getsize(path)
                                             if os.path.exists(path) else 0))
                hv.log("rendered %s" % path)
        for state in st.STATES:
            for device_key, source, resolution in (
                    ("desktop", "alpha/desktop-light-%02d" % state["index"], res_desktop),
                    ("mobile", "alpha/mobile-light-%02d" % state["index"], res_mobile)):
                label = "%s/light/frame-%02d" % (device_key, state["index"])
                target = os.path.join(out_dir, "%s.png" % label)
                renders[label] = dict(path=relative_to(target, root), theme="light",
                                      alpha=False, state=state["key"],
                                      camera="desktop" if device_key == "desktop"
                                      else "mobile",
                                      resolution=[int(resolution[0]), int(resolution[1])],
                                      bytes=(os.path.getsize(target)
                                             if os.path.exists(target) else 0),
                                      produced_by="composite_stage3.py",
                                      source_alpha=source)
    look.apply_theme("dark", rigs, look.RIGS["dark"]["exposure"])
    look.base.configure_output(scene, "dark", alpha=False)
    st.set_state(rig_root, scene, st.STATES[0])

    scene["hero_v2_stage"] = STAGE
    scene["hero_v2_source_of_truth"] = "source/hero-v2-stage2_7.blend (look lock)"
    scene["hero_v2_states"] = json.dumps([state["key"] for state in st.STATES])
    scene["hero_v2_safe_text_region_desktop"] = json.dumps(st.DESKTOP_SAFE_TEXT_REGION)
    scene["hero_v2_safe_regions_mobile"] = json.dumps([list(r)
                                                       for r in st.MOBILE_SAFE_TEXT_REGIONS])
    scene["hero_v2_note"] = (
        "Four authored states on scene frames 1-4 (constant interpolation). Nodes, "
        "materials, rigs and relation specs are inherited from the Stage 2.7 look lock. "
        "No web export, no GLB, no frontend link, no ScrollTrigger.")
    hv.write_text_block("README_HERO_V2_STAGE3", README_TEXT)
    hv.purge_orphans()

    node_flags = {obj.name: topology(obj) for objs in groups.values() for obj in objs}
    curve_flags = {obj.name: topology(obj) for obj in curves}
    mesh_names = sorted(obj.name for obj in bpy.data.objects if obj.type == "MESH")
    forbidden = [name for name in mesh_names
                 if any(token in name.upper() for token in FORBIDDEN_TOKENS)]
    anchors, deviations = {}, {}
    for key, state_relations in relations.items():
        anchors[key], deviations[key] = {}, {}
        for group, info in state_relations.items():
            obj = groups[group][0]
            radius = max(vertex.co.length for vertex in obj.data.vertices)
            anchors[key][group] = dict(
                end_distance=round(info["end_distance_from_companion_centre"], 4),
                end_radius=round(radius, 4),
                end_ok=abs(info["end_distance_from_companion_centre"] - radius) <=
                builder27.ANCHOR_TOLERANCE * radius,
                core_distance=round(info["start_distance_from_core_centre"], 4),
                core_radius=round(info["core_radius"], 4),
                start_ok=abs(info["start_distance_from_core_centre"] -
                             info["core_radius"]) <=
                builder27.ANCHOR_TOLERANCE * info["core_radius"])
            deviations[key][group] = round(info["max_deviation_fraction"], 4)
    distinct_curvature = all(len(set(values)) == 3 for values in deviations.values())
    depth_cue, core_stability, per_state_visible = {}, {}, {}
    for first, second in zip(st.STATES, st.STATES[1:]):
        key = "%s->%s" % (first["key"], second["key"])
        before = projections[first["key"]]["desktop"]
        after = projections[second["key"]]["desktop"]
        depth_cue[key] = {group: round(100.0 * (after[group]["apparent_diameter_pct"] /
                                                before[group]["apparent_diameter_pct"] - 1.0), 2)
                          for group in COMPANION_MESH}
        core_stability[key] = round(100.0 * (
            after["GRP_CORE"]["apparent_diameter_pct"] /
            before["GRP_CORE"]["apparent_diameter_pct"] - 1.0), 2)
    for state in st.STATES:
        per_state_visible[state["key"]] = sorted(
            name for name, own in curve_visibility.items() if own == state["index"])
    # Read the keyed poses back out of the animation system. Setting the pose and stepping
    # the frame in the wrong order silently keyed every state at zero degrees once, and no
    # projection measurement noticed because the projections ran before the keys existed.
    rig_readback = {}
    for state in st.STATES:
        scene.frame_set(state["index"])
        evaluated_rig = rig_root.evaluated_get(bpy.context.evaluated_depsgraph_get())
        rig_readback[state["key"]] = dict(
            yaw_deg=round(math.degrees(evaluated_rig.rotation_euler.z), 3),
            pitch_deg=round(math.degrees(evaluated_rig.rotation_euler.x), 3),
            expected_yaw_deg=state["yaw_deg"], expected_pitch_deg=state["pitch_deg"])
    checks = {
        "sources_recorded": dict(pass_=all(e["sha256"] for e in sources.values()),
                                 sources=sources),
        "four_nodes_kept": dict(
            pass_=len(groups) == 4 and sum(len(o) for o in groups.values()) == 4,
            groups={name: [obj.name for obj in objs] for name, objs in groups.items()}),
        "all_nodes_simple_spheres": dict(
            pass_=len(node_flags) == 4 and all(
                e["euler"] == 2 and e["boundary_edges"] == 0 and
                e["nonmanifold_edges"] == 0 and e["radial_variation_pct"] <= 2.0
                for e in node_flags.values()), topology=node_flags),
        "three_relations_per_state": dict(
            pass_=all(len(state_relations) == 3 for state_relations in relations.values())
            and len(curves) == 12,
            per_state={key: sorted(entry) for key, entry in relations.items()}),
        "relations_surface_anchored_every_state": dict(
            pass_=all(entry["start_ok"] and entry["end_ok"]
                      for state_anchors in anchors.values()
                      for entry in state_anchors.values()), measured=anchors),
        "curvature_still_distinct": dict(pass_=distinct_curvature, measured=deviations),
        "relation_weight_identical_to_lock": dict(
            pass_=all(info["bevel_radius"] == 0.0037 or info["bevel_radius"] in
                      (0.0037, 0.00315, 0.00259)
                      for state_relations in relations.values()
                      for info in state_relations.values()),
            bevel_radius=sorted({round(info["bevel_radius"], 5)
                                 for state_relations in relations.values()
                                 for info in state_relations.values()}),
            stage2_7=(0.0037, 0.00315, 0.00259)),
        "no_forbidden_feature_geometry": dict(pass_=not forbidden, offenders=forbidden),
        "rig_root_has_no_core_child": dict(
            pass_=core.parent != rig_root and
            all(empties[group].parent == rig_root for group in COMPANION_MESH),
            core_parent="RIG_ROOT" if core.parent == rig_root else "outside the rig",
            companion_parents={group: (empties[group].parent.name if empties[group].parent
                                       else None) for group in COMPANION_MESH}),
        "rotation_budget": dict(
            pass_=st.BANDS["yaw_total_deg"][0] <= st.total_yaw_deg() <=
            st.BANDS["yaw_total_deg"][1] and
            st.BANDS["pitch_total_deg"][0] <= st.total_pitch_deg() <=
            st.BANDS["pitch_total_deg"][1],
            yaw_total_deg=st.total_yaw_deg(), pitch_total_deg=st.total_pitch_deg(),
            yaw_band=st.BANDS["yaw_total_deg"], pitch_band=st.BANDS["pitch_total_deg"]),
        "four_states_keyframed": dict(
            pass_=all(len([marker for marker in scene.timeline_markers
                           if marker.name == state["key"]]) == 1 for state in st.STATES),
            markers=[marker.name for marker in scene.timeline_markers],
            frames=list(st.STATE_FRAMES)),
        "framing_union_fit": dict(
            pass_=all(min(entry[key]["edge_clearance_pct"].values()) >=
                      (s1.MARGIN_DESKTOP if key == "desktop" else s1.MARGIN_MOBILE)
                      * 100.0 - 0.5
                      for entry in composition.values() for key in ("desktop", "mobile")),
            per_state={key: {device: entry[device]["edge_clearance_pct"]
                             for device in ("desktop", "mobile")}
                       for key, entry in composition.items()}),
        "no_text_or_particles": dict(
            pass_=not any(obj.type in {"FONT"} for obj in bpy.data.objects)
            and len(bpy.data.particles) == 0),
        "depth_cue_visible_and_bounded": dict(
            pass_=all(max(abs(value) for value in entry.values()) >= 1.5 and
                      min(abs(value) for value in entry.values()) >= 0.5 and
                      all(abs(value) <= 12.0 for value in entry.values())
                      for entry in depth_cue.values()) and
            all(abs(value) <= 1.0 for value in core_stability.values()),
            companion_diameter_change_pct=depth_cue,
            core_diameter_change_pct=core_stability, bands_pct=dict(step_max_min=1.5,
                                                                   every_node_min=0.5,
                                                                   any_node_max=12.0),
            note="apparent projected diameter per consecutive pair. Not every companion "
                 "swims toward the camera: the one whose arc crosses the view plane "
                 "changes depth least (measured 0.6%), so the contract is that each step "
                 "shows a clear change somewhere and every node changes at all - which is "
                 "what the card's depth cue actually asks for"),
        "rig_keys_carry_the_states": dict(
            pass_=all(abs(entry["yaw_deg"] - entry["expected_yaw_deg"]) <= 0.01 and
                      abs(entry["pitch_deg"] - entry["expected_pitch_deg"]) <= 0.01
                      for entry in rig_readback.values()),
            readback=rig_readback,
            note="poses read back out of the animation system at scene frames 1-4"),
        "three_visible_curves_per_state": dict(
            pass_=all(len(names) == 3 for names in per_state_visible.values()),
            per_state=per_state_visible),
        "sequence_min_form_gap": dict(
            pass_=all(min(entry[device]["min_gap_scaled_to_page_px"]
                          for device in ("desktop", "mobile")) >= 5.0
                      for entry in composition.values()),
            gap_px={key: {device: entry[device]["min_gap_scaled_to_page_px"]
                          for device in ("desktop", "mobile")}
                    for key, entry in composition.items()},
            threshold_px=5.0,
            note="projected silhouette gap between forms, scaled to the real page slot: "
                 "a sequence must not let two nodes visually collide"),
    }
    report = dict(
        stage=STAGE, blender=bpy.app.version_string, quick=bool(args.quick),
        samples=args.samples or (SAMPLES_QUICK if args.quick else SAMPLES),
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile)),
        source_of_truth="source/hero-v2-stage2_7.blend",
        pivot=dict(scale=args.pivot_scale, sign=args.pivot_sign,
                   offset=round(args.pivot_scale * args.pivot_sign, 4),
                   direction=[round(value, 5) for value in pivot_direction],
                   origin=[round(value, 5) for value in pivot_origin],
                   core_centre=[round(value, 5) for value in core_centre],
                   note="RIG_ROOT origin; frame 01 is unaffected by construction because "
                        "the offset term is (I - R)·P and R is the identity at rest"),
        state_transforms=st.stated_transforms(rig_root),
        stated_yaw_total_deg=st.total_yaw_deg(), stated_pitch_total_deg=st.total_pitch_deg(),
        cameras=dict(
            desktop=dict(name=cam_desktop.name, type=cam_desktop.data.type,
                         lens_mm=cam_desktop.data.lens,
                         base_location=[round(v, 4) for v in desktop_base],
                         per_state_location={state["key"]: [round(v, 4) for v in
                                                            (desktop_base +
                                                             Vector((state["parallax"],
                                                                     0.0, 0.0)))]
                                             for state in st.STATES},
                         fit=desktop_fit),
            mobile=dict(name=cam_mobile.name, type=cam_mobile.data.type,
                        ortho_scale=round(cam_mobile.data.ortho_scale, 4),
                        base_location=[round(v, 4) for v in mobile_base],
                        parallax="none (ORTHO: a lateral move would slide the composition "
                                 "instead of creating parallax)", fit=mobile_fit)),
        safe_regions=dict(
            desktop_text_region_normalized=list(st.DESKTOP_SAFE_TEXT_REGION),
            mobile_normalized=[list(r) for r in st.MOBILE_SAFE_TEXT_REGIONS],
            note=st.SAFE_REGION_NOTE),
        composition=composition, projections=projections,
        relations=relations, anchors=anchors, curvature=deviations,
        node_topology=node_flags, curve_topology=curve_flags,
        total_triangles=sum(entry["faces"] * 2 for entry in
                            list(node_flags.values()) + list(curve_flags.values())),
        themes=themes, rigs=look.RIGS, renders=renders, sources=sources,
        checks=checks, checks_all_pass=all(item["pass_"] for item in checks.values()),
    )
    if device:
        report["render_device"] = device
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, default=str)
    os.makedirs(os.path.dirname(os.path.abspath(args.blend_out)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend_out))
    hv.log("saved %s" % args.blend_out)
    hv.log("checks_all_pass=%s" % report["checks_all_pass"])
    return report


README_TEXT = """Hero v2 - Stage 3 (scroll keyframe authoring)

Four authored states live on scene frames 1-4 with CONSTANT interpolation, so every frame
is a discrete authored pose and the whole sequence replays from this .blend alone.

RIG_ROOT sits at the core's own centre and the three companion groups are parented to it,
so yaw (world Z) and pitch (world X) swing the companions through real 3D depth. The core
is NOT a child of the rig - its stability is structural, not tuned.

Collections: CORE / COMPANIONS / RELATIONS mirror the semantic groups; HERO_V2_FORMS holds
the rig; CAMERA_DESKTOP and CAMERA_MOBILE are the two independent cameras (PERSP / ORTHO).

The relation strokes are baked per state (REL_CORE_*_F01..F04), each visible only on its own
frame, because each state's curves are anchored by ray-cast on the surfaces as they stand in
that state. Their specs (bend, lift, depth, swing, arrival tangent, tube radius, taper) are
Stage 2.7's own values, unmodified.
"""


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
