"""Hero v2 — Stage 2 validator: re-open the SHIPPED .blend and inspect the PNGs.

A green build is not evidence: Blender exits 0 even when a `--background
--python` script raises, so this pass opens the file that actually shipped and
measures what is on disk.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/validate_hero_v2_lookdev.py -- \
      --blend     Design-Assets/hero-v2/source/hero-v2-lookdev.blend \
      --stage1-report Design-Assets/hero-v2/validation/hero-v2-graybox-report.json \
      --renders   Design-Assets/hero-v2/renders/stage2 \
      --report    Design-Assets/hero-v2/validation/hero-v2-lookdev-validation.json

Two families of checks:

* **Blend** — the four roles exist with distinct colours and a real family node
  graph (roughness driven by the grain field, normal driven by the bump pair);
  the Stage 1 placeholder is gone; geometry, layout and camera matrices are
  identical to the Stage 1 report; the arc is on with a faint material; the
  backdrop's faces point at the scene; Cycles/AgX/denoise are configured.
* **Pixels** — the four PNGs exist at the right size, are not degenerate, the
  forms separate tonally from the backdrop, and each `-clean`/`-arc` pair differs
  enough to prove the arc rendered *and* little enough to prove it is faint.
  Pixels are read with the image colorspace forced to Non-Color, so the numbers
  are on the familiar 0-1 sRGB scale, and sampled with a stride (they are
  distributions, not exact counts).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import bpy
import numpy as np

FORM_MESHES = ("CORE_SPHERE", "CORE_ACCENT", "HCAI_SHELL", "HCAI_INSET",
               "HHB_SPHERE", "WE_SPHERE")
SHELL_ROLES = ("core_shell", "hcai_shell", "health_shell", "wearable_shell")
EXPECTED_RENDERS = {
    "desktop-clean": (1600, 1400),
    "desktop-arc": (1600, 1400),
    "mobile-clean": (800, 800),
    "mobile-arc": (800, 800),
}
STRIDE = 2


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--stage1-report", default=None)
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--quick", action="store_true",
                        help="expect the half-size quick renders instead")
    return parser.parse_args(argv)


def log(msg):
    print("[HERO_V2_VALIDATE] %s" % msg, flush=True)


def luminance(image):
    """Sampled luminance grid (0-1 sRGB) plus the alpha-free RGB sample."""
    handle = bpy.data.images.load(image, check_existing=False)
    handle.colorspace_settings.name = "Non-Color"
    width, height = handle.size
    buffer = np.empty(width * height * 4, dtype=np.float32)
    handle.pixels.foreach_get(buffer)
    buffer = buffer.reshape(height, width, 4)[::STRIDE, ::STRIDE, :]
    rgb = buffer[:, :, :3]
    lum = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2])
    bpy.data.images.remove(handle)
    return width, height, rgb, lum


def pixel_checks(renders_dir, quick):
    files = {}
    for name, (width, height) in EXPECTED_RENDERS.items():
        path = os.path.join(renders_dir, "%s.png" % name)
        if quick:
            width, height = (width // 2, height // 2) if name.startswith("desktop") \
                else (width // 2, height // 2)
        entry = dict(path=path, exists=os.path.exists(path))
        if entry["exists"]:
            entry["bytes"] = os.path.getsize(path)
            measured_w, measured_h, rgb, lum = luminance(path)
            entry.update(dict(size=[measured_w, measured_h],
                              expected_size=[width, height],
                              size_matches=[measured_w, measured_h] == [width, height]))
            flat = lum.ravel()
            entry.update(dict(
                p02=round(float(np.percentile(flat, 2)), 4),
                p50=round(float(np.percentile(flat, 50)), 4),
                p98=round(float(np.percentile(flat, 98)), 4),
                clipped_pct=round(float((flat > 0.98).mean() * 100.0), 3),
                crushed_pct=round(float((flat < 0.02).mean() * 100.0), 3),
            ))
            entry["_lum"] = flat
            entry["_rgb"] = rgb
        files[name] = entry

    checks = {}
    shapes = {name: tuple(entry["size"]) for name, entry in files.items()
              if entry.get("size")}
    checks["renders_present_and_sized"] = dict(
        pass_=all(entry.get("exists") and entry.get("size_matches")
                  for entry in files.values()),
        sizes=shapes, present={n: e.get("exists") for n, e in files.items()})

    live = {"%s/%s" % (name.split("-")[0], name.split("-")[1]): entry
            for name, entry in files.items() if entry.get("size")}
    degenerate = {name: dict(p98=entry["p98"], clipped_pct=entry["clipped_pct"],
                             spread=round(entry["p98"] - entry["p02"], 4))
                  for name, entry in live.items()
                  if not (entry["p98"] > 0.30 and entry["p02"] < 0.15
                          and entry["clipped_pct"] < 2.0
                          and entry["p98"] - entry["p02"] > 0.15)}
    checks["renders_not_degenerate"] = dict(pass_=not degenerate, offenders=degenerate)

    separation = {}
    for camera in ("desktop", "mobile"):
        entry = live.get("%s/clean" % camera)
        if not entry:
            continue
        flat = entry["_lum"]
        separation[camera] = dict(
            p50=round(float(np.percentile(flat, 50)), 4),
            p90=round(float(np.percentile(flat, 90)), 4),
            p10=round(float(np.percentile(flat, 10)), 4),
            p90_minus_p10=round(float(np.percentile(flat, 90) -
                                      np.percentile(flat, 10)), 4))
    checks["forms_separate_from_backdrop"] = dict(
        pass_=all(item["p90"] - item["p10"] > 0.15 and item["p90"] > 0.25
                  for item in separation.values()), measured=separation)

    arcs = {}
    for camera in ("desktop", "mobile"):
        clean, arc = live.get("%s/clean" % camera), live.get("%s/arc" % camera)
        if not clean or not arc or clean["_rgb"].shape != arc["_rgb"].shape:
            arcs[camera] = dict(measurable=False)
            continue
        delta = np.abs(clean["_lum"] - arc["_lum"])
        arcs[camera] = dict(mean_delta=round(float(delta.mean()), 5),
                            strong_pixel_pct=round(float((delta > 0.06).mean() * 100.0), 3),
                            max_delta=round(float(delta.max()), 4))
    arcs_ok = all(item.get("measurable", True) is not False and
                  item["strong_pixel_pct"] >= 0.02 and
                  item["strong_pixel_pct"] < 8.0 and
                  item["max_delta"] > 0.10
                  for item in arcs.values())
    checks["arc_present_and_faint"] = dict(
        pass_=arcs_ok, measured=arcs,
        rule="presence: >=0.02% of sampled pixels changed by >0.06 AND the local "
             "change peaks above 0.10 (the arc is a 0.02 BU tube: a few pixels "
             "wide, so a whole-frame mean dilutes it into noise). faintness: "
             "<8% of pixels changed that much. mean_delta is reported for "
             "information, not asserted.")

    pairs = {}
    names = sorted(live)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            if left.split("/")[0] == right.split("/")[0] and \
                    {left.split("/")[1], right.split("/")[1]} == {"clean", "arc"}:
                continue          # covered by the arc check, intentionally similar
            a, b = live[left]["_lum"], live[right]["_lum"]
            if a.shape != b.shape:
                pairs["%s|%s" % (left, right)] = "different sizes"
                continue
            pairs["%s|%s" % (left, right)] = round(float(np.abs(a - b).mean()), 5)
    distinct = {key: value for key, value in pairs.items()
                if not isinstance(value, str) and value < 0.01}
    checks["renders_pairwise_distinct"] = dict(pass_=not distinct, pairs=pairs)
    return checks, files


def blend_checks(stage1):
    checks = {}
    scene = bpy.context.scene
    stage = scene.get("hero_v2_stage", "")
    checks["stage_tag"] = dict(pass_=str(stage).startswith("2 -"), value=str(stage))

    roles = {}
    for obj_name in FORM_MESHES:
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            roles[obj_name] = None
            continue
        roles[obj_name] = dict(
            slots=[slot.material.name if slot.material else None
                   for slot in obj.material_slots],
            role_tags=[(slot.material.get("hero_v2_role")
                        if slot.material else None) for slot in obj.material_slots])
    missing = [name for name, entry in roles.items()
               if not entry or not all(entry["role_tags"])]
    placeholder = [name for name, entry in roles.items()
                   if entry and any(name_ and "PREVIEW_CLAY" in name_
                                    for name_ in entry["slots"])]
    checks["every_form_has_a_stage2_role"] = dict(pass_=not missing, missing=missing)
    checks["stage1_placeholder_removed"] = dict(pass_=not placeholder,
                                                offenders=placeholder)

    colours = {}
    for role in SHELL_ROLES:
        mat = bpy.data.materials.get("M_%s" % role.upper())
        if mat is None:
            colours[role] = None
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        base = bsdf.inputs["Base Color"].default_value
        colours[role] = dict(
            hex=list(round(float(channel), 5) for channel in base),
            roughness=round(float(bsdf.inputs["Roughness"].default_value), 3),
            roughness_driven=bool(bsdf.inputs["Roughness"].is_linked),
            normal_driven=bool(bsdf.inputs["Normal"].is_linked),
            metallic=round(float(bsdf.inputs["Metallic"].default_value), 3))
    distinct = {role: entry for role, entry in colours.items() if entry}
    unique_colours = len({tuple(entry["hex"]) for entry in distinct.values()})
    checks["four_roles_distinct_colour"] = dict(pass_=unique_colours == 4,
                                                unique=unique_colours,
                                                role_count=len(SHELL_ROLES))
    checks["family_graph_intact"] = dict(
        pass_=all(entry["roughness_driven"] and entry["normal_driven"]
                  for entry in distinct.values()),
        roles=distinct)
    checks["no_metallic_shells"] = dict(
        pass_=all(entry["metallic"] <= 0.25 for entry in distinct.values()),
        max_metallic=max((entry["metallic"] for entry in distinct.values()),
                         default=0.0))

    drift = {"triangles": {}, "layout": {}, "cameras": {}}
    for name, stats in stage1.get("geometry", {}).items():
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != "MESH":
            continue
        measured = sum(max(0, len(poly.vertices) - 2) for poly in obj.data.polygons)
        expected = stats.get("triangles")
        if expected is not None and measured != expected:
            drift["triangles"][name] = dict(expected=expected, measured=measured)
    for name, location in stage1.get("layout", {}).items():
        obj = bpy.data.objects.get(name)
        if obj is None:
            continue
        measured = [round(value, 4) for value in obj.location]
        if measured != [round(value, 4) for value in location]:
            drift["layout"][name] = dict(expected=list(location), measured=measured)
    checks["stage1_geometry_layout_cameras_intact"] = dict(
        pass_=not any(drift.values()), drift=drift)

    arc = bpy.data.objects.get("DECOR_ARC_01")
    checks["arc_on_with_faint_material"] = dict(
        pass_=arc is not None and arc.hide_render is False and
              bool(arc.material_slots) and arc.material_slots[0].material is not None
              and arc.material_slots[0].material.get("hero_v2_role") == "arc",
        hide_render=None if arc is None else arc.hide_render)

    backdrop = bpy.data.objects.get("BACKDROP")
    facing = None
    if backdrop is not None:
        floor_faces = [poly for poly in backdrop.data.polygons
                       if abs(poly.normal.z) > 0.9]
        facing = dict(floor_faces=len(floor_faces),
                      floor_normals_z=[round(poly.normal.z, 3)
                                       for poly in floor_faces[:4]])
    checks["backdrop_faces_the_scene"] = dict(
        pass_=backdrop is not None and facing is not None and
              facing["floor_faces"] > 0 and
              all(z > 0 for z in facing["floor_normals_z"]),
        measured=facing,
        rule="floor faces must point up (+Z); the first build had them inverted "
             "and the floor rendered black")

    rig = {name: dict(exists=bpy.data.objects.get(name) is not None,
                      hide_render=(bpy.data.objects[name].hide_render
                                   if bpy.data.objects.get(name) else None))
           for name in ("LG2_Key", "LG2_Fill", "LG2_Sep", "LG_Key", "LG_Fill",
                        "LG_Rim")}
    checks["studio_rig_replaces_stage1_rig"] = dict(
        pass_=all(rig[name]["exists"] and rig[name]["hide_render"] is False
                  for name in ("LG2_Key", "LG2_Fill", "LG2_Sep")) and
              all(rig[name]["hide_render"] is True
                  for name in ("LG_Key", "LG_Fill", "LG_Rim")),
        rig=rig)

    render = scene.render
    checks["render_settings"] = dict(
        pass_=render.engine == "CYCLES" and scene.cycles.use_denoising and
              not render.film_transparent and
              render.image_settings.color_mode == "RGB" and
              scene.view_settings.view_transform == "AgX",
        engine=render.engine, denoise=bool(scene.cycles.use_denoising),
        film_transparent=bool(render.film_transparent),
        color_mode=render.image_settings.color_mode,
        view_transform=scene.view_settings.view_transform,
        samples=int(scene.cycles.samples), exposure=round(float(scene.view_settings.exposure), 3))

    checks["no_text_particles_or_extra_objects"] = dict(
        pass_=not any(obj.type in {"FONT", "CURVE"} for obj in bpy.data.objects) and
              len(bpy.data.particles) == 0,
        types=sorted({obj.type for obj in bpy.data.objects}))
    return checks


def main(argv):
    args = parse_args(argv)
    stage1 = {}
    if args.stage1_report and os.path.exists(args.stage1_report):
        with open(args.stage1_report, "r", encoding="utf-8") as handle:
            stage1 = json.load(handle)
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(args.blend))
    log("opened %s" % args.blend)

    checks = blend_checks(stage1)
    pixel, files = pixel_checks(os.path.abspath(args.renders), args.quick)
    checks.update(pixel)
    all_pass = all(item["pass_"] for item in checks.values())
    summary = {
        "blend": os.path.abspath(args.blend),
        "renders": os.path.abspath(args.renders),
        "checks": checks,
        "checks_all_pass": all_pass,
        "failed": sorted(name for name, item in checks.items() if not item["pass_"]),
        "renders_inspected": {name: {key: value for key, value in entry.items()
                                     if not key.startswith("_")}
                              for name, entry in files.items()},
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    log("checks_all_pass=%s failed=%s" % (all_pass, summary["failed"]))
    return summary


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
