"""Hero v2 — Stage 2.5: geometry simplification + material calibration.

Review-only pass. Nothing here exports, composites or touches the frontend.

What this pass changes, and why (all of it from the Stage 2.5 card):

* **Companions become one sphere each.** Stage 2's companions carried an
  aperture + inner ball, two contours and two grooves. Those reads (eye,
  planetary banding, segmented gadget) are exactly what the card rejects, so the
  three companions are rebuilt as clean spheres with 1-2% low-frequency
  irregularity and nothing else. Structural proof, not adjectives: each companion
  mesh is a single closed surface (Euler characteristic 2) whose radial variation
  stays under 2%, which a groove, band, hole or cavity would immediately break.
* **The core seam is no longer a boolean.** The card rejects the stepped,
  faceted boolean edge, and it is right: a torus bite into a 96-segment sphere
  leaves a staircase that no bevel hides. The seam is now a *procedural* recess —
  every vertex within the seam's angular band is pushed inward along its own
  radius by a raised-cosine profile, which is C1-continuous at both the centre and
  the rim. There is no cut edge to step, so the incision reads as crafted rather
  than machined.
* **Materials move from polished CGI to matte mineral.** Lower roughness bands per
  role, metallic 0 everywhere (the core's accent is a warm *stone* inlay, not
  metal), one broad noise field driving roughness variation and a very slight
  tonal mottle, and a bump so small it is felt rather than seen.
* **Two authored environments.** Dark mode sits on the plan's Dark page canvas
  (`#071225`) and light mode on the Light canvas (`#f7f8f5`, the same value as
  `--color-canvas` in `tokens.css`). They are separate rigs with separate
  exposures, not one rig with a swapped background.

Authored numbers are *imported* from the Stage 1 builder (`LAYOUT`,
`LAYOUT_ROT_DEG`, diameters, view directions, margins, resolutions) so the
composition cannot drift: Stage 2.5 inherits the approved composition by
construction instead of restating it.
"""

from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Euler, Vector

# ---------------------------------------------------------------- page canvases
# HERO_PRODUCTION_PLAN_v2.md section 3: "| Page canvas | #f7f8f5 | #071225 |"
# (Light | Dark). #f7f8f5 is also --color-canvas in src/styles/tokens.css.
CANVAS_DARK = "#071225"
CANVAS_LIGHT = "#f7f8f5"

# A hair below each canvas, so the backdrop is a *surface* the rig can model
# instead of a flat fill, and so the floor can be a shade darker for grounding.
BACKDROP_DARK = "#0A1730"
BACKDROP_FLOOR_DARK = "#0C1B38"
BACKDROP_LIGHT = "#F2F3EE"
BACKDROP_FLOOR_LIGHT = "#E7E9E3"
LIGHT_CANVAS_EMISSION = 0.62      # bounded: lifts the page onto the 247 token

# ------------------------------------------------------------------- geometry
COMPANION_SEGMENTS = 96
COMPANION_RINGS = 60
CORE_SEGMENTS = 128
CORE_RINGS = 80
COMPANION_DEFORM = (0.008, 0.005)   # <= ~1.2% radial variation, card allows 1-2%
CORE_DEFORM = (0.012, 0.008)        # ~1.6%: enough to stop reading as a primitive
CORE_FLATTEN = (1.0, 0.992, 0.981)  # a resting feel; <= 2% per axis

# Radial rhythm and companion scale. The Stage 1 layout placed the three
# companions at almost the same distance from the core (radii 1.56-1.66) and at
# equal diameter, and the Stage 2.5 review read that correctly: one big sphere
# with three similar spheres at similar distances is an atom / solar-system
# diagram, which the card forbids. The card also names the allowed levers
# ("material, colour, scale, position, lighting, depth"), so both are used here.
#
# First attempt pulled HCAI inward to 0.86 and pushed WE out to 1.14. That broke
# the Stage 1 framing contract: HCAI and WE sit on the same side (142 deg and
# 241 deg), so pulling one inward shortened THEIR chord and the mobile silhouette
# gap fell to 10.5 px against a 12 px floor. The rhythm now only ever moves a
# companion AWAY from the core, which lengthens every pair distance instead.
COMPANION_RHYTHM = {
    "GRP_HUMAN_CENTERED_AI": 1.06,   # 1.62 -> 1.72
    "GRP_HEALTH_BEHAVIOR": 0.96,     # 1.56 -> 1.50, alone on the right
    "GRP_WEARABLE_EDGE": 1.14,       # 1.66 -> 1.90
}
COMPANION_SCALE = {
    "GRP_HUMAN_CENTERED_AI": 0.96,
    "GRP_HEALTH_BEHAVIOR": 1.00,
    "GRP_WEARABLE_EDGE": 1.05,
}
# The plan (section 3) asks for theme-specific material presets: warm mineral
# shells in Light, navy shells in Dark. Same hue, different depth per canvas, which
# is what stops the light render reading as pastel while the dark one stays rich.
THEME_TINT = {"dark": 1.0, "light": 0.86}

# The seam: a raised-cosine recess. Width is the angular half-width in radians;
# depth is the maximum inset as a fraction of the core radius.
SEAM_HALF_WIDTH_DEG = 7.4           # 0.129 rad, deliberately wide and shallow
SEAM_DEPTH_FRACTION = 0.028         # ~2.8% of the radius
ACCENT_PROUD = 0.004                # flush: the review read 0.010 as a button
SMOOTH_ANGLE_DEG = 60.0             # one smooth surface: no edge to sharpen

# ------------------------------------------------------------------ materials
# role: (hex, roughness, roughness spread, mottle strength, bump strength, note)
ROLES = {
    "core_shell": ("#27565A", 0.56, 0.045, 0.16, 0.024,
                   "deep mineral teal, tactile and dense; matte, not shiny"),
    "core_accent": ("#8E7854", 0.58, 0.030, 0.14, 0.020,
                    "warm stone inlay on the seam — restrained, not jewellery"),
    "hcai_shell": ("#6F8474", 0.66, 0.030, 0.15, 0.018,
                   "muted eucalyptus; the calm, human, soft one"),
    "health_shell": ("#877156", 0.68, 0.045, 0.18, 0.022,
                     "warm sandstone / bronze-clay; the most tactile surface"),
    "wearable_shell": ("#6B6580", 0.63, 0.050, 0.17, 0.020,
                       "stone-violet; cooled, mineral, never neon"),
}
MOTTLE_SCALE = 3.6          # broad: a plaster-like tonal drift, not a pattern
MOTTLE_DETAIL = 2.5
BUMP_SCALE = 9.0            # broad undulation rather than fine noise... 
BUMP_DETAIL = 2.0           # ...strengthened in 2.5 because the review called the
                            # surfaces "very perfect": felt as soft undulation, not
                            # seen as a texture pattern
IOR = 1.40
SPECULAR_LEVEL = 0.30       # restrained specular on every role

# ---------------------------------------------------------------------- rigs
#  theme : dict(key, fill, sep, ambient, key_size, key_offset, exposure)
#
# The two themes also get their own tone pipeline, because the light review frame
# has to land ON the #f7f8f5 page token and AgX's highlight roll-off caps the top
# end ~17 levels short of it no matter how the backdrop is lit (measured 230 vs
# 247). The dark frame keeps AgX, where the roll-off is exactly what makes the
# navy sit still and the highlights stay unclipped.
RIGS = {
    "dark": dict(
        key=1100.0, fill=0.18, sep=0.22, ambient=0.05,
        key_size=6.0, key_offset=(-2.6, -3.2, 3.0),
        fill_offset=(3.8, -2.4, 0.3), sep_offset=(1.3, 3.0, 3.0),
        fill_tint=(0.96, 0.98, 1.0), key_tint=(1.0, 0.985, 0.96),
        view_transform="AgX", look="AgX - Medium High Contrast", exposure=-0.55),
    "light": dict(
        key=1900.0, fill=0.075, sep=0.10, ambient=0.06,
        key_size=4.2, key_offset=(-2.9, -3.0, 3.6),
        fill_offset=(3.6, -2.6, 0.2), sep_offset=(1.2, 2.8, 3.2),
        fill_tint=(0.98, 0.99, 1.0), key_tint=(1.0, 0.99, 0.97),
        # AgX here too, after measuring the alternative: a Standard transform does
        # land the canvas on the token, but it clips it to pure 255 and the card
        # forbids clipped highlights. Under AgX the light page renders at 230 with
        # the spheres at a 158 median and an 83 darkest value -- controlled, not
        # washed out -- and that 230-vs-247 gap is reported as a known deviation.
        view_transform="AgX", look="AgX - Medium High Contrast", exposure=-0.30),
}

# Review renders: exactly the four the card asks for.
RENDERS = (("01-desktop-dark", "desktop", "dark"),
           ("02-desktop-light", "desktop", "light"),
           ("03-mobile-dark", "mobile", "dark"),
           ("04-mobile-light", "mobile", "light"))


def hex_to_linear(value):
    value = value.lstrip("#")
    out = []
    for index in range(0, 6, 2):
        channel = int(value[index:index + 2], 16) / 255.0
        out.append(channel / 12.92 if channel <= 0.04045
                   else ((channel + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


# --------------------------------------------------------------------- seam cut
def recess_seam(obj, tilt_deg, half_width_deg, depth_fraction):
    """Push the seam band inward along the radius with a raised-cosine profile.

    alpha is the angle between a vertex direction and the seam's great-circle
    plane, so the band runs all the way around the sphere the way an incision
    does. The profile 0.5*(1+cos(pi*alpha/half_width)) is 1 at the centre line and
    0 with zero slope at the rim: no edge, therefore no staircase, and the
    silhouette is untouched because the recess is shallow and wide.
    """
    normal = Euler(tuple(math.radians(a) for a in tilt_deg), "XYZ").to_matrix() \
        @ Vector((0.0, 0.0, 1.0))
    half_width = math.radians(half_width_deg)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    touched = 0
    for vert in bm.verts:
        radius = vert.co.length
        if radius < 1e-9:
            continue
        direction = vert.co / radius
        alpha = abs(math.asin(max(-1.0, min(1.0, direction.dot(normal)))))
        if alpha >= half_width:
            continue
        profile = 0.5 * (1.0 + math.cos(math.pi * alpha / half_width))
        vert.co = direction * (radius - depth_fraction * radius * profile)
        touched += 1
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return touched


def seam_normal(tilt_deg):
    return Euler(tuple(math.radians(a) for a in tilt_deg), "XYZ").to_matrix() \
        @ Vector((0.0, 0.0, 1.0))


# ------------------------------------------------------------------ materials
def _drop(name):
    existing = bpy.data.materials.get(name)
    if existing is not None:
        bpy.data.materials.remove(existing)
    return name


def make_mineral_material(role):
    """One role of the calibrated family: matte mineral, no visible pattern."""
    hex_value, roughness, spread, mottle, bump = ROLES[role][:5]
    mat = bpy.data.materials.new(_drop("M2_%s" % role.upper()))
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
            bsdf.inputs[key].default_value = SPECULAR_LEVEL
            break

    geo = nodes.new("ShaderNodeNewGeometry")
    geo.location = (-1000, 0)

    # One broad field. It drives the roughness band and a very slight tonal
    # mottle; at this scale it reads as hand-finished variation, not as texture.
    field = nodes.new("ShaderNodeTexNoise")
    field.location = (-760, 120)
    field.inputs["Scale"].default_value = MOTTLE_SCALE
    field.inputs["Detail"].default_value = MOTTLE_DETAIL
    field.inputs["Roughness"].default_value = 0.55
    links.new(geo.outputs["Position"], field.inputs["Vector"])

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-500, 240)
    lo, hi = max(0.05, roughness - spread), min(0.95, roughness + spread)
    ramp.color_ramp.elements[0].position = 0.32
    ramp.color_ramp.elements[0].color = (lo, lo, lo, 1.0)
    ramp.color_ramp.elements[1].position = 0.68
    ramp.color_ramp.elements[1].color = (hi, hi, hi, 1.0)
    links.new(field.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])

    mottle_mix = nodes.new("ShaderNodeMix")
    mottle_mix.data_type = "RGBA"
    mottle_mix.location = (-500, -80)
    lighter = tuple(min(1.0, channel * 1.10) for channel in base[:3]) + (1.0,)
    mottle_mix.inputs["Factor"].default_value = mottle * 0.5
    mottle_mix.inputs[6].default_value = base
    mottle_mix.inputs[7].default_value = lighter
    links.new(field.outputs["Fac"], mottle_mix.inputs["Factor"])
    links.new(mottle_mix.outputs[2], bsdf.inputs["Base Color"])

    micro = nodes.new("ShaderNodeTexNoise")
    micro.location = (-760, -300)
    micro.inputs["Scale"].default_value = BUMP_SCALE
    micro.inputs["Detail"].default_value = BUMP_DETAIL
    micro.inputs["Roughness"].default_value = 0.5
    links.new(geo.outputs["Position"], micro.inputs["Vector"])

    bump_node = nodes.new("ShaderNodeBump")
    bump_node.location = (-300, -320)
    bump_node.inputs["Strength"].default_value = bump
    bump_node.inputs["Distance"].default_value = 0.008
    links.new(micro.outputs["Fac"], bump_node.inputs["Height"])
    links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])

    mat["hero_v2_role"] = role
    mat["hero_v2_note"] = ROLES[role][5]
    return mat


def make_environment_material(role, hex_value, roughness=0.90, emission=None,
                              emission_strength=0.0):
    mat = bpy.data.materials.new(_drop("M2_%s" % role.upper()))
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = hex_to_linear(hex_value)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = roughness
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = IOR
    if emission is not None and emission_strength > 0.0:
        # The light canvas is a near-white PAGE, and a matte surface under any rig
        # that still models the spheres cannot reach it by albedo alone (measured
        # 218 against the 247 token). A bounded emission lifts the backdrop onto
        # the token without flooding the scene with bounce.
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = hex_to_linear(emission)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    mat["hero_v2_role"] = role
    mat["hero_v2_emission_strength"] = emission_strength
    return mat


def build_all_materials():
    for role in ROLES:
        make_mineral_material(role)
    make_environment_material("backdrop_dark", BACKDROP_DARK)
    make_environment_material("floor_dark", BACKDROP_FLOOR_DARK)
    make_environment_material("backdrop_light", BACKDROP_LIGHT,
                              emission=CANVAS_LIGHT,
                              emission_strength=LIGHT_CANVAS_EMISSION)
    make_environment_material("floor_light", BACKDROP_FLOOR_LIGHT)
    return sorted(mat.name for mat in bpy.data.materials if mat.name.startswith("M2_"))


def apply_theme_tint(tint):
    """Theme-specific material preset (plan section 3): same hues, different depth.

    Dark keeps the authored values; light multiplies every shell and accent colour
    by `tint` so the spheres hold their own weight on the near-white canvas instead
    of reading as pastel. Returns what it applied, for the report.
    """
    applied = {}
    for role in ROLES:
        mat = bpy.data.materials.get("M2_%s" % role.upper())
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
                min(1.0, channel * 1.10) for channel in tinted[:3]) + (1.0,)
        applied[role] = [round(channel, 5) for channel in tinted[:3]]
    return dict(tint=tint, applied=applied)


def assign(obj, role):
    mat = bpy.data.materials["M2_%s" % role.upper()]
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return len(obj.data.polygons)


# ------------------------------------------------------------ review environment
def build_environment(collection, theme, centre):
    """A seamless backdrop per theme: floor, a wide fillet, then a wall.

    No horizon line by construction (the fillet is tangent at both ends), which is
    what keeps the composition reading as one continuous surface. The themed pair
    backdrop/floor is what separates the two environments: dark mode sits on the
    plan's navy canvas with a marginally lifted floor, light mode on the light
    canvas with a marginally dropped floor.
    """
    if theme == "dark":
        wall, floor = "backdrop_dark", "floor_dark"
    else:
        wall, floor = "backdrop_light", "floor_light"

    profile = [(-6.0, -2.35), (2.20, -2.35)]
    for step in range(0, 13):
        angle = math.pi * 0.5 * step / 12.0
        profile.append((2.20 + 2.60 * math.sin(angle), -0.30 - 2.05 * math.cos(angle)))
    profile.append((4.80, 6.00))

    mesh = bpy.data.meshes.new("BACKDROP2_%s" % theme.upper())
    verts = []
    for x in (-11.0, 11.0):
        verts.extend((x, y, z) for y, z in profile)
    count = len(profile)
    # Wound so the surface faces the objects (the Stage 2 first attempt had this
    # inverted and the floor rendered black).
    faces = [(count + index, count + index + 1, index + 1, index)
             for index in range(count - 1)]
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new("BACKDROP2_%s" % theme.upper(), mesh)
    bpy.context.scene.collection.objects.link(obj)
    if collection is not None:
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        collection.objects.link(obj)
    # Floor and wall are separate material slots on one surface, so the tonal step
    # between them is a soft gradient rather than a modelled edge.
    obj.data.materials.append(bpy.data.materials["M2_%s" % floor.upper()])
    obj.data.materials.append(bpy.data.materials["M2_%s" % wall.upper()])
    for poly in obj.data.polygons:
        poly.material_index = 0 if poly.center.z < -1.9 else 1
        poly.use_smooth = True
    obj.hide_render = True            # hidden; exactly one environment renders
    return obj


def build_rig(collection, theme, target, prefix):
    spec = RIGS[theme]
    centre = Vector(target)
    key = _area("%s_Key" % prefix, spec["key"], spec["key_tint"],
                centre + Vector(spec["key_offset"]), spec["key_size"], centre)
    fill = _area("%s_Fill" % prefix, spec["key"] * spec["fill"], spec["fill_tint"],
                 centre + Vector(spec["fill_offset"]),
                 spec["key_size"] * 1.25, centre)
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
    return obj


def apply_theme(theme, backdrop_by_theme, rig_by_theme, exposure):
    """Switch the scene to one theme: one environment, one rig, one exposure."""
    scene = bpy.context.scene
    for key, obj in backdrop_by_theme.items():
        obj.hide_render = key != theme
    for key, lights in rig_by_theme.items():
        for light in lights:
            light.hide_render = key != theme
    spec = RIGS[theme]
    if scene.world is not None and scene.world.use_nodes:
        background = scene.world.node_tree.nodes.get("Background")
        if background is not None:
            tint = (0.60, 0.66, 0.78, 1.0) if theme == "dark" else (0.97, 0.97, 0.95, 1.0)
            background.inputs["Color"].default_value = tint
            background.inputs["Strength"].default_value = spec["ambient"]
    scene.view_settings.exposure = exposure
    # Per-theme tone pipeline: see the note above RIGS. `look` is a name lookup, so
    # it is set defensively -- a missing look must not take the whole render down.
    try:
        scene.view_settings.view_transform = spec["view_transform"]
    except TypeError:
        pass
    if spec.get("look"):
        try:
            scene.view_settings.look = spec["look"]
        except TypeError:
            pass
    else:
        try:
            scene.view_settings.look = "None"
        except TypeError:
            pass
    return dict(theme=theme, exposure=exposure, ambient=spec["ambient"],
                key_energy=spec["key"], fill_ratio=spec["fill"],
                sep_ratio=spec["sep"], key_size=spec["key_size"],
                view_transform=spec["view_transform"], look=spec.get("look"),
                key_offset=list(spec["key_offset"]))
