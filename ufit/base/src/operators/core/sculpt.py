import bpy
import bmesh
import math
from mathutils import Vector
import numpy as np
from ..utils import annotations, color_attributes, general, user_interface

color_attr_select = 'area_selection'


#################################
# Push/Pull/Smooth
#################################
def set_push_pull_smooth_shader_nodes(ufit_obj, color_attr_name):
    if ufit_obj.data.materials:
        material = ufit_obj.data.materials[ufit_obj.active_material_index]

        # check if there was a colored scan loaded
        node_tex_image = None
        node_output_mat = None
        node_bsdf_princ = None
        if len(material.node_tree.nodes) == 3:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    node_tex_image = node
                if node.type == 'OUTPUT_MATERIAL':
                    node_output_mat = node
                if node.type == 'BSDF_PRINCIPLED':
                    node_bsdf_princ = node

            if node_tex_image and node_output_mat and node_bsdf_princ:
                # Add new nodes
                node_rgb = material.node_tree.nodes.new('ShaderNodeRGB')
                node_color_attr = material.node_tree.nodes.new('ShaderNodeVertexColor')
                node_separate_color = material.node_tree.nodes.new('ShaderNodeSeparateColor')
                node_mix = material.node_tree.nodes.new('ShaderNodeMix')

                # set variables of new nodes
                node_color_attr.layer_name = color_attr_name
                node_separate_color.mode = 'RGB'
                node_mix.data_type = 'RGBA'
                node_mix.blend_type = 'BURN'
                node_mix.clamp_result = True
                node_mix.clamp_factor = False
                node_rgb.outputs['Color'].default_value = (0.0, 1.0, 0.0, 1.0)  # selection in green

                # make node links
                material.node_tree.links.new(
                    node_color_attr.outputs['Color'],
                    node_separate_color.inputs['Color']
                )
                material.node_tree.links.new(
                    node_separate_color.outputs['Green'],
                    node_mix.inputs['Factor']
                )
                material.node_tree.links.new(
                    node_tex_image.outputs['Color'],
                    node_mix.inputs[6]  # multiple 'A' inputs, we need to select type RGBA which is at index 6
                )
                material.node_tree.links.new(
                    node_rgb.outputs['Color'],
                    node_mix.inputs[7]  # multiple 'B' inputs, we need to select type RGBA which is at index 7
                )
                material.node_tree.links.new(
                    node_mix.outputs[2],  # multiple 'Result' output, we need to select type RGBA which is at index 2
                    node_bsdf_princ.inputs['Base Color']
                )


def prep_push_pull_smooth(context):
    ufit_obj = bpy.data.objects['uFit']

    # reset substep
    context.scene.ufit_substep = 0

    # add area selection color attribute and add shader nodes
    color_attributes.add_new_color_attr(ufit_obj, name=color_attr_select, color=(0, 0, 0, 1))
    set_push_pull_smooth_shader_nodes(ufit_obj, color_attr_name=color_attr_select)

    # activate vertex paint mode
    user_interface.set_shading_material_preview_mode()
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')
    context.scene.tool_settings.unified_paint_settings.size = 30  # change the brush size to 30px


# called after remeasuring
def minimal_prep_push_pull_smooth(context):
    ufit_obj = bpy.data.objects['uFit']

    # activate the uFit Object
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')

    # reset color attribute to all black vertices
    color_attributes.reset_color_attribute(ufit_obj, color_attr_select, color=(0, 0, 0, 1))

    # increase the substep number
    context.scene.ufit_substep = context.scene.ufit_substep + 1


def smooth_region(context):
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((0, 0, 0, 1)))

    # smooth selected vertices
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=context.scene.ufit_smooth_factor)

    # toggle edit mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()


def push_pull_region(context, extrusion):
    # set the ufit object
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((0, 0, 0, 1)))

    # decrease selected region
    # general.decrease_selected_vertices_region(ufit_obj, 2)

    # move vertices along there normals
    general.move_verts_along_faces_normal(ufit_obj, extrusion)

    # # increase the selected region for smoothing
    general.increase_selected_vertices_region(ufit_obj, 2)

    # smooth the smooth_vertices and deselect
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=7)


def push_pull_region_circular(context, extrusion):
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((0, 0, 0, 1)))

    # get the selected vertices again (indexes are ruined)
    selected_verts = general.get_selected_vertices(context)
    temp = np.array([(v['co'][0], v['co'][1], v['co'][2]) for v in selected_verts])
    center = Vector(np.sum(temp, axis=0) / temp.shape[0])

    # get the closest vertex to the center and the furthest vertex from the center
    selected_verts.sort(reverse=False, key=lambda v: general.get_distance(v['co'], center))
    # center_vert = [v['idx'] for v in selected_verts[0:vert_ten_perc]]
    center_vert = selected_verts[0]
    furthest_vert = selected_verts[-1]
    radius = 1.0 * general.get_distance(furthest_vert['co'], center_vert['co'])

    # hide the unselected vertices, so they are not impacted by proportional editing
    bpy.ops.mesh.hide(unselected=True)

    # select the center
    general.select_verts_by_idx(ufit_obj, [center_vert['idx']])

    # debugging
    # general.select_verts_by_idx(ufit_obj, [center_vert['idx'], furthest_vert['idx']])

    # activate proportional editing
    bpy.context.scene.tool_settings.use_proportional_edit = True

    # activate transformation orientation "normal" instead of global
    bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'

    # perform proportional editing (extrusion)
    bpy.ops.transform.translate(value=(0, 0, extrusion),
                                orient_axis_ortho='X',
                                orient_type='NORMAL',
                                # orient_matrix=((-0.869072, 0.298615, -0.39439),
                                #                (0.346459, -0.201653, -0.916135),
                                #                (-0.353101, -0.932826, 0.0717933)),
                                orient_matrix_type='NORMAL',
                                constraint_axis=(False, False, True),
                                mirror=True,
                                use_proportional_edit=True,
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=radius,
                                use_proportional_connected=False,
                                use_proportional_projected=False)

    # deactivate proportional editing and reactivate face select
    bpy.context.scene.tool_settings.use_proportional_edit = False
    bpy.ops.mesh.select_mode(type='VERT')

    # unhide hidden verts
    bpy.ops.mesh.reveal()  # automatically also selects
    bpy.ops.mesh.select_all(action='INVERT')  # reselect the region

    # increase the selected region for smoothing
    general.increase_selected_vertices_region(ufit_obj, 5)

    # perform smoothing to have a beautiful transition at the boundaries
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=7)


def push_pull_smooth_done(context):
    ufit_obj = bpy.data.objects['uFit']
    color_attributes.delete_color_attribute(ufit_obj, color_attr_select)


#################################
# Pull Bottom
#################################
def prep_pull_bottom(context):
    ufit_obj = bpy.data.objects['uFit']

    # reset substep
    context.scene.ufit_substep = 0

    # change to orthographic view
    context.scene.ufit_orthographic_view = True

    # turn on xray
    user_interface.set_xray(turn_on=True, alpha=1)

    # activate vertex selection
    general.activate_object(context, ufit_obj, mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='VERT')


# called after remeasuring
def minimal_prep_pull_bottom(context):
    ufit_obj = bpy.data.objects['uFit']

    # activate edit mode
    general.activate_object(context, ufit_obj, mode='EDIT')

    # increase the extrude number
    context.scene.ufit_substep = context.scene.ufit_substep + 1


def pull_bottom(context, extrusion):
    # set the ufit object
    ufit_obj = bpy.data.objects['uFit']

    # activate proportional editing
    bpy.context.scene.tool_settings.use_proportional_edit = True

    # activate transformation orientation "normal" instead of global
    bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'

    # perform proportional editing (extrusion)
    bpy.ops.transform.translate(value=(0, 0, extrusion),
                                orient_axis_ortho='X',
                                orient_type='NORMAL',
                                orient_matrix_type='NORMAL',
                                constraint_axis=(False, False, True),
                                mirror=True,
                                use_proportional_edit=True,
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=0.0075,
                                use_proportional_connected=False,
                                use_proportional_projected=False)

    # deactivate proportional editing and reactivate face select
    bpy.context.scene.tool_settings.use_proportional_edit = False


#################################
# Prepare Cutout
#################################
def prep_cutout_prep(context):
    # reset substep
    context.scene.ufit_substep = 0

    # create ufit measure and original objects
    ufit_obj = bpy.data.objects['uFit']
    ufit_original = general.duplicate_obj(ufit_obj, 'uFit_Original', context.collection, data=True, actions=False)
    ufit_measure = general.duplicate_obj(ufit_obj, 'uFit_Measure', context.collection, data=True, actions=False)

    # hide the UFitMeasure object
    ufit_original.hide_set(True)
    ufit_measure.hide_set(True)

    # transformation orientation global + activate vertex snapping
    context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_elements = {'FACE_NEAREST'}

    # switch to annotation tool
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Cutout')


def create_cutout_path(context):
    ufit_cutout_cu = bpy.data.curves.new("uFit_Cutout", "CURVE")
    ufit_cutout_ob = bpy.data.objects.new("uFit_Cutout", ufit_cutout_cu)
    polyline = ufit_cutout_cu.splines.new('NURBS')  # 'POLY''BEZIER''BSPLINE''CARDINAL''NURBS'

    context.scene.collection.objects.link(ufit_cutout_ob)

    # selected_verts = general.get_selected_vertices_co(context)
    all_points = annotations.get_all_points(anno_name='Selections', layer_name='Cutout')
    ordered_verts = general.order_verts_by_closest(all_points)
    filtered_verts = general.filter_close_vertex_array(ordered_verts, rtol=0.005, atol=0.005)

    points_for_path = [(v.x, v.y, v.z, 1) for v in filtered_verts]

    general.creat_path_by_points(polyline, points_for_path)

    return ufit_cutout_ob


def create_cutout_plane(context):
    ufit_cutout_ob = create_cutout_path(context)
    general.activate_object(context, ufit_cutout_ob, mode='EDIT')

    # close the curve
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.cyclic_toggle()

    bpy.context.object.data.dimensions = '3D'

    # tilt local z-axis 90 degrees so that it aligns in the xy plane
    bpy.ops.curve.tilt_clear()  # first clear the tilt
    bpy.ops.transform.tilt(value=math.radians(90),
                           mirror=False,
                           use_proportional_edit=False,
                           proportional_edit_falloff='SMOOTH',
                           proportional_size=1,
                           use_proportional_connected=False,
                           use_proportional_projected=False)

    # Z_UP not working in all cases
    bpy.context.object.data.twist_mode = bpy.context.scene.bl_rna.properties['ufit_twist_method'].default

    # extrude the curve 4cm everywhere
    bpy.context.object.data.extrude = 0.005

    # smoothen the curve
    bpy.context.object.data.twist_smooth = 100

    # deselect all
    bpy.ops.curve.select_all(action='DESELECT')

    # cleanup annotations
    user_interface.cleanup_grease_pencil(context)


#################################
# Cutout
#################################
def prep_cutout(context):
    cutout_obj = bpy.data.objects['uFit_Cutout']

    # make the cutout object selectable
    cutout_obj.hide_select = False

    # go to edit mode
    general.activate_object(context, cutout_obj, mode='EDIT')


def create_cutout_line(context):
    # set obj params
    ufit_obj = bpy.data.objects['uFit']
    ufit_cutout_obj = bpy.data.objects['uFit_Cutout']

    # increase the smoothness of the cutout plane
    bpy.context.object.data.twist_smooth = 500

    # convert curve to mesh
    general.activate_object(context, ufit_cutout_obj, mode='OBJECT')
    bpy.ops.object.convert(target='MESH')

    # apply scaling, rotation and location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Store vertex coordinates of UFitCutout object
    vert_coordinates = []
    for v in ufit_cutout_obj.data.vertices:
        vert_coordinates.append(v.co)

    # make the ufit object the active object
    general.activate_object(context, ufit_obj, mode='OBJECT')

    # remesh the ufit object so you have quads
    color_attributes.remesh_with_texture_to_color_attr(context, ufit_obj, 'scan_colors')

    # join the ufit_cutout and ufit object
    selected_objects = [ufit_obj, ufit_cutout_obj]
    join_dict = {
        'object': ufit_obj,
        'active_object': ufit_obj,
        'selected_objects': selected_objects,
        'selected_editable_objects': selected_objects
    }
    bpy.ops.object.join(join_dict)

    # make the new ufit object active and switch to edit mode
    general.activate_object(context, ufit_obj, mode='EDIT')

    # Use vertex coordinates to reselect joined UFitCutout object
    general.select_verts_by_co(ufit_obj, vert_coordinates)

    # switch to face selection
    bpy.ops.mesh.select_mode(type='FACE')

    # execute intersect (knife) - will create an edge  (intersect selected with unselected faces)
    bpy.ops.mesh.intersect(mode='SELECT_UNSELECT',
                           separate_mode='CUT',
                           solver='EXACT')

    # Use vertex coordinates again to reselect joined UFitCutout object, and delete verts
    bpy.ops.mesh.select_mode(type='VERT')
    general.select_verts_by_co(ufit_obj, vert_coordinates)
    bpy.ops.mesh.select_linked(delimit=set())  # new vertices created due to intersect should also be deleted
    selected_verts = general.get_selected_vertices_co(context)
    bpy.ops.mesh.delete(type='VERT')

    # select the cutout line
    general.select_verts_by_co(ufit_obj, selected_verts)


def get_avg_z(obj):
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    loc = [v.co.z for v in bm.verts if v.select]
    avg = 0
    if loc:
        avg = sum(loc) / len(loc)

    return avg


def perform_cutout(context):
    # set obj params
    ufit_obj = bpy.data.objects['uFit']

    # relax the edge by looptools
    bpy.ops.mesh.looptools_relax(input='selected',
                                 interpolation='cubic',
                                 iterations='10',
                                 regular=True)

    # the cutout edge is selected. Invert selection and smooth all the rest
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.vertices_smooth(factor=1.0, repeat=3)
    bpy.ops.mesh.select_all(action='INVERT')

    # split the object by the looped edge
    bpy.ops.mesh.edge_split(type='VERT')

    # small bend out around the cutout to avoid sharp edges touching the leg
    # bpy.ops.transform.resize(value=(1.01, 1.01, 1),
    #                          orient_type='GLOBAL',
    #                          # orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    #                          orient_matrix_type='GLOBAL',
    #                          constraint_axis=(True, True, False), mirror=True,
    #                          use_proportional_edit=True,
    #                          proportional_edit_falloff='LINEAR',
    #                          proportional_size=0.003,
    #                          use_proportional_connected=False,
    #                          use_proportional_projected=False)

    # create vertex group (for next step)
    general.create_new_vertex_group_for_selected(context, ufit_obj, 'cutout_edge', mode='EDIT')

    # keep the object with the lowest average z coordinate
    selected_edges = general.get_selected_edges(context)
    if selected_edges:
        bpy.ops.mesh.select_linked_pick(deselect=False,
                                        delimit=set(),
                                        object_index=ufit_obj.pass_index,
                                        index=selected_edges[0])

        # Calculate the average z-index
        avg_z_part1 = get_avg_z(ufit_obj)
        bpy.ops.mesh.select_all(action='INVERT')
        avg_z_part2 = get_avg_z(ufit_obj)

        # keep the part with lowest avg z
        if avg_z_part1 > avg_z_part2:
            bpy.ops.mesh.select_all(action='INVERT')

        # make sure the edge itself is not selected and delete
        general.deselect_edges_by_idx(context, selected_edges)
        bpy.ops.mesh.delete(type='VERT')

        # select all and remove doubles
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()

        # dissolve geometry to remove weird normals
        bpy.ops.mesh.dissolve_degenerate(threshold=0.00025)

    else:
        raise Exception('Please select the cutout line')


def cutout(context):
    create_cutout_line(context)
    perform_cutout(context)


###############################
# Scaling
###############################
def prep_scaling(context):
    # save sculpt circumferences
    context.scene.ufit_sculpt_circumferences = context.scene.ufit_circumferences


def perc_scaling(obj, liner_perc):
    # move the object origin of to the center of mass
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    obj.scale.x = 1 + liner_perc
    obj.scale.y = 1 + liner_perc
    obj.scale.z = 1 + liner_perc

    # resets the object origin to the worlds origin
    general.apply_transform(obj, use_location=True, use_rotation=True, use_scale=True)


def mm_scaling(context, obj, mm_dist):
    general.activate_object(context, obj, mode='EDIT')
    general.scale_distance(obj, mm_dist)


def scale(context):
    ufit_obj = bpy.data.objects['uFit']
    ufit_measure = bpy.data.objects['uFit_Measure']
    ufit_measure.hide_set(False)  # must be visible for scaling

    general.duplicate_obj(ufit_obj, 'uFit_Prescale', context.collection, data=True, actions=False)

    # scale according to the liner thickness
    if context.scene.ufit_scaling_unit == 'percentage':
        perc_scaling(ufit_obj, context.scene.ufit_liner_scaling / 100)  # percentage
        perc_scaling(ufit_measure, context.scene.ufit_liner_scaling / 100)  # percentage
    else:
        mm_scaling(context, ufit_obj, context.scene.ufit_liner_scaling / 1000)  # mm
        mm_scaling(context, ufit_measure, context.scene.ufit_liner_scaling / 1000)  # mm

    ufit_measure.hide_set(True)  # must be visible for scaling


#########################################
# Verify Scaling
#########################################
def prep_verify_scaling(context):
    # switch to object mode and material shading
    user_interface.change_orthographic('TOP')


def verify_scaling(context):
    # apply all transformations to UFit and UFitMeasure objects
    ufit_objs = [bpy.data.objects['uFit'], bpy.data.objects['uFit_Measure']]
    for obj in ufit_objs:
        general.apply_transform(obj, use_location=True, use_rotation=True, use_scale=True)

    # delete the pre-scaling object
    general.delete_obj_by_name_contains('uFit_Prescale')


#########################################
# Thickness
#########################################
def create_thickness(context):
    # set obj params
    ufit_obj = bpy.data.objects['uFit']

    # switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # duplicate UFit object (also copies the vertex group)
    ufit_outer_shell = general.duplicate_obj(ufit_obj, 'uFit_Outer', context.collection, data=True, actions=False)

    # scale outer shell
    thickness = context.scene.ufit_print_thickness / 1000
    general.activate_object(context, ufit_outer_shell, mode='EDIT')  # activate the UFitOuter Object
    general.scale_distance_xy(ufit_outer_shell, thickness)
    general.activate_object(context, ufit_obj, mode='OBJECT')  # activate the UFit Object

    # toggle editmode to make sure everything is applied
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    # join/merge outer and inner shell
    selected_objects = [ufit_obj, ufit_outer_shell]
    join_dict = {
        'object': ufit_obj,
        'active_object': ufit_obj,
        'selected_objects': selected_objects,
        'selected_editable_objects': selected_objects
    }
    bpy.ops.object.join(join_dict)

    # switch to edit mode and deselect all
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')  # deselect all vertices

    # activate the vertex group
    ufit_mesh = ufit_obj.data
    vertex_group = ufit_obj.vertex_groups.get('cutout_edge')
    if vertex_group is not None:
        # iterate over the vertices of the object and check if they have the vertex group assigned to them
        vertex_indices = [v.index for v in ufit_mesh.vertices if vertex_group.index in [g.group for g in v.groups]]
        general.select_verts_by_idx(ufit_obj, vertex_indices)

    # remove wrongly selected edges (very exceptional)
    general.deselect_non_loop_edges(ufit_obj)

    # connect outer and inner shell (bridge with looptools)
    # bpy.ops.mesh.looptools_relax(input='selected', interpolation='cubic', iterations='10', regular=True)
    bpy.ops.mesh.bridge_edge_loops()
    # bpy.ops.mesh.looptools_bridge(cubic_strength=1, interpolation='cubic', loft=False, loft_loop=False, min_width=0,
    #                               mode='shortest', remove_faces=True, reverse=False, segments=1, twist=0)

    # make manifold
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.print3d_clean_non_manifold()
