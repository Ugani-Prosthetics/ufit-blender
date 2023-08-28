import os
import bpy
import bmesh
import math
import numpy as np
from mathutils import Vector, Matrix, kdtree
from . import user_interface
from .....base.src.base_constants import base_path_consts


def poll_object_object_mode(context, object_name):
    # check if there is an object and a vertex selected
    active_object = context.active_object
    if active_object is not None \
            and active_object.type == 'MESH' \
            and active_object.mode == 'OBJECT' \
            and active_object.name == object_name:
        return True


def poll_object_edit_mode(context, object_name):
    # check if there is an object and a vertex selected
    active_object = context.active_object
    if active_object is not None \
            and active_object.type == 'MESH' \
            and active_object.mode == 'EDIT' \
            and active_object.name == object_name:
        return True


def get_scale(unit):
    scale = (1, 1, 1)
    if unit == 'centimeter':
        scale = (0.01, 0.01, 0.01)
    elif unit == 'millimeter':
        scale = (0.001, 0.001, 0.001)

    return scale


def delete_scene(context):
    # check if there are objects in the scene
    if context.scene.objects:
        # unhide all objects
        for obj in bpy.data.objects:
            obj.hide_set(False)
            obj.hide_select = False
            obj.select_set(True)

        # delete all objects
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        bpy.ops.outliner.orphans_purge()


def deselect_in_edit_mode(context):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    for f in bm.faces:
        f.select = False
    for e in bm.edges:
        e.select = False
    for v in bm.verts:
        v.select = False

    bm.select_flush_mode()
    obj.update()


def deselect_in_object_mode(context):
    # 2. deselect vertices, faces and edges
    face = context.object.data.polygons  # not faces!
    edge = context.object.data.edges
    vert = context.object.data.vertices

    # vertices can be selected
    # to deselect vertices you need to deselect faces(polygons) and edges at first
    for f in face:
        f.select = False
    for e in edge:
        e.select = False
    for v in vert:
        v.select = False


def deselect_edges_by_idx(context, indexes):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    for edge in bm.edges:
        if edge.index in indexes:
            edge.select = False


def get_selected_vertices(context):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    selected_vertices = []
    for v in bm.verts:
        if v.select:
            # you need to make a type of copy to avoid indexes become useless
            selected_vertices.append({
                'idx': v.index,
                'co': v.co
            })

    bm.select_flush_mode()
    return selected_vertices


def get_selected_vertices_co(context):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    selected_vertices = []
    for f in bm.verts:
        if f.select:
            selected_vertices.append(f.co)

    bm.select_flush_mode()
    return selected_vertices


def get_selected_vertices_ix(context):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    selected_vertices = []
    for f in bm.verts:
        if f.select:
            selected_vertices.append(f.index)

    bm.select_flush_mode()
    return selected_vertices


def get_selected_edges(context):
    obj = context.edit_object.data
    bm = bmesh.from_edit_mesh(obj)

    selected_edges = []
    for f in bm.edges:
        if f.select:
            selected_edges.append(f.index)

    bm.select_flush_mode()
    return selected_edges


def get_vertices_below_z(obj, z):
    verts = []
    for v in obj.data.vertices:
        if v.co.z < z:
            verts.append(v)
    return verts


def get_vertices_co_by_z(obj, z, decimals=3, margin=0.001):
    z = round(z, decimals)
    z_low = z - margin
    z_high = z + margin

    # activate vert selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')

    coords = []
    bpy.ops.object.editmode_toggle()
    for v in obj.data.vertices:
        if z_low <= round(v.co.z, 3) <= z:
            coords.append(v.co)
    bpy.ops.object.editmode_toggle()
    return coords


def move_object(obj, vector):
    obj.location = obj.location + vector


def set_selected_vert_prop(context, prop):
    # check if a vertex is selected and get selection
    selected_verts = get_selected_vertices_co(context)
    if not len(selected_verts) == 1:
        return "ERROR", "Please select exactly one vertex"
    local_vert = selected_verts[0]  # get the coordinates

    # convert local coordinates to world coordinates
    mat_world = context.active_object.matrix_world
    vert_global = mat_world @ local_vert

    # set vertex coordinates in property
    context.active_object[prop] = (vert_global.x, vert_global.y, vert_global.z)

    return None


def get_single_vert_co(context):
    # check if a vertex is selected and get selection
    selected_verts = get_selected_vertices_co(context)
    if not len(selected_verts) == 1:
        return None
    local_vert = selected_verts[0]  # get the coordinates

    # convert local coordinates to world coordinates
    mat_world = context.active_object.matrix_world
    vert_global = mat_world @ local_vert

    # set vertex coordinates in property
    return Vector((vert_global.x, vert_global.y, vert_global.z))


def get_distance(point1: Vector, point2: Vector) -> float:
    """Calculate distance between two points."""
    return (point2 - point1).length


def set_object_origin(bottom_vertex):
    bpy.ops.object.mode_set(mode='OBJECT')

    # set the location of the cursor
    bpy.context.scene.cursor.location = bottom_vertex

    # use the location of the cursor as origin (no better way to do this)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')


def select_verts_by_co(obj, vert_coordinates):
    # activate vert selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.editmode_toggle()
    for v in obj.data.vertices:
        if v.co in vert_coordinates:
            v.select = True
    bpy.ops.object.editmode_toggle()


def select_verts_by_idx(obj, vert_idx):
    # activate vert selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.editmode_toggle()
    for v in obj.data.vertices:
        if v.index in vert_idx:
            v.select = True
    bpy.ops.object.editmode_toggle()


def select_verts(obj, verts):
    # activate vert selection mode
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')

    verts_idx = [v.index for v in verts]

    select_verts_by_idx(obj, verts_idx)


def duplicate_obj(obj, new_name, collection, data=True, actions=True):
    obj_copy = obj.copy()
    obj_copy.name = new_name
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    collection.objects.link(obj_copy)
    return obj_copy


# custom function to apply transformation without switching the context
# def apply_transform_all(obj):
#     # make sure to toggle edit mode so that all calculations are done
#     bpy.ops.object.editmode_toggle()
#     bpy.ops.object.editmode_toggle()
#
#     matrix = obj.matrix_world.copy()
#     for vert in obj.data.vertices:
#         vert.co = matrix @ vert.co
#     obj.matrix_world.identity()


def apply_transform(obj, use_location=False, use_rotation=False, use_scale=False):
    mb = obj.matrix_basis
    I = Matrix()
    loc, rot, scale = mb.decompose()

    # rotation
    T = Matrix.Translation(loc)
    # R = rot.to_matrix().to_4x4()
    R = mb.to_3x3().normalized().to_4x4()
    S = Matrix.Diagonal(scale).to_4x4()

    transform = [I, I, I]
    basis = [T, R, S]

    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_location:
        swap(0)
    if use_rotation:
        swap(1)
    if use_scale:
        swap(2)

    M = transform[0] @ transform[1] @ transform[2]
    if hasattr(obj.data, "transform"):
        obj.data.transform(M)
    for c in obj.children:
        c.matrix_local = M @ c.matrix_local

    obj.matrix_basis = basis[0] @ basis[1] @ basis[2]


def scale_distance(obj, distance):
    # get bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    for v in bm.verts:
        # move the vertices
        norms = [f.normal for f in v.link_faces]
        n = sum(norms, Vector()) / len(norms)
        v.co += distance * n

    bmesh.update_edit_mesh(me)


def scale_distance_xy(obj, distance):
    # get bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    for v in bm.verts:
        # move the vertices
        norms = []
        for f in v.link_faces:
            vec = Vector((f.normal.x, f.normal.y, 0.1 * f.normal.z))
            vec.normalize()
            norms.append(vec)

        if norms:
            n = sum(norms, Vector()) / len(norms)
            v.co += distance * n

    bmesh.update_edit_mesh(me)


def scale_selected_verts_distance_xy(obj, distance):
    # get bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    selected_verts = [v for v in bm.verts if v.select]

    for v in selected_verts:
        # move the vertices
        norms = []
        for f in v.link_faces:
            if f.select:
                vec = Vector((f.normal.x, f.normal.y, 0))
                vec.normalize()
                norms.append(vec)
        n = sum(norms, Vector()) / len(norms)
        v.co += distance * n

    bmesh.update_edit_mesh(me)


def activate_object(context, active_obj, mode='OBJECT', hide_select_all=True):
    # to switch to object mode, you need an active object
    context.view_layer.objects.active = active_obj
    active_obj.hide_select = False  # make sure it is selectable
    active_obj.select_set(True)

    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        if obj != active_obj:
            obj.select_set(False)
            if hide_select_all:
                obj.hide_select = True

    # context.view_layer.objects.active = active_obj
    # active_obj.select_set(True)

    bpy.ops.object.mode_set(mode=mode)
    if mode == 'VERTEX_PAINT' and context.scene.ufit_full_screen:
        # bug in blender: tool header gets visible in full screen mode
        bpy.ops.wm.context_set_value(data_path="space_data.show_region_tool_header", value='False')


def order_verts_by_closest(verts):
    ordered_verts = []
    non_ordered_verts = verts.copy()
    for i in range(0, len(verts)):
        if i == 0:
            ordered_verts.append(non_ordered_verts[0])
        else:
            vert = ordered_verts[-1]
            non_ordered_verts.sort(reverse=False, key=lambda v: get_distance(v, vert))
            ordered_verts.append(non_ordered_verts[0])

        del non_ordered_verts[0]

    return ordered_verts


def creat_path_by_points(cpath, points):
    if cpath.type in ['NURBS', 'POLY']:
        cpath.points.add(len(points)-1)
        for (index, point) in enumerate(points):
            cpath.points[index].co = point
        cpath.use_endpoint_u = False
    elif cpath.type in ['BEZIER']:
        cpath.bezier_points.add(len(points)-1)
        for (index, point) in enumerate(points):
            x, y, z, w = point
            cpath.bezier_points[index].co = x, y, z
            cpath.bezier_points[index].handle_left = x-1, y-1, z-1
            cpath.bezier_points[index].handle_right = x+1, y+1, z+1
    return


def get_curve_circumference(curve_ob):
    curve = curve_ob.data
    circumference = 0.0
    for spline in curve.splines:
        for i in range(len(spline.points)):
            pt1 = spline.points[i].co
            pt2 = spline.points[(i + 1) % len(spline.points)].co
            circumference += (pt2 - pt1).length

    return circumference


def get_mesh_circumference(obj):
    # get bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    circumference = 0.0
    for edge in bm.edges:
        if len(edge.link_faces) < 2:
            circumference += edge.calc_length()
    return circumference


def unsubdivide_mesh(obj, iterations=1):
    # get bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # Perform the unsubdivide operation
    bmesh.ops.unsubdivide(bm, verts=bm.verts, iterations=iterations)

    # Update the mesh from the BMesh data
    bmesh.update_edit_mesh(me)


def reset_ufit_properties(context, scene_props):
    # todo: add other types of props (e.g. object props)
    for prop in scene_props:
        context.scene.property_unset(prop)


def get_scene_enum_item(context, prop, prop_str):
    for enum_item in context.scene.bl_rna.properties[prop_str].enum_items:
        if enum_item.identifier == prop:
            return enum_item


def delete_obj_by_name_contains(name):
    for obj in bpy.data.objects:
        if obj.name.startswith(name):
            bpy.data.objects.remove(obj, do_unlink=True)


# todo: isn't a valid feature yet. You cannot specify the point to rollback to
def rollback_to_blender_history_point(point_name):
    # Get the undo history
    undo_history = bpy.ops.ed.undo_history()

    for i in range(0, bpy.context.preferences.edit.undo_steps):
        undo_step = bpy.ops.ed.undo_history(item=i)

    # # Loop through the history until we find the named point
    # for entry in undo_history['entries']:
    #     if entry['message'] == point_name:
    #         break
    #     bpy.ops.ed.undo()


def get_kd_tree(obj):
    # get the mesh
    mesh = obj.data
    size = len(mesh.vertices)
    kd = kdtree.KDTree(size)

    # Create a kd-tree from the mesh vertices
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    kd.balance()

    return kd


def find_closest_vertex_ix(obj, point):
    kd = get_kd_tree(obj)

    # Find the closest vertex
    co, index, distance = kd.find(point)

    return index


def find_closest_n_vertices_ix(obj, points, n=4):
    kd = get_kd_tree(obj)

    closests_verts = set()

    for p in points:
        for (co, index, distance) in kd.find_n(p, n=n):  # find the closest x verts to a point
            closests_verts.add(index)

    return list(closests_verts)


def subdivide_until_vertex_count(obj, n):
    # select all
    bpy.ops.mesh.select_all(action='SELECT')

    # subdivide to increase the amount of polygons
    nr_vertices = len(obj.data.vertices)
    division_cuts = math.log(n / nr_vertices, 4)  # solve for 4^x = n/triangles
    range_cuts = int(round(division_cuts, 0))
    for i in range(range_cuts):
        bpy.ops.mesh.subdivide(number_cuts=1)


def move_verts_along_faces_normal(obj, distance, verts_weights=None):
    # create bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # move the selected vertices along normals
    verts = set(v for f in bm.faces if f.select for v in f.verts)
    for v in verts:
        # move the vertices
        norms = [f.normal for f in v.link_faces if f.select]
        n = sum(norms, Vector()) / len(norms)

        if not verts_weights:
            v.co += distance * n
        else:
            v.co += verts_weights[v.index] * distance * n

        # v.select = False

    bmesh.update_edit_mesh(me)


def get_orientation_matrix_by_normal(normal):
    # Define the normal vector of the plane and the direction to align with x-axis
    # global_x_dir = Vector((1, 0, 0))  # work with the global x direction as reference
    # y_axis = normal.cross(global_x_dir).normalized()
    # x_axis = normal.cross(y_axis).normalized()

    # global_y_dir = Vector((0, 1, 0))  # work with the global x direction as reference
    # y_axis = normal.cross(global_y_dir).normalized()
    # x_axis = normal.cross(y_axis).normalized()

    global_z_dir = Vector((0, 0, 1))  # work with the global z direction as reference
    x_axis = normal.cross(global_z_dir).normalized()
    y_axis = normal.cross(x_axis).normalized()

    # Construct the rotation matrix using the normalized normal, v, and u vectors
    orientation_matrix = Matrix([x_axis, y_axis, normal])

    return orientation_matrix


def move_selected_verts_along_local_axis(obj, distance, axis=(False, False, False)):
    # create bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # move the selected vertices along normals
    verts = [v for v in bm.verts if v.select]
    for v in verts:
        orientation_matrix = get_orientation_matrix_by_normal(v.normal)

        if axis[0]:
            x_axis = orientation_matrix[0]
            v.co += distance * x_axis
        if axis[1]:
            y_axis = orientation_matrix[1]
            v.co += distance * y_axis
        if axis[2]:
            z_axis = orientation_matrix[2]
            v.co += distance * z_axis

    bmesh.update_edit_mesh(me)


def increase_selected_vertices_region(obj, amount):
    # create bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    verts = set(v for f in bm.faces if f.select for v in f.verts)
    increased_verts = set(verts)
    for i in range(amount):
        new_increased_verts = increased_verts.copy()
        for v in increased_verts:
            for f in v.link_faces:
                new_increased_verts.update([vert for vert in f.verts])
        increased_verts = new_increased_verts

    # select all vertices
    for v in increased_verts:
        v.select = True

    bmesh.update_edit_mesh(me)


# check if a vertex is near the border of the selection
def is_vertex_near_border(vertex, selection):
    for neighbor in vertex.link_edges:
        if neighbor.other_vert(vertex) not in selection:
            return True
    return False


def decrease_selected_vertices_region(obj, amount):
    # create bmesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    for i in range(amount):
        selected_verts = set(v for v in bm.verts if v.select)
        for v in selected_verts:
            if is_vertex_near_border(v, selected_verts):
                v.select = False

    bm.select_flush(False)  # update selection status
    bmesh.update_edit_mesh(me)


def find_closest_vertices_kdtree(source_obj, target_obj):
    """Find the closest vertex in target_obj for each vertex in source_obj using kdTree"""

    # Create a dictionary to store closest vertices
    closest_vertices = {}

    # Create kdTree for source_obj
    target_kd_tree = get_kd_tree(target_obj)

    # Loop through vertices of target_obj
    for source_vertex in source_obj.data.vertices:
        _, closest_index, _ = target_kd_tree.find(source_vertex.co)

        # Store closest vertex index in dictionary
        closest_vertices[source_vertex.index] = closest_index

    return closest_vertices


def find_closest_n_vertices_kdtree(source_obj, target_obj, n=4):
    """Find the closest n vertices in target_obj for each vertex in source_obj using kdTree"""

    # Create a dictionary to store closest vertices
    closest_vertices = {}

    # Create kdTree for source_obj
    target_kd_tree = get_kd_tree(target_obj)

    # Loop through vertices of target_obj
    for source_vertex in source_obj.data.vertices:
        _, closest_index, _ = target_kd_tree.find(source_vertex.co)

        closest_verts = []
        for (co, index, distance) in target_kd_tree.find_n(source_vertex.co, n=n):  # find the closest x verts
            closest_verts.append(index)

        # Store closest vertex index in dictionary
        closest_vertices[source_vertex.index] = closest_verts

    return closest_vertices


def select_vertices_from_vertex_group(context, obj, vg_name):
    # edit mode
    activate_object(context, obj, mode='EDIT')

    # deselect all vertices
    bpy.ops.mesh.select_all(action='DESELECT')

    # activate the scale inner vertex group
    vgroups = obj.vertex_groups
    vgroups.active_index = vgroups[vg_name].index
    bpy.ops.object.vertex_group_select()


def get_vertices_from_vertex_group(obj, vg_name):
    # Get the vertex group
    vg_index = obj.vertex_groups[vg_name].index

    # Get the mesh data
    mesh = obj.data

    # Loop through the vertices and get their coordinates if they are in the vertex group
    vertices = []
    for vert in mesh.vertices:
        for group in vert.groups:
            if group.group == vg_index:
                vertices.append({
                    'idx': vert.index,
                    'co': vert.co
                })

    return vertices


def move_vertices_from_vertex_group(obj, vg_name, vector):
    # Create a bmesh from the object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    # Get the vertex group
    vg_index = obj.vertex_groups[vg_name].index

    # Get the vertices in the vertex group (bmesh doesn't have groups)
    verts = [v.index for v in obj.data.vertices if vg_index in [vg.group for vg in v.groups]]
    bm_verts = [v for v in bm.verts if v.index in verts]

    # Move the vertices
    for v in bm_verts:
        v.co += vector

    # Update the mesh
    bmesh.update_edit_mesh(me)


def get_depsgraph_object(context, obj):
    # get a copy of the object with the modifiers applied (you need to be in object mode!
    depsgraph = context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)

    return obj_eval


def get_depsgraph_mesh(context, obj, mode='OBJECT'):
    # get a copy of the object with the modifiers applied
    depsgraph = context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh_eval = obj_eval.to_mesh()

    return mesh_eval


def create_obj_from_selection(context, obj_name, copy_vg=False):
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    selected_verts = [v for v in bm.verts if v.select]
    selected_faces = [f for f in bm.faces if f.select]

    # establishes a map between the new mesh vertex indices and
    # actual mesh vertex indices (required for the function from_pydata)
    vmap = dict()
    for i, vert in enumerate(selected_verts):
        vmap[vert.index] = i

    # vertices for function from_pydata
    vertices = [v.co for v in selected_verts]

    # build faces with new indices
    faces = []
    for face in selected_faces:
        faces.append([vmap[v.index] for v in face.verts])

    # Create a new object from the selected vertices and faces
    new_mesh = bpy.data.meshes.new(name=obj_name)
    new_mesh.from_pydata(vertices, [], faces)
    new_obj = bpy.data.objects.new(name=obj_name, object_data=new_mesh)

    if copy_vg:
        # copy vertex groups
        vg_groups = {}
        for vg in obj.vertex_groups:
            verts = [v for v in obj.data.vertices if vg.index in [vg.group for vg in v.groups]]
            vg_group_verts = [vmap[v.index] for v in verts if v.index in vmap]
            if vg_group_verts:
                vg_groups[vg.name] = vg_group_verts

        for name in vg_groups.keys():
            new_vg_group = new_obj.vertex_groups.new(name=name)
            new_vg_group.add(vg_groups[name], 1.0, 'REPLACE')

    # Link the new object to the scene
    context.scene.collection.objects.link(new_obj)

    bm.select_flush_mode()

    return new_obj


def calculate_angle_between_vectors(point_a, point_b, point_c):
    vector_ab = point_b - point_a
    vector_ac = point_c - point_a

    angle = vector_ab.angle(vector_ac)
    return angle


def return_to_default_edit_mode(context, obj):
    activate_object(context, obj, mode='EDIT', hide_select_all=True)

    # deselect everything
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # activate select box
    user_interface.set_active_tool('builtin.select_box')


def return_to_default_object_mode(context, obj):
    activate_object(context, obj, mode='OBJECT', hide_select_all=True)

    # select tool
    user_interface.set_active_tool('builtin.select_box')


def return_to_default_state(context, object_name, light, color_type):
    # activate object in object mode
    obj = bpy.data.objects[object_name]

    # return to default edit mode
    return_to_default_edit_mode(context, obj)

    # return to default object mode
    return_to_default_object_mode(context, obj)

    # shading mode and orthographic
    user_interface.set_shading_solid_mode(light=light, color_type=color_type)
    user_interface.change_orthographic('FRONT')

    # focus on the object
    user_interface.focus_on_selected()

    # prevent selection for all objects (except object_name)
    # bpy.context.space_data.show_restrict_column_select = True
    # for obj in bpy.data.objects:
    #     if obj.name != object_name:
    #         obj.hide_select = True

    # deactivate quad and orthographic view
    context.scene.ufit_quad_view = False
    context.scene.ufit_orthographic_view = False


def filter_close_vertex_array(arr, rtol, atol):
    filtered_arr = [arr[0]]
    for value in arr[1:]:
        if not np.isclose(Vector(value), Vector(filtered_arr[-1]), rtol=rtol, atol=atol).all():
            filtered_arr.append(value)

    return filtered_arr


def add_image_texture(texture_name, file_dir, file_name, extension='EXTEND'):
    # load image
    bpy.data.images.load(f'{file_dir}/{file_name}', check_existing=True)  # load img from disk

    # (re)create new texture
    if texture_name in bpy.data.textures:
        bpy.data.textures.remove(bpy.data.textures[texture_name], do_unlink=True)

    # add image to texture
    bpy.data.textures.new(name=texture_name, type="IMAGE")
    texture = bpy.data.textures[texture_name]
    texture.image = bpy.data.images[file_name]
    texture.extension = extension  # EXTEND # CLIP # CLIP_CUBE # REPEAT # CHECKER


def set_ufit_logo():
    # keep looping until the context is filled after opening a new file
    # if bpy.data.images is None:
    #     bpy.app.timers.register(set_ufit_logo, first_interval=0.1)

    # check if the background of the viewport is close to white
    active_theme = bpy.context.preferences.themes[0]  # Get the active theme
    high_gradient = active_theme.view_3d.space.gradients.high_gradient  # Get the RGB values
    threshold = 0.1  # Define a threshold for closeness to white
    is_close_to_white = all(math.isclose(channel, 1.0, rel_tol=threshold) for channel in high_gradient)

    # set paths to assistance image
    images_dir = os.path.join(os.path.dirname(__file__), f"../../../..{base_path_consts['paths']['images_path']}")

    if not is_close_to_white:
        file_name = f'ufit_logo.png'
    else:
        file_name = f'ufit_logo_no_bg.png'

    add_image_texture('ufit_logo', images_dir, file_name)


def deselect_non_loop_edges(obj):
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    selected_edges = [e for e in bm.edges if e.select]

    vertex_count = {}
    for e in selected_edges:
        if e.select:
            if e.verts[0] not in vertex_count:
                vertex_count[e.verts[0]] = 0
            if e.verts[1] not in vertex_count:
                vertex_count[e.verts[1]] = 0

            vertex_count[e.verts[0]] += 1
            vertex_count[e.verts[1]] += 1

    # do not deselect the whole edge because of its vertices can still be part of the loop
    for e in selected_edges:
        if vertex_count[e.verts[0]] < 2:
            e.verts[0].select = False
        if vertex_count[e.verts[1]] < 2:
            e.verts[1].select = False

    bm.select_flush_mode()
    mesh.update()


def get_outer_vertices_selection(obj):
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)

    selected_verts = [v for v in bm.verts if v.select]

    outer_verts = []
    for vert in selected_verts:
        # Check if all neighboring vertices are also selected
        if is_vertex_near_border(vert, selected_verts):
            outer_verts.append({
                'idx': vert.index,
                'co': vert.co
            })

    # Ensure the BMesh is freed
    # bmesh.update_edit_mesh(mesh)
    bm.free()

    return outer_verts


def ratio_center_border_distance_vertices(center_vert, border_verts, selected_verts):
    ratio_dict = {}
    for vert in selected_verts:
        # distance to center
        distance_to_center = get_distance(vert['co'], center_vert['co'])

        # order border vertices by their distance to the vert
        border_verts.sort(reverse=False, key=lambda v: get_distance(v['co'], vert['co']))

        # distance to border
        distance_to_border = get_distance(border_verts[0]['co'], vert['co'])

        total_distance = distance_to_center + distance_to_border

        ratio = distance_to_center / total_distance

        ratio_dict[vert['idx']] = {
            'distance_to_center': distance_to_center,
            'distance_to_border': distance_to_border,
            'ratio': ratio
        }

    return ratio_dict


def create_new_vertex_group_for_selected(context, obj, vg_name, mode='OBJECT'):
    # get selected vertices
    selected_vertices = get_selected_vertices_ix(context)

    # only works in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    vertex_group = obj.vertex_groups.new(name=vg_name)  # make sure you are in object mode
    vertex_group.add(selected_vertices, 1, 'REPLACE')

    # return to the required mode
    bpy.ops.object.mode_set(mode=mode)
