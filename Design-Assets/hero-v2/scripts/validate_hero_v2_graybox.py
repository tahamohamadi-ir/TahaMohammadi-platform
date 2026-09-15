# validate_hero_v2_graybox.py -- verify the SHIPPED .blend, in a fresh process.
#
# A builder that returns success is not evidence that the file on disk is right:
# Blender exits 0 even when a --background --python script raises, and a late
# finisher can silently overwrite an artefact. This opens the saved file from
# scratch and asserts the contract against it.
#
# Usage:
#   "<blender.exe>" --background --factory-startup \
#     --python validate_hero_v2_graybox.py -- --blend <file.blend> [--report <json>]
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector

CORE_DIAMETER = 1.45
DOMAIN_DIAMETER = 1.00
EXPECTED = {
    "GRP_CORE": {"CORE_SPHERE", "CORE_ACCENT"},
    "GRP_HUMAN_CENTERED_AI": {"HCAI_SHELL", "HCAI_INSET"},
    "GRP_HEALTH_BEHAVIOR": {"HHB_SPHERE"},
    "GRP_WEARABLE_EDGE": {"WE_SPHERE"},
}
EXPECTED_CAMERAS = {"CAM_DESKTOP", "CAM_MOBILE"}
DECOR = "DECOR_ARC_01"
CLAY = "PREVIEW_CLAY"
TAG = "[HERO_V2-VALIDATE]"


def log(msg):
    print(TAG + " " + msg, flush=True)


def diameter(objs):
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    deps = bpy.context.evaluated_depsgraph_get()
    for obj in objs:
        ev = obj.evaluated_get(deps)
        mesh = ev.to_mesh()
        try:
            for v in mesh.vertices:
                w = ev.matrix_world @ v.co
                lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
                hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
        finally:
            ev.to_mesh_clear()
    size = hi - lo
    return max(size.x, size.y, size.z)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    if not os.path.exists(args.blend):
        log("FAIL missing blend %s" % args.blend)
        return 1

    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(args.blend))
    bpy.context.view_layer.update()
    log("opened %s (%d bytes)" % (args.blend, os.path.getsize(args.blend)))

    checks = {}

    def check(name, ok, **detail):
        checks[name] = dict(pass_=bool(ok), **detail)
        log("%-38s %s%s" % (name, "PASS" if ok else "FAIL",
                            "" if ok else "  " + str(detail)))

    objects = {o.name: o for o in bpy.data.objects}

    # --- hierarchy: exact member-name SETS, never a bare count that can drift
    for group, members in EXPECTED.items():
        empty = objects.get(group)
        if empty is None or empty.type != "EMPTY":
            check("group:%s" % group, False, reason="missing group empty")
            continue
        found = {o.name for o in empty.children}
        check("group:%s members" % group, found == members,
              expected=sorted(members), found=sorted(found))

    root = objects.get("HERO_V2_ROOT")
    check("single_root", root is not None and root.type == "EMPTY"
          and {o.name for o in root.children} == set(EXPECTED),
          children=sorted(o.name for o in root.children) if root else None)

    # --- scale contract
    for group, members in EXPECTED.items():
        objs = [objects[m] for m in sorted(members) if m in objects]
        if not objs:
            continue
        target = CORE_DIAMETER if group == "GRP_CORE" else DOMAIN_DIAMETER
        measured = diameter(objs)
        check("diameter:%s" % group, abs(measured - target) <= 5e-3,
              target=target, measured=round(measured, 4))

    # --- cameras
    for name in sorted(EXPECTED_CAMERAS):
        cam = objects.get(name)
        check("camera:%s exists" % name, cam is not None and cam.type == "CAMERA")
    desktop, mobile = objects.get("CAM_DESKTOP"), objects.get("CAM_MOBILE")
    if desktop:
        check("camera:CAM_DESKTOP 70mm perspective",
              desktop.data.type == "PERSP"
              and abs(desktop.data.lens - 70.0) < 1e-6
              and abs(desktop.data.sensor_width - 36.0) < 1e-6,
              lens=desktop.data.lens, type=desktop.data.type)
    if mobile:
        check("camera:CAM_MOBILE orthographic",
              mobile.data.type == "ORTHO", type=mobile.data.type,
              ortho_scale=round(mobile.data.ortho_scale, 4))

    # --- materials: exactly one neutral placeholder, used by every mesh
    mats = sorted(m.name for m in bpy.data.materials)
    check("single placeholder material", mats == [CLAY], materials=mats)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    unassigned = [o.name for o in meshes
                  if [m.name for m in o.data.materials if m] != [CLAY]]
    check("every mesh uses the placeholder", not unassigned, offenders=unassigned)

    # --- geometry hygiene
    deps = bpy.context.evaluated_depsgraph_get()
    degenerate, modifiers, unapplied = [], [], []
    for obj in meshes:
        if obj.modifiers:
            modifiers.append(obj.name)
        if max(abs(obj.scale.x - 1), abs(obj.scale.y - 1), abs(obj.scale.z - 1)) > 1e-6:
            unapplied.append(obj.name)
        ev = obj.evaluated_get(deps)
        mesh = ev.to_mesh()
        try:
            for poly in mesh.polygons:
                if poly.area < 1e-12:
                    degenerate.append(obj.name)
                    break
        finally:
            ev.to_mesh_clear()
    check("no unapplied modifiers", not modifiers, offenders=modifiers)
    check("mesh scale applied", not unapplied, offenders=unapplied)
    check("no zero-area faces", not degenerate, offenders=degenerate)

    # --- the plan's bans, asserted on the saved scene
    banned = {
        "text_objects": [o.name for o in bpy.data.objects if o.type == "FONT"],
        "particle_systems": [o.name for o in bpy.data.objects if o.particle_systems],
        "grease_pencil": [o.name for o in bpy.data.objects
                          if o.type in ("GPENCIL", "GREASEPENCIL")],
    }
    check("no text / labels / particles / panels", not any(banned.values()),
          found=banned)

    # --- decor arc authored but excluded from this stage's renders
    arc = objects.get(DECOR)
    check("decor arc authored and not rendered",
          arc is not None and arc.hide_render, hide_render=arc.hide_render if arc else None)

    # --- render setup the previews were produced with
    scene = bpy.context.scene
    check("cycles + transparent film",
          scene.render.engine == "CYCLES" and scene.render.film_transparent,
          engine=scene.render.engine, film_transparent=scene.render.film_transparent)

    report = dict(blend=os.path.abspath(args.blend),
                  bytes=os.path.getsize(args.blend),
                  blender=bpy.app.version_string,
                  checks=checks,
                  checks_all_pass=all(c["pass_"] for c in checks.values()))
    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
        log("wrote %s" % args.report)
    failed = [k for k, v in checks.items() if not v["pass_"]]
    log("checks_all_pass=%s (%d checks, %d failed)"
        % (report["checks_all_pass"], len(checks), len(failed)))
    return 0 if report["checks_all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []))
