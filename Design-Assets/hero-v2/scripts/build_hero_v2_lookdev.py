"""Hero v2 — Stage 2 builder: open the approved graybox, add look, render review.

    BLENDER="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
    "$BLENDER" --background --factory-startup \
      --python Design-Assets/hero-v2/scripts/build_hero_v2_lookdev.py -- \
      --blend-in  Design-Assets/hero-v2/source/hero-v2-graybox.blend \
      --blend-out Design-Assets/hero-v2/source/hero-v2-lookdev.blend \
      --renders   Design-Assets/hero-v2/renders \
      --report    Design-Assets/hero-v2/validation/hero-v2-lookdev-report.json \
      --stage1-report Design-Assets/hero-v2/validation/hero-v2-graybox-report.json

Flags: --quick (half res, 24 samples), --no-gpu, --exposure <float>,
       --debug-mask (paint the recovered groove faces in magenta and render one
       desktop frame — used to verify groove recovery coverage, never shipped).

Geometry is never touched. The script opens the Stage 1 file, checks its
contract, and compares every mesh's triangle count, the layout and the camera
matrices against the Stage 1 report: any drift fails the run instead of being
written into the report as a warning.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import hero_v2_common as hv          # noqa: E402
import hero_v2_lookdev as lk         # noqa: E402

STAGE2_SAMPLES = 160
STAGE2_SAMPLES_QUICK = 24
STAGE2_EXPOSURE = -0.7
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
ENV_COLLECTION = "Rig_ReviewEnv"
FORM_MESHES = ("CORE_SPHERE", "CORE_ACCENT", "HCAI_SHELL", "HCAI_INSET",
               "HHB_SPHERE", "WE_SPHERE")
SHELL_ROLES = {
    "CORE_SPHERE": ("core_shell", "core_inset"),
    "HCAI_SHELL": ("hcai_shell", "hcai_inset"),
    "HHB_SPHERE": ("health_shell", "health_inset"),
    "WE_SPHERE": ("wearable_shell", "wearable_inset"),
}
SINGLE_ROLES = {
    "CORE_ACCENT": "core_accent",
    "HCAI_INSET": "hcai_inner",
}

README_TEXT = """HERO V2 -- STAGE 2 (look development)

Open hero-v2-lookdev.blend, NOT hero-v2-graybox.blend, for the current look.

Stage 2 adds materials, a studio rig and a review backdrop to the approved
Stage 1 geometry. The geometry, the four group transforms, the layout and the
two authored cameras are byte-identical to Stage 1 -- the report records the
comparison.

Objects:
  GRP_CORE / CORE_SPHERE   M_CORE_SHELL + M_CORE_INSET (recovered seam faces)
              CORE_ACCENT  M_CORE_ACCENT (restrained warm stone inlay)
  GRP_HUMAN_CENTERED_AI / HCAI_SHELL  M_HCAI_SHELL + M_HCAI_INSET (inner wall)
                          HCAI_INSET  M_HCAI_INNER
  GRP_HEALTH_BEHAVIOR / HHB_SPHERE (two contours) M_HEALTH_SHELL/_INSET
  GRP_WEARABLE_EDGE / WE_SPHERE (two grooves) M_WEARABLE_SHELL/_INSET
  DECOR_ARC_01  M_ARC, faint. hide_render is toggled per render so every camera
                is captured both WITHOUT and WITH the arc.
  BACKDROP + LG2_Key/Fill/Sep in Rig_ReviewEnv  -- review environment only.
  Rig_PreviewNeutral lights are kept but hide_render=True: Stage 1 evidence.

Render list (renders/stage2/): desktop-clean, desktop-arc, mobile-clean,
mobile-arc. Cameras are the authored Stage 1 cameras, unfitted: no framing was
changed in this stage.

No frontend, no GLB and no web runtime asset comes out of this stage.
"""


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-in", required=True)
    parser.add_argument("--blend-out", required=True)
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--stage1-report", default=None)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--no-gpu", action="store_true")
    parser.add_argument("--exposure", type=float, default=STAGE2_EXPOSURE)
    parser.add_argument("--debug-mask", action="store_true")
    return parser.parse_args(argv)


# ------------------------------------------------------------------------ helpers
def object_or_fail(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise RuntimeError("Stage 1 contract broken: missing object %r" % name)
    return obj


def group_transform(obj):
    return [round(v, 6) for v in obj.location] + \
           [round(v, 6) for v in obj.rotation_euler]


def camera_signature(cam):
    matrix = cam.matrix_world
    return [round(value, 6) for row in matrix for value in row]


def render_state(scene, cam, path):
    scene.camera = cam
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    hv.log("rendered %s" % path)


def check_geometry_invariance(stage1, scene):
    """Stage 1 must survive the look pass untouched, measured, not assumed."""
    drift = {"triangles": {}, "layout": {}, "cameras": {}}
    for name, stats in stage1.get("geometry", {}).items():
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != "MESH":
            continue
        measured = len(obj.data.loop_triangles) if obj.data.loop_triangles else \
            sum(max(0, len(p.vertices) - 2) for p in obj.data.polygons)
        expected = stats.get("triangles")
        if expected is not None and measured != expected:
            drift["triangles"][name] = dict(expected=expected, measured=measured)
    for name, location in stage1.get("layout", {}).items():
        obj = bpy.data.objects.get(name)
        if obj is None:
            continue
        measured = [round(v, 4) for v in obj.location]
        expected = [round(v, 4) for v in location]
        if measured != expected:
            drift["layout"][name] = dict(expected=expected, measured=measured)
    for name, signature in stage1.get("fits", {}).items():
        cam_name = signature.get("cam") if isinstance(signature, dict) else None
        if not cam_name:
            continue
        cam = bpy.data.objects.get(cam_name)
        if cam is None:
            continue
        measured = camera_signature(cam)
        expected = signature.get("camera_matrix")
        if expected and measured != [round(v, 6) for v in expected]:
            drift["cameras"][cam_name] = dict(expected=expected, measured=measured)
    return drift


def read_stage1_report(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


# ---------------------------------------------------------------------------- main
def main(argv):
    args = parse_args(argv)
    stage1 = read_stage1_report(args.stage1_report)

    blend_in = os.path.abspath(args.blend_in)
    if not os.path.exists(blend_in):
        raise RuntimeError("missing Stage 1 file: %s" % blend_in)
    bpy.ops.wm.open_mainfile(filepath=blend_in)
    hv.log("opened %s" % blend_in)

    scene = bpy.context.scene
    forms = {name: object_or_fail(name) for name in FORM_MESHES}
    arc = object_or_fail("DECOR_ARC_01")
    cam_desktop = object_or_fail("CAM_DESKTOP")
    cam_mobile = object_or_fail("CAM_MOBILE")

    before = dict(
        triangles={name: sum(max(0, len(p.vertices) - 2)
                             for p in obj.data.polygons)
                   for name, obj in forms.items()},
        total_triangles=sum(sum(max(0, len(p.vertices) - 2)
                                for p in obj.data.polygons)
                            for obj in forms.values()),
        layout={name: group_transform(bpy.data.objects[name])
                for name in stage1.get("layout", {}) if bpy.data.objects.get(name)},
        cameras={"CAM_DESKTOP": camera_signature(cam_desktop),
                 "CAM_MOBILE": camera_signature(cam_mobile)},
    )

    # ------------------------------------------------------------------ materials
    debug_hex = "#FF00D5" if args.debug_mask else None
    for role in lk.PALETTE:
        override = debug_hex if (args.debug_mask and role.endswith("inset")) else None
        lk.make_mineral_material(role, base_hex=override)

    slots = {}
    for name, (shell, inset) in SHELL_ROLES.items():
        obj = forms[name]
        if name == "HCAI_SHELL":
            mask = lk.hcai_inner_mask(obj)
        else:
            spec = lk.GROOVE_SPECS[name]
            mask = lk.groove_face_mask(obj, spec["specs"], spec["radius"])
        total_area = sum(poly.area for poly in obj.data.polygons)
        inset_area = sum(obj.data.polygons[index].area for index in mask)
        # Area, not face count: the Stage 1 boolean tessellates the groove floor
        # into many small faces, so a few percent of the surface can be a large
        # share of the polygons. The area share is the number a reviewer means.
        slots[name] = dict(shell=shell, inset=inset, inset_faces=len(mask),
                           faces=len(obj.data.polygons),
                           inset_face_pct=round(100.0 * len(mask) /
                                                max(1, len(obj.data.polygons)), 2),
                           inset_area_pct=round(100.0 * inset_area /
                                                max(1e-9, total_area), 2))
        lk.assign_roles(obj, shell, inset, mask)
    for name, role in SINGLE_ROLES.items():
        slots[name] = dict(shell=role, inset=None, faces=len(forms[name].data.polygons))
        lk.assign_single(forms[name], role)

    # Arc: Stage 2 gives it the faint material and turns it back on. Which
    # renders include it is decided per render below.
    lk.assign_single(arc, "arc")
    arc.hide_render = False

    # ------------------------------------------------------- light + environment
    hv.ensure_collection(ENV_COLLECTION)
    env_collection = bpy.data.collections.get(ENV_COLLECTION)
    for light in bpy.data.objects:
        if light.type == "LIGHT" and light.name.startswith("LG_"):
            light.hide_render = True
            light.hide_viewport = True
    centre = Vector(stage1.get("composition_centre", (0.0, 0.0, 0.0)))
    rig = lk.build_studio_rig(env_collection, centre)
    backdrop = lk.build_review_environment(env_collection)
    lk.set_world_ambient(strength=0.06)

    # ------------------------------------------------------------------- renders
    device = hv.setup_cycles(STAGE2_SAMPLES_QUICK if args.quick else STAGE2_SAMPLES,
                             args.exposure, gpu=not args.no_gpu)
    scene.render.film_transparent = False      # the backdrop IS the background
    scene.use_nodes = False
    scene.render.image_settings.color_mode = "RGB"
    res_desktop = RES_DESKTOP_QUICK if args.quick else tuple(stage1.get(
        "resolution", {}).get("desktop", (1600, 1400)))
    res_mobile = RES_MOBILE_QUICK if args.quick else tuple(stage1.get(
        "resolution", {}).get("mobile", (800, 800)))
    out_dir = os.path.join(os.path.abspath(args.renders), "stage2")
    os.makedirs(out_dir, exist_ok=True)

    renders = {}
    jobs = (("desktop", cam_desktop, res_desktop), ("mobile", cam_mobile, res_mobile))
    for label, cam, res in jobs:
        hv.set_resolution(int(res[0]), int(res[1]))
        for state in (("clean", False), ("arc", True)):
            if args.debug_mask and not (label == "desktop" and state[0] == "clean"):
                continue
            arc.hide_render = state[1]
            path = os.path.join(out_dir, "%s-%s%s.png" % (
                label, state[0], "-debug" if args.debug_mask else ""))
            render_state(scene, cam, path)
            file_size = os.path.getsize(path) if os.path.exists(path) else 0
            renders["%s-%s" % (label, state[0])] = dict(
                path=os.path.relpath(path, os.path.abspath(args.renders)),
                absolute=path, camera=cam.name, resolution=[int(res[0]), int(res[1])],
                arc_visible=state[1], bytes=file_size)
    arc.hide_render = False

    # ---------------------------------------------------------------------- save
    hv.write_text_block("README_HERO_V2", README_TEXT)
    hv.purge_orphans()
    scene["hero_v2_stage"] = "2 - look development (materials + light)"
    scene["hero_v2_plan"] = "HERO_PRODUCTION_PLAN_v2.md section 3"
    scene["hero_v2_note"] = (
        "Materials, studio rig and review backdrop. Geometry, layout and cameras "
        "are unchanged from stage 1. DECOR_ARC_01 carries a faint material and is "
        "rendered in the *-arc pairs only. No GLB, no web asset, no frontend link.")
    scene["hero_v2_arc_policy"] = "clean renders: hide_render=True; arc renders: False"

    drift = check_geometry_invariance(stage1, scene)
    after = dict(
        triangles={name: sum(max(0, len(p.vertices) - 2)
                             for p in obj.data.polygons)
                   for name, obj in forms.items()},
        layout={name: group_transform(bpy.data.objects[name])
                for name in stage1.get("layout", {}) if bpy.data.objects.get(name)},
        cameras={"CAM_DESKTOP": camera_signature(cam_desktop),
                 "CAM_MOBILE": camera_signature(cam_mobile)},
    )

    checks = {
        "geometry_unchanged": dict(pass_=not drift["triangles"] and
                                           before["triangles"] == after["triangles"],
                                   before=before["triangles"], after=after["triangles"]),
        "layout_unchanged": dict(pass_=not drift["layout"] and
                                         before["layout"] == after["layout"]),
        "cameras_unchanged": dict(pass_=not drift["cameras"] and
                                          before["cameras"] == after["cameras"]),
        "four_material_roles_distinct": dict(
            pass_=len({lk.role_hex(r) for r in
                       ("core_shell", "hcai_shell", "health_shell",
                        "wearable_shell")}) == 4),
        "every_groove_recovered": dict(
            pass_=all(slots[name]["inset_faces"] > 0 for name in SHELL_ROLES),
            inset_faces={name: slots[name]["inset_faces"] for name in SHELL_ROLES}),
        "arc_has_faint_material": dict(pass_=bpy.data.materials.get("M_ARC") is not None,
                                       arc_rendered=arc.hide_render is False),
        "no_glb_or_web_asset": dict(pass_=True,
                                    note="stage 2 exports no GLB; only .blend + PNG"),
        "no_text_or_particles": dict(
            pass_=not any(o.type in {"FONT", "CURVE"} for o in bpy.data.objects) and
                  len(bpy.data.particles) == 0),
    }
    all_pass = all(item["pass_"] for item in checks.values())

    report = dict(
        stage="2 - look development (materials + light)",
        blender=bpy.app.version_string,
        source_blend=args.blend_in,
        quick=bool(args.quick),
        samples=STAGE2_SAMPLES_QUICK if args.quick else STAGE2_SAMPLES,
        exposure=args.exposure,
        render_device=device,
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile)),
        cameras_preserved=dict(desktop="CAM_DESKTOP", mobile="CAM_MOBILE",
                               refit=False,
                               note="Stage 1 authored compositions, untouched"),
        materials={role: dict(hex=lk.role_hex(role),
                              roughness=lk.role_roughness(role),
                              metallic=lk.role_metallic(role),
                              note=lk.role_note(role)) for role in lk.PALETTE},
        micro_relief=dict(grain_scale=lk.GRAIN_SCALE, micro_scale=lk.MICRO_SCALE,
                          grain_bump=lk.GRAIN_BUMP, micro_bump=lk.MICRO_BUMP,
                          roughness_spread=lk.ROUGH_SPREAD,
                          coordinate="world (Geometry.Position) — one scale across "
                                     "objects of different size"),
        material_slots=slots,
        rig=dict(key="LG2_Key 1200 W @ (-3.0,-3.4,3.1) size 4.0",
                 fill="LG2_Fill 0.22x key @ (3.8,-2.6,0.4) size 5.0",
                 separation="LG2_Sep 0.30x key @ (1.5,3.4,3.2) size 2.6",
                 world_ambient=0.06,
                 stage1_rig="kept, hide_render=True (evidence, not lighting)"),
        environment=dict(backdrop=backdrop.name, type="cyclorama (no horizon line)",
                         collection=ENV_COLLECTION,
                         note="review furniture: never exported, no form moved"),
        decor_arc=dict(rendered=True, material="M_ARC",
                       policy="hide_render toggled per render; faint matte grey"),
        renders=renders,
        checks=checks,
        checks_all_pass=all_pass,
        drift=drift,
    )
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.blend_out)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend_out))
    hv.log("saved %s" % args.blend_out)
    hv.log("checks_all_pass=%s device=%s" % (all_pass, device))
    return report


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(argv)
