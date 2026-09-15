# build_hero_v2_graybox.py -- STAGE 1 of HERO_PRODUCTION_PLAN_v2.md: graybox composition.
#
# SCOPE (deliberately narrow):
#   * one central identity core + three companion research-axis spheres
#   * organic premium editorial composition, large negative space,
#     soft asymmetrical balance
#   * two cameras (desktop perspective 70mm / mobile orthographic)
#   * ONE neutral preview clay + a simple neutral three-light preview rig
#   * two preview renders
#
# NOT in scope for this pass: final materials, procedural or image textures,
# final theme lighting, WebP derivatives, frontend wiring. See the plan's
# section 3 for the four material roles and section 4 for the final render list.
#
# Geometry contract (plan section 3):
#   core diameter 1.45 BU, every companion 1.00 BU, equal rank, AND the
#   companions sit above-left / right / below-left of a core that is slightly
#   forward, with visible gaps between silhouettes.
#
# Safety: never calls bpy.ops.wm.read_factory_settings(). Writes only the paths
# passed on the command line.
#
# Usage:
#   "<blender.exe>" --background --python build_hero_v2_graybox.py -- \
#     --blend <hero-v2-graybox.blend> --renders <dir> --report <json> \
#     [--quick] [--skip-renders] [--no-gpu]
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hero_v2_common as hv  # noqa: E402  (Blender needs the path first)

# --------------------------------------------------------------------- contract
CORE_DIAMETER = 1.45        # plan section 3: the identity core
DOMAIN_DIAMETER = 1.00      # plan section 3: every companion, equal in rank
CORE_RADIUS = CORE_DIAMETER * 0.5
DOMAIN_RADIUS = DOMAIN_DIAMETER * 0.5

HCAI_AXIS = Vector((0.84, -0.48, 0.25)).normalized()   # faces forward-right
HCAI_APERTURE_HEIGHT = 0.31 * (DOMAIN_RADIUS / 0.5)    # generous, still a shell
HCAI_WALL = 0.052
HCAI_INSET_RADIUS = 0.160
HCAI_INSET_DEPTH = 0.100
# Slide the inset OFF the aperture axis. A ball centred in a circular opening is
# an eyeball; a form resting off to one side of the cavity is a designed recess.
HCAI_INSET_OFFSET = -0.090

CORE_SEAM_DEPTH = 0.026         # one recessed seam (1.8% of diameter: reads at page size)
CORE_SEAM_TILT = (22.0, 0.0, -34.0)   # NOT equatorial: no planetary equator
CORE_ACCENT_PARAM = -22.0       # where on the seam the accent detail sits
CORE_ACCENT_RADIUS = 0.085      # WIDE and flat: an inlay, not a button

# Two shallow contours: one swept near-great circle plus one crown-ring contour.
# The second carries its own tilt so the two planes differ by ~29 degrees -- with
# only ~16 degrees they project as a parallel pair and read as planetary latitude
# lines. Both are gated on DRAWN length, not just on facing the camera.
HHB_CONTOURS = ((90.0, 0.019, (16.0, 0.0, 12.0)),
                (54.0, 0.016, (-14.0, 0.0, -22.0)))
# Three broad segments. The two grooves carry DIFFERENT tilts, so the three
# segments are not stacked bands. Selected because both grooves keep a long
# camera-facing span (checked by contour_visible_span) while never crossing.
WE_SEGMENTS = ((62.0, 0.045, (18.0, 0.0, 20.0)),
               (118.0, 0.038, (10.0, 0.0, -34.0)))

# Soft asymmetrical balance. X = right, Y = away from the camera, Z = up.
# Companions above-left / right / below-left around a core that sits slightly
# forward (-Y). Spacing is deliberately IRREGULAR so the diamond reads as an
# authored composition rather than a symmetric hub. Gaps are verified
# numerically further down, never by eye.
LAYOUT = {
    "GRP_CORE": (-0.06, -0.22, -0.04),
    "GRP_HUMAN_CENTERED_AI": (-1.28, 0.30, 1.00),
    "GRP_HEALTH_BEHAVIOR": (1.52, 0.10, 0.34),
    "GRP_WEARABLE_EDGE": (-0.80, 0.44, -1.46),
}
LAYOUT_ROT_DEG = {
    "GRP_CORE": (0.0, 0.0, 0.0),
    "GRP_HUMAN_CENTERED_AI": (0.0, 0.0, 0.0),
    "GRP_HEALTH_BEHAVIOR": (0.0, 0.0, -14.0),
    "GRP_WEARABLE_EDGE": (-6.0, 8.0, 0.0),
}

# The single decorative arc the plan allows ("at most one faint, incomplete
# orbital arc ... without endpoints or arrowheads"). It is authored with a
# tapered tube so it reads as a drawn gesture, but it is NOT rendered in this
# graybox pass: "faint" is a material property and no materials exist yet.
ARC_RADIUS = 2.60
ARC_SWEEP_DEG = 118.0
ARC_TUBE_MAX = 0.010
ARC_CENTER = (0.35, 2.05, 0.10)
ARC_ROT_DEG = (76.0, 0.0, -28.0)
ARC_CLEARANCE_MIN = 0.05        # world units, verified against every form

VIEW_DIR_DESKTOP = Vector((math.sin(math.radians(-6.0)) * math.cos(math.radians(7.0)),
                           math.cos(math.radians(-6.0)) * math.cos(math.radians(7.0)),
                           -math.sin(math.radians(7.0)))).normalized()
VIEW_DIR_MOBILE = Vector((math.sin(math.radians(-6.0)) * math.cos(math.radians(4.0)),
                          math.cos(math.radians(-6.0)) * math.cos(math.radians(4.0)),
                          -math.sin(math.radians(4.0)))).normalized()

RES_DESKTOP = (1600, 1400)
RES_MOBILE = (800, 800)
RES_DESKTOP_QUICK = (800, 700)
RES_MOBILE_QUICK = (400, 400)
MARGIN_DESKTOP = 0.08           # plan: >= 8% clear space at the image edges
MARGIN_MOBILE = 0.04            # plan: a TIGHTER diamond on mobile

SAMPLES = 160
SAMPLES_QUICK = 24
# AgX holds the highlights, so a mid-grey clay still renders bright against the
# #f7f8f5 page. The exposure is the knob that actually moves the form median away
# from the canvas; --exposure overrides it for look-dev.
PREVIEW_EXPOSURE = -0.9

CANVAS_LIGHT = "#f7f8f5"        # plan section 3 palette, Light page canvas

# plan section 6: the narrowest real page size the artwork is judged at
DESKTOP_SLOT_HEIGHT_PX = 600.0
MOBILE_SLOT_HEIGHT_PX = 288.0
MIN_GAP_ON_PAGE_PX = 12.0
MIN_CONTOUR_SPAN_DEG = 100.0    # below this a groove has effectively turned away
MIN_CONTOUR_DRAWN_LENGTH = 1.10  # projected length, in sphere-radii

CLAY_NAME = "PREVIEW_CLAY"
# Mid-grey placeholder. A pale clay on the #f7f8f5 Light page canvas renders with
# the form median only ~25 levels below the background, which hides exactly the
# silhouette this pass has to prove. Measured after the change, not assumed.
CLAY_BASE = (0.330, 0.325, 0.316, 1.0)
CLAY_ROUGH = 0.45

LIGHT_COLLECTION = "Rig_PreviewNeutral"
CAM_COLLECTION = "Cameras"


# ------------------------------------------------------------------ form builders
def seam_direction(rotation_deg, t_deg):
    """A unit direction that lands ON the core's seam circle.

    The accent detail is anchored to the seam so it reads as an intentional
    interruption of that line instead of a bump that happens to be nearby.
    """
    rot = Euler(tuple(math.radians(a) for a in rotation_deg), "XYZ").to_matrix()
    t = math.radians(t_deg)
    return (rot @ Vector((math.cos(t), math.sin(t), 0.0))).normalized()


def build_core(coll):
    """Soft mineral sphere + one recessed seam + a restrained accent detail."""
    sphere = hv.new_uv_sphere("CORE_SPHERE", CORE_RADIUS)
    hv.link_to(sphere, coll)

    # One recessed seam, cut by a torus whose tube-centre circle lies exactly on
    # the sphere surface, then tilted well away from the equator.
    tool = hv.spherical_groove_tool("CUT_CORE_SEAM", CORE_RADIUS, 90.0,
                                    CORE_SEAM_DEPTH, CORE_SEAM_TILT)
    hv.boolean_difference(sphere, tool)
    hv.clean_mesh(sphere)
    # Soften the crease: an 89-degree groove wall reads as machined, not mineral.
    hv.add_bevel(sphere, 0.006, 3, 35.0)

    # Broad organic deformation (2-4% of diameter) so it stops reading as a
    # primitive, plus a gentle flattening for a resting-pebble feel.
    hv.radial_harmonic_deform(sphere, 0.024, 0.017)
    hv.scale_verts(sphere, 1.0, 0.988, 0.973)
    hv.shade_smooth_by_angle(sphere, 38.0)
    hv.normalize_group([sphere], CORE_DIAMETER)

    # Accent detail: a shallow domed inlay straddling the seam, sitting just
    # proud of the surface. Ray-cast against the FINISHED surface so it can
    # never float or sink.
    direction = seam_direction(CORE_SEAM_TILT, CORE_ACCENT_PARAM)
    hit, loc, _nrm, _idx = sphere.ray_cast(Vector((0.0, 0.0, 0.0)), direction)
    if not hit:
        raise RuntimeError("CORE accent ray-cast missed the core surface")
    bead = hv.new_uv_sphere("CORE_ACCENT", CORE_ACCENT_RADIUS, segments=64,
                            rings=38)
    hv.link_to(bead, coll)
    hv.scale_verts(bead, 1.0, 1.0, 0.22)
    hv.shade_smooth_by_angle(bead, 50.0)
    bead.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    hv.deselect_all()
    hv.set_active(bead)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    # `loc` is the groove FLOOR, so lift by the groove depth first.
    hv.translate_verts(bead, loc + direction * (CORE_SEAM_DEPTH - 0.012))
    hv.log("core accent on seam at %s (dir %s)"
           % ([round(v, 4) for v in loc], [round(v, 3) for v in direction]))
    return [sphere, bead]


def build_human_centered_ai(coll):
    """Rounded shell with one generous opening around an inset form."""
    shell = hv.new_uv_sphere("HCAI_SHELL", DOMAIN_RADIUS)
    hv.link_to(shell, coll)
    hv.bisect_remove_cap(shell, HCAI_AXIS * HCAI_APERTURE_HEIGHT, HCAI_AXIS)
    hv.add_solidify(shell, HCAI_WALL, offset=-1.0)
    hv.add_bevel(shell, 0.007, 3, 40.0)
    hv.radial_harmonic_deform(shell, 0.016, 0.011)
    hv.shade_smooth_by_angle(shell, 38.0)
    hv.normalize_group([shell], DOMAIN_DIAMETER)

    inset = hv.new_uv_sphere("HCAI_INSET", HCAI_INSET_RADIUS, segments=64, rings=40)
    hv.link_to(inset, coll)
    hv.radial_harmonic_deform(inset, 0.020, 0.014)
    hv.shade_smooth_by_angle(inset, 50.0)
    # "Up" inside the aperture plane, so the offset is a slide across the opening.
    up = Vector((0.0, 0.0, 1.0)) - HCAI_AXIS * HCAI_AXIS.dot(Vector((0.0, 0.0, 1.0)))
    up.normalize()
    hv.translate_verts(inset, HCAI_AXIS * HCAI_INSET_DEPTH + up * HCAI_INSET_OFFSET)
    return [shell, inset]


def build_health_behavior(coll):
    """Smooth sphere with two shallow contours following its volume."""
    sphere = hv.new_uv_sphere("HHB_SPHERE", DOMAIN_RADIUS)
    hv.link_to(sphere, coll)
    for index, (colatitude, width, rotation) in enumerate(HHB_CONTOURS, start=1):
        tool = hv.spherical_groove_tool("CUT_HHB_%d" % index, DOMAIN_RADIUS,
                                        colatitude, width, rotation)
        hv.boolean_difference(sphere, tool)
    hv.clean_mesh(sphere)
    hv.add_bevel(sphere, 0.004, 2, 35.0)
    hv.radial_harmonic_deform(sphere, 0.012, 0.008)
    hv.shade_smooth_by_angle(sphere, 38.0)
    hv.normalize_group([sphere], DOMAIN_DIAMETER)
    return [sphere]


def build_wearable_edge(coll):
    """Compact sphere divided into three broad, rounded segments."""
    sphere = hv.new_uv_sphere("WE_SPHERE", DOMAIN_RADIUS)
    hv.link_to(sphere, coll)
    for index, (colatitude, width, rotation) in enumerate(WE_SEGMENTS, start=1):
        tool = hv.spherical_groove_tool("CUT_WE_%d" % index, DOMAIN_RADIUS,
                                        colatitude, width, rotation)
        hv.boolean_difference(sphere, tool)
    hv.clean_mesh(sphere)
    hv.add_bevel(sphere, 0.006, 3, 35.0)
    # "Compact": a small flattening plus a faint organic offset, <= 4% of diameter.
    hv.radial_harmonic_deform(sphere, 0.010, 0.007)
    hv.scale_verts(sphere, 1.0, 0.978, 0.962)
    hv.shade_smooth_by_angle(sphere, 38.0)
    hv.normalize_group([sphere], DOMAIN_DIAMETER)
    return [sphere]


# ------------------------------------------------------------------------ scene
def build_material():
    mat = bpy.data.materials.get(CLAY_NAME)
    if mat is None:
        mat = bpy.data.materials.new(CLAY_NAME)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = CLAY_BASE
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = CLAY_ROUGH
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.45
    return mat


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def build_forms(coll):
    """Build all four forms centred on the world origin, then place the groups."""
    mat = build_material()
    groups = {
        "GRP_CORE": build_core(coll),
        "GRP_HUMAN_CENTERED_AI": build_human_centered_ai(coll),
        "GRP_HEALTH_BEHAVIOR": build_health_behavior(coll),
        "GRP_WEARABLE_EDGE": build_wearable_edge(coll),
    }
    for objs in groups.values():
        for obj in objs:
            assign(obj, mat)

    empties = {}
    for name, objs in groups.items():
        empty = hv.make_empty(name)
        for obj in objs:
            obj.parent = empty          # empty is still at the origin: no jump
        empties[name] = empty

    # Only now move the group empties into the composition.
    for name, empty in empties.items():
        empty.location = LAYOUT[name]
        empty.rotation_euler = Euler(
            tuple(math.radians(a) for a in LAYOUT_ROT_DEG[name]), "XYZ")
    bpy.context.view_layer.update()
    for name, empty in empties.items():
        hv.link_to(empty, coll)
    return groups, empties


def build_decor(coll):
    arc = hv.tapered_arc("DECOR_ARC_01", ARC_RADIUS, ARC_SWEEP_DEG, ARC_TUBE_MAX,
                         tube_min_ratio=0.10)
    hv.link_to(arc, coll)
    mat = bpy.data.materials.get(CLAY_NAME)
    if mat is not None:
        arc.data.materials.append(mat)
    arc.location = ARC_CENTER
    arc.rotation_euler = Euler(
        tuple(math.radians(a) for a in ARC_ROT_DEG), "XYZ")
    # Authored, but excluded from the graybox render: see the module docstring.
    arc.hide_render = True
    arc.hide_viewport = False
    return arc


def build_lights(target):
    coll = hv.ensure_collection(LIGHT_COLLECTION)
    centre = Vector(target)
    # plan section 3: three broad area lights, key above/front from the left,
    # soft fill from the right, restrained rear rim; 1 : 0.3 : 0.35.
    # Neutral white ONLY in this pass -- colour and levels belong to stage 2.
    # The KEY is scaled up and the ambient pulled right down so the forms read
    # sculpturally at a glance; a flatly lit graybox cannot be judged as a
    # premium composition.
    key_energy = 1400.0
    key = hv.add_area_light("LG_Key", key_energy, (1.0, 1.0, 1.0),
                            centre + Vector((-3.2, -3.2, 3.0)), 3.4, centre, coll)
    fill = hv.add_area_light("LG_Fill", key_energy * 0.30, (1.0, 1.0, 1.0),
                             centre + Vector((3.6, -2.6, 0.7)), 3.0, centre, coll)
    rim = hv.add_area_light("LG_Rim", key_energy * 0.35, (1.0, 1.0, 1.0),
                            centre + Vector((1.4, 3.6, 2.6)), 2.2, centre, coll)
    return [key, fill, rim]


def build_world():
    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("HERO_V2_World")
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.5, 0.5, 0.5, 1.0)
    bg.inputs["Strength"].default_value = 0.03   # neutral ambient only; keep it dark
    return world


# ----------------------------------------------------------------------- checks
def contour_visible_span(colatitude_deg, rotation_deg, group_rotation_deg,
                         view_dir, radius=1.0, steps=720):
    """Angular span of a spherical contour that actually faces the camera.

    A groove only reads where its circle lies on the camera-facing hemisphere.
    The first graybox pass shipped a companion whose second contour had swung
    round to the back and vanished; measuring the span catches that before a
    render is spent on it. The direction is scale-invariant, so radius is 1.
    """
    rot = Euler(tuple(math.radians(a) for a in rotation_deg), "XYZ").to_matrix()
    grp = Euler(tuple(math.radians(a) for a in group_rotation_deg), "XYZ").to_matrix()
    m = grp @ rot
    phi0 = math.radians(colatitude_deg)
    a = radius * math.sin(phi0)
    h = radius * math.cos(phi0)
    to_cam = -Vector(view_dir).normalized()
    hits = 0
    for i in range(steps):
        t = 2.0 * math.pi * i / steps
        p = m @ Vector((a * math.cos(t), a * math.sin(t), h))
        if p.normalized().dot(to_cam) > 0.0:
            hits += 1
    return 360.0 * hits / steps


def contour_screen_length(colatitude_deg, rotation_deg, group_rotation_deg,
                          view_dir, radius=1.0, steps=720):
    """Projected length of the DRAWN part of a spherical contour, in sphere-radii.

    Visibility alone is not legibility: a groove high on the sphere can face the
    camera and still foreshorten to almost nothing (a cap ring at colatitude 36
    scored 199 degrees visible and was invisible in the render). This measures
    what actually lands on screen. Orthographic approximation -- the camera is
    far enough that it ranks candidate designs correctly.
    """
    rot = Euler(tuple(math.radians(a) for a in rotation_deg), "XYZ").to_matrix()
    grp = Euler(tuple(math.radians(a) for a in group_rotation_deg), "XYZ").to_matrix()
    m = grp @ rot
    phi0 = math.radians(colatitude_deg)
    a = radius * math.sin(phi0)
    h = radius * math.cos(phi0)
    view = Vector(view_dir).normalized()
    to_cam = -view
    perp = view.cross(Vector((0.0, 0.0, 1.0)))
    if perp.length < 1e-6:
        perp = Vector((1.0, 0.0, 0.0))
    perp.normalize()
    up = perp.cross(view).normalized()
    total, prev = 0.0, None
    for i in range(steps + 1):
        t = 2.0 * math.pi * (i % steps) / steps
        p = m @ Vector((a * math.cos(t), a * math.sin(t), h))
        p = p.normalized()          # the sphere's outward normal at that point
        if p.dot(to_cam) <= 0.0:
            prev = None
            continue
        s = (p.dot(perp), p.dot(up))
        if prev is not None:
            total += math.hypot(s[0] - prev[0], s[1] - prev[1])
        prev = s
    return total


def contract_checks(groups):
    checks = {}
    for name, objs in groups.items():
        target = CORE_DIAMETER if name == "GRP_CORE" else DOMAIN_DIAMETER
        measured = hv.group_diameter(objs)
        checks["diameter:%s" % name] = dict(
            target=target, measured=round(measured, 4),
            pass_=abs(measured - target) <= 5e-3)
    banned = dict(
        text_objects=[o.name for o in bpy.data.objects if o.type == "FONT"],
        particle_systems=[o.name for o in bpy.data.objects if o.particle_systems],
        grease_pencil=[o.name for o in bpy.data.objects
                       if o.type in ("GPENCIL", "GREASEPENCIL")])
    checks["no_text_labels_particles_or_panels"] = dict(
        found=banned, pass_=not any(banned.values()))
    modifiers = [o.name for o in bpy.data.objects if o.modifiers]
    checks["all_modifiers_applied"] = dict(found=modifiers, pass_=not modifiers)
    return checks


def arc_clearance(arc, groups):
    """Nearest world-space gap between the decorative arc and any form's surface."""
    pts = hv.evaluated_verts(arc)
    worst = None
    for name, objs in groups.items():
        for obj in objs:
            d = hv.min_distance_to_object(obj, pts)
            if worst is None or d < worst[0]:
                worst = (d, obj.name)
    return worst


# ------------------------------------------------------------------------- main
def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--renders", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--skip-renders", action="store_true")
    parser.add_argument("--no-gpu", action="store_true")
    parser.add_argument("--exposure", type=float, default=PREVIEW_EXPOSURE,
                        help="view-transform exposure for the preview pass")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    hv.log("blender %s" % bpy.app.version_string)
    hv.clear_scene()

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    forms_coll = hv.ensure_collection("HERO_V2_FORMS")
    groups, empties = build_forms(forms_coll)
    arc = build_decor(forms_coll)
    root = hv.make_empty("HERO_V2_ROOT")
    hv.link_to(root, forms_coll)
    for empty in empties.values():
        empty.parent = root

    # Lights and cameras frame the composition, so derive the centre from it.
    all_forms = [o for objs in groups.values() for o in objs]
    lo, hi = hv.world_bounds(all_forms)
    centre = (lo + hi) * 0.5
    hv.log("world bounds lo=%s hi=%s size=%s"
           % ([round(v, 3) for v in lo], [round(v, 3) for v in hi],
              [round(v, 3) for v in (hi - lo)]))
    bpy.context.view_layer.update()
    build_world()
    build_lights(centre)

    cam_coll = hv.ensure_collection(CAM_COLLECTION)
    res_desktop = RES_DESKTOP_QUICK if args.quick else RES_DESKTOP
    res_mobile = RES_MOBILE_QUICK if args.quick else RES_MOBILE

    cam_desktop = hv.make_camera("CAM_DESKTOP", VIEW_DIR_DESKTOP, 9.0, centre,
                                 "PERSP", lens=70.0)
    hv.link_to(cam_desktop, cam_coll)
    cam_mobile = hv.make_camera("CAM_MOBILE", VIEW_DIR_MOBILE, 12.0, centre,
                                "ORTHO")
    hv.link_to(cam_mobile, cam_coll)

    desktop_fit = hv.fit_camera(cam_desktop, groups, VIEW_DIR_DESKTOP, centre,
                                MARGIN_DESKTOP, *res_desktop)
    mobile_fit = hv.fit_camera(cam_mobile, groups, VIEW_DIR_MOBILE, centre,
                               MARGIN_MOBILE, *res_mobile)
    hv.log("desktop fit %s" % desktop_fit)
    hv.log("mobile  fit %s" % mobile_fit)

    composition = {
        "desktop": hv.composition_report(cam_desktop, groups, *res_desktop),
        "mobile": hv.composition_report(cam_mobile, groups, *res_mobile),
    }
    for key, slot in (("desktop", DESKTOP_SLOT_HEIGHT_PX),
                      ("mobile", MOBILE_SLOT_HEIGHT_PX)):
        page_px = composition[key]["min_silhouette_gap_px"] * (
            slot / composition[key]["resolution"][1])
        composition[key]["min_gap_scaled_to_page_px"] = round(page_px, 1)
        composition[key]["slot_height_px"] = slot

    checks = contract_checks(groups)
    contour_spans = {}
    for label, contours, group_name in (
            ("CORE_SEAM", [(90.0, CORE_SEAM_TILT)], "GRP_CORE"),
            ("HHB_CONTOURS", [(c[0], c[2]) for c in HHB_CONTOURS],
             "GRP_HEALTH_BEHAVIOR"),
            ("WE_GROOVES", [(c[0], c[2]) for c in WE_SEGMENTS],
             "GRP_WEARABLE_EDGE")):
        spans = [round(contour_visible_span(c, r, LAYOUT_ROT_DEG[group_name],
                                            VIEW_DIR_DESKTOP), 1)
                 for c, r in contours]
        lengths = [round(contour_screen_length(c, r, LAYOUT_ROT_DEG[group_name],
                                               VIEW_DIR_DESKTOP), 3)
                   for c, r in contours]
        contour_spans[label] = dict(spans_deg=spans, drawn_length_radii=lengths)
        checks["contour_visible_span:%s" % label] = dict(
            spans_deg=spans, drawn_length_radii=lengths,
            required_deg=MIN_CONTOUR_SPAN_DEG,
            required_length=MIN_CONTOUR_DRAWN_LENGTH,
            pass_=(all(s >= MIN_CONTOUR_SPAN_DEG for s in spans)
                   and all(x >= MIN_CONTOUR_DRAWN_LENGTH for x in lengths)))
    # A "generous opening" that never reaches the outline still leaves a plain
    # circle in silhouette. The rim touches the silhouette only once the
    # aperture axis is far enough away from the camera direction.
    rim_half_angle = math.degrees(math.acos(HCAI_APERTURE_HEIGHT / DOMAIN_RADIUS))
    axis_angle = math.degrees(math.acos(
        HCAI_AXIS.dot(-VIEW_DIR_DESKTOP.normalized())))
    checks["hcai_aperture_breaks_silhouette"] = dict(
        rim_half_angle_deg=round(rim_half_angle, 1),
        axis_from_camera_deg=round(axis_angle, 1),
        required_deg=round(90.0 - rim_half_angle, 1),
        pass_=axis_angle > 90.0 - rim_half_angle)
    clear = arc_clearance(arc, groups)
    checks["decor_arc_clearance"] = dict(
        measured=round(clear[0], 4), nearest=clear[1],
        pass_=clear[0] >= ARC_CLEARANCE_MIN)
    for key in ("desktop", "mobile"):
        checks["edge_clearance:%s" % key] = dict(
            required_pct=round((MARGIN_DESKTOP if key == "desktop"
                                else MARGIN_MOBILE) * 100.0, 2),
            measured_pct=composition[key]["edge_clearance_pct"],
            pass_=min(composition[key]["edge_clearance_pct"].values())
            >= (MARGIN_DESKTOP if key == "desktop" else MARGIN_MOBILE) * 100.0 - 0.5)
        checks["silhouette_gap_on_page:%s" % key] = dict(
            required_px=MIN_GAP_ON_PAGE_PX,
            measured_px=composition[key]["min_gap_scaled_to_page_px"],
            pass_=composition[key]["min_gap_scaled_to_page_px"] >= MIN_GAP_ON_PAGE_PX)

    for name, result in sorted(checks.items()):
        hv.log("check %-34s %s" % (name, "PASS" if result["pass_"] else "FAIL"))

    stats = {}
    for group, objs in sorted(groups.items()):
        for obj in objs:
            stats[obj.name] = hv.mesh_stats(obj)
    total_tris = sum(s["triangles"] for s in stats.values())

    renders = {}
    if not args.skip_renders:
        device = hv.setup_cycles(SAMPLES_QUICK if args.quick else SAMPLES,
                                 args.exposure, gpu=not args.no_gpu)
        hv.log("cycles device: %s" % device)
        for key, cam, res in (("desktop", cam_desktop, res_desktop),
                              ("mobile", cam_mobile, res_mobile)):
            hv.set_resolution(*res)
            base = os.path.join(args.renders, "graybox-%s" % key)
            hv.render_transparent(base + "-alpha.png", cam)
            renders[key] = dict(resolution=list(res), cam=cam.name,
                                transparent=base + "-alpha.png",
                                on_canvas=base + ".png")
        renders["device"] = device
        hv.log("next step (system python + Pillow): composite_previews.py "
               "--renders %s --hex %s" % (args.renders, CANVAS_LIGHT))

    hv.write_text_block("README_HERO_V2", README_TEXT)
    hv.purge_orphans()
    scene["hero_v2_stage"] = "1 - graybox composition"
    scene["hero_v2_plan"] = "HERO_PRODUCTION_PLAN_v2.md section 3"
    scene["hero_v2_note"] = (
        "Graybox only. One neutral preview clay, one neutral preview rig. "
        "DECOR_ARC_01 exists but is excluded from renders until stage 2 gives it "
        "a faint material. Materials, textures and final theme lighting are not "
        "authored yet.")

    report = dict(
        stage="1 - graybox composition",
        blender=bpy.app.version_string,
        resolution=dict(desktop=list(res_desktop), mobile=list(res_mobile)),
        quick=bool(args.quick),
        samples=SAMPLES_QUICK if args.quick else SAMPLES,
        layout=LAYOUT,
        layout_rotation_deg=LAYOUT_ROT_DEG,
        layout_rationale=("core slightly forward (-Y); companions above-left, "
                          "right and below-left; visible gaps verified in pixels"),
        material=dict(name=CLAY_NAME, base=list(CLAY_BASE), roughness=CLAY_ROUGH,
                      role="neutral preview placeholder - NOT a final material"),
        exposure=args.exposure,
        rig="neutral three-light preview (key/fill/rim = 1 : 0.30 : 0.35)",
        composition_centre=[round(v, 4) for v in centre],
        world_bounds=dict(lo=[round(v, 4) for v in lo], hi=[round(v, 4) for v in hi],
                          size=[round(v, 4) for v in (hi - lo)]),
        fits=dict(desktop=desktop_fit, mobile=mobile_fit),
        composition=composition,
        contour_visible_span_deg=contour_spans,
        checks=checks,
        checks_all_pass=all(c["pass_"] for c in checks.values()),
        geometry=stats,
        total_triangles=total_tris,
        decor_arc=dict(name=arc.name, rendered=False,
                       reason=("'faint' is a material property; no materials "
                               "exist in stage 1")),
        renders=renders,
    )
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)

    os.makedirs(os.path.dirname(os.path.abspath(args.blend)), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.blend))
    hv.log("saved %s" % args.blend)
    hv.log("checks_all_pass=%s total_triangles=%d"
           % (report["checks_all_pass"], total_tris))
    return report


README_TEXT = """HERO V2 -- hero-v2-graybox.blend (STAGE 1)

Stage 1 of HERO_PRODUCTION_PLAN_v2.md section 3: graybox composition only.
There are NO final materials, NO textures and NO theme lighting in this file.

SCENE
  HERO_V2_ROOT
    GRP_CORE                 CORE_SPHERE, CORE_ACCENT
    GRP_HUMAN_CENTERED_AI    HCAI_SHELL, HCAI_INSET
    GRP_HEALTH_BEHAVIOR      HHB_SPHERE
    GRP_WEARABLE_EDGE        WE_SPHERE
    DECOR_ARC_01             authored, hide_render = True (see below)

CONTRACT
  core diameter 1.45 BU, every companion 1.00 BU, companions equal in rank.
  Group empties carry the composition; the meshes themselves are centred on the
  world origin, so moving a group moves its whole form.

CAMERAS
  CAM_DESKTOP   1600x1400, perspective, 70 mm on a 36 mm sensor, 8% edge margin
  CAM_MOBILE     800x800, orthographic, tighter diamond (4% edge margin)

DECOR_ARC_01
  The plan allows "at most one faint, incomplete orbital arc". The arc is built
  and clearance-checked, but "faint" is a material property and stage 1 has no
  materials, so it is excluded from the graybox renders. Give it a faint
  material and clear hide_render in stage 2, or delete it.

MATERIAL
  PREVIEW_CLAY only. A neutral placeholder applied to every mesh so the
  composition can be judged. Replace with the plan's four material roles in
  stage 2.
"""


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
