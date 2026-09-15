"""Hero v2 — Stage 3 validator: continuity and framing, measured after the fact.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage3.py -- \
      --blend  Design-Assets/hero-v2/source/hero-v2-stage3.blend \
      --report Design-Assets/hero-v2/validation/hero-v2-stage3-report.json \
      --out    Design-Assets/hero-v2/validation/hero-v2-stage3-validation.json

Implements the card's continuity tests A-I from two deliberately different sources:

* the **saved .blend**, stepped through scene frames 1-4 with `scene.frame_set`, which proves
  the keyframes really carry the four states and lets the motion be measured analytically;
* the **rendered pixels** (16 alpha masters, 16 review frames), which catches what projection
  maths can be wrong about: clipping, safe-region invasion, and how much silhouette actually
  moved between consecutive frames.

The silhouette metric is defined identically in `contact_sheet_stage3.py` (mean absolute alpha
difference and IoU at alpha >= 0.5); neither file imports the other's implementation, so a
shared bug cannot hide in both.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import hero_v2_stage3 as st                                     # noqa: E402
from build_hero_v2_stage3 import action_fcurves                  # noqa: E402

COMPANIONS = ("GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR", "GRP_WEARABLE_EDGE")
SUFFIX_TO_GROUP = {"HUMAN_CENTERED_AI": "GRP_HUMAN_CENTERED_AI",
                   "HEALTH_BEHAVIOR": "GRP_HEALTH_BEHAVIOR",
                   "WEARABLE_EDGE": "GRP_WEARABLE_EDGE"}
ALPHA_THRESHOLD = 0.5
LOCKED_HEX = {"CORE_SHELL": "#27565A", "HCAI_SHELL": "#6F8474", "HEALTH_SHELL": "#877156",
              "WEARABLE_SHELL": "#6B6580", "RELATION": "#C6B191"}
GROUP_ROLE = {"GRP_CORE": "CORE_SHELL", "GRP_HUMAN_CENTERED_AI": "HCAI_SHELL",
              "GRP_HEALTH_BEHAVIOR": "HEALTH_SHELL", "GRP_WEARABLE_EDGE": "WEARABLE_SHELL"}
SOURCE_FILES = ("source/hero-v2-stage2_7.blend",
                "validation/hero-v2-stage2_7-report.json",
                "validation/hero-v2-stage2_7-validation.json")
STEPS = ((1, 2), (2, 3), (3, 4))
FAR = (1, 4)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def log(message):
    print("[HERO_V2_S3_VALIDATE] %s" % message)


def sha256(path):
    if not os.path.exists(path):
        return None
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_luminance_alpha(path):
    """(width, height, luminance 0..1, alpha 0..1), top-left origin."""
    image = bpy.data.images.load(path, check_existing=False)
    width, height = int(image.size[0]), int(image.size[1])
    buffer = np.array(image.pixels[:], dtype=np.float32).reshape(height, width, 4)[::-1]
    rgb = buffer[:, :, :3]
    luminance = (rgb[:, :, 0] * 0.2126 + rgb[:, :, 1] * 0.7152 + rgb[:, :, 2] * 0.0722)
    alpha = buffer[:, :, 3]
    bpy.data.images.remove(image)
    return width, height, luminance, alpha


def silhouette_metrics(alpha_a, alpha_b):
    mask_a = alpha_a >= ALPHA_THRESHOLD
    mask_b = alpha_b >= ALPHA_THRESHOLD
    union = int(np.count_nonzero(mask_a | mask_b))
    common = int(np.count_nonzero(mask_a & mask_b))
    return dict(pixels_first=int(np.count_nonzero(mask_a)),
                pixels_second=int(np.count_nonzero(mask_b)), common=common,
                iou=round(common / float(union), 4) if union else 0.0,
                mean_absolute_alpha_delta=round(float(np.abs(alpha_a - alpha_b).mean()), 5))


def form_pixels_in(alpha, region):
    height, width = alpha.shape
    x0, y0, x1, y1 = region
    box = alpha[int(round(y0 * height)):max(1, int(round(y1 * height))),
                int(round(x0 * width)):max(1, int(round(x1 * width)))]
    return int(np.count_nonzero(box >= ALPHA_THRESHOLD))


def edge_band_form_pixels(alpha, margin):
    """Form pixels inside a border band of `margin` (fraction) - i.e. clipping."""
    height, width = alpha.shape
    rows = max(1, int(round(margin * height)))
    columns = max(1, int(round(margin * width)))
    mask = alpha >= ALPHA_THRESHOLD
    return int(np.count_nonzero(mask[:rows, :]) + np.count_nonzero(mask[-rows:, :]) +
               np.count_nonzero(mask[:, :columns]) +
               np.count_nonzero(mask[:, -columns:]))


def sphere_radius(obj):
    return max(vertex.co.length for vertex in obj.data.vertices)


def state_for_frame(index):
    """The authored state that lives on a given scene frame."""
    for state in st.STATES:
        if state["index"] == index:
            return state
    raise KeyError(index)


def sphere_of(group):
    """The mesh child of a semantic group empty (nodes are named by mesh, not by group)."""
    empty = bpy.data.objects[group]
    for child in empty.children:
        if child.type == "MESH":
            return child
    raise KeyError("no mesh child for %s" % group)


def set_resolution(scene, width, height):
    scene.render.resolution_x = int(width)
    scene.render.resolution_y = int(height)
    bpy.context.view_layer.update()


def evaluated(obj):
    return obj.evaluated_get(bpy.context.evaluated_depsgraph_get())


def structure_checks(scene):
    checks = {}
    stage = str(scene.get("hero_v2_stage", ""))
    markers = sorted(marker.name for marker in scene.timeline_markers)
    checks["states_keyframed_on_frames"] = dict(
        pass_=stage.startswith("3") and scene.frame_start == 1 and
        scene.frame_end == 4 and
        markers == sorted(state["key"] for state in st.STATES),
        stage=stage, frame_range=[int(scene.frame_start), int(scene.frame_end)],
        markers=markers)

    rig = bpy.data.objects.get("RIG_ROOT")
    parents = {}
    for group in COMPANIONS:
        empty = bpy.data.objects.get(group)
        parents[group] = empty.parent.name if empty and empty.parent else None
    core_empty = bpy.data.objects.get("GRP_CORE")
    checks["rig_root_parents_companions_only"] = dict(
        pass_=rig is not None and all(value == "RIG_ROOT" for value in parents.values())
        and (core_empty.parent.name if core_empty.parent else None) != "RIG_ROOT",
        rig=[round(value, 4) for value in rig.location] if rig else None,
        companion_parents=parents,
        core_parent=(core_empty.parent.name if core_empty and core_empty.parent else None),
        note="the core stays outside the rig: its stability is structural, not tuned")

    curves = sorted(obj.name for obj in bpy.data.objects
                    if obj.name.startswith("REL_CORE_"))
    visible, interpolations = {}, set()
    for state in st.STATES:
        scene.frame_set(state["index"])
        visible[state["key"]] = sorted(
            obj.name for obj in bpy.data.objects if obj.name.startswith("REL_CORE_")
            and not evaluated(obj).hide_render)
        for name in curves:
            obj = bpy.data.objects[name]
            if obj.animation_data and obj.animation_data.action:
                for fcurve in action_fcurves(obj.animation_data.action):
                    for point in fcurve.keyframe_points:
                        interpolations.add(point.interpolation)
    checks["three_relations_visible_per_state"] = dict(
        pass_=len(curves) == 12 and
        all(len(names) == 3 for names in visible.values()), total_curve_objects=len(curves),
        per_state=visible)
    checks["keyframes_are_constant"] = dict(
        pass_=interpolations == {"CONSTANT"}, interpolation=sorted(interpolations),
        note="each scene frame is an authored state, not an interpolation")

    roles = {}
    for group, role in GROUP_ROLE.items():
        sphere = sphere_of(group)
        materials = [slot.material.name for slot in sphere.material_slots]
        base = bpy.data.materials.get(materials[0]) if materials else None
        colour = None
        if base and base.use_nodes:
            node = base.node_tree.nodes.get("Mix")
            if node is not None:
                colour = node.inputs[6].default_value
        roles[group] = dict(material=materials[0] if materials else None,
                            base_color_linear=[round(value, 4) for value in colour]
                            if colour else None)
    checks["material_identity_locked"] = dict(
        pass_=all(entry["material"] == "M2_7_%s" % GROUP_ROLE[group]
                  for group, entry in roles.items()),
        measured=roles, locked_hex=LOCKED_HEX,
        note="each sphere keeps its own locked material, so the semantic node identity "
             "cannot be swapped by the motion")

    anchors, injected = {}, 0
    for state in st.STATES:
        scene.frame_set(state["index"])
        anchors[state["key"]] = {}
        for name in visible[state["key"]]:
            curve = bpy.data.objects[name]
            suffix = name.replace("REL_CORE_", "").rsplit("_F", 1)[0]
            group = SUFFIX_TO_GROUP[suffix]
            sphere = sphere_of(group)
            centre = sphere.matrix_world.translation
            radius = sphere_radius(sphere)
            core = sphere_of("GRP_CORE")
            core_centre = core.matrix_world.translation
            core_radius = sphere_radius(core)
            near_companion = min(((curve.matrix_world @ vertex.co) - centre).length
                                 for vertex in curve.data.vertices)
            near_core = min(((curve.matrix_world @ vertex.co) - core_centre).length
                            for vertex in curve.data.vertices)
            anchors[state["key"]][name] = dict(
                companion_distance=round(near_companion, 4),
                companion_radius=round(radius, 4),
                companion_ok=abs(near_companion - radius) <= 0.02 * radius,
                core_distance=round(near_core, 4), core_radius=round(core_radius, 4),
                core_ok=abs(near_core - core_radius) <= 0.02 * core_radius)
    checks["relation_endpoints_anchored_every_state"] = dict(
        pass_=all(entry["core_ok"] and entry["companion_ok"]
                  for state_anchors in anchors.values()
                  for entry in state_anchors.values()),
        measured=anchors, tolerance=0.02)
    return checks, curves


def motion_checks(scene, resolutions):
    """Tests A-D: motion measured through the real cameras, per state and per device.

    The scene resolution is set per device before projecting: `world_to_camera_view` reads
    the render aspect, so projecting the mobile camera against a desktop-sized frame would
    report a mobile composition that does not exist.
    """
    cameras = {"desktop": bpy.data.objects["CAMERA_DESKTOP"],
               "mobile": bpy.data.objects["CAMERA_MOBILE"]}
    per_state = {}
    for state in st.STATES:
        scene.frame_set(state["index"])
        per_state[state["key"]] = {}
        for device, camera in cameras.items():
            width, height = resolutions[device]
            set_resolution(scene, width, height)
            scene.frame_set(state["index"])
            entry = {}
            for group in ("GRP_CORE",) + COMPANIONS:
                sphere = sphere_of(group)
                origin = sphere.matrix_world.translation
                radius = sphere_radius(sphere)
                centroid = st.project(scene, evaluated(camera), origin)
                entry[group] = dict(
                    centroid_px=[round(centroid[0] * width, 2),
                                 round(centroid[1] * height, 2)],
                    apparent_diameter_px=round(
                        st.projected_radius(scene, evaluated(camera), origin,
                                            radius) * 2.0 * width, 2))
            per_state[state["key"]][device] = entry

    core_shift, companion_shift, scale_change = {}, {}, {}
    for device in cameras:
        for first, second in STEPS + (FAR,):
            key = "%s %d->%d" % (device, first, second)
            before = per_state[state_for_frame(first)["key"]][device]
            after = per_state[state_for_frame(second)["key"]][device]
            width = float(resolutions[device][0])
            core_shift[key] = round(100.0 * float(np.hypot(
                after["GRP_CORE"]["centroid_px"][0] - before["GRP_CORE"]["centroid_px"][0],
                after["GRP_CORE"]["centroid_px"][1] - before["GRP_CORE"]["centroid_px"][1]))
                / width, 4)
            companion_shift[key] = {group: round(100.0 * float(np.hypot(
                after[group]["centroid_px"][0] - before[group]["centroid_px"][0],
                after[group]["centroid_px"][1] - before[group]["centroid_px"][1])) / width, 4)
                for group in COMPANIONS}
            scale_change[key] = {group: round(100.0 * (
                after[group]["apparent_diameter_px"] /
                before[group]["apparent_diameter_px"] - 1.0), 3)
                for group in ("GRP_CORE",) + COMPANIONS}
    bands = st.BANDS
    checks = {}
    checks["A_core_centroid_stable"] = dict(
        pass_=all(value <= bands["core_displacement_pct"][1]
                  for value in core_shift.values()),
        measured_pct_of_width=core_shift, band=bands["core_displacement_pct"],
        note="includes the authored camera parallax; the core is not parented to the rig, "
             "so this is the geometry's real stability rather than a tuned value")
    step_keys = [key for key in companion_shift
                 if key.endswith(("1->2", "2->3", "3->4"))]
    mobile_far = companion_shift["mobile 1->4"]
    mobile_movers = sorted((group for group, value in mobile_far.items()
                            if value >= bands["companion_total_min_pct"]))
    checks["B_companions_move_visibly_but_bounded"] = dict(
        pass_=
        all(max(companion_shift[key].values()) >= bands["companion_step_max_pct"]
            for key in step_keys) and
        all(value >= bands["companion_displacement_pct"][0]
            for key in step_keys if key.startswith("desktop")
            for value in companion_shift[key].values()) and
        all(value >= bands["companion_total_min_pct"]
            for value in companion_shift["desktop 1->4"].values()) and
        len(mobile_movers) >= bands["companion_mobile_min_nodes"] and
        all(value <= bands["companion_displacement_pct"][1]
            for key in step_keys for value in companion_shift[key].values()),
        measured_pct_of_width=companion_shift,
        mobile_nodes_moving=mobile_movers,
        bands_pct=dict(step_max_min=bands["companion_step_max_pct"],
                       desktop_every_step_min=bands["companion_displacement_pct"][0],
                       every_node_total_min=bands["companion_total_min_pct"],
                       mobile_min_nodes_moving=bands["companion_mobile_min_nodes"],
                       step_max=bands["companion_displacement_pct"][1]),
        note="visible but bounded, stated so that both cameras can satisfy it: every step "
             "shows a clear move somewhere; on the perspective desktop view every "
             "companion moves on every step; every companion travels across the sequence "
             "on the desktop and at least two of three do on mobile. The exception is "
             "measured rather than hidden: an ORTHO camera cannot show motion that is "
             "mostly along its view axis, and one companion's arc crosses that axis "
             "(mobile %s). The card anticipates this - mobile frames must correspond "
             "semantically, not in exact screen coordinates." % json.dumps(mobile_far))
    isolation = {}
    for state in st.STATES:
        entry = per_state[state["key"]]["desktop"]
        for index, group in enumerate(COMPANIONS):
            for other in COMPANIONS[index + 1:]:
                distance = float(np.hypot(
                    entry[group]["centroid_px"][0] - entry[other]["centroid_px"][0],
                    entry[group]["centroid_px"][1] - entry[other]["centroid_px"][1]))
                gap = distance - 0.5 * (entry[group]["apparent_diameter_px"] +
                                        entry[other]["apparent_diameter_px"])
                isolation["%s %s|%s" % (state["key"], group, other)] = round(
                    100.0 * gap / 1600.0, 3)
    checks["C_node_identity_cannot_swap"] = dict(
        pass_=all(value >= 0.5 for value in isolation.values()),
        separation_pct_of_width=isolation, threshold_pct=0.5,
        note="no two companions' projected discs come within half a percent of the frame "
             "of each other, and each keeps its own locked material, so no visual identity "
             "swap is possible")
    checks["D_no_scale_jump"] = dict(
        pass_=all(abs(value) <= bands["node_scale_change_pct"][1]
                  for key, entry in scale_change.items() if key.endswith(("1->2", "2->3",
                                                                          "3->4"))
                  for value in entry.values()) and
        all(abs(value) <= 1.0 for key, entry in scale_change.items()
            if key.endswith(("1->2", "2->3", "3->4")) for group, value in entry.items()
            if group == "GRP_CORE"),
        measured_pct=scale_change, band=bands["node_scale_change_pct"],
        note="the core's apparent size must not move at all; the companions must")
    return checks, per_state


def pixel_checks(renders, resolutions):
    checks = {}
    inventory, edge, safe, clipped = {}, {}, {}, {}
    alpha_cache = {}
    for device, (review_w, review_h) in resolutions.items():
        for theme in ("dark", "light"):
            for state in st.STATES:
                index = "%02d" % state["index"]
                alpha_path = os.path.join(renders, "alpha", "%s-%s-%s.png"
                                          % (device, theme, index))
                review_path = os.path.join(renders, device, theme,
                                           "frame-%s.png" % index)
                label = "%s-%s-%s" % (device, theme, index)
                if not os.path.exists(alpha_path):
                    inventory[label] = dict(alpha=None, review=os.path.exists(review_path))
                    continue
                width, height, luminance, alpha = read_luminance_alpha(alpha_path)
                alpha_cache[label] = alpha
                inventory[label] = dict(
                    alpha=[width, height], review=os.path.exists(review_path),
                    corner_alpha=[round(float(alpha[y, x]), 3) for y, x in
                                  ((2, 2), (2, -3), (-3, 2), (-3, -3))],
                    coverage_pct=round(100.0 * float((alpha >= ALPHA_THRESHOLD).mean()), 2))
                edge[label] = edge_band_form_pixels(alpha, bands_scale())
                if device == "desktop":
                    safe[label] = form_pixels_in(alpha, st.DESKTOP_SAFE_TEXT_REGION)
                else:
                    safe[label] = sum(form_pixels_in(alpha, region)
                                      for region in st.MOBILE_SAFE_TEXT_REGIONS)
                if os.path.exists(review_path):
                    _w, _h, review_lum, _a = read_luminance_alpha(review_path)
                    clipped[label] = dict(
                        max_level=int(round(float(review_lum.max()) * 255)),
                        pixels_at_255=int(np.count_nonzero(review_lum >= 254.0 / 255.0)))
    checks["render_inventory_complete"] = dict(
        pass_=len(inventory) == 16 and
        all(entry.get("alpha") == list(resolutions[
            "desktop" if key.startswith("desktop") else "mobile"]) and entry.get("review")
            for key, entry in inventory.items()),
        expected=16, measured=inventory)
    checks["F_safe_text_region_empty"] = dict(
        pass_=all(value == 0 for value in safe.values()), form_pixels=safe,
        desktop_region=list(st.DESKTOP_SAFE_TEXT_REGION),
        mobile_regions=[list(region) for region in st.MOBILE_SAFE_TEXT_REGIONS],
        note=st.SAFE_REGION_NOTE)
    checks["G_nothing_clipped_by_frame"] = dict(
        pass_=all(value == 0 for value in edge.values()), form_pixels_in_border=edge,
        border_fraction=bands_scale())
    checks["no_blown_highlights"] = dict(
        pass_=all(entry["max_level"] <= 253 and entry["pixels_at_255"] == 0
                  for entry in clipped.values()), measured=clipped)

    def metrics(first, second, device="desktop", theme="dark"):
        a = alpha_cache["%s-%s-%02d" % (device, theme, first)]
        b = alpha_cache["%s-%s-%02d" % (device, theme, second)]
        return silhouette_metrics(a, b)

    continuity, far = {}, {}
    for first, second in STEPS:
        continuity["%d->%d" % (first, second)] = metrics(first, second)
        continuity["%d->%d-mobile" % (first, second)] = metrics(first, second, "mobile")
    far["1->4"] = metrics(*FAR)
    far["1->4-mobile"] = metrics(*FAR, device="mobile")
    checks["H_frame_04_differs_from_01"] = dict(
        pass_=far["1->4"]["iou"] <= st.BANDS["movement_01_04_iou_max"] and
        far["1->4"]["mean_absolute_alpha_delta"] >= st.BANDS["movement_01_04_delta_min"],
        measured=far, iou_max=st.BANDS["movement_01_04_iou_max"],
        delta_min=st.BANDS["movement_01_04_delta_min"],
        note="IoU of the silhouette; lower means the two states differ more")
    steps_pass, detail = True, {}
    for key, entry in continuity.items():
        reference = far["1->4"] if key.endswith("mobile") is False else far["1->4-mobile"]
        ok = (entry["mean_absolute_alpha_delta"] < reference["mean_absolute_alpha_delta"] and
              entry["iou"] >= reference["iou"])
        detail[key] = dict(step_delta=entry["mean_absolute_alpha_delta"],
                           far_delta=reference["mean_absolute_alpha_delta"],
                           step_iou=entry["iou"], far_iou=reference["iou"], pass_=ok)
        steps_pass = steps_pass and ok
    checks["I_each_step_smaller_than_the_whole"] = dict(
        pass_=steps_pass, measured=detail,
        note="every consecutive pair must change the silhouette less than the direct "
             "frame 01 -> frame 04 jump does")
    return checks, {"inventory": inventory, "continuity": continuity, "far": far,
                    "safe": safe, "edge": edge, "clipped": clipped}


def bands_scale():
    return st.BANDS["edge_margin_pct"] / 100.0


def main(argv):
    args = parse_args(argv)
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(args.blend)), ".."))
    renders = os.path.join(root, "renders", "stage3")
    recorded = {}
    if os.path.exists(args.report):
        with open(args.report, "r", encoding="utf-8") as handle:
            recorded = json.load(handle)
    resolution = recorded.get("resolution", {"desktop": [1600, 1400], "mobile": [800, 800]})
    resolutions = {device: tuple(int(value) for value in resolution[device])
                   for device in ("desktop", "mobile")}

    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(args.blend))
    log("opened %s" % args.blend)
    scene = bpy.context.scene
    structure, curve_names = structure_checks(scene)
    motion, per_state = motion_checks(scene, resolutions)
    pixel, raw = pixel_checks(renders, resolutions)

    checks = {}
    checks.update(structure)
    checks.update(pixel)
    checks.update(motion)
    checks["stated_yaw_and_pitch_in_band"] = dict(
        pass_=st.BANDS["yaw_total_deg"][0] <= st.total_yaw_deg() <=
        st.BANDS["yaw_total_deg"][1] and
        st.BANDS["pitch_total_deg"][0] <= st.total_pitch_deg() <=
        st.BANDS["pitch_total_deg"][1],
        yaw_total_deg=st.total_yaw_deg(), pitch_total_deg=st.total_pitch_deg(),
        yaw_band=st.BANDS["yaw_total_deg"], pitch_band=st.BANDS["pitch_total_deg"])

    recorded_hashes = recorded.get("sources", {})
    hmm = {relative: sha256(os.path.join(root, relative)) for relative in SOURCE_FILES}
    checks["stage_2_7_source_untouched"] = dict(
        pass_=all(recorded_hashes.get(relative, {}).get("sha256") == value
                  for relative, value in hmm.items()),
        measured={key: (value or "")[:16] for key, value in hmm.items()},
        recorded={key: (entry.get("sha256") or "")[:16]
                  for key, entry in recorded_hashes.items() if key in SOURCE_FILES})

    reviews = recorded.get("renders", {})
    checks["all_sixteen_reviews_recorded"] = dict(
        pass_=len([key for key in reviews if not key.startswith("alpha/")]) == 16,
        review_frames=sorted(key for key in reviews if not key.startswith("alpha/")))

    stray, formats = [], []
    for base, _dirs, files in os.walk(root):
        if any(part in base for part in ("node_modules", ".git", "test-results")):
            continue
        for name in files:
            if os.path.splitext(name)[1].lower() in {".glb", ".gltf", ".webp", ".avif"}:
                formats.append(os.path.join(base, name))
    front = os.path.abspath(os.path.join(root, "..", "..", "Front-End"))
    for base, _dirs, files in os.walk(front):
        if any(part in base for part in ("node_modules", ".git", "test-results")):
            continue
        for name in files:
            if name.startswith(("hero-v2-stage3", "hero_v2_stage3", "frame-0")):
                stray.append(os.path.join(base, name))
    checks["no_web_formats_created"] = dict(pass_=not formats, found=formats[:10])
    checks["frontend_untouched"] = dict(pass_=not stray, found=stray[:10])

    sheets, diagnostic, gif = {}, {}, {}
    for device in ("desktop", "mobile"):
        for theme in ("dark", "light"):
            path = os.path.join(renders, "contact-%s-%s.png" % (device, theme))
            sheets["%s-%s" % (device, theme)] = dict(
                path=path, exists=os.path.exists(path),
                bytes=os.path.getsize(path) if os.path.exists(path) else 0)
    for prefix in ("desktop-dark", "mobile-dark"):
        path = os.path.join(renders, "contact-motion-difference-%s.png" % prefix)
        diagnostic[prefix] = dict(path=path, exists=os.path.exists(path))
    gif_path = os.path.join(root, "validation", "stage3-motion-review.gif")
    gif = dict(path=gif_path, exists=os.path.exists(gif_path),
               bytes=os.path.getsize(gif_path) if os.path.exists(gif_path) else 0)
    checks["contact_sheets_exist"] = dict(
        pass_=all(entry["exists"] for entry in sheets.values()) and
        all(entry["exists"] for entry in diagnostic.values()) and gif["exists"],
        contact_sheets=sheets, diagnostic=diagnostic, motion_review=gif)

    failed = sorted(name for name, entry in checks.items() if not entry["pass_"])
    summary = dict(blend=os.path.abspath(args.blend), checks=checks,
                   checks_all_pass=not failed, failed=failed,
                   counts=dict(checks=len(checks), passed=len(checks) - len(failed)),
                   bands=st.BANDS, states=[state["key"] for state in st.STATES],
                   projections=per_state, pixel_evidence=raw)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)
    log("checks_all_pass=%s failed=%s" % (not failed, failed))
    return summary


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
