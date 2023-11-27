import bpy
import numpy as np
from mathutils import Vector
from . import general


def add_new_color_attr(obj, name, color):
    # add new color attribute
    mesh = obj.data
    mesh.color_attributes.new(
        name=name,
        type='FLOAT_COLOR',
        domain='POINT',
    )

    area_selection = obj.data.color_attributes[name].data  # this is all white
    for vert in area_selection:
        vert.color = color  # make it color


def delete_color_attribute(obj, name):
    # remove color attribute
    color_attr = obj.data.color_attributes[name]
    obj.data.color_attributes.remove(color_attr)


def activate_color_attribute(obj, name):
    for i, ca in enumerate(obj.data.color_attributes):
        if ca.name == name:
            obj.data.attributes.active_color_index = i
            break


def reset_color_attribute(obj, name, color):
    area_selection = obj.data.color_attributes[name].data
    for vert in area_selection:
        vert.color = color  # make it color


def change_alpha_rgb(color_vec, alpha, keep_color=False):
    multiplier = 1
    if keep_color:
        multiplier = 2 - alpha

    r = color_vec[0]*multiplier
    g = color_vec[1]*multiplier
    b = color_vec[2]*multiplier
    brightness = alpha*color_vec[3]

    return Vector((r, g, b, brightness))


def transfer_color_attr_source_target(source_obj, target_obj, source_color_attr_name, target_color_attr_name):
    # find the closest n vertices on the source_obj
    map_target_source = general.find_closest_n_vertices_kdtree(target_obj, source_obj, n=4)

    target_obj_color = target_obj.data.color_attributes[source_color_attr_name].data  # this is all white
    source_obj_color = source_obj.data.color_attributes[target_color_attr_name].data
    for i, target_obj_vert in enumerate(map_target_source.keys()):
        source_obj_verts = map_target_source[target_obj_vert]

        # Calculate the average color
        colors = [Vector(source_obj_color[v].color) for v in source_obj_verts]
        avg_color = sum(colors, Vector((0.0, 0.0, 0.0, 0.0))) / len(colors)

        # change alpha but keep the same color
        avg_color = change_alpha_rgb(avg_color, alpha=0.9, keep_color=True)
        target_obj_color[target_obj_vert].color = avg_color


def bake_texture_to_color_attr(context, obj, material, color_attr_name, min_amount_vertices, mode='OBJECT'):
    # edit mode for subdivision
    general.activate_object(context, obj, mode='EDIT')

    # subdivide
    general.subdivide_until_vertex_count(obj, min_amount_vertices)  # minimum n vertices for good baking

    # object mode for baking
    general.activate_object(context, obj, mode='OBJECT')

    # remove the BSDF node
    node_pb = material.node_tree.nodes['Principled BSDF']
    material.node_tree.nodes.remove(node_pb)

    # add an emission node for baking with Emit
    material.node_tree.nodes.new('ShaderNodeEmission')

    # make the right connections
    material.node_tree.links.new(
        material.node_tree.nodes['Image Texture'].outputs['Color'],
        material.node_tree.nodes['Emission'].inputs['Color']
    )
    material.node_tree.links.new(
        material.node_tree.nodes['Emission'].outputs['Emission'],
        material.node_tree.nodes['Material Output'].inputs['Surface']
    )

    # create a new vertex color property for baking the vertex colors to
    mesh = obj.data
    mesh.color_attributes.new(
        name=color_attr_name,
        type='FLOAT_COLOR',
        domain='POINT',
    )

    # bake the texture in the ufit object before duplicating
    context.scene.render.engine = 'CYCLES'  # changes to the CYCLES render engine
    context.scene.render.bake.target = 'VERTEX_COLORS'  # bake vertex colors and not texture
    context.scene.cycles.bake_type = 'EMIT'  # use the emit method
    bpy.ops.object.bake(type='EMIT')

    # switch to requested mode
    general.activate_object(context, obj, mode=mode)


def remesh_with_texture_to_color_attr(context, obj, color_attr_name='original_colors'):
    material = obj.data.materials[obj.active_material_index]

    # bake texture to color attributes
    bake_texture_to_color_attr(context, obj, material, 'scan_colors', 100000, mode='OBJECT')

    # duplicate the object
    obj_baked = general.duplicate_obj(obj, f'{obj.name}_Baked', context.collection, data=True, actions=False)

    # remesh the ufit object so you have quads
    remesh_mod = obj.modifiers.new(name="Remesh", type='REMESH')
    remesh_mod.mode = 'SMOOTH'
    remesh_mod.octree_depth = 7
    remesh_mod.scale = 0.99

    # bug in blender - you have to use an override to apply the modifier
    override = {"object": obj, "active_object": obj}
    bpy.ops.object.modifier_apply(override, modifier="Remesh")

    # create color attribute for copying vertex colors
    mesh = obj.data
    mesh.color_attributes.new(
        name=color_attr_name,
        type='FLOAT_COLOR',
        domain='POINT',
    )

    # take over the color
    transfer_color_attr_source_target(obj_baked, obj, color_attr_name, color_attr_name)

    # delete ufit_bake
    general.delete_obj_by_name_contains(f'{obj.name}_Baked')


def get_vertices_by_color_exclude(obj, color_attr_name, color_exclude: Vector((0.0, 0.0, 0.0, 0.0))):
    mesh = obj.data
    color_layer = mesh.color_attributes.get(color_attr_name)

    if color_layer and len(color_layer.data) > 0:
        color_attr = color_layer.data

        result_verts = []
        for vert in mesh.vertices:
            color = Vector(color_attr[vert.index].color)

            # increase performance by first comparing exact
            if not color == color_exclude:
                # max 20 % difference on all elements of the vectors compared
                if not np.isclose(Vector(color), color_exclude, rtol=0.2, atol=0.2).all():
                    result_verts.append(vert)

        return result_verts


def get_vertices_by_color_exclude_simple(obj, color_attr_name, color_exclude: Vector((0.0, 0.0, 0.0, 0.0))):
    mesh = obj.data
    color_layer = mesh.color_attributes.get(color_attr_name)

    if color_layer and len(color_layer.data) > 0:
        color_attr = color_layer.data

        result_verts = []
        for vert in mesh.vertices:
            color = Vector(color_attr[vert.index].color)

            # increase performance by only comparing exact
            if not color == color_exclude:
                result_verts.append(vert)

        return result_verts


def select_vertices_by_color_exclude(context, obj, color_attr_name, color_exclude: Vector((0.0, 0.0, 0.0, 0.0))):
    # select vertices by color attribute layer - exclude default color black
    colored_verts = get_vertices_by_color_exclude(obj, color_attr_name, color_exclude)

    # switch to edit mode after vertices are retrieved
    general.activate_object(context, obj, mode='EDIT')
    general.deselect_in_edit_mode(context)

    # effectively select the vertices
    general.select_verts(obj, colored_verts)


def color_selected_vertices(context, obj, color_attr_name, color: Vector((0.0, 0.0, 0.0, 0.0))):
    # make sure you are in edit mode
    general.activate_object(context, obj, mode='EDIT')

    # get the index of the selected vertices
    selected_verts_ix = general.get_selected_vertices_ix(context)

    # activate object mode
    general.activate_object(context, obj, mode='OBJECT')

    # get the color layer (needs to be in Object mode)
    color_layer = obj.data.color_attributes.get(color_attr_name)

    # give color to the selected vertices
    for vert_idx in selected_verts_ix:
        color_layer.data[vert_idx].color = color


def set_vertices_color(obj, color_attr_name, vertices, color):
    mesh = obj.data
    color_layer = mesh.color_attributes.get(color_attr_name)

    # set color for all vertices
    for vertex in vertices:
        color_layer.data[vertex.index].color = color
