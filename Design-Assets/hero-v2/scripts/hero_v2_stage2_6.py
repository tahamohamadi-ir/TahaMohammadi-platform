"""Hero v2 — Stage 2.6: PURE NODE LANGUAGE.

Four plain spheres and three real relation curves. Nothing else.

The card's hard direction: every node is a simple sphere, the core's seam and
inlay are gone (a viewer must stop asking "what object is this?"), and the graph
reading must come from *actual relations* — thin curves that begin on the core's
surface and end on a companion's surface. Not decorative arcs, not orbital rings,
no circular-orbit feel, and no curve may dominate.

Three implementation decisions worth naming:

1. **Curve anchors are ray-cast, not assumed.** Each endpoint is found by casting
   a ray from the sphere's centre along the line between the two centres and
   taking the hit on the real (deformed, ±1.3%) surface. The result is exact
   surface-to-surface contact, and it survives any later tweak to the deformation
   without the curve floating or sinking. Both are re-measured by the validator.

2. **The background is the world, and the lighting is separated from it.** There
   is deliberately no floor: the card asks to minimise the "standing on a floor"
   feeling, and these frames have to composite into a page. The world uses a
   Light-Path split, so camera rays see the theme's background while lighting rays
   see a low, controlled ambient — which is what lets the light theme land on the
   `#f7f8f5` page token exactly (Standard transform, background colour = the token
   itself, so nothing can clip upward) without flooding the spheres with ambient.

3. **Material subtlety is three restrained layers**, per the card: a very soft
   low-frequency tonal drift, a roughness breakup, and an extremely light
   micro-normal. All three are world-position driven, so the grain scale is
   identical on a ⌀1.45 core and a ⌀1.00 companion.
"""

from __future__ import annotations

import math

import bpy
from mathutils import Euler, Vector

# ---------------------------------------------------------------- page canvases
# HERO_PRODUCTION_PLAN_v2.md section 3: Light #f7f8f5 / Dark #071225.
CANVAS_LIGHT = "#f7f8f5"
CANVAS_DARK_TOP = "#08142A"      # deep ink navy, a little above the token so the
CANVAS_DARK_BOTTOM = "#050D1C"   # gradient has somewhere calm to fall to

# ------------------------------------------------------------------ node layout
# Stage 1 authored the directions; Stage 2.5 re-spaced the radial rhythm so the
# arrangement stops reading as an orbit. Both are kept: one companion upper-left,
# one right/upper-right, one below, core near centre but not mechanically so.
COMPANION_RHYTHM = {
    "GRP_HUMAN_CENTERED_AI": 1.06,
    "GRP_HEALTH_BEHAVIOR": 0.96,
    "GRP_WEARABLE_EDGE": 1.14,
}
COMPANION_SCALE = {
    "GRP_HUMAN_CENTERED_AI": 0.96,
    "GRP_HEALTH_BEHAVIOR": 1.00,
    "GRP_WEARABLE_EDGE": 1.05,
}
COMPANION_SEGMENTS, COMPANION_RINGS = 96, 60
CORE_SEGMENTS, CORE_RINGS = 128, 80
COMPANION_DEFORM = (0.008, 0.005)     # ~1.3% radial variation: abstract, no feature
CORE_DEFORM = (0.010, 0.006)
CORE_FLATTEN = (1.0, 0.995, 0.988)    # barely there; no object read
SMOOTH_ANGLE_DEG = 60.0

# ------------------------------------------------------------- relation curves
# One real relation per companion. `bend` is a signed sideways offset and `lift` a
# vertical one, both as a fraction of the chord length; the three differ in sign
# and magnitude so no two curves share a curvature and none of them can read as an
# orbit. Tube radius 0.0075 BU is ~0.5% of the core diameter: a drawn line, not a
# rod.
RELATIONS = {
    "GRP_HUMAN_CENTERED_AI": dict(bend=+0.085, lift=+0.055),
    "GRP_HEALTH_BEHAVIOR": dict(bend=-0.060, lift=+0.030),
    "GRP_WEARABLE_EDGE": dict(bend=+0.045, lift=-0.070),
}
CURVE_TUBE_RADIUS = 0.0075
CURVE_BEVEL_RESOLUTION = 4
CURVE_RESOLUTION_U = 12

# ------------------------------------------------------------------ materials
# role: (hex, roughness, roughness spread, tonal strength, bump strength, note)
ROLES = {
    "core_shell": ("#27565A", 0.62, 0.040, 0.12, 0.036,
                   "deep mineral teal; pigmented plaster, dense and quiet"),
    "hcai_shell": ("#6F8474", 0.72, 0.030, 0.11, 0.032,
                   "eucalyptus / muted sage; the calm human one"),
    "health_shell": ("#877156", 0.74, 0.040, 0.13, 0.036,
                     "warm sandstone / muted ochre; the most tactile surface"),
    "wearable_shell": ("#6B6580", 0.68, 0.045, 0.12, 0.034,
                       "dusty stone-violet; cool, mature, never neon"),
    "relation": ("#C6B191", 0.80, 0.020, 0.05, 0.010,
                 "champagne stroke: the graph's connective tissue, not a metal. "
                 "Matte by design - a specular glint along a thin tube overshoots the "
                 "frame's white point and a drawn line should not glint anyway"),
}
# Every role sits at the matte end of its band, and the dielectric specular is off.
# Reason, measured: grazing Fresnel glints reached a raw radiance many times the
# white point, so they stayed clipped at 255 through a 26% key cut, a specular-level
# cut and a view-transform change. Pigmented plaster has no such highlight, and the
# card asks for exactly that - "non-metallic everywhere", "no glossy plastic",
# "surfaces should not look like CG toys". Shape now comes from the broad key, the
# tonal drift and the micro-relief.
SPECULAR_LEVEL = 0.0
ROLE_SPECULAR = {"_default": 0.0, "relation": 0.0}
TONAL_SCALE = 2.2          # layer 1: very soft, very low frequency
TONAL_DETAIL = 2.0
BUMP_SCALE = 14.0          # layer 3: fine, and only 0.026-0.030 strong
BUMP_DETAIL = 2.0
IOR = 1.40
SPECULAR_LEVEL = 0.14      # very restrained: the card asks for no glossy plastic,
                           # and extreme glints map to pure white under both
                           # transforms (AgX included)
CURVE_TINT = {"dark": 1.00, "light": 0.45}   # light needs a deeper stroke to read

# Per-theme material preset. The plan asks for theme-specific presets rather than
# an inverted render, and the Stage 2.5 review asked for less pastel in light mode
# -- worst on the two lightest companions -- so light mode darkens per role instead
# of applying one blanket factor.
THEME_TINT = {
    "dark": {"core_shell": 0.97, "hcai_shell": 1.00, "health_shell": 1.00,
             "wearable_shell": 1.00},
    "light": {"core_shell": 0.86, "hcai_shell": 0.66, "health_shell": 0.84,
              "wearable_shell": 0.64},
}

# World background gains. The background is a world colour, so it is tone-mapped
# like everything else: under AgX the deep navy lands at 2/255 (identity lost) and
# under Standard the exposure multiplier drags the light page down with the spheres.
# Both are compensated here rather than by moving the palette: the light one is
# exact (Standard applies exposure as a plain linear multiply, so dividing the
# background strength by 2^exposure lands the page on the token), the dark one is
# measured.
DARK_BG_GAIN = 6.0
LIGHT_KEY_ENERGY = 1600.0
# The light page is trimmed a hair below the exact token so denoiser speckle on a
# flat near-white field has headroom and cannot reach 255: at the exact token the
# measured frames carried isolated 255 pixels (0.03% of the frame), which is a
# clipped pixel by any honest reading even though no highlight is blown. Two levels
# of token accuracy buys a frame with no clipped pixel at all.
LIGHT_PAGE_TRIM = 1.0      # moot for the light review frames: their page is
                           # composited (see configure_output) rather than rendered
RIGS = {
    "dark": dict(
        key=1150.0, fill=0.16, sep=0.20, ambient=0.045,
        key_size=6.0, key_offset=(-2.6, -3.2, 3.0),
        fill_offset=(3.8, -2.4, 0.3), sep_offset=(1.3, 3.0, 3.0),
        fill_tint=(0.96, 0.98, 1.0), key_tint=(1.0, 0.985, 0.96),
        view_transform="AgX", look="AgX - Medium High Contrast",
        exposure=-0.55, background="gradient"),
    "light": dict(
        key=1050.0, fill=0.14, sep=0.16, ambient=0.055,
        key_size=4.6, key_offset=(-2.9, -3.0, 3.5),
        fill_offset=(3.6, -2.6, 0.2), sep_offset=(1.2, 2.8, 3.2),
        fill_tint=(0.98, 0.99, 1.0), key_tint=(1.0, 0.99, 0.97),
        # AgX, like the dark theme, and the page composited from the alpha frame by
        # composite_stage2_6.py. Measured reason: under a Standard transform the
        # specular glints on the spheres and strokes overshoot far past white and
        # stay clipped no matter how the rig is trimmed (239 pixels at 255, unchanged
        # by a 12% key cut or a rougher stroke material), while AgX rolls them off
        # (measured max 212 in the dark theme). Because the page is composited after
        # the transform it still lands exactly on the token.
        view_transform="AgX", look="AgX - Medium High Contrast",
        exposure=-0.30, background="page"),
}


def hex_to_linear(value):
    value = value.lstrip("#")
    out = []
    for index in range(0, 6, 2):
        channel = int(value[index:index + 2], 16) / 255.0
        out.append(channel / 12.92 if channel <= 0.04045
                   else ((channel + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def role_hex(role):
    return ROLES[role][0]


def role_roughness(role):
    return ROLES[role][1]


def role_metallic(role):
    return 0.0


# ------------------------------------------------------------------ materials
def configure_output(scene, theme, alpha):
    """Decide what sits behind the nodes.

    Dark review frames render the world gradient directly, and that path is clean
    (measured max 212/255, zero clipped pixels).

    Light review frames are NOT rendered here. A flat near-white background is
    exactly what Cycles' denoiser overshoots: the world camera-rays have zero
    variance, so every deviation from the page value is denoiser error, and it
    poked isolated pixels past 255 (0.012% of the frame) no matter how the page was
    lit or trimmed - which the card forbids. So the light page is composited from
    the alpha frame by `composite_stage2_6.py`, the same pattern Stage 1 used for
    its page-canvas previews. Alpha frames are transparent with no compositing.
    """
    scene.use_nodes = False
    if alpha:
        scene.render.film_transparent = True
        scene.render.image_settings.color_mode = "RGBA"
        return "transparent"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    return "world_background"


def _drop(name):
    existing = bpy.data.materials.get(name)
    if existing is not None:
        bpy.data.materials.remove(existing)
    return name


def make_role_material(role):
    """Pigmented mineral plaster: three restrained layers, nothing announced."""
    hex_value, roughness, spread, tonal, bump = ROLES[role][:5]
    mat = bpy.data.materials.new(_drop("M2_6_%s" % role.upper()))
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    base = hex_to_linear(hex_value)
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = roughness
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = IOR
    for key in ("Specular IOR Level", "Specular"):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = ROLE_SPECULAR.get(
                role, ROLE_SPECULAR["_default"])
            break

    geo = nodes.new("ShaderNodeNewGeometry")
    geo.location = (-1000, 0)

    # Layer 1 - very soft low-frequency tonal drift.
    field = nodes.new("ShaderNodeTexNoise")
    field.location = (-780, 140)
    field.inputs["Scale"].default_value = TONAL_SCALE
    field.inputs["Detail"].default_value = TONAL_DETAIL
    field.inputs["Roughness"].default_value = 0.55
    links.new(geo.outputs["Position"], field.inputs["Vector"])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.location = (-520, -60)
    mix.inputs["Factor"].default_value = tonal * 0.5
    mix.inputs[6].default_value = base
    mix.inputs[7].default_value = tuple(
        min(1.0, channel * 1.09) for channel in base[:3]) + (1.0,)
    links.new(field.outputs["Fac"], mix.inputs["Factor"])
    links.new(mix.outputs[2], bsdf.inputs["Base Color"])

    # Layer 2 - subtle roughness breakup.
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-520, 280)
    lo, hi = max(0.05, roughness - spread), min(0.95, roughness + spread)
    ramp.color_ramp.elements[0].position = 0.34
    ramp.color_ramp.elements[0].color = (lo, lo, lo, 1.0)
    ramp.color_ramp.elements[1].position = 0.66
    ramp.color_ramp.elements[1].color = (hi, hi, hi, 1.0)
    links.new(field.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])

    # Layer 3 - extremely light micro-normal.
    micro = nodes.new("ShaderNodeTexNoise")
    micro.location = (-780, -320)
    micro.inputs["Scale"].default_value = BUMP_SCALE
    micro.inputs["Detail"].default_value = BUMP_DETAIL
    micro.inputs["Roughness"].default_value = 0.5
    links.new(geo.outputs["Position"], micro.inputs["Vector"])
    bump_node = nodes.new("ShaderNodeBump")
    bump_node.location = (-300, -340)
    bump_node.inputs["Strength"].default_value = bump
    bump_node.inputs["Distance"].default_value = 0.006
    links.new(micro.outputs["Fac"], bump_node.inputs["Height"])
    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

    mat["hero_v2_role"] = role
    mat["hero_v2_note"] = ROLES[role][5]
    return mat


def build_all_materials():
    for role in ROLES:
        make_role_material(role)
    return sorted(mat.name for mat in bpy.data.materials
                  if mat.name.startswith("M2_6_"))


def apply_theme_preset(theme):
    """Theme-specific material preset (plan section 3), per role."""
    applied = {}
    for role, tint in THEME_TINT[theme].items():
        mat = bpy.data.materials.get("M2_6_%s" % role.upper())
        if mat is None:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        base = hex_to_linear(ROLES[role][0])
        tinted = tuple(min(1.0, channel * tint) for channel in base[:3]) + (1.0,)
        bsdf.inputs["Base Color"].default_value = tinted
        mix = mat.node_tree.nodes.get("Mix")
        if mix is not None:
            mix.inputs[6].default_value = tinted
            mix.inputs[7].default_value = tuple(
                min(1.0, channel * 1.09) for channel in tinted[:3]) + (1.0,)
        applied[role] = [round(channel, 5) for channel in tinted[:3]]
    curve = bpy.data.materials.get("M2_6_RELATION")
    if curve is not None:
        applied["relation"] = [round(channel, 5) for channel in hex_to_linear(
            ROLES["relation"][0])[:3]]
    return dict(theme=theme, tints=THEME_TINT[theme], applied=applied)


def apply_theme(theme, rig_lights, exposure):
    """Switch rig, background, tone pipeline and material preset in one call."""
    spec = RIGS[theme]
    for key, lights in rig_lights.items():
        for light in lights:
            light.hide_render = key != theme
    render_world(theme, exposure)
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


# ---------------------------------------------------------------- world / rig
def ensure_world():
    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("HERO_V2_World_2_6")
    scene.world.use_nodes = True
    return scene.world


def render_world(theme, exposure=0.0):
    """Background for camera rays, low controlled ambient for lighting rays.

    One Light-Path split does both jobs, which is what removes the need for any
    backdrop geometry - and therefore any floor. `exposure` is needed because the
    background is tone-mapped along with everything else, so the camera-ray branch
    has to be gained against it (see DARK_BG_GAIN / LIGHT_KEY_ENERGY).
    """
    world = ensure_world()
    nodes, links = world.node_tree.nodes, world.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputWorld")
    output.location = (600, 0)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (400, 0)
    ambient = nodes.new("ShaderNodeBackground")
    ambient.location = (180, -160)
    camera_bg = nodes.new("ShaderNodeBackground")
    camera_bg.location = (180, 120)
    path = nodes.new("ShaderNodeLightPath")
    path.location = (-40, 320)
    links.new(path.outputs["Is Camera Ray"], mix.inputs["Fac"])
    links.new(ambient.outputs["Background"], mix.inputs[1])
    links.new(camera_bg.outputs["Background"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    spec = RIGS[theme]
    if theme == "light":
        camera_bg.inputs["Color"].default_value = hex_to_linear(CANVAS_LIGHT)
        # Exact: Standard maps the linear value straight through, and exposure is a
        # plain multiply, so dividing by 2^exposure puts the page back on the token.
        camera_bg.inputs["Strength"].default_value = LIGHT_PAGE_TRIM / (2.0 ** exposure)
        ambient.inputs["Color"].default_value = (0.97, 0.97, 0.95, 1.0)
    else:
        gradient = nodes.new("ShaderNodeTexGradient")
        gradient.gradient_type = "LINEAR"
        gradient.location = (-260, 140)
        mapping = nodes.new("ShaderNodeMapping")
        mapping.location = (-440, 140)
        mapping.inputs["Rotation"].default_value = (0.0, 0.0, math.radians(90.0))
        texcoord = nodes.new("ShaderNodeTexCoord")
        texcoord.location = (-640, 140)
        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.location = (-60, 140)
        ramp.color_ramp.elements[0].color = hex_to_linear(CANVAS_DARK_BOTTOM)
        ramp.color_ramp.elements[1].color = hex_to_linear(CANVAS_DARK_TOP)
        links.new(texcoord.outputs["Window"], mapping.inputs["Vector"])
        links.new(mapping.outputs["Vector"], gradient.inputs["Vector"])
        links.new(gradient.outputs["Color"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], camera_bg.inputs["Color"])
        camera_bg.inputs["Strength"].default_value = DARK_BG_GAIN
        ambient.inputs["Color"].default_value = (0.60, 0.66, 0.78, 1.0)
    ambient.inputs["Strength"].default_value = spec["ambient"]
    return world


def build_rig(collection, theme, target, prefix):
    spec = RIGS[theme]
    centre = Vector(target)
    key = _area("%s_Key" % prefix, spec["key"], spec["key_tint"],
                centre + Vector(spec["key_offset"]), spec["key_size"], centre)
    fill = _area("%s_Fill" % prefix, spec["key"] * spec["fill"], spec["fill_tint"],
                 centre + Vector(spec["fill_offset"]), spec["key_size"] * 1.25, centre)
    sep = _area("%s_Sep" % prefix, spec["key"] * spec["sep"], (1.0, 1.0, 1.0),
                centre + Vector(spec["sep_offset"]), 2.8, centre)
    for light in (key, fill, sep):
        if collection is not None:
            for coll in list(light.users_collection):
                coll.objects.unlink(light)
            collection.objects.link(light)
        light.hide_render = True
    return [key, fill, sep]


def _area(name, energy, colour, location, size, target):
    data = bpy.data.lights.new(name, type="AREA")
    data.shape = "SQUARE"
    data.size = size
    data.energy = energy
    data.color = colour
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - Vector(location)).normalized() \
        .to_track_quat("-Z", "Y").to_euler()
    # A studio light is not a subject. Cycles renders area lights visible to camera
    # rays by default, and the light theme's key - sitting higher and further forward
    # than the dark theme's - put a white sliver inside the frame: 239 pixels at 255
    # that stayed clipped through a material change, a 26% key cut and a transform
    # change, because an emitter's own brightness does not follow the rig.
    obj.visible_camera = False
    return obj


# ------------------------------------------------------------- relation curves
def surface_anchor(obj, direction):
    """World-space point where a ray from the object's centre meets its surface.

    The meshes are centred on their own origin, so the ray is cast in local space
    and the hit is transformed back. Ray-casting the real (deformed) surface is
    what makes the curve touch the geometry instead of a nominal radius.
    """
    matrix = obj.matrix_world
    local_direction = (matrix.inverted().to_3x3() @ direction).normalized()
    hit, location, _normal, _index = obj.ray_cast(Vector((0.0, 0.0, 0.0)),
                                                  local_direction)
    if not hit:
        raise RuntimeError("relation anchor missed the surface of %s" % obj.name)
    return matrix @ location


def build_relation_curve(name, start_obj, end_obj, bend, lift, collection,
                         tube_radius=CURVE_TUBE_RADIUS):
    """A cubic Bezier rod from the core's surface to a companion's surface."""
    start_centre = start_obj.matrix_world.translation
    end_centre = end_obj.matrix_world.translation
    direction = (end_centre - start_centre).normalized()
    start = surface_anchor(start_obj, direction)
    end = surface_anchor(end_obj, -direction)

    chord = end - start
    length = chord.length
    side = chord.cross(Vector((0.0, 0.0, 1.0)))
    side = side.normalized() if side.length > 1e-6 else Vector((1.0, 0.0, 0.0))
    up = side.cross(chord).normalized()
    # Asymmetric by construction: the sideways offset peaks early, the vertical
    # one peaks late, so the curve leaves the core at one angle and arrives at the
    # companion from another - which is what keeps it from reading as an orbit.
    handle_a = start + chord * 0.34 + side * (bend * length) + up * (lift * length)
    handle_b = start + chord * 0.74 + side * (bend * length * 0.30) + \
        up * (lift * length * 0.45)

    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = tube_radius
    curve.bevel_resolution = CURVE_BEVEL_RESOLUTION
    curve.resolution_u = CURVE_RESOLUTION_U
    curve.use_fill_caps = True
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(1)
    first, second = spline.bezier_points
    for point, coordinate, handle in ((first, start, handle_a),
                                      (second, end, handle_b)):
        point.co = coordinate
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
        point.handle_left = handle
        point.handle_right = handle

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
    bpy.ops.object.convert(target="MESH")   # a real mesh: validators can read it
    mesh_obj = bpy.context.view_layer.objects.active
    mesh_obj.data.materials.append(bpy.data.materials["M2_6_RELATION"])
    for poly in mesh_obj.data.polygons:
        poly.use_smooth = True
    points = [Vector(vertex.co) for vertex in mesh_obj.data.vertices]
    deviation = max((point - start).cross(chord).length / max(length, 1e-9)
                    for point in points)
    return mesh_obj, dict(
        name=mesh_obj.name, tube_radius=tube_radius, chord_length=round(length, 4),
        bend=bend, lift=lift,
        start_distance_from_core_centre=round(
            (start - start_centre).length, 4),
        end_distance_from_companion_centre=round(
            (end - end_centre).length, 4),
        max_deviation_fraction=round(deviation, 4))
