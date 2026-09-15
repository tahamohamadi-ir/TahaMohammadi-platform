"""Hero v2 — Stage 3: scroll keyframe authoring (four static 3D states).

Stage 2.7 is the LOOK LOCK. Nothing here re-develops the look: the spheres are built by
Stage 2.7's own helpers with Stage 2.7's own constants, the materials come from
`hero_v2_stage2_7.build_all_materials()`, the rigs from `hero_v2_stage2_7.build_rig()`, and
the relation strokes from `hero_v2_stage2_7.build_relation_curve()` - so every locked value
(node geometry, material family, palette, dark/light look, lighting character, relation
line character, four nodes, three relationships) is inherited by construction rather than
re-authored.

What this module adds is *motion*: four authored states of one continuous reorientation.

Mechanism: `RIG_ROOT` is an empty placed at the core's own centre; the three companion
groups are parented to it with their world positions preserved. Rotating RIG_ROOT about
world Z (yaw) and world X (pitch) swings the companions around the core through real 3D
depth - the core itself is deliberately NOT a child of the rig, which is what makes its
perceptual stability a structural fact rather than a tuned one. The four states are baked
as constant-interpolation keyframes on scene frames 1-4, so the whole sequence is
reproducible from the saved .blend without any viewport state.

Deliberate limits, all from the card: 34 degrees of total yaw (band 22-38) and 7 degrees of
total pitch (band 4-12); no equal-angle rotation (0 / 9 / 25 / 34, and the middle step is
the largest because that is where the depth has to read); camera change is a sub-pixel-to-
few-pixel lateral parallax, not a move; no depth of field, motion blur, glow, particles,
fog or lens effects.
"""

from __future__ import annotations

import math

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

# ------------------------------------------------------------------- the four states
# `yaw_deg` / `pitch_deg` are applied to RIG_ROOT about world Z / world X, in degrees.
# `parallax` is a lateral camera offset in scene units (desktop only: the mobile camera is
# ORTHO, where a lateral move would slide the composition instead of creating parallax).
STATES = (
    dict(index=1, key="FRAME_01_REST", label="rest (the approved Stage 2.7 composition)",
         yaw_deg=0.0, pitch_deg=0.0, parallax=0.000,
         intent="initial Home state; identical to the look lock"),
    dict(index=2, key="FRAME_02_EARLY_ROTATION", label="early rotation",
         yaw_deg=10.0, pitch_deg=3.0, parallax=0.050,
         intent="small but visible depth change; one companion forward, one back"),
    dict(index=3, key="FRAME_03_MID_STRONGEST_DEPTH", label="mid / strongest depth",
         yaw_deg=26.0, pitch_deg=10.0, parallax=0.110,
         intent="strongest 3D and parallax distinction, still calm"),
    dict(index=4, key="FRAME_04_SETTLED_REVEAL", label="settled reveal",
         yaw_deg=36.0, pitch_deg=7.0, parallax=0.070,
         intent="another meaningful viewing angle; not a return to frame 01"),
)
STATE_FRAMES = tuple(state["index"] for state in STATES)

# ------------------------------------------------------------- pivot-offset sweep
# The crowding at FRAME_04 is solved by moving the rotation pivot, not by weakening the
# motion: RIG_ROOT's origin is offset from the core's centre so the companions sweep on a
# slightly larger arc. The offset direction is DERIVED from the core -> HEALTH vector in
# the rig's horizontal (XY) rotation plane, because for a yaw about Z the projection picks
# up d = (I - R)·P = ((1-c)·px + s·py, -s·px + (1-c)·py), and sending P along that vector
# makes both terms push HEALTH outward in screen space.
PIVOT_SWEEP = (0.00, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16)
PIVOT_MIN_GAP_PX = 5.0
PIVOT_PREFERRED_GAP_PX = 8.0
PIVOT_MAX_CORE_DRIFT_PCT = 2.5


def pivot_direction(core_position, health_position):
    """Unit direction in the horizontal rotation plane, from the core toward HEALTH."""
    delta = Vector((health_position[0] - core_position[0],
                    health_position[1] - core_position[1], 0.0))
    if delta.length < 1e-6:
        return Vector((1.0, 0.0, 0.0))
    return delta.normalized()

# --------------------------------------------------------------- safe text regions
# Desktop: the hero art occupies the RIGHT page column and the HTML copy owns the left
# one, so the region the art must never enter is the frame's left strip. It is declared
# here as a constant (not derived from the render) precisely so that it can fail.
# Normalized frame coordinates, top-left origin: (x0, y0, x1, y1).
DESKTOP_SAFE_TEXT_REGION = (0.015, 0.050, 0.085, 0.950)
# Mobile: the graph sits above or between content blocks, so the reserved zones are the
# top and bottom margins of the square art frame.
MOBILE_SAFE_TEXT_REGIONS = ((0.0, 0.0, 1.0, 0.045), (0.0, 0.955, 1.0, 1.0))
# The page-level integration contract this encodes: text column 0-38% of the page, art
# slot 40-96%. Inside the art slot the frame's left strip stays optically clear so the
# two columns do not touch. Reported with measurements in the Stage 3 report.
SAFE_REGION_NOTE = ("desktop: left strip of the art frame, kept clear so the HTML text "
                    "column beside the frame never touches the object; mobile: top and "
                    "bottom margins, because the graph sits between content blocks")

# ------------------------------------------------------------- continuity thresholds
# Bands, not targets: the validator reports the measured value next to the band it is
# checked against, so a change of intent is visible in the numbers.
BANDS = dict(
    core_displacement_pct=(0.0, 2.5),       # of frame width, per consecutive pair
    companion_displacement_pct=(0.5, 22.0),  # every node, every step / every node total
    companion_step_max_pct=2.0,             # at least one node clearly moves per step
    companion_total_min_pct=3.0,            # every node travels across the sequence
    companion_mobile_min_nodes=2,           # ortho: see the note in the validator
    node_scale_change_pct=(0.0, 12.0),      # apparent projected diameter
    companion_separation_pct=8.0,           # no two companions may collide/swap
    movement_01_04_iou_max=0.97,            # frame 04 must differ from frame 01
    movement_01_04_delta_min=0.02,
    edge_margin_pct=1.0,                    # no alpha pixel this close to a frame edge
    yaw_total_deg=(22.0, 38.0),
    pitch_total_deg=(4.0, 12.0),
)


def state_by_key(key):
    for state in STATES:
        if state["key"] == key:
            return state
    raise KeyError(key)


def total_yaw_deg():
    return max(state["yaw_deg"] for state in STATES) - \
        min(state["yaw_deg"] for state in STATES)


def total_pitch_deg():
    return max(state["pitch_deg"] for state in STATES) - \
        min(state["pitch_deg"] for state in STATES)


# ------------------------------------------------------------------------- rig helpers
def rig_rotation(state):
    """Euler for RIG_ROOT: pitch about X, yaw about Z, applied in XYZ order."""
    return (math.radians(state["pitch_deg"]), 0.0, math.radians(state["yaw_deg"]))


def set_state(rig_root, scene, state):
    """Move the scene to an authored state.

    Order matters: `frame_set` re-evaluates the animation, so setting the rotation first
    and stepping the frame afterwards throws the pose away (that silently keyed all four
    states at zero degrees once). The frame is set first, then the pose, then the depsgraph
    is updated.
    """
    scene.frame_set(state["index"])
    rig_root.rotation_euler = rig_rotation(state)
    bpy.context.view_layer.update()


def project(scene, camera, point):
    """Normalized (x, y) of a world point in the camera's frame: 0..1, top-left origin."""
    coords = world_to_camera_view(scene, camera, Vector(point))
    return (float(coords.x), 1.0 - float(coords.y))


def projected_radius(scene, camera, centre, radius):
    """Apparent radius of a sphere in normalized frame units, by projecting a limb point.

    The limb is offset perpendicular to the view direction, which is close enough at these
    distances and - unlike a formula - is measured through the same camera the render uses.
    """
    centre = Vector(centre)
    view = (centre - camera.matrix_world.translation).normalized()
    perpendicular = view.cross(Vector((0.0, 0.0, 1.0)))
    if perpendicular.length < 1e-6:
        perpendicular = Vector((1.0, 0.0, 0.0))
    perpendicular.normalize()
    a = Vector(project(scene, camera, centre))
    b = Vector(project(scene, camera, centre + perpendicular * radius))
    return (b - a).length


def stated_transforms(rig_root):
    """The authored values, recorded verbatim for the report."""
    return [dict(frame=state["index"], key=state["key"], label=state["label"],
                 yaw_deg=state["yaw_deg"], pitch_deg=state["pitch_deg"],
                 parallax=state["parallax"], intent=state["intent"],
                 rig_rotation_euler_deg=[round(math.degrees(a), 3)
                                         for a in rig_rotation(state)])
            for state in STATES]
