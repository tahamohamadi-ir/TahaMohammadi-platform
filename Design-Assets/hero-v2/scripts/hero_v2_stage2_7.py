"""Hero v2 — Stage 2.7: material + relation polish (final look lock).

Stage 2.6's geometry language is approved, so this module keeps the four plain
spheres and the three real relations exactly as they are and changes only how they
are *made*: the plaster becomes a believable dielectric, the strokes become
hairlines, and the light theme gets its own pigment/roughness calibration rather
than a blanket darkening.

Three things were learned the hard way in 2.6 and are encoded here:

* **Zero specular was a dead end.** Stage 2.6 killed the dielectric response to stop
  grazing Fresnel glints from clipping. That is physically dead, and the card asks
  for a real response. The fix is a *broad* one: a plausible IOR with a high
  roughness spreads the specular lobe out until it no longer concentrates a
  highlight, plus lights that stay modest. The validator asserts both that the
  response is non-zero and that nothing clips.
* **Roughness does material work that pigment cannot.** In light mode the sage and
  violet turned pastel because their sheen was fighting the near-white page. Light
  mode therefore deepens pigment *and* raises roughness (flatter response) *and*
  uses its own rig - not one blanket multiplier.
* **Multi-scale, decorrelated.** Macro tonal drift, meso roughness patches and a
  micro normal use three different noise scales and details, deliberately
  uncorrelated so nothing reads as a repeated pattern at any size.

Geometry, composition, cameras, the mask-free sphere topology and the world/composite
architecture all come from the frozen Stage 2.6 module.
"""

from __future__ import annotations

import math

import bpy
from mathutils import Euler, Quaternion, Vector

import hero_v2_stage2_6 as base
from hero_v2_stage2_6 import _area as area_light      # frozen 2.6 studio-light helper

# ------------------------------------------------------------------- geometry
# Identical to Stage 2.6 by import, not by restatement: the deformation amplitudes
# travel from build_hero_v2_graybox through base, so the approved silhouettes cannot
# drift here.
COMPANION_RHYTHM = base.COMPANION_RHYTHM
COMPANION_SCALE = base.COMPANION_SCALE
COMPANION_SEGMENTS, COMPANION_RINGS = base.COMPANION_SEGMENTS, base.COMPANION_RINGS
CORE_SEGMENTS, CORE_RINGS = base.CORE_SEGMENTS, base.CORE_RINGS
COMPANION_DEFORM, CORE_DEFORM, CORE_FLATTEN = (base.COMPANION_DEFORM, base.CORE_DEFORM,
                                              base.CORE_FLATTEN)
SMOOTH_ANGLE_DEG = base.SMOOTH_ANGLE_DEG

# ------------------------------------------------------------- relation curves
# 49% of the Stage 2.6 tube radius (0.0075 -> 0.0037), the top of the card's 35-50%
# band. 43% measured below the visibility floor at the real 686x600 footprint for the
# thinnest stroke in light mode (a ~1.2 px anti-aliased line); 49% is the most the card
# allows and buys roughly half a device pixel of presence.
CURVE_TUBE_RADIUS = 0.0037
CURVE_TAPER = (1.00, 0.68)      # spline-point radius at the core end and the far end
CURVE_BEVEL_RESOLUTION = 3
CURVE_RESOLUTION_U = 14
# bend / lift as fractions of the chord; `depth` pushes the middle away from the
# camera (+Y) and `anchor_swing_deg` rotates the core-side anchor around the core's
# up axis so the stroke leaves from the far hemisphere and is partly occluded by the
# core - real depth instead of a flat diagram. `weight` scales the stroke's radius.
RELATIONS = {
    # `arrival_tangent` tilts the end handle sideways so the stroke meets its
    # companion at a grazing angle instead of head-on. A bond is inserted radially
    # into a ball; a line that arrives at an angle reads as drawn. Signs and
    # magnitudes differ per stroke so no two arcs mirror each other.
    "GRP_HUMAN_CENTERED_AI": dict(bend=+0.095, lift=+0.060, depth=+0.020,
                                  anchor_swing_deg=0.0, weight=1.00,
                                  arrival_tangent=+0.130),
    "GRP_HEALTH_BEHAVIOR": dict(bend=-0.070, lift=+0.035, depth=+0.035,
                                anchor_swing_deg=12.0, weight=0.85,
                                arrival_tangent=-0.100),
    # 14 degrees, not 38: a bigger swing puts the anchor so far round the far
    # hemisphere that the chord to the companion cuts INSIDE the core (measured 3x its
    # own tube radius deep). 14 degrees plus a deeper +Y bow gives the occlusion the
    # card wants - the stroke leaves from just past the core's silhouette and its
    # first stretch is hidden - without any interpenetration.
    "GRP_WEARABLE_EDGE": dict(bend=+0.050, lift=-0.075, depth=+0.045,
                              anchor_swing_deg=14.0, weight=0.70,
                              arrival_tangent=+0.090),
}

# ------------------------------------------------------------------ materials
# role: hex, roughness, roughness spread, tonal, bump, IOR, specular level, note
# Roughness sits at the matte end of the card's 0.58-0.76 suggestion; the IORs are
# the plausible dielectric range 1.42-1.50, and `specular` 0.5 is Blender's
# physically-correct F0 for that IOR (not a hand-tuned cheat).
ROLES = {
    "core_shell": ("#27565A", 0.62, 0.055, 0.10, 0.030, 1.46, 0.50,
                   "deep mineral teal; the authoritative one, slightly denser"),
    "hcai_shell": ("#6F8474", 0.71, 0.045, 0.09, 0.026, 1.43, 0.50,
                   "muted eucalyptus / mineral sage; the calm, human one"),
    "health_shell": ("#877156", 0.72, 0.055, 0.11, 0.030, 1.45, 0.50,
                     "warm sandstone / muted ochre; warm but never gold"),
    "wearable_shell": ("#6B6580", 0.68, 0.060, 0.10, 0.028, 1.44, 0.50,
                       "dusty stone violet; desaturated, never candy"),
    "relation": ("#C6B191", 0.62, 0.020, 0.04, 0.006, 1.44, 0.35,
                 "champagne / aged-brass stroke; hairline, matte-ish, no sparkle"),
}
# Multi-scale: three decorrelated fields. Macro drifts tone, meso patches roughness,
# micro adds the tactile normal.
MACRO_SCALE, MACRO_DETAIL = 1.6, 2.0
MESO_SCALE, MESO_DETAIL = 6.5, 3.0
MICRO_SCALE, MICRO_DETAIL = 22.0, 2.5
MICRO_DISTANCE = 0.004
TINT_STRENGTH = 1.07            # macro drift pulls the base colour by +/-3.5%

# Per-theme preset. Light mode is not a blanket darkening: pigment goes deeper on the
# two companions that read pastel, the whole set gains roughness (a flatter, more
# mineral response against a near-white page), and the light rig is steered harder.
THEME_PRESET = {
    "dark": dict(pigment={"core_shell": 0.97, "hcai_shell": 1.00,
                          "health_shell": 1.00, "wearable_shell": 1.00},
                 roughness_delta=0.00, stroke=1.00),
    "light": dict(pigment={"core_shell": 0.86, "hcai_shell": 0.62,
                           "health_shell": 0.82, "wearable_shell": 0.60},
                  roughness_delta=+0.045, stroke=0.22),
}

# ---------------------------------------------------------------------- rigs
# Museum/editorial: every source is a large area light at a low level, so the
# dielectric response shows up as a broad sheen rather than a hotspot.
RIGS = {
    "dark": dict(key=1050.0, fill=0.17, sep=0.20, ambient=0.045,
                 key_size=6.4, key_offset=(-2.7, -3.2, 3.1),
                 fill_offset=(3.8, -2.4, 0.3), sep_offset=(1.3, 3.0, 3.0),
                 fill_tint=(0.96, 0.98, 1.0), key_tint=(1.0, 0.985, 0.96),
                 view_transform="AgX", look="AgX - Medium High Contrast",
                 exposure=-0.55),
    "light": dict(key=980.0, fill=0.10, sep=0.13, ambient=0.05,
                  key_size=4.4, key_offset=(-3.0, -3.0, 3.6),
                  fill_offset=(3.6, -2.6, 0.2), sep_offset=(1.2, 2.8, 3.2),
                  fill_tint=(0.98, 0.99, 1.0), key_tint=(1.0, 0.99, 0.97),
                  view_transform="AgX", look="AgX - Medium High Contrast",
                  exposure=-0.30),
}

CANVAS_DARK_GRADIENT = (base.CANVAS_DARK_BOTTOM, base.CANVAS_DARK_TOP)
DARK_BG_GAIN = base.DARK_BG_GAIN
CANVAS_LIGHT = base.CANVAS_LIGHT


def hex_to_linear(value):
    return base.hex_to_linear(value)


def role_hex(role):
    return ROLES[role][0]


def role_roughness(role):
    return ROLES[role][1]


def role_ior(role):
    return ROLES[role][5]


def role_specular(role):
    return ROLES[role][6]


# ------------------------------------------------------------------ materials
def _drop(name):
    existing = bpy.data.materials.get(name)
    if existing is not None:
        bpy.data.materials.remove(existing)
    return name


def make_role_material(role):
    hex_value, roughness, spread, tonal, bump, ior, specular = ROLES[role][:7]
    mat = bpy.data.materials.new(_drop("M2_7_%s" % role.upper()))
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    base_colour = hex_to_linear(hex_value)
    bsdf.inputs["Base Color"].default_value = base_colour
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = roughness
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = ior          # real dielectric, not a cheat
    for key in ("Specular IOR Level", "Specular"):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = specular
            break

    geo = nodes.new("ShaderNodeNewGeometry")
    geo.location = (-1100, 0)

    # A - macro tonal drift. Very low frequency, so it reads as material unevenness
    # rather than as clouds.
    macro = nodes.new("ShaderNodeTexNoise")
    macro.location = (-880, 220)
    macro.inputs["Scale"].default_value = MACRO_SCALE
    macro.inputs["Detail"].default_value = MACRO_DETAIL
    macro.inputs["Roughness"].default_value = 0.5
    links.new(geo.outputs["Position"], macro.inputs["Vector"])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.location = (-560, -120)
    mix.inputs["Factor"].default_value = tonal * 0.5
    mix.inputs[6].default_value = base_colour
    mix.inputs[7].default_value = tuple(
        min(1.0, channel * TINT_STRENGTH) for channel in base_colour[:3]) + (1.0,)
    links.new(macro.outputs["Fac"], mix.inputs["Factor"])
    links.new(mix.outputs[2], bsdf.inputs["Base Color"])

    # B - meso roughness patches, from a different, decorrelated field.
    meso = nodes.new("ShaderNodeTexNoise")
    meso.location = (-880, -60)
    meso.inputs["Scale"].default_value = MESO_SCALE
    meso.inputs["Detail"].default_value = MESO_DETAIL
    meso.inputs["Roughness"].default_value = 0.62
    links.new(geo.outputs["Position"], meso.inputs["Vector"])

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-560, 300)
    lo, hi = max(0.05, roughness - spread), min(0.95, roughness + spread)
    ramp.color_ramp.elements[0].position = 0.33
    ramp.color_ramp.elements[0].color = (lo, lo, lo, 1.0)
    ramp.color_ramp.elements[1].position = 0.67
    ramp.color_ramp.elements[1].color = (hi, hi, hi, 1.0)
    links.new(meso.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])

    # C - micro tactile normal. Fine enough to disappear at website scale.
    micro = nodes.new("ShaderNodeTexNoise")
    micro.location = (-880, -420)
    micro.inputs["Scale"].default_value = MICRO_SCALE
    micro.inputs["Detail"].default_value = MICRO_DETAIL
    micro.inputs["Roughness"].default_value = 0.5
    links.new(geo.outputs["Position"], micro.inputs["Vector"])

    bump_node = nodes.new("ShaderNodeBump")
    bump_node.location = (-320, -420)
    bump_node.inputs["Strength"].default_value = bump
    bump_node.inputs["Distance"].default_value = MICRO_DISTANCE
    links.new(micro.outputs["Fac"], bump_node.inputs["Height"])
    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

    mat["hero_v2_role"] = role
    mat["hero_v2_note"] = ROLES[role][7]
    return mat


def build_all_materials():
    for role in ROLES:
        make_role_material(role)
    return sorted(mat.name for mat in bpy.data.materials
                  if mat.name.startswith("M2_7_"))


def apply_theme_preset(theme):
    """Pigment per role, plus a roughness offset - never one blanket multiplier."""
    preset = THEME_PRESET[theme]
    applied = {}
    for role, tint in preset["pigment"].items():
        mat = bpy.data.materials.get("M2_7_%s" % role.upper())
        if mat is None:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        base_colour = hex_to_linear(ROLES[role][0])
        tinted = tuple(min(1.0, channel * tint) for channel in base_colour[:3]) + (1.0,)
        bsdf.inputs["Base Color"].default_value = tinted
        mix = mat.node_tree.nodes.get("Mix")
        if mix is not None:
            mix.inputs[6].default_value = tinted
            mix.inputs[7].default_value = tuple(
                min(1.0, channel * TINT_STRENGTH) for channel in tinted[:3]) + (1.0,)
        roughness = min(0.95, ROLES[role][1] + preset["roughness_delta"])
        bsdf.inputs["Roughness"].default_value = roughness
        ramp = mat.node_tree.nodes.get("ValToRGB")
        if ramp is not None:
            spread = ROLES[role][2]
            ramp.color_ramp.elements[0].color = (max(0.05, roughness - spread),) * 3 + (1.0,)
            ramp.color_ramp.elements[1].color = (min(0.95, roughness + spread),) * 3 + (1.0,)
        applied[role] = dict(pigment=[round(c, 5) for c in tinted[:3]],
                             roughness=round(roughness, 3))
    stroke = bpy.data.materials.get("M2_7_RELATION")
    if stroke is not None:
        bsdf = stroke.node_tree.nodes.get("Principled BSDF")
        base_colour = hex_to_linear(ROLES["relation"][0])
        stroke_colour = tuple(min(1.0, channel * preset["stroke"])
                              for channel in base_colour[:3]) + (1.0,)
        bsdf.inputs["Base Color"].default_value = stroke_colour
        mix = stroke.node_tree.nodes.get("Mix")
        if mix is not None:
            mix.inputs[6].default_value = stroke_colour
            mix.inputs[7].default_value = tuple(
                min(1.0, channel * TINT_STRENGTH)
                for channel in stroke_colour[:3]) + (1.0,)
        applied["relation"] = dict(pigment=[round(c, 5) for c in stroke_colour[:3]],
                                   roughness=round(float(
                                       bsdf.inputs["Roughness"].default_value), 3))
    return dict(theme=theme, preset=preset, applied=applied)


def apply_theme(theme, rig_lights, exposure):
    spec = RIGS[theme]
    for key, lights in rig_lights.items():
        for light in lights:
            light.hide_render = key != theme
    base.render_world(theme, exposure)
    scene = bpy.context.scene
    scene.view_settings.exposure = exposure
    try:
        scene.view_settings.view_transform = spec["view_transform"]
    except TypeError:
        pass
    try:
        scene.view_settings.look = spec["look"] or "None"
    except TypeError:
        pass
    preset = apply_theme_preset(theme)
    return dict(theme=theme, exposure=exposure, key_energy=spec["key"],
                fill_ratio=spec["fill"], sep_ratio=spec["sep"],
                ambient=spec["ambient"], key_size=spec["key_size"],
                view_transform=spec["view_transform"], look=spec["look"],
                key_offset=list(spec["key_offset"]), material_preset=preset)


def build_rig(collection, theme, target, prefix):
    spec = RIGS[theme]
    centre = Vector(target)
    key = area_light("%s_Key" % prefix, spec["key"], spec["key_tint"],
                     centre + Vector(spec["key_offset"]), spec["key_size"], centre)
    fill = area_light("%s_Fill" % prefix, spec["key"] * spec["fill"], spec["fill_tint"],
                      centre + Vector(spec["fill_offset"]),
                      spec["key_size"] * 1.25, centre)
    sep = area_light("%s_Sep" % prefix, spec["key"] * spec["sep"], (1.0, 1.0, 1.0),
                     centre + Vector(spec["sep_offset"]), 2.8, centre)
    for light in (key, fill, sep):
        if collection is not None:
            for coll in list(light.users_collection):
                coll.objects.unlink(light)
            collection.objects.link(light)
        light.hide_render = True
    return [key, fill, sep]


# ------------------------------------------------------------- relation curves
def build_relation_curve(name, start_obj, end_obj, spec, collection,
                         tube_radius=CURVE_TUBE_RADIUS):
    """A hairline stroke from the core's surface to a companion's surface.

    The core-side anchor can be swung around the core's up axis, which puts it on the
    far hemisphere: the stroke then leaves from behind the core and is partly
    occluded from the camera. That is the card's "real 3D depth" - and the validator
    checks the stroke still clears the sphere rather than passing through it.
    """
    start_centre = start_obj.matrix_world.translation
    end_centre = end_obj.matrix_world.translation
    direction = (end_centre - start_centre).normalized()
    swing = math.radians(spec.get("anchor_swing_deg", 0.0))
    offset = direction
    if swing:
        axis = direction.cross(Vector((0.0, 0.0, 1.0)))
        axis = axis.normalized() if axis.length > 1e-6 else Vector((1.0, 0.0, 0.0))
        offset = (Quaternion(axis, swing).to_matrix() @ direction).normalized()
    start = base.surface_anchor(start_obj, offset)
    end = base.surface_anchor(end_obj, -direction)

    chord = end - start
    length = chord.length
    side = chord.cross(Vector((0.0, 0.0, 1.0)))
    side = side.normalized() if side.length > 1e-6 else Vector((1.0, 0.0, 0.0))
    up = side.cross(chord).normalized()
    back = Vector((0.0, 1.0, 0.0))          # +Y is away from the camera
    bend, lift = spec["bend"], spec["lift"]
    depth = spec.get("depth", 0.0)
    handle_a = (start + chord * 0.34 + side * (bend * length)
                + up * (lift * length) + back * (depth * length))
    handle_b = (start + chord * 0.74 + side * (bend * length * 0.30)
                + up * (lift * length * 0.45) + back * (depth * length * 0.35)
                + side * (spec.get("arrival_tangent", 0.0) * length))

    # A swung anchor plus a negative lift can bow the path INTO the core (measured:
    # 7 mm inside, three times the tube radius). Rather than hand-tuning three offsets
    # per stroke, the handles are pushed radially outward until the sampled path
    # clears the sphere: the authored curvature survives and interpenetration becomes
    # impossible by construction. The correction is reported, not hidden.
    radius = max(vertex.co.length for vertex in start_obj.data.vertices)
    bevel_radius = tube_radius * spec.get("weight", 1.0)
    needed = radius + bevel_radius * 1.25

    def cubic(t):
        inverse = 1.0 - t
        return (start * (inverse ** 3) + handle_a * (3.0 * inverse * inverse * t)
                + handle_b * (3.0 * inverse * t * t) + end * (t ** 3))

    correction = 0.0
    companion_radius = max(vertex.co.length for vertex in end_obj.data.vertices)
    for _ in range(16):
        samples = [cubic(index / 48.0) for index in range(4, 46)]
        slack = bevel_radius * 1.25
        deficits = []
        for centre, radius in ((start_centre, radius),
                               (end_centre, companion_radius)):
            worst = min((point - centre).length for point in samples)
            deficits.append((centre, radius + slack - worst))
        deficits = [(centre, deficit) for centre, deficit in deficits
                    if deficit > 1e-5]
        if not deficits:
            break
        centre, deficit = max(deficits, key=lambda pair: pair[1])
        for handle in (handle_a, handle_b):
            outward = handle - centre
            if outward.length > 1e-9:
                handle += outward.normalized() * deficit * 0.9
        correction += deficit * 0.9

    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = bevel_radius
    curve.bevel_resolution = CURVE_BEVEL_RESOLUTION
    curve.resolution_u = CURVE_RESOLUTION_U
    curve.use_fill_caps = True
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(1)
    first, second = spline.bezier_points
    for point, coordinate, handle, weight in (
            (first, start, handle_a, CURVE_TAPER[0]),
            (second, end, handle_b, CURVE_TAPER[1])):
        point.co = coordinate
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
        point.handle_left = handle
        point.handle_right = handle
        point.radius = weight          # the taper: no uniform visual weight

    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    if collection is not None:
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    for other in bpy.context.selected_objects:
        other.select_set(False)
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    mesh_obj = bpy.context.view_layer.objects.active
    mesh_obj.data.materials.append(bpy.data.materials["M2_7_RELATION"])
    for poly in mesh_obj.data.polygons:
        poly.use_smooth = True

    points = [Vector(vertex.co) for vertex in mesh_obj.data.vertices]
    deviation = max((point - start).cross(chord).length / max(length, 1e-9)
                    for point in points)
    # Two different questions, measured separately:
    # * burial at the ANCHOR is attachment. A stroke meeting a curved surface at a
    #   oblique angle necessarily sinks about a tube radius where it lands; that is
    #   what "terminates on the surface" looks like.
    # * burial along the MID-PATH is the failure mode - a stroke cutting through the
    #   sphere like a skewer. That is what must stay within one tube radius.
    # The previous single metric conflated the two and failed a correctly attached
    # stroke, so both numbers are now reported.
    core_radius = max(vertex.co.length for vertex in start_obj.data.vertices)
    signed = min((point - start_centre).length - core_radius for point in points)
    anchor_zone = max(0.06 * length, 3.0 * bevel_radius)
    mid = [(point - start_centre).length - core_radius for point in points
           if min((point - start).length, (point - end).length) > anchor_zone]
    mid_signed = min(mid) if mid else signed
    excess = max(0.0, -(mid_signed) - bevel_radius)
    centreline_min = min((cubic(index / 96.0) - start_centre).length
                         for index in range(2, 95))
    return mesh_obj, dict(
        name=mesh_obj.name, bevel_radius=round(bevel_radius, 5),
        taper=list(CURVE_TAPER), chord_length=round(length, 4),
        bend=bend, lift=lift, depth=depth,
        swing_deg=spec.get("anchor_swing_deg", 0.0),
        start_distance_from_core_centre=round((start - start_centre).length, 4),
        end_distance_from_companion_centre=round((end - end_centre).length, 4),
        max_deviation_fraction=round(deviation, 4),
        min_signed_clearance=round(signed, 5),
        mid_path_signed_clearance=round(mid_signed, 5),
        centreline_min_radius=round(centreline_min, 5),
        core_radius=round(core_radius, 5),
        interpenetration_excess=round(excess, 5),
        outward_correction=round(correction, 5),
        vertices=len(points))


# ------------------------------------------------------------- web-scale check
WEB_SCALE = {"desktop": (686, 600), "mobile": (288, 288)}
