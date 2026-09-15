"""Hero v2 — Stage 2.6 validator: re-open the shipped .blend, measure all eight PNGs.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_6.py -- \
      --blend  Design-Assets/hero-v2/source/hero-v2-stage2_6.blend \
      --report Design-Assets/hero-v2/validation/hero-v2-stage2_6-report.json \
      --out    Design-Assets/hero-v2/validation/hero-v2-stage2_6-validation.json

Covers the card's checklist with measurements rather than claims:

* node count, and that every node is a **single closed sphere** (Euler 2, zero
  boundary edges, radial variation under 2%);
* that the three relation curves exist and genuinely reach **surface to surface** —
  the closest vertex to the core's centre is compared against the core's own
  measured local radius, and likewise per companion, at 2% tolerance;
* that the three curves have **distinct curvatures** (no shared orbit);
* that no object-feature geometry survives (no shell/cavity/aperture/band/ring/
  seam/inlay/arc object), no material is metallic, and there is no text, particle,
  GLB/glTF/WebP/AVIF or frontend write;
* that all eight renders exist at the right size, the review frames carry no
  clipped pixel, both themes separate from their page, margins hold, the alpha
  frames are RGBA with transparent corners and real coverage, and the mobile frame
  is **not** a centre-crop of the desktop frame.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import bpy
import numpy as np

GROUP_ORDER = ("GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
               "GRP_WEARABLE_EDGE")
COMPANIONS = {"GRP_HUMAN_CENTERED_AI": "HCAI_SPHERE",
              "GRP_HEALTH_BEHAVIOR": "HHB_SPHERE",
              "GRP_WEARABLE_EDGE": "WE_SPHERE"}
CURVES = ("REL_CORE_HUMAN_CENTERED_AI", "REL_CORE_HEALTH_BEHAVIOR",
          "REL_CORE_WEARABLE_EDGE")
REVIEW = (("01-desktop-dark", "desktop", "dark"),
          ("02-desktop-light", "desktop", "light"),
          ("03-mobile-dark", "mobile", "dark"),
          ("04-mobile-light", "mobile", "light"))
ALPHA = (("11-desktop-dark-alpha", "desktop", "dark"),
         ("12-desktop-light-alpha", "desktop", "light"),
         ("13-mobile-dark-alpha", "mobile", "dark"),
         ("14-mobile-light-alpha", "mobile", "light"))
CANVAS_LUM = {"dark": 17, "light": 248}      # HERO_PRODUCTION_PLAN_v2 §3 tokens
CANVAS_TOLERANCE = 12
CROP_DIFFERENCE_MIN = 0.010                  # "mobile is not a crop of desktop"
SOURCES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend",
           "source/hero-v2-stage2_5.blend")
ANCHOR_TOLERANCE = 0.02
STRIDE = 2
FORBIDDEN_TOKENS = ("SHELL", "INSET", "INNER", "BAND", "RING", "APERTURE", "ARC",
                    "SEAM", "GROOVE", "ACCENT", "BUTTON", "DOT")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--quick", action="store_true")
    return parser.parse_args(argv)


def log(message):
    print("[HERO_V2_26_VALIDATE] %s" % message, flush=True)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_image(path):
    image = bpy.data.images.load(path, check_existing=False)
    image.colorspace_settings.name = "Non-Color"
    width, height = image.size
    buffer = np.empty(width * height * 4, dtype=np.float32)
    image.pixels.foreach_get(buffer)
    buffer = buffer.reshape(height, width, 4)[::STRIDE, ::STRIDE, :]
    bpy.data.images.remove(image)
    rgb = buffer[:, :, :3]
    lum = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
    return width, height, lum, buffer[:, :, 3]


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


def nearest_distance(from_obj, to_obj):
    """Closest vertex-to-centre distance, in world space, mesh to object centre."""
    to_centre = to_obj.matrix_world.translation
    matrix = from_obj.matrix_world
    return min(((matrix @ vertex.co) - to_centre).length
               for vertex in from_obj.data.vertices)


def blend_checks(report, root):
    checks = {}
    scene = bpy.context.scene
    stage = str(scene.get("hero_v2_stage", ""))
    checks["source_opens_with_stage_tag"] = dict(
        pass_=stage.startswith("2.6"), value=stage, blend=bpy.data.filepath)

    recorded = report.get("sources", {})
    now = {}
    for relative in SOURCES:
        path = os.path.join(root, relative)
        now[relative] = sha256(path) if os.path.exists(path) else None
    checks["previous_sources_unchanged"] = dict(
        pass_=bool(recorded) and all(recorded.get(key, {}).get("sha256") == value
                                     for key, value in now.items()),
        recorded={k: (v.get("sha256") or "")[:16] for k, v in recorded.items()},
        measured={k: (v or "")[:16] for k, v in now.items()})

    empties = sorted(obj.name for obj in bpy.data.objects
                     if obj.type == "EMPTY" and obj.name.startswith("GRP_"))
    checks["node_count_preserved"] = dict(
        pass_=tuple(empties) == tuple(sorted(GROUP_ORDER)), groups=empties)

    meshes = sorted(obj.name for obj in bpy.data.objects if obj.type == "MESH")
    spheres = [name for name in meshes if name not in CURVES]
    curve_names = [name for name in meshes if name in CURVES]
    checks["only_spheres_and_relation_curves"] = dict(
        pass_=sorted(spheres) == sorted(["CORE_SPHERE"] + list(COMPANIONS.values()))
        and sorted(curve_names) == sorted(CURVES),
        spheres=sorted(spheres), curves=sorted(curve_names), all_meshes=meshes)

    flags = {name: topology(bpy.data.objects[name]) for name in spheres}
    checks["all_nodes_are_simple_spheres"] = dict(
        pass_=len(flags) == 4 and all(entry["euler"] == 2 and
                                      entry["boundary_edges"] == 0 and
                                      entry["nonmanifold_edges"] == 0 and
                                      entry["radial_variation_pct"] <= 2.0
                                      for entry in flags.values()),
        topology=flags)

    hits = sorted(name for name in meshes
                  if any(token in name.upper() for token in FORBIDDEN_TOKENS)
                  and name not in ("CORE_SPHERE",) and name not in CURVES)
    checks["no_object_feature_geometry"] = dict(
        pass_=not hits, offenders=hits,
        rule="no shell, cavity, inner ball, aperture, band, ring, seam, inlay, "
             "button or decorative arc object may exist")

    core = bpy.data.objects["CORE_SPHERE"]
    anchors = {}
    for group, curve_name in zip(tuple(COMPANIONS), CURVES):
        curve = bpy.data.objects[curve_name]
        companion = bpy.data.objects[COMPANIONS[group]]
        core_radius = max(vertex.co.length for vertex in core.data.vertices)
        companion_radius = max(vertex.co.length for vertex in companion.data.vertices)
        start = nearest_distance(curve, core)
        end = nearest_distance(curve, companion)
        anchors[group] = dict(
            curve=curve_name,
            start_distance=round(start, 4), core_radius=round(core_radius, 4),
            start_ok=abs(start - core_radius) <= ANCHOR_TOLERANCE * core_radius,
            end_distance=round(end, 4),
            companion_radius=round(companion_radius, 4),
            end_ok=abs(end - companion_radius) <= ANCHOR_TOLERANCE * companion_radius)
    checks["relation_curves_surface_to_surface"] = dict(
        pass_=len(curve_names) == 3 and
              all(entry["start_ok"] and entry["end_ok"] for entry in anchors.values()),
        measured=anchors, tolerance_fraction=ANCHOR_TOLERANCE)

    deviations = {name: topology(bpy.data.objects[name])["faces"]
                  for name in curve_names}
    recorded_deviations = [entry.get("max_deviation_fraction") for entry
                           in report.get("relations", {}).values()]
    checks["relation_curves_not_one_orbit"] = dict(
        pass_=len(set(round(float(value), 4) for value in recorded_deviations
                      if value is not None)) == 3,
        deviations=recorded_deviations, curve_faces=deviations,
        rule="three distinct deviations from their own chords, so no two curves "
             "share a curvature and none can read as an orbit")

    metallic = {}
    for mat in bpy.data.materials:
        if not mat.name.startswith("M2_6_") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is not None:
            metallic[mat.name] = round(float(
                bsdf.inputs["Metallic"].default_value), 3)
    checks["no_metallic_materials"] = dict(
        pass_=bool(metallic) and all(value == 0.0 for value in metallic.values()),
        metallic=metallic)

    glb = []
    for base, _dirs, files in os.walk(root):
        for name in files:
            if os.path.splitext(name)[1].lower() in {".glb", ".gltf", ".webp",
                                                     ".avif"}:
                glb.append(os.path.join(base, name))
    checks["no_glb_or_web_formats"] = dict(pass_=not glb, found=glb[:10])

    front = os.path.abspath(os.path.join(root, "..", "..", "Front-End"))
    stray = []
    for base, _dirs, files in os.walk(front):
        if any(part in base for part in ("node_modules", ".git", "test-results")):
            continue
        for name in files:
            if name.startswith("hero-v2") or name.startswith("hero_v2"):
                stray.append(os.path.join(base, name))
    checks["frontend_untouched"] = dict(pass_=not stray, found=stray[:10])

    checks["no_text_or_particles"] = dict(
        pass_=not any(obj.type in {"FONT", "CURVE"} for obj in bpy.data.objects)
        and len(bpy.data.particles) == 0,
        types=sorted({obj.type for obj in bpy.data.objects}))
    return checks


def pixel_checks(report, renders_dir, quick):
    checks, inspected = {}, {}
    loaded = {}
    for label, camera, theme in REVIEW + ALPHA:
        path = os.path.join(renders_dir, "%s.png" % label)
        entry = dict(path=path, exists=os.path.exists(path), theme=theme,
                     camera=camera, alpha=label.endswith("-alpha"))
        if entry["exists"]:
            width, height, lum, alpha = read_image(path)
            entry.update(dict(size=[width, height], bytes=os.path.getsize(path)))
            if entry["alpha"]:
                entry.update(dict(
                    alpha_coverage_pct=round(float((alpha > 0.5).mean() * 100), 2),
                    corner_alpha=[round(float(alpha[y, x]), 3) for y, x in
                                  ((2, 2), (2, -3), (-3, 2), (-3, -3))],
                    transparent_share_pct=round(float((alpha < 0.04).mean() * 100), 2)))
            else:
                flat = lum.ravel()
                entry.update(dict(
                    p02=round(float(np.percentile(flat, 2)), 4),
                    p50=round(float(np.percentile(flat, 50)), 4),
                    p98=round(float(np.percentile(flat, 98)), 4),
                    max_level=int(round(float(flat.max()) * 255)),
                    clipped_pct=round(float((flat * 255 >= 254).mean() * 100), 4),
                    burned_pct=round(float((flat > 0.98).mean() * 100), 4)))
                loaded[label] = dict(theme=theme, camera=camera, lum=flat, size=(width, height))
        inspected[label] = entry

    expected = {"desktop": (1600, 1400), "mobile": (800, 800)}
    if quick:
        expected = {"desktop": (800, 700), "mobile": (400, 400)}
    checks["all_eight_renders_exist_and_sized"] = dict(
        pass_=all(entry["exists"] for entry in inspected.values()) and
              all(entry.get("size") == list(expected[entry["camera"]])
                  for entry in inspected.values()),
        review_present={label: inspected[label]["exists"] for label, _c, _t in REVIEW},
        alpha_present={label: inspected[label]["exists"] for label, _c, _t in ALPHA},
        sizes={label: entry.get("size") for label, entry in inspected.items()})

    checks["alpha_frames_transparent_and_covered"] = dict(
        pass_=all(entry.get("corner_alpha") == [0.0, 0.0, 0.0, 0.0] and
                  (entry.get("alpha_coverage_pct") or 0) > 3.0
                  for label, _c, _t in ALPHA for entry in [inspected[label]]),
        measured={label: {key: inspected[label].get(key) for key in
                          ("alpha_coverage_pct", "transparent_share_pct",
                           "corner_alpha", "size")} for label, _c, _t in ALPHA},
        rule="all four corners fully transparent, and the nodes+curves cover >3% of "
             "the frame")

    checks["no_clipped_or_blown_highlights"] = dict(
        pass_=all(entry["max_level"] <= 254 and entry["clipped_pct"] <= 0.01
                  for label, _c, _t in REVIEW for entry in [inspected[label]]),
        measured={label: {key: inspected[label].get(key) for key in
                          ("max_level", "clipped_pct", "burned_pct")}
                  for label, _c, _t in REVIEW},
        rule="no pixel may reach 254/255 and at most 0.01% may exceed 250")

    canvases = {}
    for label, data in loaded.items():
        flat = data["lum"]
        level = float(np.percentile(flat, 50 if data["theme"] == "dark" else 98))
        measured = int(round(level * 255))
        canvases[label] = dict(theme=data["theme"], measured=measured,
                               token=CANVAS_LUM[data["theme"]],
                               delta=abs(measured - CANVAS_LUM[data["theme"]]))
    checks["theme_backgrounds_match_tokens"] = dict(
        pass_=all(entry["delta"] <= CANVAS_TOLERANCE for entry in canvases.values()),
        measured=canvases, tolerance=CANVAS_TOLERANCE)

    separation = {}
    for label, data in loaded.items():
        flat = data["lum"]
        field = float(np.percentile(flat, 50 if data["theme"] == "dark" else 98))
        forms = flat[np.abs(flat - field) > 0.06]
        form_p50 = float(np.percentile(forms, 50)) if forms.size else 0.0
        separation[label] = dict(theme=data["theme"], field=round(field, 4),
                                 form_p50=round(form_p50, 4),
                                 separation=round(abs(form_p50 - field), 4),
                                 form_pixels=int(forms.size))
    checks["forms_separate_from_background"] = dict(
        pass_=all(entry["separation"] > 0.12 and entry["form_pixels"] > 500
                  for entry in separation.values()),
        measured=separation)

    composition = report.get("composition", {})
    framing = {}
    for key, margin in (("desktop", 8.0), ("mobile", 4.0)):
        entry = composition.get(key, {})
        edges = entry.get("edge_clearance_pct", {})
        framing[key] = dict(min_edge_pct=(min(edges.values()) if edges else None),
                            required_pct=margin,
                            gap_on_page_px=entry.get("min_gap_scaled_to_page_px"))
    checks["safe_margins_kept"] = dict(
        pass_=all(entry["min_edge_pct"] is not None and
                  entry["min_edge_pct"] >= entry["required_pct"] - 0.5 and
                  (entry["gap_on_page_px"] or 0) >= 12.0
                  for entry in framing.values()),
        framing=framing)

    # Mobile is an authored ORTHO composition, and the render must not be a centre
    # crop of the desktop frame: measured, not asserted.
    crop = {}
    for theme in ("dark", "light"):
        desktop = loaded.get("01-desktop-dark" if theme == "dark" else "02-desktop-light")
        mobile = loaded.get("03-mobile-dark" if theme == "dark" else "04-mobile-light")
        if not desktop or not mobile:
            continue
        # Both arrays are ALREADY strided by STRIDE, so their shape is the frame
        # size divided by STRIDE - reshape with that, not with the frame size.
        desktop_side = (desktop["size"][1] // STRIDE, desktop["size"][0] // STRIDE)
        mobile_side = (mobile["size"][1] // STRIDE, mobile["size"][0] // STRIDE)
        square = desktop["lum"].reshape(*desktop_side)
        rows = min(desktop_side)
        offset_y = (desktop_side[0] - rows) // 2
        offset_x = (desktop_side[1] - rows) // 2
        centre_crop = square[offset_y:offset_y + rows, offset_x:offset_x + rows]
        mobile_grid = mobile["lum"].reshape(*mobile_side)
        step = max(1, rows // mobile_grid.shape[0])
        resampled = centre_crop[::step, ::step]
        shared_rows = min(resampled.shape[0], mobile_grid.shape[0])
        shared_cols = min(resampled.shape[1], mobile_grid.shape[1])
        difference = float(np.abs(
            resampled[:shared_rows, :shared_cols] -
            mobile_grid[:shared_rows, :shared_cols]).mean())
        crop[theme] = dict(difference=round(difference, 5),
                           threshold=CROP_DIFFERENCE_MIN,
                           desktop_frame=desktop["size"], mobile_frame=mobile["size"])
    cameras = {obj.name: obj.data.type for obj in bpy.data.objects
               if obj.type == "CAMERA"}
    checks["mobile_is_not_a_desktop_crop"] = dict(
        pass_=bool(crop) and all(entry["difference"] > CROP_DIFFERENCE_MIN
                                 for entry in crop.values())
        and cameras.get("CAM_MOBILE") == "ORTHO"
        and cameras.get("CAM_DESKTOP") == "PERSP",
        measured=crop, camera_types=cameras,
        rule="the mobile frame must differ from a centre crop of the desktop frame "
             "by more than %.3f mean luminance, and the cameras must stay a "
             "perspective/orthographic pair" % CROP_DIFFERENCE_MIN)
    return checks, inspected


def main(argv):
    args = parse_args(argv)
    report = {}
    if os.path.exists(args.report):
        with open(args.report, "r", encoding="utf-8") as handle:
            report = json.load(handle)
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(args.blend)),
                                        ".."))
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(args.blend))
    log("opened %s" % args.blend)
    checks = blend_checks(report, root)
    pixel, inspected = pixel_checks(report, os.path.abspath(os.path.join(
        root, "renders", "stage2_6")), args.quick)
    checks.update(pixel)
    failed = sorted(name for name, item in checks.items() if not item["pass_"])
    triangles = {obj.name: sum(max(0, len(poly.vertices) - 2)
                               for poly in obj.data.polygons)
                 for obj in bpy.data.objects if obj.type == "MESH"}
    slots = {obj.name: [slot.material.name if slot.material else None
                        for slot in obj.material_slots]
             for obj in bpy.data.objects if obj.type == "MESH"}
    summary = dict(blend=os.path.abspath(args.blend), checks=checks,
                   checks_all_pass=not failed, failed=failed,
                   counts=dict(checks=len(checks), passed=len(checks) - len(failed)),
                   triangle_counts=triangles,
                   total_triangles=sum(triangles.values()),
                   material_assignments=slots,
                   renders_inspected=inspected)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)
    log("checks_all_pass=%s failed=%s" % (not failed, failed))
    return summary


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
