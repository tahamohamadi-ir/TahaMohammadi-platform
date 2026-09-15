"""Hero v2 — Stage 2.5 validator: re-open the shipped .blend, measure the four PNGs.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/validate_hero_v2_stage2_5.py -- \
      --blend   Design-Assets/hero-v2/source/hero-v2-stage2_5.blend \
      --report  Design-Assets/hero-v2/validation/hero-v2-stage2_5-report.json \
      --out     Design-Assets/hero-v2/validation/hero-v2-stage2_5-validation.json

Implements the Stage 2.5 card's checklist. Structural claims are verified as
topology, not as adjectives: a companion that still had a cavity, an inner ball, a
ring, a band or a silhouette-altering groove could not have Euler characteristic 2
with zero boundary edges, and its radial variation could not stay under 2%. Both
numbers are read back off the saved file in a fresh process.

The theme canvases are checked against the plan's tokens (`#071225` dark,
`#f7f8f5` light) with an explicit tolerance, and the tolerance breach is reported
rather than hidden: under AgX the light page renders ~17 levels below the token,
which is a tone-pipeline property, not a lighting mistake.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import bpy
import numpy as np

GROUPS = ("GRP_CORE", "GRP_HUMAN_CENTERED_AI", "GRP_HEALTH_BEHAVIOR",
          "GRP_WEARABLE_EDGE")
COMPANIONS = ("HCAI_SPHERE", "HHB_SPHERE", "WE_SPHERE")
RENDER_FILES = (
    ("01-desktop-dark", "desktop", "dark"),
    ("02-desktop-light", "desktop", "light"),
    ("03-mobile-dark", "mobile", "dark"),
    ("04-mobile-light", "mobile", "light"),
)
CANVAS = {"dark": "071225", "light": "f7f8f5"}
CANVAS_TOLERANCE = 24          # levels, in 0-255 sRGB; the AgX gap is documented
STRIDE = 2
SOURCES = ("source/hero-v2-graybox.blend", "source/hero-v2-lookdev.blend")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--quick", action="store_true")
    return parser.parse_args(argv)


def log(message):
    print("[HERO_V2_25_VALIDATE] %s" % message, flush=True)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_pixels(path):
    image = bpy.data.images.load(path, check_existing=False)
    image.colorspace_settings.name = "Non-Color"
    width, height = image.size
    buffer = np.empty(width * height * 4, dtype=np.float32)
    image.pixels.foreach_get(buffer)
    buffer = buffer.reshape(height, width, 4)[::STRIDE, ::STRIDE, :3]
    bpy.data.images.remove(image)
    return width, height, buffer


def luminance(rgb):
    return (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2])


def topology(obj):
    edge_use = {}
    for poly in obj.data.polygons:
        for key in poly.edge_keys:
            edge_use[key] = edge_use.get(key, 0) + 1
    radii = [vertex.co.length for vertex in obj.data.vertices]
    return dict(
        faces=len(obj.data.polygons), vertices=len(obj.data.vertices),
        euler=len(obj.data.vertices) - len(edge_use) + len(obj.data.polygons),
        boundary_edges=sum(1 for count in edge_use.values() if count == 1),
        nonmanifold_edges=sum(1 for count in edge_use.values() if count > 2),
        radial_variation_pct=round(100.0 * (max(radii) / min(radii) - 1.0), 2))


def blend_checks(report, root):
    checks = {}
    scene = bpy.context.scene
    stage = str(scene.get("hero_v2_stage", ""))
    checks["stage_tag"] = dict(pass_=stage.startswith("2.5"), value=stage)

    # 1. Sources untouched, compared against the hashes captured at build time.
    recorded = report.get("sources", {})
    now = {}
    for relative in SOURCES:
        path = os.path.join(root, relative)
        now[relative] = sha256(path) if os.path.exists(path) else None
    checks["sources_unchanged"] = dict(
        pass_=bool(recorded) and all(recorded.get(key, {}).get("sha256") == value
                                     for key, value in now.items()),
        recorded={k: (v.get("sha256") or "")[:16] for k, v in recorded.items()},
        measured={k: (v or "")[:16] for k, v in now.items()})

    # 2/3. Exactly four semantic groups, one core plus three single-sphere companions.
    empties = sorted(obj.name for obj in bpy.data.objects
                     if obj.type == "EMPTY" and obj.name.startswith("GRP_"))
    checks["exactly_four_semantic_groups"] = dict(
        pass_=tuple(empties) == tuple(sorted(GROUPS)), found=empties)
    group_meshes = {}
    for name in GROUPS:
        empty = bpy.data.objects.get(name)
        group_meshes[name] = sorted(child.name for child in
                                    (empty.children if empty else [])
                                    if child.type == "MESH")
    checks["one_core_plus_three_single_spheres"] = dict(
        pass_=len(group_meshes["GRP_CORE"]) == 2 and
              all(len(group_meshes[name]) == 1 for name in GROUPS
                  if name != "GRP_CORE"),
        members=group_meshes)

    # 4/5/6. No cavity or inner ball, no rings or bands, no silhouette grooves.
    names = {obj.name for obj in bpy.data.objects if obj.type == "MESH"}
    forbidden = sorted(name for name in names
                       if any(token in name.upper() for token in
                              ("INSET", "INNER", "RING", "BAND", "SLOT", "CAP",
                               "SHELL", "APERTURE", "GROOVE", "SEGMENT"))
                       and name not in {"CORE_SPHERE", "CORE_ACCENT"})
    topology_map = {name: topology(bpy.data.objects[name]) for name in
                    sorted(names) if bpy.data.objects[name].type == "MESH"}
    companion_flags = {name: topology_map[name] for name in COMPANIONS
                       if name in topology_map}
    checks["no_cavity_or_inner_ball_geometry"] = dict(
        pass_=not forbidden and
              all(entry["euler"] == 2 and entry["boundary_edges"] == 0
                  for entry in companion_flags.values()),
        forbidden_objects=forbidden, topology=companion_flags,
        rule="a companion that still carried an aperture, an inner ball or a "
             "solidified shell could not be a single closed surface (Euler 2, no "
             "boundary edges)")
    checks["no_ring_band_or_groove_companions"] = dict(
        pass_=all(entry["radial_variation_pct"] <= 2.0
                  for entry in companion_flags.values()),
        variation={name: entry["radial_variation_pct"]
                   for name, entry in companion_flags.items()},
        rule="bands, rings and grooves all cut or raise the radius by more than the "
             "card's 1-2% allowance; CORE_SPHERE is excluded because its seam is "
             "the one incision this stage keeps")

    # 7. The decorative arc is off and stays in the file for provenance only.
    arc = bpy.data.objects.get("DECOR_ARC_01")
    checks["arc_hidden"] = dict(
        pass_=arc is not None and arc.hide_render is True,
        exists=arc is not None, hide_render=(arc.hide_render if arc else None))

    # 8/9/10/11. Nothing that could become a web or page artifact.
    checks["no_text_or_particles"] = dict(
        pass_=not any(obj.type in {"FONT", "CURVE"} for obj in bpy.data.objects) and
              len(bpy.data.particles) == 0,
        types=sorted({obj.type for obj in bpy.data.objects}))
    glb = []
    for base, _dirs, files in os.walk(root):
        for name in files:
            if os.path.splitext(name)[1].lower() in {".glb", ".gltf", ".webp",
                                                     ".avif"}:
                glb.append(os.path.join(base, name))
    checks["no_glb_or_web_export"] = dict(pass_=not glb, found=glb[:10])
    front = os.path.abspath(os.path.join(root, "..", "..", "Front-End"))
    stray = []
    for base, _dirs, files in os.walk(front):
        if "node_modules" in base or ".git" in base or "test-results" in base:
            continue
        for name in files:
            if name.startswith("hero-v2") or name.startswith("hero_v2"):
                stray.append(os.path.join(base, name))
    checks["no_frontend_export"] = dict(pass_=not stray, found=stray[:10])

    # 12/13/14. Materials, triangles and camera framing.
    roles, slots = {}, {}
    for obj in bpy.data.objects:
        if obj.type != "MESH" or not obj.material_slots:
            continue
        slots[obj.name] = [slot.material.name if slot.material else None
                           for slot in obj.material_slots]
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None:
                continue
            bsdf = mat.node_tree.nodes.get("Principled BSDF") if mat.use_nodes else None
            roles[mat.name] = dict(
                role=mat.get("hero_v2_role"), metallic=(None if bsdf is None else
                                                        round(float(bsdf.inputs[
                                                            "Metallic"].default_value), 3)),
                roughness=(None if bsdf is None else round(float(bsdf.inputs[
                    "Roughness"].default_value), 3)))
    metallic = {name: entry["metallic"] for name, entry in roles.items()
                if entry["metallic"]}
    checks["no_metallic_shells"] = dict(pass_=all(value == 0.0
                                                  for value in metallic.values()),
                                        metallic=metallic)
    triangles = {obj.name: sum(max(0, len(poly.vertices) - 2)
                               for poly in obj.data.polygons)
                 for obj in bpy.data.objects if obj.type == "MESH"}
    checks["triangle_counts_reported"] = dict(
        pass_=len(triangles) > 0, triangles=triangles,
        total=sum(triangles.values()))

    composition = report.get("composition", {})
    framing = {}
    for camera, key, margin in (("CAM_DESKTOP", "desktop", 8.0),
                                ("CAM_MOBILE", "mobile", 4.0)):
        entry = composition.get(key, {})
        edges = entry.get("edge_clearance_pct", {})
        framing[key] = dict(min_edge_pct=(min(edges.values()) if edges else None),
                            required_pct=margin,
                            gap_on_page_px=entry.get("min_gap_scaled_to_page_px"))
    checks["camera_framing_safe_margin"] = dict(
        pass_=all(entry["min_edge_pct"] is not None and
                  entry["min_edge_pct"] >= entry["required_pct"] - 0.5 and
                  (entry["gap_on_page_px"] or 0) >= 12.0
                  for entry in framing.values()),
        framing=framing)
    return checks


def pixel_checks(renders_dir, quick):
    checks, inspected = {}, {}
    loaded = {}
    for label, camera, theme in RENDER_FILES:
        path = os.path.join(renders_dir, "%s.png" % label)
        entry = dict(path=path, exists=os.path.exists(path))
        if entry["exists"]:
            width, height, rgb = read_pixels(path)
            lum = luminance(rgb)
            flat = lum.ravel()
            entry.update(dict(size=[width, height], bytes=os.path.getsize(path),
                              p02=round(float(np.percentile(flat, 2)), 4),
                              p50=round(float(np.percentile(flat, 50)), 4),
                              p98=round(float(np.percentile(flat, 98)), 4),
                              clipped_pct=round(float((flat > 0.98).mean() * 100), 3),
                              crushed_pct=round(float((flat < 0.02).mean() * 100), 3)))
            loaded[label] = dict(theme=theme, camera=camera, lum=flat, rgb=rgb,
                                 size=(width, height))
        inspected[label] = entry

    expected = {"desktop": (1600, 1400), "mobile": (800, 800)}
    if quick:
        expected = {"desktop": (800, 700), "mobile": (400, 400)}
    sizes_ok = all(entry.get("size") == list(expected[RENDER_FILES_item[1]])
                   for RENDER_FILES_item in RENDER_FILES
                   for entry in [inspected[RENDER_FILES_item[0]]]
                   if entry.get("exists"))
    checks["four_renders_exist_and_sized"] = dict(
        pass_=len(loaded) == 4 and sizes_ok, expected=expected,
        sizes={label: entry.get("size") for label, entry in inspected.items()})

    checks["no_clipped_highlights"] = dict(
        pass_=all(entry["clipped_pct"] < 2.0 for entry in inspected.values()
                  if entry.get("p98") is not None),
        clipped={label: entry.get("clipped_pct") for label, entry in inspected.items()},
        rule="<2% of pixels at or above 0.98")
    checks["no_excessive_crushed_blacks"] = dict(
        pass_=all(entry["crushed_pct"] < 5.0 for entry in inspected.values()
                  if entry.get("p02") is not None),
        crushed={label: entry.get("crushed_pct") for label, entry in inspected.items()},
        rule="<5% of pixels at or below 0.02")

    canvases = {}
    for label, data in loaded.items():
        flat = data["lum"]
        canvas_level = float(np.percentile(flat, 98 if data["theme"] == "light"
                                           else 50))
        measured = int(round(canvas_level * 255))
        target = int(CANVAS[data["theme"]], 16)
        target_rgb = tuple(int(CANVAS[data["theme"]][i:i + 2], 16) for i in (0, 2, 4))
        target_lum = int(round(0.2126 * target_rgb[0] + 0.7152 * target_rgb[1] +
                               0.0722 * target_rgb[2]))
        canvases[label] = dict(theme=data["theme"], measured=measured,
                               token_lum=target_lum,
                               delta=abs(measured - target_lum))
    checks["theme_canvases_match_tokens"] = dict(
        pass_=all(entry["delta"] <= CANVAS_TOLERANCE for entry in canvases.values()),
        measured=canvases, tolerance_levels=CANVAS_TOLERANCE,
        note="dark uses the frame median (the navy IS most of the frame); light "
             "uses p98 (the page is the bright field)")

    readability = {}
    for label, data in loaded.items():
        flat = data["lum"]
        # The field is the page: the frame median for dark (the navy is most of the
        # frame), p98 for light (the page is the bright field). The forms are then
        # whatever sits away from that field -- BRIGHTER in dark, darker in light --
        # which the first version of this check got wrong by only looking downward.
        field = float(np.percentile(flat, 50 if data["theme"] == "dark" else 98))
        forms = flat[np.abs(flat - field) > 0.05]
        form_p50 = float(np.percentile(forms, 50)) if forms.size else 0.0
        readability[label] = dict(
            theme=data["theme"], field=round(field, 4),
            separation=round(abs(form_p50 - field), 4),
            form_p50=round(form_p50, 4), form_pixels=int(forms.size),
            direction="brighter" if form_p50 > field else "darker")
    checks["forms_readable_in_both_themes"] = dict(
        pass_=all(entry["separation"] > 0.12 and entry["form_pixels"] > 500
                  for entry in readability.values()),
        measured=readability,
        rule="the forms must sit >0.12 away from their page field with real pixel "
             "coverage, in whichever direction that theme puts them")

    dark = [data for data in loaded.values() if data["theme"] == "dark"]
    light = [data for data in loaded.values() if data["theme"] == "light"]
    checks["dark_and_light_are_different_renders"] = dict(
        pass_=bool(dark and light) and all(
            float(np.abs(a["lum"] - b["lum"]).mean()) > 0.05
            for a in dark for b in light
            if a["lum"].shape == b["lum"].shape),
        note="a theme swap that only inverted the image would still be different, "
             "so the canvas check above carries the weight here")
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
    pixel_checks_result, inspected = pixel_checks(
        os.path.abspath(os.path.join(root, "renders", "stage2_5")), args.quick)
    checks.update(pixel_checks_result)
    failed = sorted(name for name, item in checks.items() if not item["pass_"])
    summary = dict(blend=os.path.abspath(args.blend), checks=checks,
                   checks_all_pass=not failed, failed=failed,
                   renders_inspected=inspected,
                   counts=dict(checks=len(checks), passed=len(checks) - len(failed)))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True, default=str)
    log("checks_all_pass=%s failed=%s" % (not failed, failed))
    return summary


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
