import bpy
import bmesh
import math
from mathutils import Vector
import numpy as np
from ..utils import annotations, color_attributes, general, user_interface, nodes

color_attr_select = 'area_selection'


#################################
# Push/Pull/Smooth
#################################
def prep_push_pull_smooth(context):
    ufit_obj = bpy.data.objects['uFit']

    # add area selection color attribute and add shader nodes
    color_attributes.add_new_color_attr(ufit_obj, name=color_attr_select, color=(1, 1, 1, 1))
    nodes.set_push_pull_smooth_shader_nodes(ufit_obj, color_attr_name=color_attr_select)

    # activate vertex paint mode
    user_interface.set_shading_material_preview_mode()
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')
    context.scene.tool_settings.unified_paint_settings.size = 30  # change the brush size to 30px
    bpy.data.brushes["Draw"].color = (0, 1, 0)  # green
    bpy.data.brushes["Draw"].secondary_color = (1, 1, 1)  # white

    # set the falloff to max
    bpy.ops.brush.curve_preset(shape='MAX')


# called after remeasuring
def minimal_prep_push_pull_smooth(context):
    ufit_obj = bpy.data.objects['uFit']

    # activate the uFit Object
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')

    # reset color attribute to all white vertices
    context.scene.ufit_vertex_color_all = False
    # color_attributes.reset_color_attribute(ufit_obj, color_attr_select, color=(1, 1, 1, 1))


# called after remeasuring
def minimal_prep_free_sculpt(context):
    ufit_obj = bpy.data.objects['uFit']

    # activate the uFit Object
    general.activate_object(context, ufit_obj, mode='SCULPT')


def smooth_region(context):
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((1, 1, 1, 1)))

    # smooth selected vertices
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=context.scene.ufit_smooth_factor)

    # toggle edit mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()


def push_pull_region(context, extrusion, exclude_vertex_groups=None):
    # set the ufit object
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((1, 1, 1, 1)))

    # decrease selected region
    # general.decrease_selected_vertices_region(ufit_obj, 2)

    # deselect vertices that should be excluded
    if exclude_vertex_groups:
        general.deselect_vertices_from_vertex_groups(context, ufit_obj, exclude_vertex_groups)

    # move vertices along there normals
    general.move_verts_along_faces_normal(ufit_obj, extrusion)

    # increase the selected region for smoothing
    general.increase_selected_vertices_region(ufit_obj, 2)

    # deselect vertices again that should be excluded
    if exclude_vertex_groups:
        general.deselect_vertices_from_vertex_groups(context, ufit_obj, exclude_vertex_groups)

    # smooth the smooth_vertices and deselect
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=7)


def push_pull_region_circular(context, extrusion):
    ufit_obj = bpy.data.objects['uFit']

    # select vertices by color attribute layer - exclude default color black
    color_attributes.select_vertices_by_color_exclude(context, ufit_obj, color_attr_select, Vector((1, 1, 1, 1)))

    # get the selected vertices (indexes are ruined)
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
    bpy.ops.transform.translate(value=(0, 0, extrusion*1.5),
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


def pull_bottom(context, extrusion):
    # set the ufit object
    ufit_obj = bpy.data.objects['uFit']

    # activate proportional editing
    bpy.context.scene.tool_settings.use_proportional_edit = True

    # activate transformation orientation "normal" instead of global
    bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'

    # perform proportional editing (extrusion)
    bpy.ops.transform.translate(value=(0, 0, extrusion),
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


def pull_bottom_done(context):
    # turn of the xray
    context.scene.ufit_x_ray = False


#################################
# Prepare Cutout
#################################
def lift_ufit_non_manifold_top(context):
    ufit_obj = bpy.data.objects['uFit']
    non_manifold_areas = general.create_non_manifold_vertex_groups(context, ufit_obj, max_verts=None)

    # get the non-manifold area with the biggest amount of vertices (big gap at top of socket)
    max_nma = None
    max_verts = 0
    for nma, verts in non_manifold_areas.items():
        if len(verts) > max_verts:
            max_verts = len(verts)
            max_nma = nma

    if max_nma:
        # highlight vertices from non-manifold area (vertex group)
        general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=[max_nma])

        # deactivate snapping to move verts up
        bpy.context.scene.tool_settings.use_snap = False

        # move the verts x cm up
        context.scene.transform_orientation_slots[0].type = 'GLOBAL'
        bpy.ops.transform.translate(value=(0, 0, 0.05))


def add_straight_cutout_plane(context):
    ufit_obj = bpy.data.objects['uFit']

    # set the local object origin already to the center of mass
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    # add straight cutout plane
    bpy.ops.mesh.primitive_plane_add(size=0.35, location=ufit_obj.location)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    # rename plane
    cut_obj = context.active_object
    cut_obj.name = "uFit_Cutout"

    # apply location
    general.apply_transform(ufit_obj, use_location=True, use_rotation=True, use_scale=True)

    # lock to z direction movement
    # cut_obj.lock_location[0] = True
    # cut_obj.lock_location[1] = True

    # hide objects
    cut_obj.hide_set(True)


def prep_cutout_prep(context):
    ufit_obj = bpy.data.objects['uFit']

    add_straight_cutout_plane(context)

    # apply location
    general.apply_transform(ufit_obj, use_location=True, use_rotation=True, use_scale=True)

    # now duplicate ufit_obj
    ufit_original = general.duplicate_obj(ufit_obj, 'uFit_Original', context.collection, data=True, actions=False)
    ufit_measure = general.duplicate_obj(ufit_obj, 'uFit_Measure', context.collection, data=True, actions=False)

    # remesh the uFit object so you have quads
    if context.scene.ufit_device_type in ('transfemoral'):
        lift_ufit_non_manifold_top(context)
    color_attributes.remesh_with_texture_to_color_attr(context, ufit_obj, 'scan_colors')

    # hide objects
    ufit_original.hide_set(True)
    ufit_measure.hide_set(True)

    # transformation orientation global + activate vertex snapping
    context.scene.transform_orientation_slots[0].type = 'LOCAL'
    context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_elements = {'FACE_NEAREST'}

    # switch to annotation tool
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Cutout')

    # activate ufit
    general.activate_object(context, ufit_obj, mode='OBJECT')


def minimal_prep_cutout_prep(context):
    # switch to annotation tool
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Cutout')


def minimal_prep_new_cutout(context):
    add_straight_cutout_plane(context)

    bpy.context.scene.tool_settings.use_snap = True

    # set cutout style back to default
    context.scene.ufit_cutout_style = 'free'

    # switch to annotation tool
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Cutout')


def create_cutout_path(context):
    if 'uFit_Cutout' in bpy.data.objects:
        general.delete_obj_by_name_contains('uFit_Cutout')

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
    if context.scene.ufit_cutout_style == 'free':
        ufit_cutout_ob = create_cutout_path(context)
        general.activate_object(context, ufit_cutout_ob, mode='EDIT')

        # close the curve
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.cyclic_toggle()

        bpy.context.object.data.dimensions = '3D'

        # tilt local z-axis x degrees
        bpy.ops.curve.tilt_clear()  # first clear the tilt
        bpy.ops.transform.tilt(value=math.radians(int(bpy.context.scene.bl_rna.properties['ufit_mean_tilt'].default)),
                               mirror=False,
                               use_proportional_edit=False,
                               proportional_edit_falloff='SMOOTH',
                               proportional_size=1,
                               use_proportional_connected=False,
                               use_proportional_projected=False)

        # Z_UP not working in all cases
        bpy.context.object.data.twist_mode = 'Z_UP'

        # extrude the curve x cm everywhere
        bpy.context.object.data.extrude = 0.01

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
    if context.scene.ufit_cutout_style == 'free':
        cutout_obj = bpy.data.objects['uFit_Cutout']

        # make the cutout object selectable
        cutout_obj.hide_select = True

        # go to edit mode
        general.activate_object(context, cutout_obj, mode='EDIT')


def create_cutout_line(context):
    # set obj params
    ufit_obj = bpy.data.objects['uFit']
    ufit_cutout_obj = bpy.data.objects['uFit_Cutout']

    # turn off xray
    context.scene.ufit_x_ray = False

    # activate ufit_cutout_obj
    general.activate_object(context, ufit_cutout_obj, mode='EDIT')

    if context.scene.ufit_cutout_style == "free":
        # increase the smoothness of the cutout plane
        bpy.context.object.data.twist_smooth = 500

        # convert curve to mesh
        general.activate_object(context, ufit_cutout_obj, mode='OBJECT')
        bpy.ops.object.convert(target='MESH')
    elif context.scene.ufit_cutout_style == "straight":
        # increase the number of vertices for accurate cut
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=10)
        general.activate_object(context, ufit_cutout_obj, mode='OBJECT')

    # apply scaling, rotation and location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Store vertex coordinates of UFitCutout object
    vert_coordinates = []
    for v in ufit_cutout_obj.data.vertices:
        vert_coordinates.append(v.co)

    # make the ufit object the active object
    general.activate_object(context, ufit_obj, mode='OBJECT')

    # remesh the ufit object so you have quads (happens before for other devices)
    # if context.scene.ufit_device_type in ('transtibial', 'transfemoral'):
    #     color_attributes.remesh_with_texture_to_color_attr(context, ufit_obj, 'scan_colors')

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

    # split the object by the looped edge
    bpy.ops.mesh.edge_split(type='VERT')

    # create vertex group (for next step)
    edge_num = int(context.scene.ufit_number_of_cutouts)
    general.create_new_vertex_group_for_selected(context, ufit_obj, f'cutout_edge_{edge_num}', mode='EDIT')
    context.scene.ufit_number_of_cutouts += 1

    # select all cutout edges
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

    # Invert selection and smooth all the rest to avoid weird normals on scaling
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.vertices_smooth(factor=1.0, repeat=3)
    bpy.ops.mesh.select_all(action='INVERT')

    # select again the created cutout edge
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=[f'cutout_edge_{edge_num}'])

    # keep the object with the lowest average z coordinate
    selected_edges = general.get_selected_edges(context)
    if selected_edges:
        bpy.ops.mesh.select_linked_pick(deselect=False,
                                        delimit=set(),
                                        object_index=ufit_obj.pass_index,
                                        index=selected_edges[0])

        num_verts_part1 = len(general.get_selected_vertices(context))
        bpy.ops.mesh.select_all(action='INVERT')
        num_verts_part2 = len(general.get_selected_vertices(context))

        if num_verts_part2 > num_verts_part1:
            bpy.ops.mesh.select_all(action='INVERT')

        # # Calculate the average z-index
        # avg_z_part1 = get_avg_z(ufit_obj)
        # bpy.ops.mesh.select_all(action='INVERT')
        # avg_z_part2 = get_avg_z(ufit_obj)
        #
        # # keep the part with lowest avg z
        # if avg_z_part1 > avg_z_part2:
        #     bpy.ops.mesh.select_all(action='INVERT')

        # make sure the edge itself is not selected and delete
        general.deselect_edges_by_idx(context, selected_edges)
        bpy.ops.mesh.delete(type='VERT')

        # select all and remove doubles
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()

        # dissolve geometry to remove weird normals
        bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)  # make sure to use the same distance as remove_doubles

    else:
        raise Exception('No cutout line found')


def cutout(context):
    create_cutout_line(context)
    perform_cutout(context)


def cutout_straight(context):
    # cleanup annotations
    user_interface.cleanup_grease_pencil(context)
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

    general.duplicate_obj(ufit_obj, 'uFit_Prescale', context.collection, data=True, actions=False)

    # scale according to the liner thickness
    if context.scene.ufit_scaling_unit == 'percentage':
        perc_scaling(ufit_obj, context.scene.ufit_liner_scaling / 100)  # percentage
    else:
        mm_scaling(context, ufit_obj, context.scene.ufit_liner_scaling / 1000)  # mm

    if 'uFit_Measure' in bpy.data.objects:
        ufit_measure = bpy.data.objects['uFit_Measure']
        ufit_measure.hide_set(False)  # must be visible for scaling

        # scale according to the liner thickness
        if context.scene.ufit_scaling_unit == 'percentage':
            perc_scaling(ufit_measure, context.scene.ufit_liner_scaling / 100)  # percentage
        else:
            mm_scaling(context, ufit_measure, context.scene.ufit_liner_scaling / 1000)  # mm

        ufit_measure.hide_set(True)  # make invisible again

    # smooth to avoid weird normals due to scaling (avoid smoothning of cutout edge)
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=10)


#########################################
# Verify Scaling
#########################################
def prep_verify_scaling(context):
    # switch to object mode and material shading
    user_interface.change_orthographic('TOP')


def verify_scaling(context):
    # apply all transformations to UFit and UFitMeasure objects
    general.apply_transform(bpy.data.objects['uFit'], use_location=True, use_rotation=True, use_scale=True)

    if 'uFit_Measure' in bpy.data.objects:
        general.apply_transform(bpy.data.objects['uFit_Measure'], use_location=True, use_rotation=True, use_scale=True)

    # delete the pre-scaling object
    general.delete_obj_by_name_contains('uFit_Prescale')


#################################
# Draw
#################################
def prep_draw(context):
    ufit_obj = bpy.data.objects['uFit']

    # apply location
    general.apply_transform(ufit_obj, use_location=True, use_rotation=True, use_scale=True)

    # now duplicate ufit_obj
    if 'uFit_Original' not in bpy.data.objects:
        general.duplicate_obj(ufit_obj, 'uFit_Original', context.collection, data=True, actions=False)
    if 'uFit_Measure' not in bpy.data.objects:
        general.duplicate_obj(ufit_obj, 'uFit_Measure', context.collection, data=True, actions=False)

    ufit_original = bpy.data.objects['uFit_Original']
    ufit_measure = bpy.data.objects['uFit_Measure']

    ufit_original.hide_set(False)
    ufit_measure.hide_set(True)

    # create new color attributes
    ca_draw = 'draw_selection'
    ca_voronoi_one = 'voronoi_one_selection'
    ca_voronoi_two = 'voronoi_two_selection'
    color_attributes.add_new_color_attr(ufit_obj, name='draw_selection', color=(1, 1, 1, 1))
    color_attributes.add_new_color_attr(ufit_obj, name='voronoi_one_selection', color=(1, 1, 1, 1))
    color_attributes.add_new_color_attr(ufit_obj, name='voronoi_two_selection', color=(1, 1, 1, 1))
    bpy.data.brushes["Draw"].color = (1, 0, 0)  # Red

    # activate color attribute
    # color_attributes.activate_color_attribute(ufit_obj, color_attr_select)

    # select all vertices within x distance of a border
    cutout_edge_vgs = [vg.name for vg in ufit_obj.vertex_groups if vg.name.startswith('cutout_edge_')]
    general.select_vertices_from_vertex_groups(context, ufit_obj, cutout_edge_vgs)

    # color red within 1 cm of the border red
    general.select_vertices_within_distance_of_selected(ufit_obj, max_distance=0.01)
    color_attributes.color_selected_vertices(context, ufit_obj, ca_draw, color=Vector((1, 0, 0, 1)))
    color_attributes.color_selected_vertices(context, ufit_obj, ca_voronoi_one, color=Vector((1, 0, 0, 1)))

    # color yellow within 0.2 cm of the border black
    # general.select_vertices_from_vertex_groups(context, ufit_obj, cutout_edge_vgs)
    # # general.select_vertices_within_distance_of_selected(ufit_obj, max_distance=0.002)
    # color_attributes.color_selected_vertices(context, ufit_obj, ca_draw, color=Vector((1, 1, 0, 1)))
    # color_attributes.color_selected_vertices(context, ufit_obj, ca_voronoi_one, color=Vector((1, 1, 0, 1)))
    # color_attributes.color_selected_vertices(context, ufit_obj, ca_voronoi_two, color=Vector((1, 1, 0, 1)))

    # activate vertex paint
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')

    # trigger callback
    context.scene.ufit_draw_type = 'free'


def apply_draw(context):
    ufit_obj = bpy.data.objects['uFit']
    ufit_original = bpy.data.objects['uFit_Original']

    ufit_original.hide_set(True)

    # node_tree = bpy.data.node_groups['Voronoi Nodes Empty']

    general.apply_all_modifiers(context, ufit_obj)

    general.activate_object(context, ufit_obj, mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()

    # add remesh (0.03cm) + smooth (factor 0.5, repeat 5)


#########################################
# Milling
#########################################
def create_milling_model(context):
    # set obj params
    ufit_obj = bpy.data.objects['uFit']

    if context.scene.ufit_milling_flare:
        # execute standard flaring
        prep_flare(context)
        flare(context)
        flare_done(context)  # deactivate proportional editing

    # select cutout edge
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

    # use the standard duplicate operator (Shift + D)
    bpy.ops.mesh.duplicate_move()
    # bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1},
    #                             TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_axis_ortho": 'X',
    #                                                     "orient_type": 'GLOBAL',
    #                                                     "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    #                                                     "orient_matrix_type": 'GLOBAL',
    #                                                     "constraint_axis": (False, False, False), "mirror": False,
    #                                                     "use_proportional_edit": False,
    #                                                     "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
    #                                                     "use_proportional_connected": False,
    #                                                     "use_proportional_projected": False, "snap": True,
    #                                                     "snap_elements": {'FACE_NEAREST'}, "use_snap_project": False,
    #                                                     "snap_target": 'CLOSEST', "use_snap_self": True,
    #                                                     "use_snap_edit": True, "use_snap_nonedit": True,
    #                                                     "use_snap_selectable": False, "snap_point": (0, 0, 0),
    #                                                     "snap_align": False, "snap_normal": (0, 0, 0),
    #                                                     "gpencil_strokes": False, "cursor_transform": False,
    #                                                     "texture_space": False, "remove_on_cancel": False,
    #                                                     "view2d_edge_pan": False, "release_confirm": False,
    #                                                     "use_accurate": False, "use_automerge_and_split": False})

    # add the copied vertices to a new vertex group
    general.create_new_vertex_group_for_selected(context, ufit_obj, 'milling_model_edge', mode='EDIT')

    # select again the vertices from cutout_edge group (contains the original + copied vertices)
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

    # connect vertices via bridge edge loops
    bpy.ops.mesh.bridge_edge_loops()

    # get the max z
    max_z = general.get_selected_max_z(ufit_obj)
    new_z = max_z + context.scene.ufit_milling_margin/100  # add milling margin

    # set new z coordinate for the milling_model_edge vertex group
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=['milling_model_edge'])
    general.set_selected_to_z(ufit_obj, new_z)

    # fill the hole
    bpy.ops.mesh.edge_face_add()


#########################################
# Thickness
#########################################
MARGIN_DISTANCE = 0.015  # meter

def prep_thickness(context):
    ufit_obj = bpy.data.objects['uFit']

    # trigger the callback to set default values
    context.scene.ufit_thickness_voronoi = 'normal'

    # create color attribute
    color_attributes.add_new_color_attr(ufit_obj, name=color_attr_select, color=(1, 1, 1, 1))
    bpy.data.brushes["Draw"].color = (1, 0, 0)  # Red

    # get border vertices (using vertex groups from previous cutout)
    vgs = general.get_all_cutout_edges(context)
    border_vertices = general.get_vertices_from_multiple_vertex_groups(ufit_obj, vgs)

    # add a safety margin to the border by including more vertices
    extended_border_vertices = general.expand_border_vertices(
        ufit_obj, border_vertices, MARGIN_DISTANCE
    )

    # color border vertices
    color_attributes.set_vertices_color(
        ufit_obj,
        color_attr_select,
        extended_border_vertices,
        color=(1.0, 0.0, 0.0, 1.0), # Red
    )

    # activate color attribute
    color_attributes.activate_color_attribute(ufit_obj, color_attr_select)


def create_printing_thickness(context):
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
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

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


#########################################
# Custom Thickness
#########################################
def prep_custom_thickness(context):
    ufit_obj = bpy.data.objects['uFit']

    # add area selection color attribute and add shader nodes
    color_attributes.add_new_color_attr(ufit_obj, name=color_attr_select, color=(1, 1, 1, 1))

    # activate color attribute area_selection:
    color_attributes.activate_color_attribute(ufit_obj, color_attr_select)

    # activate vertex paint mode
    general.activate_object(context, ufit_obj, mode='VERTEX_PAINT')
    context.scene.tool_settings.unified_paint_settings.size = 30  # change the brush size to 30px
    bpy.data.brushes["Draw"].color = (0, 1, 0)  # green
    bpy.data.brushes["Draw"].secondary_color = (1, 1, 1)  # white


def minimal_prep_custom_thickness(context):
    minimal_prep_push_pull_smooth(context)


def create_custom_thickness(context, extrusion):
    vgs = general.get_all_cutout_edges(context)
    push_pull_region(context, extrusion, exclude_vertex_groups=vgs)


def custom_thickness_done(context):
    ufit_obj = bpy.data.objects['uFit']
    color_attributes.delete_color_attribute(ufit_obj, color_attr_select)


#########################################
# Flare
#########################################
def prep_flare(context):
    ufit_obj = bpy.data.objects['uFit']

    # activate quad view
    context.scene.ufit_quad_view = True

    # activate proportional editing
    bpy.context.scene.tool_settings.use_proportional_edit = True

    # switch to edit mode and select vertices from cutout edge
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

    # move cursor to the middle of the selection
    bpy.ops.view3d.snap_cursor_to_selected()

    # set the default flare tool
    user_interface.set_active_tool(bpy.context.scene.bl_rna.properties['ufit_flare_tool'].default)

    # set proportional size to default size of ufit_flare_percentage
    bpy.context.tool_settings.proportional_size = 0.01

    # turn off the overlay
    bpy.context.space_data.overlay.show_overlays = False


def flare(context):
    # set ufit obj
    ufit_obj = bpy.data.objects['uFit']

    # make sure the vertices from the cutout edge are selected
    vgs = general.get_all_cutout_edges(context)
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=vgs)

    # calculate the flare percentage
    flare_perc = 1 + context.scene.ufit_flare_percentage/100

    # flare
    bpy.ops.transform.resize(value=(flare_perc, flare_perc, 1),
                             orient_type='GLOBAL',
                             # orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                             orient_matrix_type='GLOBAL',
                             constraint_axis=(True, True, False),
                             mirror=True,
                             use_proportional_edit=True,
                             proportional_edit_falloff='SMOOTH',
                             proportional_size=context.tool_settings.proportional_size,
                             use_proportional_connected=False,
                             use_proportional_projected=False)


def flare_done(context):
    bpy.context.scene.tool_settings.use_proportional_edit = False


