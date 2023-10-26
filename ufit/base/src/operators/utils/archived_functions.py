import bpy
import bmesh
from mathutils import Vector
from . import general


def make_inner_outer_parallel(context, conn_obj):
    # function that was used to equalize the angle between the inner and outer shell of the connector
    # A group of vertices on the connector was used in a shrinkwrap modifier to be projected on the socket (z direction)
    # The outer vertices are scaled so that they beautifully fit the socket
    # The inner vertices aren't scaled, so they are straight up.
    # Goal of the function is to make the inner shell (almost) parallel to the outer shell)

    general.select_vertices_from_vertex_groups(context, conn_obj, vg_names=['scale_group_inner'])

    if context.scene.ufit_resize > 0:
        # object mode required for depsgraph object
        general.activate_object(context, conn_obj, 'OBJECT')

        # set measure points shrinkwrap + scaling
        conn_obj_eval = general.get_depsgraph_object(context, conn_obj)
        context.scene.ufit_mp_outer_sw_sc = general.get_vertices_from_vertex_group(conn_obj_eval, 'measurepoint_outer')[0]['co']

        scale_angle_inner = 0
        scale_angle_outer = general.calculate_angle_between_vectors(point_a=Vector(context.scene.ufit_mp_outer),
                                                                    point_b=Vector(context.scene.ufit_mp_outer_sw),
                                                                    point_c=Vector(context.scene.ufit_mp_outer_sw_sc))

        i = 0
        calc_resize = 1.01  # always scale with 1%
        while scale_angle_inner < scale_angle_outer or i > 50:
            # scale vertices in edit mode
            general.activate_object(context, conn_obj, 'EDIT')
            bpy.ops.transform.resize(value=(calc_resize, calc_resize, calc_resize))

            # object mode required for depsgraph object
            general.activate_object(context, conn_obj, 'OBJECT')
            conn_obj_eval = general.get_depsgraph_object(context, conn_obj)
            context.scene.ufit_mp_inner_sw_sc = general.get_vertices_from_vertex_group(conn_obj_eval, 'measurepoint_inner')[0]['co']
            scale_angle_inner = general.calculate_angle_between_vectors(point_a=Vector(context.scene.ufit_mp_inner),
                                                                        point_b=Vector(context.scene.ufit_mp_inner_sw),
                                                                        point_c=Vector(
                                                                            context.scene.ufit_mp_inner_sw_sc))

            i += 1  # protect infinite loop


def create_cutter_obj(context, conn_obj):
    # select vertices from vertex group (switches to edit mode)
    general.select_vertices_from_vertex_groups(context, conn_obj, vg_names=['scale_group_inner'])

    # separate vertices
    cut_obj = general.create_obj_from_selection(context, 'Cutter')

    # deselect vertices from connector object
    general.deselect_in_edit_mode(context)

    # active object
    general.activate_object(context, cut_obj, mode='EDIT')
    me = cut_obj.data
    bm = bmesh.from_edit_mesh(me)

    # # Move all vertices in the positive global z-direction
    z_move = 5*context.scene.ufit_print_thickness/1000
    z_move = 0.002
    for v in bm.verts:
        v.co.z += z_move

    # apply new coordinates
    bmesh.update_edit_mesh(me)

    bpy.ops.mesh.edge_face_add()  # add faces

    # Extrude the selected vertices in the negative global z-direction
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -0.1), "constraint_axis": (False, False, True)})

    # back to object mode for remeshing
    general.activate_object(context, cut_obj, mode='OBJECT')

    # voxel remesh object to remove material between inner and outer shell
    voxel_remesh = cut_obj.modifiers.new("Voxel Remesh", type='REMESH')
    voxel_remesh.mode = 'VOXEL'
    voxel_remesh.voxel_size = 0.001  # Set the voxel size

    # bug in blender - you have to use an override to apply the modifier
    override = {"object": cut_obj, "active_object": cut_obj}
    bpy.ops.object.modifier_apply(override, modifier="Voxel Remesh")

    return cut_obj


