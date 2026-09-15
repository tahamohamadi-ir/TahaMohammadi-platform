"""Hero v2 — Stage 2.7 validator: re-open the shipped .blend, measure all 12 PNGs.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_7.py -- \
      --blend  Design-Assets/hero-v2/source/hero-v2-stage2_7.blend \
      --report Design-Assets/hero-v2/validation/hero-v2-stage2_7-report.json \
      --out    Design-Assets/hero-v2/validation/hero-v2-stage2_7-validation.json

Covers the card's checklist, with the two additions this stage specifically needs:

* **the dielectric response must exist and be plausible** - metallic 0, IOR inside the
  physical range, a non-zero specular level, and a roughness inside the card's
  suggested band. Stage 2.6 shipped a physically dead zero-specular material; this
  check is what stops that from coming back;
* **the web-scale previews are validated too**, because the card asks the look to be
  judged at the real CSS footprint (686x600 desktop, 288x288 mobile) rather than only
  at 1600x1400 - and because resampling can invent values a render never had (LANCZOS
  ringing put 223 pixels at 255 in the first light preview, from a source frame with
  none).

Measurement helpers are imported from the Stage 2.6 validator so both stages agree on
what "clipped", "separation" and "topology" mean.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from validate_hero_v2_stage2_6 import (STRIDE, log, read_image, sha256,  # noqa: E402
                                       topology)

GROUPS = ("GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
          "GRP_WEARABLE_EDGE")
COMPANIONS = ("HCAI_SPHERE", "HHB_SPHERE", "WE_SPHERE")
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
WEBSCALE = (("21-desktop-dark-webscale", "desktop", "dark", (686, 600)),
            ("22-desktop-light-webscale", "desktop", "light", (686, 600)),
            ("23-mobile-dark-webscale", "mobile", "dark", (288, 288)),
            ("24-mobile-light-webscale", "mobile", "light", (288, 288)))
CANVAS_LUM = {"dark": 17, "light": 248}
CANVAS_TOLERANCE = 14
ANCHOR_TOLERANCE = 0.02
FORBIDDEN_TOKENS = ("SHELL", "INSET", "INNER", "BAND", "RING", "APERTURE", "ARC",
                    "SEAM", "GROOVE", "ACCENT", "BUTTON")
SOURCES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend",
           "source/hero-v2-stage2_5.blend", "source/hero-v2-stage2_6.blend")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def blend_checks(report, root):
    checks = {}
    scene = bpy.context.scene
    stage = str(scene.get("hero_v2_stage", ""))
    checks["source_opens_with_stage_tag"] = dict(
        pass_=stage.startswith("2.7"), value=stage, blend=bpy.data.filepath)

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
    checks["four_nodes_only"] = dict(
        pass_=tuple(empties) == tuple(sorted(GROUPS)), groups=empties)

    meshes = sorted(obj.name for obj in bpy.data.objects if obj.type == "MESH")
    spheres = [name for name in meshes if name not in CURVES]
    curves = [name for name in meshes if name in CURVES]
    checks["only_spheres_and_strokes"] = dict(
        pass_=sorted(spheres) == sorted(["CORE_SPHERE"] + list(COMPANIONS)) and
              sorted(curves) == sorted(CURVES),
        spheres=sorted(spheres), curves=sorted(curves))

    flags = {name: topology(bpy.data.objects[name]) for name in spheres}
    checks["all_nodes_simple_spheres"] = dict(
        pass_=len(flags) == 4 and all(e["euler"] == 2 and e["boundary_edges"] == 0 and
                                      e["nonmanifold_edges"] == 0 and
                                      e["radial_variation_pct"] <= 2.0
                                      for e in flags.values()), topology=flags)

    offenders = [name for name in meshes
                 if any(token in name.upper() for token in FORBIDDEN_TOKENS)]
    checks["no_forbidden_feature_geometry"] = dict(pass_=not offenders,
                                                   offenders=offenders)

    core = bpy.data.objects["CORE_SPHERE"]
    core_radius = max(vertex.co.length for vertex in core.data.vertices)
    anchors = {}
    for curve_name, companion_name in zip(CURVES, COMPANIONS):
        curve = bpy.data.objects[curve_name]
        companion = bpy.data.objects[companion_name]
        companion_radius = max(vertex.co.length for vertex in companion.data.vertices)
        to_core = min(((curve.matrix_world @ vertex.co) -
                       core.matrix_world.translation).length
                      for vertex in curve.data.vertices)
        to_companion = min(((curve.matrix_world @ vertex.co) -
                            companion.matrix_world.translation).length
                           for vertex in curve.data.vertices)
        anchors[curve_name] = dict(
            core_distance=round(to_core, 4), core_radius=round(core_radius, 4),
            core_ok=abs(to_core - core_radius) <= max(ANCHOR_TOLERANCE * core_radius,
                                                      0.006),
            companion_distance=round(to_companion, 4),
            companion_radius=round(companion_radius, 4),
            companion_ok=abs(to_companion - companion_radius) <=
            max(ANCHOR_TOLERANCE * companion_radius, 0.006))
    checks["stroke_endpoints_surface_anchored"] = dict(
        pass_=len(curves) == 3 and all(e["core_ok"] and e["companion_ok"]
                                       for e in anchors.values()),
        measured=anchors,
        note="the stroke's nearest vertex to each centre is compared against that "
             "sphere's own measured radius; the tolerance is 2% or 6 mm, whichever "
             "is larger, because the tube has thickness")

    measured = {}
    for mat in bpy.data.materials:
        if not mat.name.startswith("M2_7_") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf is None:
            continue
        specular = 0.0
        for key in ("Specular IOR Level", "Specular"):
            if key in bsdf.inputs:
                specular = float(bsdf.inputs[key].default_value)
                break
        measured[mat.name] = dict(
            metallic=round(float(bsdf.inputs["Metallic"].default_value), 3),
            ior=round(float(bsdf.inputs["IOR"].default_value), 3),
            specular=round(specular, 3),
            roughness=round(float(bsdf.inputs["Roughness"].default_value), 3))
    shells = {name: entry for name, entry in measured.items()
              if not name.endswith("RELATION")}
    checks["dielectric_response_plausible"] = dict(
        pass_=bool(shells) and all(e["metallic"] == 0.0 and 1.42 <= e["ior"] <= 1.50
                                   and e["specular"] > 0.0 and
                                   0.58 <= e["roughness"] <= 0.76
                                   for e in shells.values()),
        measured=measured,
        rule="metallic 0, IOR inside 1.42-1.50, a non-zero specular level, and "
             "roughness inside the card's 0.58-0.76 band - i.e. a broad soft "
             "dielectric sheen, not a dead material and not a hotspot")

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


def pixel_checks(renders_dir, report):
    checks, inspected, loaded = {}, {}, {}
    frames = ([(label, camera, theme) for label, camera, theme in REVIEW + ALPHA] +
              [(label, camera, theme)
               for label, camera, theme, _size in WEBSCALE])
    for label, camera, theme in frames:
        path = os.path.join(renders_dir, "%s.png" % label)
        entry = dict(path=path, exists=os.path.exists(path), theme=theme,
                     camera=camera, kind=("alpha" if label.endswith("-alpha")
                                          else "webscale" if "webscale" in label
                                          else "review"))
        if entry["exists"]:
            width, height, lum, alpha = read_image(path)
            flat = lum.ravel()
            entry.update(dict(size=[width, height], bytes=os.path.getsize(path),
                              max_level=int(round(float(flat.max()) * 255)),
                              clipped_pct=round(float((flat * 255 >= 254).mean() * 100), 4)))
            if entry["kind"] == "alpha":
                entry.update(dict(
                    alpha_coverage_pct=round(float((alpha > 0.5).mean() * 100), 2),
                    corner_alpha=[round(float(alpha[y, x]), 3) for y, x in
                                  ((2, 2), (2, -3), (-3, 2), (-3, -3))]))
            loaded[label] = dict(theme=theme, kind=entry["kind"], lum=flat,
                                 size=(width, height))
        inspected[label] = entry

    checks["all_twelve_renders_exist_and_sized"] = dict(
        pass_=all(entry["exists"] for entry in inspected.values()) and
              all(entry.get("size") == list(expected)
                  for label, _c, _t, expected in WEBSCALE
                  for entry in [inspected[label]]) and
              all(inspected[label].get("size") == expected
                  for label, _c, _t, expected in
                  (("01-desktop-dark", None, None, [1600, 1400]),
                   ("02-desktop-light", None, None, [1600, 1400]),
                   ("03-mobile-dark", None, None, [800, 800]),
                   ("04-mobile-light", None, None, [800, 800]),
                   ("11-desktop-dark-alpha", None, None, [1600, 1400]),
                   ("12-desktop-light-alpha", None, None, [1600, 1400]),
                   ("13-mobile-dark-alpha", None, None, [800, 800]),
                   ("14-mobile-light-alpha", None, None, [800, 800]))),
        review={label: inspected[label].get("size") for label, _c, _t in REVIEW},
        alpha={label: inspected[label].get("size") for label, _c, _t in ALPHA},
        webscale={label: inspected[label].get("size")
                  for label, _c, _t, _s in WEBSCALE})

    checks["no_clipping_anywhere"] = dict(
        pass_=all(entry["max_level"] <= 253 and entry["clipped_pct"] <= 0.01
                  for entry in inspected.values() if entry.get("max_level") is not None),
        measured={label: {key: entry.get(key) for key in ("max_level", "clipped_pct")}
                  for label, entry in inspected.items()},
        rule="no pixel at or above 254 in any of the twelve outputs - including the "
             "web-scale previews, where resampling could otherwise invent values")

    checks["alpha_corners_are_zero"] = dict(
        pass_=all(entry.get("corner_alpha") == [0.0, 0.0, 0.0, 0.0] and
                  (entry.get("alpha_coverage_pct") or 0) > 3.0
                  for label, _c, _t in ALPHA for entry in [inspected[label]]),
        measured={label: {key: inspected[label].get(key) for key in
                          ("alpha_coverage_pct", "corner_alpha")}
                  for label, _c, _t in ALPHA})

    canvases = {}
    for label, data in loaded.items():
        if data["kind"] != "review":
            continue
        level = float(np.percentile(data["lum"], 50 if data["theme"] == "dark" else 98))
        measured_level = int(round(level * 255))
        canvases[label] = dict(theme=data["theme"], measured=measured_level,
                               token=CANVAS_LUM[data["theme"]],
                               delta=abs(measured_level - CANVAS_LUM[data["theme"]]))
    checks["theme_backgrounds_valid"] = dict(
        pass_=all(e["delta"] <= CANVAS_TOLERANCE for e in canvases.values()),
        measured=canvases, tolerance=CANVAS_TOLERANCE)

    separation = {}
    for label, data in loaded.items():
        flat = data["lum"]
        field = float(np.percentile(flat, 50 if data["theme"] == "dark" else 98))
        forms = flat[np.abs(flat - field) > 0.06]
        form_p50 = float(np.percentile(forms, 50)) if forms.size else 0.0
        separation[label] = dict(kind=data["kind"], theme=data["theme"],
                                 separation=round(abs(form_p50 - field), 4),
                                 form_pixels=int(forms.size))
    checks["forms_separate_from_background"] = dict(
        pass_=all(e["separation"] > 0.12 and e["form_pixels"] > 300
                  for e in separation.values()), measured=separation)

    composition = report.get("composition", {})
    framing = {}
    for key, margin in (("desktop", 8.0), ("mobile", 4.0)):
        entry = composition.get(key, {})
        edges = entry.get("edge_clearance_pct", {})
        framing[key] = dict(min_edge_pct=(min(edges.values()) if edges else None),
                            required_pct=margin,
                            gap_on_page_px=entry.get("min_gap_scaled_to_page_px"))
    checks["safe_margins_kept"] = dict(
        pass_=all(e["min_edge_pct"] is not None and
                  e["min_edge_pct"] >= e["required_pct"] - 0.5 and
                  (e["gap_on_page_px"] or 0) >= 12.0 for e in framing.values()),
        framing=framing)

    cameras = {obj.name: obj.data.type for obj in bpy.data.objects
               if obj.type == "CAMERA"}
    checks["independent_cameras_kept"] = dict(
        pass_=cameras.get("CAM_MOBILE") == "ORTHO" and
              cameras.get("CAM_DESKTOP") == "PERSP", camera_types=cameras)
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
    pixel, inspected = pixel_checks(os.path.abspath(os.path.join(
        root, "renders", "stage2_7")), report)
    checks.update(pixel)
    failed = sorted(name for name, item in checks.items() if not item["pass_"])
    strokes = {}
    for name in CURVES:
        obj = bpy.data.objects.get(name)
        if obj is not None:
            strokes[name] = dict(faces=len(obj.data.polygons),
                                 vertices=len(obj.data.vertices))
    summary = dict(blend=os.path.abspath(args.blend), checks=checks,
                   checks_all_pass=not failed, failed=failed,
                   counts=dict(checks=len(checks), passed=len(checks) - len(failed)),
                   stroke_topology=strokes,
                   node_topology={name: topology(bpy.data.objects[name])
                                  for name in ("CORE_SPHERE",) + COMPANIONS},
                   renders_inspected=inspected)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)
    log("checks_all_pass=%s failed=%s" % (not failed, failed))
    return summary


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
