import os
import bpy
from mathutils import Vector
from ..utils import annotations, general, user_interface


#########################################
# Import Connector
#########################################
def prep_import_connector(context):
    # change orthographic
    user_interface.change_orthographic('BOTTOM')

    # activate grease pensil
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Connector_Loc')

    # deactivate snapping
    bpy.context.scene.tool_settings.use_snap = False


def import_connector(context, path_consts, connector_type, foot_type, amputation_side):
    objs = [obj for obj in bpy.data.objects if obj.name.startswith("uFit")]
    ufit_circum_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Circum_")]
    objs.extend(ufit_circum_objects)

    # switch origin to center of mass
    ufit_obj = bpy.data.objects['uFit']
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    # move the object to origin of world
    anchor_point = Vector((ufit_obj.location.x, ufit_obj.location.y, 0))

    # set new anchor point for all ufit objects and circums
    default_z_loc = 0.4
    if context.scene.ufit_device_type == 'transfemoral':
        default_z_loc = 0.6

    for obj in objs:
        obj.hide_set(False)
        general.activate_object(context, obj, mode='OBJECT')
        general.set_object_origin(anchor_point)
        general.move_object(obj, -anchor_point)  # bring to the center
        general.move_object(obj, Vector((0, 0, default_z_loc)))  # move up
        if obj.name != 'uFit':
            obj.hide_set(True)

    # go to object mode
    general.activate_object(context, ufit_obj, mode='OBJECT')
    user_interface.set_shading_solid_mode()

    # set connector file params
    connectors_dir = os.path.join(os.path.dirname(__file__), f"../../../..{path_consts['paths']['connectors_path']}")
    conn_file_path = f'{connectors_dir}/{connector_type}'
    conn_inner_path = 'Object'
    object_connector = 'Connector'

    # load the connector
    bpy.ops.wm.append(
        filepath=os.path.join(conn_file_path, conn_inner_path, object_connector),
        directory=os.path.join(conn_file_path, conn_inner_path),
        filename=object_connector
    )

    # set foot file params
    feet_dir = os.path.join(os.path.dirname(__file__), f"../../../..{path_consts['paths']['feet_path']}")
    foot_file_path = f'{feet_dir}/{foot_type}'
    foot_inner_path = 'Object'
    object_foot = 'Foot'

    # load the connector
    bpy.ops.wm.append(
        filepath=os.path.join(foot_file_path, foot_inner_path, object_foot),
        directory=os.path.join(foot_file_path, foot_inner_path),
        filename=object_foot
    )

    # set foot obj
    foot_obj = bpy.data.objects[object_foot]
    if amputation_side == 'left':
        # mirror the foot in the direction of x-axis
        foot_obj.scale.x = -1

    # set connector obj
    conn_obj = bpy.data.objects[object_connector]

    # move connector obj
    bottom_vert = annotations.get_all_points('Selections', 'Connector_Loc')[-1]  # get last
    distance = bottom_vert.z + (default_z_loc - 0.02)
    general.move_object(conn_obj, Vector((0, 0, distance)))

    # shrinkwrap modifier on the connector object
    shrinkwrap_mod = conn_obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")
    shrinkwrap_mod.wrap_method = 'PROJECT'
    shrinkwrap_mod.wrap_mode = 'OUTSIDE_SURFACE'
    shrinkwrap_mod.subsurf_levels = 0
    shrinkwrap_mod.vertex_group = "shrinkwrap_group"
    shrinkwrap_mod.use_project_z = True
    shrinkwrap_mod.target = ufit_obj
    shrinkwrap_mod.auxiliary_target = ufit_obj
    shrinkwrap_mod.vertex_group = "shrinkwrap_group"

    # cleanup annotations
    user_interface.cleanup_grease_pencil(context)
    
    
#################################
# Alignment
#################################
def prep_alignment(context):
    conn_obj = bpy.data.objects['Connector']
    foot_obj = bpy.data.objects['Foot']

    foot_obj.hide_select = False  # make selectable
    foot_obj.select_set(True)  # also select foot for focus (UFit obj already selected)
    user_interface.focus_on_selected()  # focus on both selected objects
    foot_obj.select_set(False)  # deselect foot after focus
    foot_obj.hide_select = True  # do not make selectable
    conn_obj.hide_set(True)

    context.scene.ufit_quad_view = True
    context.scene.ufit_orthographic_view = True

    # change the view for the user
    user_interface.change_orthographic('FRONT')

    # show the z-axis
    context.space_data.overlay.show_axis_z = True
    context.space_data.overlay.show_cursor = False

    # activate the rotation tool
    context.scene.ufit_alignment_tool = 'builtin.rotate'
    context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'


def save_alignment(context):
    ufit_obj = bpy.data.objects['uFit']
    ufit_measure_obj = bpy.data.objects['uFit_Measure']
    ufit_original_obj = bpy.data.objects['uFit_Original']
    conn_obj = bpy.data.objects['Connector']

    # save the connector locaiton
    context.scene.ufit_connector_loc = conn_obj.location

    # apply transformations
    transform_objs = [obj for obj in bpy.data.objects if obj.name.startswith("Circum_")]
    transform_objs.extend([ufit_measure_obj, ufit_original_obj])
    for obj in transform_objs:
        obj.location = ufit_obj.location
        obj.rotation_euler = ufit_obj.rotation_euler
        general.apply_transform(obj, use_location=True, use_rotation=True, use_scale=True)

    for obj in [ufit_obj, conn_obj]:
        general.apply_transform(obj, use_location=True, use_rotation=True, use_scale=True)


#########################################
# Transition Connector
#########################################
def scale_connector_scale_groups(context):
    conn_obj = bpy.data.objects['Connector']

    # make sure the connector object is not hidden and activated
    conn_obj.hide_set(False)

    # select scale_group_inner and scale smaller
    general.select_vertices_from_vertex_group(context, conn_obj, "scale_group_inner")
    bpy.ops.transform.resize(value=(0.95, 0.95, 0.95))

    # select scale_group_outer and scale bigger
    general.select_vertices_from_vertex_group(context, conn_obj, "scale_group_outer")
    bpy.ops.transform.resize(value=(2, 2, 2))


def prep_transition_connector(context):
    context.scene.ufit_quad_view = False

    conn_obj = bpy.data.objects['Connector']
    ufit_obj = bpy.data.objects['uFit']

    # change to the correct mode
    user_interface.change_orthographic('FRONT')
    user_interface.set_shading_solid_mode()

    # update the shrinkwrap modifier
    shrinkwrap_mod = conn_obj.modifiers["Shrinkwrap"]
    shrinkwrap_mod.wrap_method = 'NEAREST_SURFACEPOINT'
    shrinkwrap_mod.wrap_mode = 'ON_SURFACE'

    # switch to object mode
    general.activate_object(context, ufit_obj, mode='OBJECT')

    # add a plane (automatically the active object
    z_loc = context.scene.ufit_connector_loc[2] + 0.05
    bpy.ops.mesh.primitive_plane_add(size=0.2, enter_editmode=False, align='WORLD',
                                     location=(0, 0, z_loc), scale=(1, 1, 1))

    # name the new object
    cut_obj = bpy.context.active_object
    cut_obj.name = "Cutter"

    # lock to y direction movement
    cut_obj.lock_location[0] = True
    cut_obj.lock_location[1] = True

    # set the move tool
    bpy.ops.wm.tool_set_by_id(name="builtin.move")

    # add boolean modifier to the UFit obj to make the cut
    boolean_mod = ufit_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'DIFFERENCE'
    boolean_mod.solver = 'EXACT'
    boolean_mod.object = cut_obj

    # scale the connector inner and outer shell
    # scale_connector_scale_groups(context, conn_obj)

    # activate the cutter object
    general.activate_object(context, cut_obj, mode='OBJECT')

    # make the ufit object unselectable
    ufit_obj.hide_select = True

    # turn of the xray
    context.scene.ufit_x_ray = False


def correct_thickness_connector(context, conn_obj):
    # # subdivide outer shell
    # general.activate_object(context, conn_obj, mode='OBJECT')
    # general.select_vertices_from_vertex_group(context, conn_obj, 'outer_shell_group')
    # bpy.ops.mesh.subdivide(number_cuts=5)

    # create inner shell object for shrinkwrap
    general.select_vertices_from_vertex_group(context, conn_obj, 'inner_shell_group')
    inner_shell_obj = general.create_obj_from_selection(context, 'Inner_Shell', copy_vg=True)

    # # extrude the bottom of the inner shell object along it's curve
    general.select_vertices_from_vertex_group(context, inner_shell_obj, 'inner_shell_bottom')
    general.move_selected_verts_along_local_axis(inner_shell_obj, 0.02, axis=(False, True, False))

    # relax the inner_shell_bottom
    bpy.ops.mesh.looptools_relax(input='selected', interpolation='linear', iterations='25', regular=True)

    # # make the inner_shell_bottom vertices a perfect circle
    # bpy.ops.mesh.looptools_circle(custom_radius=False, fit='best', flatten=True, influence=100, lock_x=False,
    #                               lock_y=False, lock_z=False, radius=1, angle=0, regular=True)
    #
    # # subdivide inner shell object
    # # general.select_vertices_from_vertex_group(context, inner_shell_obj, 'inner_shell_group')
    # # bpy.ops.mesh.subdivide(number_cuts=5)

    # add shrinkwrap modifier to connector
    shrinkwrap_mod = conn_obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")
    shrinkwrap_mod.wrap_method = 'NEAREST_SURFACEPOINT'  # 'NEAREST_VERTEX'
    shrinkwrap_mod.wrap_mode = 'ON_SURFACE'
    shrinkwrap_mod.target = inner_shell_obj
    shrinkwrap_mod.offset = 0.0005  # negligible
    shrinkwrap_mod.vertex_group = 'outer_shell_group'

    # apply shrinkwrap
    general.activate_object(context, conn_obj, mode='OBJECT')
    override = {"object": conn_obj, "active_object": conn_obj}
    bpy.ops.object.modifier_apply(override, modifier="Shrinkwrap")

    # move outer shell in the xy direction
    thickness = context.scene.ufit_print_thickness / 1000 - 0.0005
    general.select_vertices_from_vertex_group(context, conn_obj, 'outer_shell_group')
    general.scale_selected_verts_distance_xy(conn_obj, thickness)

    # get all vertices below x mm and pull/push to connector height down
    general.activate_object(context, conn_obj, mode='OBJECT')
    connector_height = context.scene.ufit_connector_loc[2]

    for v in general.get_vertices_below_z(conn_obj, z=(connector_height + 0.005)):
        v.co.z = connector_height

    # delete the inner shell object
    general.delete_obj_by_name_contains('Inner_Shell')


def transition_connector(context):
    ufit_obj = bpy.data.objects['uFit']
    conn_obj = bpy.data.objects['Connector']

    # bug in blender - you have to use an override to apply the modifier
    general.activate_object(context, ufit_obj, mode='OBJECT')
    override = {"object": ufit_obj, "active_object": ufit_obj}
    bpy.ops.object.modifier_apply(override, modifier="Boolean")

    general.activate_object(context, conn_obj, mode='OBJECT')
    override = {"object": conn_obj, "active_object": conn_obj}
    bpy.ops.object.modifier_apply(override, modifier="Shrinkwrap")

    # delete the cutter object
    general.delete_obj_by_name_contains(name='Cutter')

    # make sure the thickness is horizontally consistent
    if context.scene.ufit_try_perfect_print:
        correct_thickness_connector(context, conn_obj)

    # join the connector and ufit object
    # selected_objects = [ufit_obj, conn_obj]
    # join_dict = {
    #     'object': ufit_obj,
    #     'active_object': ufit_obj,
    #     'selected_objects': selected_objects,
    #     'selected_editable_objects': selected_objects
    # }
    # bpy.ops.object.join(join_dict)

    # boolean modifier to merge the two objects
    boolean_mod = ufit_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'UNION'
    boolean_mod.solver = 'EXACT'
    boolean_mod.object = conn_obj
    # boolean_mod.use_self = True  # costs a crazy amount of performance

    # apply the boolean modifier
    general.activate_object(context, ufit_obj, mode='OBJECT')
    override = {"object": ufit_obj, "active_object": ufit_obj}
    bpy.ops.object.modifier_apply(override, modifier="Boolean")

    # delete connector object
    bpy.data.objects.remove(conn_obj, do_unlink=True)

    # voxel remesh object to remove material between inner and outer shell
    voxel_remesh = ufit_obj.modifiers.new("Voxel Remesh", type='REMESH')
    voxel_remesh.mode = 'VOXEL'
    voxel_remesh.voxel_size = 0.0005  # Set the voxel size

    # Add a corrective smooth modifier to round corners
    corrective_smooth = ufit_obj.modifiers.new("Corrective Smooth", type='CORRECTIVE_SMOOTH')
    corrective_smooth.factor = 1
    corrective_smooth.iterations = 5  # Set the number of iterations (repeat parameter)
    corrective_smooth.smooth_type = 'LENGTH_WEIGHTED'
    corrective_smooth.use_only_smooth = True

    # apply modifiers
    # bug in blender - you have to use an override to apply the modifier
    override = {"object": ufit_obj, "active_object": ufit_obj}
    bpy.ops.object.modifier_apply(override, modifier="Voxel Remesh")
    bpy.ops.object.modifier_apply(override, modifier="Corrective Smooth")

    # decimate geometry to reduce vertices
    general.activate_object(context, ufit_obj, mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.decimate(ratio=0.05)
