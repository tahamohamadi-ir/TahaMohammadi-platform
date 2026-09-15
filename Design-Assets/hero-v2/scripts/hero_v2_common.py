# hero_v2_common.py -- shared infrastructure for the Home hero v2 Blender asset.
#
# Scope: HERO_PRODUCTION_PLAN_v2.md sections 2 and 3. One scene, four tactile
# organic forms, two camera compositions. Nothing here is wired into the
# frontend; this module only builds geometry, a NEUTRAL PREVIEW rig, and the
# composition measurements a reviewer can re-read.
#
# Safety: NEVER calls bpy.ops.wm.read_factory_settings() -- it has previously
# unloaded the owner's Blender MCP addon. The scene is emptied object by object.
import math

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

TAG = "[HERO_V2]"


def log(msg):
    print(TAG + " " + msg, flush=True)


# ------------------------------------------------------------------ scene basics
def purge_orphans():
    """Drop datablocks nothing references.

    Blender's factory startup file itself carries materials ("Material",
    "Dots Stroke"), and clearing only the objects leaves them behind in the
    saved artefact where a validator will -- correctly -- find them.
    """
    for collection in (bpy.data.materials, bpy.data.meshes, bpy.data.lights,
                       bpy.data.cameras, bpy.data.textures, bpy.data.images,
                       bpy.data.node_groups):
        for block in list(collection):
            if block.users == 0:
                collection.remove(block)


def clear_scene():
    """Empty the scene OBJECT BY OBJECT (never read_factory_settings)."""
    for obj in list(bpy.data.objects):
        try:
            bpy.data.objects.remove(obj, do_unlink=True)
        except Exception as exc:  # pragma: no cover - defensive
            log("clear_scene: could not remove %s (%s)" % (obj.name, exc))
    for coll in list(bpy.data.collections):
        try:
            bpy.data.collections.remove(coll)
        except Exception:  # pragma: no cover - defensive
            pass
    purge_orphans()
    bpy.context.view_layer.update()


def ensure_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
    return coll


def link_to(obj, coll):
    """Link an object into exactly one collection (objects are created in the
    scene root collection, so unlink them there first)."""
    for owner in list(obj.users_collection):
        if owner is not coll:
            owner.objects.unlink(obj)
    if obj.name not in coll.objects:
        coll.objects.link(obj)
    return obj


def deselect_all():
    for obj in bpy.context.view_layer.objects:
        if obj is None:
            # Removing objects outright can leave stale entries in the view
            # layer until the next update; calling select_set on them throws.
            continue
        obj.select_set(False)


def set_active(obj):
    if obj is None:
        return
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def apply_modifier(obj, mod_name):
    deselect_all()
    set_active(obj)
    try:
        bpy.ops.object.modifier_apply(modifier=mod_name)
    except RuntimeError as exc:  # pragma: no cover - defensive
        log("modifier_apply %s on %s FAILED: %s" % (mod_name, obj.name, exc))
        raise


# ------------------------------------------------------------------ mesh helpers
def mesh_to_bmesh(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    return bm


def bmesh_to_mesh(obj, bm):
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def scale_verts(obj, sx, sy, sz):
    """Non-uniform scale baked straight into the vertices (no operator context)."""
    bm = mesh_to_bmesh(obj)
    for v in bm.verts:
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz
    bmesh_to_mesh(obj, bm)


def translate_verts(obj, vec):
    bm = mesh_to_bmesh(obj)
    for v in bm.verts:
        v.co += vec
    bmesh_to_mesh(obj, bm)


def radial_harmonic_deform(obj, a2, a3):
    """Broad organic deformation, bounded by |a2|*2/3 + |a3| of the radius.

    A soft low-order radial field, so the form still reads as a sphere while the
    surface stops reading as a primitive. Documented amplitude budget: keep the
    total inside HERO_PRODUCTION_PLAN_v2 section 3's 2-4% of diameter.
    """
    bm = mesh_to_bmesh(obj)
    for v in bm.verts:
        p = v.co
        r = p.length
        if r < 1e-9:
            continue
        ct = p.z / r
        st2 = max(0.0, 1.0 - ct * ct)
        phi = math.atan2(p.y, p.x)
        scale = 1.0 + a2 * (ct * ct - 1.0 / 3.0) + a3 * st2 * math.cos(2.0 * phi)
        v.co = p * scale
    bmesh_to_mesh(obj, bm)


def shade_smooth_by_angle(obj, angle_deg):
    """Smooth shading with sharp edges above `angle_deg`.

    Blender 4.1+ splits normals on `edge.smooth == False` directly, so this needs
    no auto-smooth option and no operator context.
    """
    bm = mesh_to_bmesh(obj)
    limit = math.cos(math.radians(angle_deg))
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) != 2:
            e.smooth = False
        else:
            e.smooth = e.link_faces[0].normal.dot(e.link_faces[1].normal) >= limit
    bmesh_to_mesh(obj, bm)


def clean_mesh(obj, dist=1e-5):
    """Hygiene pass: merge doubles, drop degenerate faces/edges."""
    bm = mesh_to_bmesh(obj)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh_to_mesh(obj, bm)


def mesh_stats(obj):
    deps = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(deps)
    mesh = eval_obj.to_mesh()
    try:
        triangles = sum(len(p.vertices) - 2 for p in mesh.polygons)
        return dict(
            vertices=len(mesh.vertices),
            faces=len(mesh.polygons),
            triangles=triangles,
            dimensions=[round(d, 4) for d in obj.dimensions],
            materials=[m.name if m else None for m in obj.data.materials],
        )
    finally:
        eval_obj.to_mesh_clear()


# ---------------------------------------------------------------- geometry build
def new_uv_sphere(name, radius, segments=96, rings=60):
    deselect_all()
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=radius, location=(0, 0, 0))
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name + "_mesh"
    return obj


def new_torus(name, major, minor, location=(0, 0, 0), rotation=(0, 0, 0),
              major_segments=112, minor_segments=20):
    deselect_all()
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major, minor_radius=minor, major_segments=major_segments,
        minor_segments=minor_segments, location=location, rotation=rotation)
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name + "_mesh"
    return obj


def boolean_difference(target, cutter):
    """EXACT boolean difference, then remove the cutter."""
    mod = target.modifiers.new("BOOLEAN_CUT", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    try:
        mod.solver = "EXACT"
    except (AttributeError, TypeError):  # pragma: no cover - older/newer solver set
        pass
    apply_modifier(target, mod.name)
    cutter_mesh = cutter.data
    bpy.data.objects.remove(cutter, do_unlink=True)
    if cutter_mesh.users == 0:
        bpy.data.meshes.remove(cutter_mesh)


def spherical_groove_tool(name, sphere_radius, colatitude_deg, width,
                          rotation_deg=(0, 0, 0)):
    """A torus whose tube-centre circle lies exactly ON the sphere surface.

    With major = R*sin(phi0) and the tube centred at height R*cos(phi0), the tool
    cuts a groove of maximum depth `width` and surface width `2*width` that
    follows the volume, for ANY colatitude. Rotating the tool just moves the
    circle elsewhere on the same sphere.
    """
    phi0 = math.radians(colatitude_deg)
    major = sphere_radius * math.sin(phi0)
    height = sphere_radius * math.cos(phi0)
    # The rotation has to happen about the SPHERE's centre, not about the tool's
    # own origin: a cutter that sits off-centre would swing away from the
    # surface. Blender composes R * local + location, so pre-rotating the offset
    # yields R * (local + offset) -- a true rotation about the sphere centre.
    rot = Euler(tuple(math.radians(a) for a in rotation_deg), "XYZ")
    offset = rot.to_matrix() @ Vector((0.0, 0.0, height))
    return new_torus(name, major, width, location=offset,
                     rotation=tuple(math.radians(a) for a in rotation_deg))


def delete_faces_in_cone(obj, axis, cos_limit):
    """Drop the faces whose normal lies inside a cone around `axis`.

    Used for the shell aperture (an OPENING, not a boolean bite).
    """
    bm = mesh_to_bmesh(obj)
    a = Vector(axis).normalized()
    kill = [f for f in bm.faces if f.normal.dot(a) >= cos_limit]
    count = len(kill)
    if kill:
        bmesh.ops.delete(bm, geom=kill, context="FACES")
    bmesh_to_mesh(obj, bm)
    return count


def bisect_remove_cap(obj, plane_co, plane_no):
    """Cut a clean circular opening and drop the cap on the normal's side.

    A face-normal cone test leaves a jagged staircase rim; bisecting with a real
    plane gives an exact boundary loop, which is what the solidifier turns into
    the shell's rim.
    """
    bm = mesh_to_bmesh(obj)
    geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
    result = bmesh.ops.bisect_plane(
        bm, geom=geom, dist=1e-6, plane_co=Vector(plane_co),
        plane_no=Vector(plane_no), clear_outer=True)
    bmesh_to_mesh(obj, bm)
    return len(result["geom_cut"])


def add_solidify(obj, thickness, offset=-1.0):
    mod = obj.modifiers.new("SOLIDIFY", "SOLIDIFY")
    mod.thickness = thickness
    mod.offset = offset
    mod.use_rim = True
    mod.use_rim_only = False
    apply_modifier(obj, mod.name)


def add_bevel(obj, width, segments, angle_limit_deg=40.0):
    mod = obj.modifiers.new("BEVEL", "BEVEL")
    mod.width = width
    mod.segments = segments
    mod.limit_method = "ANGLE"
    try:
        mod.angle_limit = math.radians(angle_limit_deg)
    except (AttributeError, TypeError):  # pragma: no cover
        pass
    apply_modifier(obj, mod.name)


def tapered_arc(name, radius, sweep_deg, tube_max, tube_min_ratio,
                frames=180, tube_segments=10):
    """A thin, tapered, INCOMPLETE arc -- no endpoints, no arrowheads.

    The tube fades to a fine point at both ends, which is what lets a decoration
    read as a drawn gesture instead of a solid ring.
    """
    bm = bmesh.new()
    sweep = math.radians(sweep_deg)
    rings = []
    for i in range(frames + 1):
        t = i / frames
        ang = -sweep / 2.0 + sweep * t
        # sin(pi*t) is 0 at both ends -> a graceful taper to a needle point
        k = tube_min_ratio + (1.0 - tube_min_ratio) * (math.sin(math.pi * t) ** 0.65)
        r_t = tube_max * k
        centre = Vector((math.cos(ang) * radius, math.sin(ang) * radius, 0.0))
        radial = Vector((math.cos(ang), math.sin(ang), 0.0))
        up = Vector((0.0, 0.0, 1.0))
        ring = []
        for j in range(tube_segments):
            a = 2.0 * math.pi * j / tube_segments
            ring.append(bm.verts.new(
                centre + radial * (math.cos(a) * r_t) + up * (math.sin(a) * r_t)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(tube_segments):
            j2 = (j + 1) % tube_segments
            bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
    bm.faces.new(tuple(reversed(rings[0])))
    bm.faces.new(tuple(rings[-1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = bpy.data.objects.new(name, bpy.data.meshes.new(name + "_mesh"))
    bpy.context.scene.collection.objects.link(obj)
    bm.to_mesh(obj.data)
    bm.free()
    return obj


# -------------------------------------------------------------- scale contract
def world_bounds(objs):
    """World-space bounding box of DEPSGRAPH-EVALUATED geometry.

    `Object.bound_box` lags behind direct bmesh edits, which once normalised a
    node to 0.92 while the report claimed 1.0.
    """
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for obj in objs:
        if obj.type != "MESH":
            continue
        eval_obj = obj.evaluated_get(deps)
        mesh = eval_obj.to_mesh()
        try:
            matrix = eval_obj.matrix_world
            for vertex in mesh.vertices:
                w = matrix @ vertex.co
                lo = Vector((min(lo.x, w.x), min(lo.y, w.y), min(lo.z, w.z)))
                hi = Vector((max(hi.x, w.x), max(hi.y, w.y), max(hi.z, w.z)))
        finally:
            eval_obj.to_mesh_clear()
    return lo, hi


def group_diameter(objs):
    lo, hi = world_bounds(objs)
    size = hi - lo
    return max(size.x, size.y, size.z)


def normalize_group(objs, target_diam):
    """Scale a whole node to the contract diameter (never per mesh)."""
    diameter = group_diameter(objs)
    if diameter <= 0:
        return 1.0
    factor = target_diam / diameter
    for obj in objs:
        scale_verts(obj, factor, factor, factor)
        obj.scale = (1.0, 1.0, 1.0)
    return factor


def evaluated_verts(obj):
    """World-space vertices of the evaluated mesh (for measurement only)."""
    deps = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(deps)
    mesh = eval_obj.to_mesh()
    try:
        matrix = eval_obj.matrix_world
        return [matrix @ v.co for v in mesh.vertices]
    finally:
        eval_obj.to_mesh_clear()


def min_distance_to_object(obj, world_points):
    """Nearest distance from world points to an object's SURFACE (BVH query).

    Uses `closest_point_on_mesh`, not an O(N*M) vertex scan, so a clearance
    check over a few thousand sample points stays instant.
    """
    bpy.context.view_layer.update()
    inverse = obj.matrix_world.inverted()
    best = 1e9
    for wp in world_points:
        ok, loc, _nrm, _idx = obj.closest_point_on_mesh(inverse @ wp)
        if not ok:
            continue
        best = min(best, (obj.matrix_world @ loc - wp).length)
    return best


# -------------------------------------------------------------------- hierarchy
def make_empty(name, parent=None):
    empty = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(empty)
    empty.empty_display_type = "PLAIN_AXES"
    empty.empty_display_size = 0.25
    if parent:
        empty.parent = parent
    return empty


# --------------------------------------------------- projected composition maths
def look_at(obj, target):
    """Point an object's local -Z at `target` (cameras AND area lights)."""
    direction = Vector(obj.location) - Vector(target)   # local -Z points at target
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()


def project_verts(cam, objs, stride=1):
    """Project evaluated vertices to normalised camera view coords (0..1)."""
    from bpy_extras.object_utils import world_to_camera_view
    scene = bpy.context.scene
    bpy.context.view_layer.update()
    out = {}
    for obj in objs:
        pts = []
        for w in evaluated_verts(obj)[::stride]:
            p = world_to_camera_view(scene, cam, w)
            pts.append((p.x, p.y))
        out[obj.name] = pts
    return out


def hull2d(points):
    """Andrew's monotone chain; returns a CCW convex hull."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _seg_seg_distance(p1, p2, p3, p4):
    """2D minimum distance between two segments."""
    def point_seg(p, a, b):
        ab = (b[0] - a[0], b[1] - a[1])
        denom = ab[0] * ab[0] + ab[1] * ab[1]
        if denom <= 1e-18:
            return math.hypot(p[0] - a[0], p[1] - a[1])
        t = ((p[0] - a[0]) * ab[0] + (p[1] - a[1]) * ab[1]) / denom
        t = max(0.0, min(1.0, t))
        return math.hypot(p[0] - (a[0] + t * ab[0]), p[1] - (a[1] + t * ab[1]))

    if _segments_intersect(p1, p2, p3, p4):
        return 0.0
    return min(point_seg(p1, p3, p4), point_seg(p2, p3, p4),
               point_seg(p3, p1, p2), point_seg(p4, p1, p2))


def _segments_intersect(p1, p2, p3, p4):
    def orient(a, b, c):
        val = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if abs(val) < 1e-12:
            return 0
        return 1 if val > 0 else 2

    o1, o2 = orient(p1, p2, p3), orient(p1, p2, p4)
    o3, o4 = orient(p3, p4, p1), orient(p3, p4, p2)
    return o1 != o2 and o3 != o4


def hull_distance(h1, h2):
    """Minimum separation between two convex hulls (0.0 when they overlap)."""
    if len(h1) < 2 or len(h2) < 2:
        return 0.0
    if _hull_contains(h1, h2[0]) or _hull_contains(h2, h1[0]):
        return 0.0
    best = 1e9
    for i in range(len(h1)):
        a1, a2 = h1[i], h1[(i + 1) % len(h1)]
        for j in range(len(h2)):
            b1, b2 = h2[j], h2[(j + 1) % len(h2)]
            best = min(best, _seg_seg_distance(a1, a2, b1, b2))
    return best


def _hull_contains(hull, p):
    """Convex polygon containment (hull is CCW)."""
    n = len(hull)
    if n < 3:
        return False
    for i in range(n):
        a, b = hull[i], hull[(i + 1) % n]
        if (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) < -1e-12:
            return False
    return True


# -------------------------------------------------------------------- cameras
def make_camera(name, view_dir, distance, target, cam_type="PERSP", lens=70.0):
    cam_data = bpy.data.cameras.new(name)
    cam_data.type = cam_type
    cam_data.sensor_fit = "AUTO"
    cam_data.sensor_width = 36.0
    if cam_type == "PERSP":
        cam_data.lens = lens
    obj = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = Vector(target) - Vector(view_dir).normalized() * distance
    look_at(obj, target)
    return obj


def _set_camera_pose(cam, view_dir, distance, target):
    cam.location = Vector(target) - Vector(view_dir).normalized() * distance
    look_at(cam, target)


def _projected_bounds(cam, objs, stride=1):
    pts = []
    for group in objs.values():
        for name, p in project_verts(cam, group, stride=stride).items():
            pts.extend(p)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def fit_camera(cam, objs, view_dir, target, margin, res_x, res_y,
               iterations=26):
    """Frame the four forms so they occupy (1 - 2*margin) of BOTH axes.

    Plans section 3 asks for at least 8% clear space at the image edges, so
    `margin=0.08` targets a 0.84 screen extent.
    """
    scene = bpy.context.scene
    target_fill = 1.0 - 2.0 * margin
    # world_to_camera_view() reads the SCENE resolution, so the frame the camera
    # is fitted against must already be the render's own frame.
    set_resolution(res_x, res_y)
    target = Vector(target)
    distance = 10.0
    perp = Vector(view_dir).normalized().cross(Vector((0.0, 0.0, 1.0)))
    if perp.length < 1e-6:
        perp = Vector((1.0, 0.0, 0.0))
    perp.normalize()
    up = perp.cross(Vector(view_dir).normalized()).normalized()

    if cam.data.type == "ORTHO":
        for _ in range(6):
            _set_camera_pose(cam, view_dir, distance, target)
            bpy.context.view_layer.update()
            lo_x, lo_y, hi_x, hi_y = _projected_bounds(cam, objs, stride=4)
            span = max(hi_x - lo_x, hi_y - lo_y)
            if span <= 1e-9:
                break
            # ortho projection is linear in ortho_scale, so one step converges
            cam.data.ortho_scale *= span / target_fill
        _set_camera_pose(cam, view_dir, distance, target)
        bpy.context.view_layer.update()
        return _recenter_and_measure(cam, objs, view_dir, target, distance,
                                     target_fill, res_x, res_y, perp, up,
                                     ortho=True)

    for _ in range(iterations):
        _set_camera_pose(cam, view_dir, distance, target)
        bpy.context.view_layer.update()
        lo_x, lo_y, hi_x, hi_y = _projected_bounds(cam, objs, stride=4)
        span = max(hi_x - lo_x, hi_y - lo_y)
        if span <= 1e-9:
            break
        distance *= span / target_fill
    _set_camera_pose(cam, view_dir, distance, target)
    bpy.context.view_layer.update()
    return _recenter_and_measure(cam, objs, view_dir, target, distance,
                                 target_fill, res_x, res_y, perp, up,
                                 ortho=False)


def _recenter_and_measure(cam, objs, view_dir, target, distance, target_fill,
                          res_x, res_y, perp, up, ortho):
    """Nudge the camera so the projected content is centred, then report."""
    scene = bpy.context.scene
    for _ in range(10):
        _set_camera_pose(cam, view_dir, distance, target)
        bpy.context.view_layer.update()
        lo_x, lo_y, hi_x, hi_y = _projected_bounds(cam, objs, stride=4)
        cx, cy = (lo_x + hi_x) * 0.5, (lo_y + hi_y) * 0.5
        if abs(cx - 0.5) < 1e-4 and abs(cy - 0.5) < 1e-4:
            break
        # world size of one normalised unit at the content plane
        if ortho:
            if res_x >= res_y:
                unit_x = cam.data.ortho_scale
                unit_y = unit_x * res_y / float(res_x)
            else:
                unit_y = cam.data.ortho_scale
                unit_x = unit_y * res_x / float(res_y)
        else:
            # sensor_fit AUTO maps sensor_width onto the LARGER image dimension
            big = 2.0 * distance * math.tan(
                math.atan(cam.data.sensor_width * 0.5 / cam.data.lens))
            if res_x >= res_y:
                unit_x, unit_y = big, big * res_y / float(res_x)
            else:
                unit_y, unit_x = big, big * res_x / float(res_y)
        target = Vector(target) + perp * ((cx - 0.5) * unit_x) \
            + up * ((cy - 0.5) * unit_y)

    _set_camera_pose(cam, view_dir, distance, target)
    bpy.context.view_layer.update()
    lo_x, lo_y, hi_x, hi_y = _projected_bounds(cam, objs)
    return dict(distance=round(distance, 4),
                target=[round(v, 4) for v in target],
                projected_bbox=[round(lo_x, 4), round(lo_y, 4),
                                round(hi_x, 4), round(hi_y, 4)],
                fill_x=round(hi_x - lo_x, 4), fill_y=round(hi_y - lo_y, 4))


def composition_report(cam, objs, res_x, res_y):
    """Per-form projected sizes, silhouette gaps and edge clearance in PIXELS.

    Gaps are measured between FORMS -- a form is one group, its shell AND its
    inset together. Comparing sub-meshes would report the core's accent detail
    as a zero gap against the core it is embedded in, which is meaningless.
    """
    set_resolution(res_x, res_y)
    px_x, px_y = float(res_x), float(res_y)

    forms = {}
    meshes = {}
    hulls = {}
    all_x, all_y = [], []
    for group_name, group in objs.items():
        projected = project_verts(cam, group)
        xs, ys = [], []
        for mesh_name, pts in projected.items():
            mxs = [p[0] * px_x for p in pts]
            mys = [p[1] * px_y for p in pts]
            meshes[mesh_name] = dict(
                width_px=round(max(mxs) - min(mxs), 1),
                height_px=round(max(mys) - min(mys), 1))
            xs += mxs
            ys += mys
        hulls[group_name] = hull2d(list(zip(xs, ys)))
        all_x += xs
        all_y += ys
        forms[group_name] = dict(
            bbox_px=[round(min(xs), 1), round(min(ys), 1),
                     round(max(xs), 1), round(max(ys), 1)],
            width_px=round(max(xs) - min(xs), 1),
            height_px=round(max(ys) - min(ys), 1),
            projected_diameter_px=round(max(max(xs) - min(xs),
                                            max(ys) - min(ys)), 1),
        )

    names = sorted(hulls)
    gaps = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            gaps["%s|%s" % (a, b)] = round(hull_distance(hulls[a], hulls[b]), 1)

    lo_x, hi_x = min(all_x), max(all_x)
    lo_y, hi_y = min(all_y), max(all_y)
    return dict(
        resolution=[res_x, res_y],
        forms=forms,
        meshes=meshes,
        silhouette_gaps_px=gaps,
        min_silhouette_gap_px=round(min(gaps.values()), 1) if gaps else None,
        content_bbox_px=[round(lo_x, 1), round(lo_y, 1), round(hi_x, 1),
                         round(hi_y, 1)],
        edge_clearance_px=dict(left=round(lo_x, 1), right=round(px_x - hi_x, 1),
                               bottom=round(lo_y, 1), top=round(px_y - hi_y, 1)),
        edge_clearance_pct=dict(
            left=round(lo_x / px_x * 100.0, 2),
            right=round((px_x - hi_x) / px_x * 100.0, 2),
            bottom=round(lo_y / px_y * 100.0, 2),
            top=round((px_y - hi_y) / px_y * 100.0, 2)),
        fill_pct=dict(x=round((hi_x - lo_x) / px_x * 100.0, 2),
                      y=round((hi_y - lo_y) / px_y * 100.0, 2)),
    )


# ----------------------------------------------------------------------- lights
def add_area_light(name, energy, color, location, size, target, coll=None):
    data = bpy.data.lights.new(name, type="AREA")
    data.shape = "SQUARE"
    data.size = size
    data.energy = energy
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    look_at(obj, target)
    if coll is not None:
        link_to(obj, coll)
    return obj


# ---------------------------------------------------------------- render setup
def setup_cycles(samples, exposure, gpu=True):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
    except TypeError:  # pragma: no cover
        pass
    scene.cycles.max_bounces = 8
    scene.cycles.diffuse_bounces = 4
    scene.cycles.glossy_bounces = 4
    scene.cycles.transmission_bounces = 4
    scene.cycles.transparent_max_bounces = 4
    scene.cycles.use_fast_gi = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = exposure
    for candidate in ("AgX - Medium High Contrast", "Medium High Contrast",
                      "AgX - Base Contrast", "None"):
        try:
            scene.view_settings.look = candidate
            break
        except TypeError:
            continue
    if not gpu:
        scene.cycles.device = "CPU"
        return "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "CUDA"
        prefs.get_devices()
        enabled = 0
        for device in prefs.devices:
            device.use = device.type == "CUDA"
            if device.use:
                enabled += 1
        scene.cycles.device = "GPU" if enabled else "CPU"
        return "CUDA(%d)" % enabled if enabled else "CPU"
    except Exception as exc:  # pragma: no cover - defensive
        log("GPU setup failed (%s); falling back to CPU" % exc)
        scene.cycles.device = "CPU"
        return "CPU"


def set_resolution(res_x, res_y):
    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y


def render_transparent(path, cam):
    """Plan section 3: transparent film, no floor, no baked background."""
    scene = bpy.context.scene
    scene.use_nodes = False
    scene.render.film_transparent = True
    scene.camera = cam
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    log("rendered %s" % path)


def write_text_block(name, content):
    block = bpy.data.texts.get(name)
    if block is None:
        block = bpy.data.texts.new(name)
    block.clear()
    block.write(content)
    return block
