"""Hero v2 — Stage 2 look development: materials, light, review environment.

Stage 1 (approved) ships geometry only: one neutral preview clay on every mesh and
one neutral preview rig. This module adds the *look* and nothing else. It never
touches geometry, the layout, the group rotations or the authored cameras, and it
never creates a GLB or a web asset.

Design rules encoded here (HERO_PRODUCTION_PLAN_v2 section 3 + the Stage 2 card):

* One coherent mineral/ceramic family. Every shell shares one node graph: a
  world-position micro-relief pair, a satin roughness band and a small roughness
  variation. Only the base colour and the roughness *centre* change per role.
  The relief is driven by ``Geometry.Position`` (world space) on purpose: a
  Generated/Object coordinate would stretch the grain with each form's size, so a
  1.45 core and a 1.00 companion would no longer share one texture scale.
* Grooves, seams and insets read as *slightly darker and flatter* than their own
  shell, never as high-contrast inlays: a tonal shift is what keeps four objects
  in one family.
* The metallic accent is one bead on the core seam, low metallic and high
  roughness — a warm stone, not jewellery.

Groove recovery
---------------
Stage 1 cut the grooves with real booleans (``spherical_groove_tool``), so the
cutter objects are gone and the recessed faces cannot be found by material slot.
They are recovered *geometrically* instead, from the same tool parameters the
Stage 1 builder used: a torus whose tube-centre circle lies exactly on the sphere
surface removes everything inside its tube, therefore the surviving groove
surface is exactly the set of points at distance ``width`` from that circle.
``GROOVE_SPECS`` therefore mirrors the Stage 1 constants verbatim and
``groove_face_mask`` marks every polygon with a vertex inside a band around the
tube surface. The band is deliberately generous (a groove rim rounded by the
Stage 1 bevel, plus one tessellation step of slack): a face that belongs to the
groove but is missed shows up as a *light* patch inside a dark groove, which
reads as a defect, while a face that is included one step early only softens the
groove's edge.
"""

from __future__ import annotations

import math

import bpy
from mathutils import Euler, Vector

# --------------------------------------------------------------------------- palette
# sRGB hex. Values are chosen inside one family: desaturated minerals, no
# neon, no candy, no chrome. The core is the deepest and most saturated; the
# three companions are lighter or equal in value so the core stays the anchor.
PALETTE = {
    # role            hex        roughness  metallic  note
    "core_shell": (("#27565A", 0.40, 0.0),
                   "deep mineral teal — the brand-leading anchor"),
    "core_inset": (("#1E4347", 0.58, 0.0),
                   "the core seam: same hue, darker and flatter"),
    "core_accent": (("#8A6C48", 0.55, 0.25),
                    "warm bronze-stone inlay — restrained, not jewellery"),
    "hcai_shell": (("#6E8B72", 0.58, 0.0),
                   "muted eucalyptus: lighter and softer than the core"),
    "hcai_inset": (("#5C7062", 0.60, 0.0),
                   "shell opening / inner wall: a mild tonal shift only, so the "
                   "cavity cannot read as an iris"),
    "hcai_inner": (("#6A8070", 0.56, 0.0),
                   "the inset form inside the cavity: close to the shell in value, "
                   "readable but understated"),
    "health_shell": (("#8C7050", 0.60, 0.0),
                     "deep mineral bronze-clay — the warm contrast role, "
                     "deliberately not bread-coloured"),
    "health_inset": (("#775F45", 0.66, 0.0),
                     "the two contours: a low-contrast recess, not a band"),
    "wearable_shell": (("#6A6383", 0.48, 0.0),
                       "deep stone-violet — the cool support role, no candy"),
    "wearable_inset": (("#5A5474", 0.62, 0.0),
                       "the two grooves: deeper violet, still no neon"),
    "arc": (("#55595D", 0.70, 0.0),
            "DECOR_ARC_01: faint, matte, deliberately close to the backdrop"),
    "backdrop": (("#23262A", 0.85, 0.0),
                 "review environment only — a matte, deep, neutral graphite"),
}

# Micro-relief: one scale for every object, in world units.
GRAIN_SCALE = 14.0        # "mineral grain" — the readable one
MICRO_SCALE = 55.0        # micro-roughness — felt, not seen
GRAIN_BUMP = 0.055
MICRO_BUMP = 0.018
ROUGH_SPREAD = 0.035      # tactile roughness variation, +/- this
IOR = 1.45

# Per-role shader character. The QA pass on the first look-dev render came back
# with "four colours of one shader", which is a real failure of the brief: the
# roles must be four *materials* that still belong to one family. These three
# multipliers are the whole difference -- no role changes the node graph, so the
# family holds -- and they map to what the eye reads as material:
#   spread -> how satin vs uniform the sheen is
#   grain  -> how much mineral relief the surface carries
#   micro  -> the fine, felt-only roughness on top of it
CHARACTER = {
    "_default": dict(spread=ROUGH_SPREAD, grain=1.0, micro=1.0),
    "core_shell": dict(spread=0.050, grain=1.15, micro=1.0),
    "core_inset": dict(spread=0.045, grain=1.10, micro=0.9),
    "core_accent": dict(spread=0.040, grain=0.85, micro=1.2),
    "hcai_shell": dict(spread=0.025, grain=0.70, micro=0.8),
    "hcai_inset": dict(spread=0.030, grain=0.80, micro=0.9),
    "hcai_inner": dict(spread=0.025, grain=0.75, micro=0.9),
    "health_shell": dict(spread=0.050, grain=1.30, micro=1.1),
    "health_inset": dict(spread=0.045, grain=1.25, micro=1.0),
    "wearable_shell": dict(spread=0.060, grain=1.00, micro=1.0),
    "wearable_inset": dict(spread=0.050, grain=1.05, micro=1.0),
}

# Groove recovery. (colatitude_deg, width, rotation_deg) copied from
# build_hero_v2_graybox.py; the radius is the PRE-normalisation sphere radius the
# tool was built against. `scale` is re-derived per object at apply time.
GROOVE_SPECS = {
    "CORE_SPHERE": dict(radius=0.725, specs=((90.0, 0.026, (22.0, 0.0, -34.0)),)),
    "HHB_SPHERE": dict(radius=0.5, specs=((90.0, 0.019, (16.0, 0.0, 12.0)),
                                          (54.0, 0.016, (-14.0, 0.0, -22.0)))),
    "WE_SPHERE": dict(radius=0.5, specs=((62.0, 0.045, (18.0, 0.0, 20.0)),
                                         (118.0, 0.038, (10.0, 0.0, -34.0)))),
}
# The HCAI aperture is an OPENING, not a bite, so it has no cutter to recover.
# Its inner wall sits at R - 0.052 (10.4% inside); the threshold is loose enough
# to also catch the solidified rim ring.
HCAI_INNER_THRESHOLD = 0.94

BAND_LO = 0.45            # fraction of the tool width
BAND_HI = 1.55


def hex_to_linear(value):
    """sRGB hex -> linear RGB (Blender's base colours are linear)."""
    value = value.lstrip("#")
    out = []
    for index in range(0, 6, 2):
        channel = int(value[index:index + 2], 16) / 255.0
        out.append(channel / 12.92 if channel <= 0.04045
                   else ((channel + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def role_hex(role):
    """sRGB hex as authored (for reports and checks)."""
    return PALETTE[role][0][0]


def role_colour(role):
    """Linear RGB for a Blender socket."""
    return hex_to_linear(PALETTE[role][0][0])


def role_roughness(role):
    return PALETTE[role][0][1]


def role_metallic(role):
    return PALETTE[role][0][2]


def role_note(role):
    return PALETTE[role][1]


# ----------------------------------------------------------------------- materials
def _clear(role):
    name = "M_%s" % role.upper()
    existing = bpy.data.materials.get(name)
    if existing is not None:
        bpy.data.materials.remove(existing)
    return name


def make_mineral_material(role, base_hex=None):
    """One shell/inset material of the family. Same graph for every role.

    `base_hex` overrides the palette colour (used by --debug-mask).
    """
    name = _clear(role)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (
        hex_to_linear(base_hex) if base_hex else role_colour(role))
    character = CHARACTER.get(role, CHARACTER["_default"])
    bsdf.inputs["Metallic"].default_value = role_metallic(role)
    bsdf.inputs["Roughness"].default_value = role_roughness(role)
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = IOR

    geo = nodes.new("ShaderNodeNewGeometry")
    geo.location = (-900, 0)

    grain = nodes.new("ShaderNodeTexNoise")
    grain.location = (-660, 120)
    grain.inputs["Scale"].default_value = GRAIN_SCALE
    grain.inputs["Detail"].default_value = 3.0
    grain.inputs["Roughness"].default_value = 0.5
    links.new(geo.outputs["Position"], grain.inputs["Vector"])

    micro = nodes.new("ShaderNodeTexNoise")
    micro.location = (-660, -180)
    micro.inputs["Scale"].default_value = MICRO_SCALE
    micro.inputs["Detail"].default_value = 2.0
    micro.inputs["Roughness"].default_value = 0.45
    links.new(geo.outputs["Position"], micro.inputs["Vector"])

    bump_grain = nodes.new("ShaderNodeBump")
    bump_grain.location = (-400, -60)
    bump_grain.inputs["Strength"].default_value = GRAIN_BUMP * character["grain"]
    bump_grain.inputs["Distance"].default_value = 0.02
    links.new(grain.outputs["Fac"], bump_grain.inputs["Height"])

    bump_micro = nodes.new("ShaderNodeBump")
    bump_micro.location = (-220, -60)
    bump_micro.inputs["Strength"].default_value = MICRO_BUMP * character["micro"]
    bump_micro.inputs["Distance"].default_value = 0.01
    links.new(micro.outputs["Fac"], bump_micro.inputs["Height"])
    links.new(bump_grain.outputs["Normal"], bump_micro.inputs["Normal"])
    links.new(bump_micro.outputs["Normal"], bsdf.inputs["Normal"])

    # Roughness variation: the grain field nudged into a narrow satin band. This
    # is what makes the surface feel tactile instead of airbrushed.
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-400, 260)
    lo = max(0.05, role_roughness(role) - character["spread"])
    hi = min(0.95, role_roughness(role) + character["spread"])
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (lo, lo, lo, 1.0)
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (hi, hi, hi, 1.0)
    links.new(grain.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])

    mat["hero_v2_role"] = role
    mat["hero_v2_note"] = role_note(role)
    return mat


def make_backdrop_material():
    """Review environment only: matte, deep, neutral. Slightly desaturated so the
    coloured forms are the only chroma in frame."""
    name = _clear("backdrop")
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = role_colour("backdrop")
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = role_roughness("backdrop")
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = IOR
    mat["hero_v2_role"] = "backdrop"
    mat["hero_v2_note"] = role_note("backdrop")
    return mat


def material_roles():
    """Every role Stage 2 authors, in report order."""
    return tuple(PALETTE.keys())


# ------------------------------------------------------------------- groove recovery
def _tool_frame(colatitude_deg, width, rotation_deg, radius, scale):
    """Torus tube-centre circle -> (axis, centre, tube radius) in mesh space."""
    phi0 = math.radians(colatitude_deg)
    rot = Euler(tuple(math.radians(a) for a in rotation_deg), "XYZ").to_matrix()
    axis = (rot @ Vector((0.0, 0.0, 1.0))).normalized()
    centre = rot @ Vector((0.0, 0.0, radius * math.cos(phi0)))
    return axis, centre, radius * math.sin(phi0), width * scale


def _mean_face_size(mesh):
    total = 0.0
    for poly in mesh.polygons:
        if poly.area <= 0.0:
            continue
        total += math.sqrt(poly.area)
    return total / max(1, len(mesh.polygons))


def groove_face_mask(obj, specs, radius):
    """Polygon indices lying on (or one step around) a groove surface.

    A point is on the groove if its distance to the tool's tube-centre circle is
    the tube radius. Points inside the tube were removed by the boolean, so the
    marked set is the recessed floor, its walls and the rounded rim.
    """
    mesh = obj.data
    outer = max((Vector(v.co).length for v in mesh.vertices), default=0.0)
    scale = outer / radius if radius > 0 and outer > 0 else 1.0
    slack = min(0.30 * _mean_face_size(mesh), 0.35 * max(
        [w for _c, w, _r in specs], default=0.0) * scale)
    frames = [_tool_frame(colat, width, rot, radius, scale)
              for colat, width, rot in specs]
    marked = set()
    for poly in mesh.polygons:
        for index in poly.vertices:
            point = Vector(mesh.vertices[index].co)
            for axis, centre, major, tube in frames:
                rel = point - centre
                axial = rel.dot(axis)
                perp = (rel - axis * axial).length
                distance = math.hypot(perp - major, axial)
                if (BAND_LO * tube - slack) <= distance <= (BAND_HI * tube + slack):
                    marked.add(poly.index)
                    break
            else:
                continue
            break
    return marked


def hcai_inner_mask(obj, threshold=HCAI_INNER_THRESHOLD):
    """Faces on the solidified shell's inner wall plus the rim ring."""
    mesh = obj.data
    outer = max((Vector(v.co).length for v in mesh.vertices), default=0.0)
    limit = outer * threshold
    marked = set()
    for poly in mesh.polygons:
        for index in poly.vertices:
            if Vector(mesh.vertices[index].co).length < limit:
                marked.add(poly.index)
                break
    return marked


def assign_roles(obj, shell_role, inset_role=None, mask=None):
    """Assign the shell role to the object, and the inset role to `mask`."""
    shell = bpy.data.materials["M_%s" % shell_role.upper()]
    obj.data.materials.clear()
    obj.data.materials.append(shell)
    if inset_role is None or not mask:
        return 0
    inset = bpy.data.materials["M_%s" % inset_role.upper()]
    obj.data.materials.append(inset)
    slot = len(obj.data.materials) - 1
    for index in mask:
        obj.data.polygons[index].material_index = slot
    return len(mask)


def assign_single(obj, role):
    mat = bpy.data.materials["M_%s" % role.upper()]
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return len(obj.data.polygons)


# ---------------------------------------------------------------- review environment
def build_review_environment(collection):
    """A seamless matte backdrop so shadows read and silhouettes separate.

    A cyclorama rather than a floor plane: a floor introduces a horizon line,
    which is exactly the "busy" the card rules out. The fillet curve leaves no
    seam for the light to break on, and the tonal gradient comes from the light
    falloff itself instead of a painted gradient. This is review furniture: it is
    never exported and no authored form is moved to accommodate it.
    """
    profile = []
    for step in range(0, 13):
        angle = math.pi * 0.5 * step / 12.0
        profile.append((2.60 + 2.00 * math.sin(angle), -0.10 - 2.00 * math.cos(angle)))
    profile.append((4.60, 5.20))          # the wall
    profile.insert(0, (-5.00, -2.10))     # the floor reaching toward the camera
    profile.insert(1, (2.60, -2.10))

    mesh = bpy.data.meshes.new("BACKDROP")
    verts = []
    for x in (-9.0, 9.0):
        verts.extend((x, y, z) for y, z in profile)
    faces = []
    count = len(profile)
    for index in range(count - 1):
        # Wound so the surface faces the objects: the first attempt used the
        # opposite order, which left the floor facing down and the wall facing
        # away -- both shaded black, with a hard tonal step across the frame.
        faces.append((count + index, count + index + 1, index + 1, index))
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new("BACKDROP", mesh)
    bpy.context.scene.collection.objects.link(obj)
    if collection is not None:
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        collection.objects.link(obj)
    obj.data.materials.append(make_backdrop_material())
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def build_studio_rig(collection, target, key_energy=1200.0):
    """Soft key + gentle fill + one subtle top-back separation light.

    Deliberately not rim-heavy: every source is a large area light at a low
    level, so the falloff stays elegant and the shadows stay readable without
    going harsh. Neutral-to-barely-warm key, barely-cool fill.
    """
    centre = Vector(target)
    key = _area("LG2_Key", key_energy, (1.0, 0.985, 0.955),
                centre + Vector((-3.0, -3.4, 3.1)), 4.0, centre)
    fill = _area("LG2_Fill", key_energy * 0.22, (0.95, 0.97, 1.0),
                 centre + Vector((3.8, -2.6, 0.4)), 5.0, centre)
    sep = _area("LG2_Sep", key_energy * 0.30, (1.0, 1.0, 1.0),
                centre + Vector((1.5, 3.4, 3.2)), 2.6, centre)
    for light in (key, fill, sep):
        if collection is not None:
            for coll in list(light.users_collection):
                coll.objects.unlink(light)
            collection.objects.link(light)
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
    direction = (target - Vector(location)).normalized()
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


def set_world_ambient(strength=0.06, colour=(0.62, 0.66, 0.72, 1.0)):
    """Low, faintly cool ambient only. The rig does the work."""
    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("HERO_V2_World")
    world = scene.world
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = colour
    background.inputs["Strength"].default_value = strength
    return world
