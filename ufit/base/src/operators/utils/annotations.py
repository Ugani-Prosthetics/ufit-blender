# We are using the annotation functionality of blender to achieve
# selection of vertices, faces and edges without having to activate the wireframe.

import bpy
from . import general


def get_anno_layer(anno_name, layer_name):
    try:
        my_anno = bpy.data.grease_pencils.get(anno_name)
        my_layer = my_anno.layers.get(layer_name)
        return my_layer
    except Exception as e:
        raise e


def get_all_points(anno_name, layer_name):
    # get the annotation layer
    anno_layer = get_anno_layer(anno_name, layer_name)

    all_points = []
    if anno_layer and anno_layer.active_frame:
        strokes = anno_layer.active_frame.strokes

        for i, stroke in enumerate(strokes):
            for pt in stroke.points:
                all_points.append(pt.co)

    return all_points


def get_strokes_dict(anno_name, layer_name):
    # get the annotation layer
    anno_layer = get_anno_layer(anno_name, layer_name)

    strokes_dict = {}
    if anno_layer:
        strokes = anno_layer.active_frame.strokes

        for i, stroke in enumerate(strokes):
            for pt in stroke.points:
                strokes_dict[i] = pt.co

    return strokes_dict


def get_num_of_strokes(anno_name, layer_name):
    # get the annotation layer
    anno_layer = get_anno_layer(anno_name, layer_name)

    num_of_strokes = 0
    if anno_layer:
        strokes = anno_layer.active_frame.strokes
        num_of_strokes = len(strokes)

    return num_of_strokes


# activate a single vertex based on the annotations
def select_single_vert(obj, anno_name, layer_name):
    # get the annotation layer
    anno_layer = get_anno_layer(anno_name, layer_name)

    selected_verts = []
    if anno_layer:
        strokes = anno_layer.active_frame.strokes

        for i, stroke in enumerate(strokes):
            for pt in stroke.points:
                selected_verts.append(pt.co)

        if not len(selected_verts) == 1:
            return None

    if selected_verts:
        vert_ix = general.find_closest_vertex_ix(obj, selected_verts[0])
        general.select_verts_by_idx(obj, [vert_ix])

        # # set vertex coordinates in property
        # return Vector((vert_global.x, vert_global.y, vert_global.z))


# get selected verts based on annotation(s)
def select_verts(obj, anno_name, layer_name):
    # get the annotation layer
    anno_layer = get_anno_layer(anno_name, layer_name)

    selected_verts = []
    if anno_layer:
        strokes = anno_layer.active_frame.strokes

        for i, stroke in enumerate(strokes):
            for pt in stroke.points:
                selected_verts.append(pt.co)

    if selected_verts:
        verts_ixs = general.find_closest_n_vertices_ix(obj, selected_verts, n=2)
        general.select_verts_by_idx(obj, verts_ixs)
        for v in verts_ixs:
            bpy.ops.mesh.shortest_path


def select_by_annotation_region_max_z(context, obj, anno_name, layer_name):
    # select vertices by annotation strokes
    select_verts(obj, anno_name, layer_name)

    # get the selected verts
    selected_verts = general.get_selected_vertices(context)
    vertex_with_max_idx = max(selected_verts, key=lambda vertex: vertex['idx'])
    vertex_with_max_z = max(selected_verts, key=lambda vertex: vertex['co'].z)
    idx_select = vertex_with_max_idx['idx'] + 1

    # hide selected verts (so they form a gap for linked selection)
    bpy.ops.mesh.hide(unselected=False)

    # select verts linked
    bpy.ops.mesh.select_linked_pick(deselect=False,
                                    delimit=set(),
                                    object_index=obj.pass_index,
                                    index=idx_select)

    # invert linked selection if max z is above max z of initial selection
    selected_verts_linked = general.get_selected_vertices(context)
    vertex_with_max_z_linked = max(selected_verts_linked, key=lambda vertex: vertex['co'].z)

    if vertex_with_max_z_linked['co'].z > vertex_with_max_z['co'].z:
        bpy.ops.mesh.select_all(action='INVERT')

    # unhide hidden verts
    bpy.ops.mesh.reveal()


def select_by_annotation_region_amount_verts(context, obj, anno_name, layer_name):
    # select vertices by annotation strokes
    select_verts(obj, anno_name, layer_name)

    # get the selected verts
    selected_verts = general.get_selected_vertices(context)
    vertex_with_max_idx = max(selected_verts, key=lambda vertex: vertex['idx'])
    idx_select = vertex_with_max_idx['idx'] + 1

    # hide selected verts (so they form a gap for linked selection)
    bpy.ops.mesh.hide(unselected=False)

    # select verts linked
    bpy.ops.mesh.select_linked_pick(deselect=False,
                                    delimit=set(),
                                    object_index=obj.pass_index,
                                    index=idx_select)

    # invert linked selection if max z is above max z of initial selection
    selected_verts_part1 = general.get_selected_vertices(context)
    bpy.ops.mesh.select_all(action='INVERT')
    selected_verts_part2 = general.get_selected_vertices(context)
    if len(selected_verts_part2) > len(selected_verts_part1):
        bpy.ops.mesh.select_all(action='INVERT')  # keep the selection with the least amount of vertices

    # unhide hidden verts
    bpy.ops.mesh.reveal()
