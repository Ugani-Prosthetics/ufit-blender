import bpy
import math


# create a cylinder on the z=0 plane
def create_cylinder(radius, depth, number_of_vertices=128, location=(0,0,0.015)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
        vertices=number_of_vertices, enter_editmode=False, align='WORLD',
        location=location, scale=(1,1,1))


# resize selected geometry
def resize_selected_edges(value, orient_matrix):
    bpy.ops.transform.resize(value=value, #value=(1.0366, 1.0366, 1.0366), 
    orient_type='GLOBAL', 
    orient_matrix=orient_matrix, #((1, 0, 0), (0, 1, 0), (0, 0, 0)), 
    orient_matrix_type='GLOBAL', 
    mirror=True, use_proportional_edit=False, 
    proportional_edit_falloff='SMOOTH', 
    proportional_size=1, use_proportional_connected=False, 
    use_proportional_projected=False, 
    snap=False, snap_elements={'INCREMENT'}, 
    use_snap_project=False, snap_target='CLOSEST', 
    use_snap_self=True, use_snap_edit=True, 
    use_snap_nonedit=True, use_snap_selectable=False)


# extrude selected 
def extrude_selected_edges_co_by_z(z):
    bpy.ops.mesh.extrude_edges_move(
        MESH_OT_extrude_edges_indiv={"use_normal_flip":False, "mirror":False}, 
        TRANSFORM_OT_translate={
            "value":(0, 0, z), 
            "orient_axis_ortho":'X', 
            "orient_type":'GLOBAL', 
            "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            "orient_matrix_type":'GLOBAL', 
            "constraint_axis":(True, True, True), 
            "mirror":False, 
            "use_proportional_edit":False, 
            "proportional_edit_falloff":'SMOOTH', 
            "proportional_size":1, 
            "use_proportional_connected":False, 
            "use_proportional_projected":False, 
            "snap":False, "snap_elements":{'INCREMENT'}, 
            "use_snap_project":False, 
            "snap_target":'CLOSEST', 
            "use_snap_self":True, 
            "use_snap_edit":True, 
            "use_snap_nonedit":True, 
            "use_snap_selectable":False, 
            "snap_point":(0, 0, 0), 
            "snap_align":False, 
            "snap_normal":(0, 0, 0), 
            "gpencil_strokes":False, 
            "cursor_transform":False, 
            "texture_space":False, 
            "remove_on_cancel":False, 
            "view2d_edge_pan":False, 
            "release_confirm":False, 
            "use_accurate":False, 
            "use_automerge_and_split":False
            }
        )


def generate_socket(context, object_name, circ_interval, circ_list):
    """
    makes a socket model from circumference measurements

    Parameters:
    object_name (str): object name
    circ_interval (float): distance between consecutive circumference readings
    circ_list (List<float>): List of circumferences

    Returns:
    None
    """

    #circ_list = [438.0, 419.0, 400.0, 390.0, 390.0, 385.0, 372.0, 340.0, 240.0]
    # Add a derived circumference measure for the base of the socket at circ_interval
    # distance from the last reading keeping the same ratio of circumference difference
    # as between the last two circumferences
    circ_list.append(circ_list[-1] * (circ_list[-1] / circ_list[-2]))


    # build a list of radius from the circumference readings
    # and reverse the list because we will bould the socket from botton up
    radius_list = [circ / (2 * math.pi) for circ in circ_list]
    radius_list.reverse()
    #print(radius_list)

    # create a cylinder from the last circumference measurement
    create_cylinder(radius_list[0], circ_interval, location=(0, 0, circ_interval / 2)) #  + 0.015

    obj = context.object
    mesh = obj.data
    verts = mesh.vertices
    obj.name = object_name

    # all vertices and edges of the new mesh are selected for some reason
    # deselect them in edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action = 'DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')

    obj.select_set(False)

    # select the edges on the top face of the cylinder
    for v in verts:
        #print((obj.matrix_world  @ v.co)[2])
        if abs((obj.matrix_world  @ v.co)[2] - circ_interval) < 0.0001:
            v.select = True
        else:
            v.select = False

    # now we resize and extrude these edges for the rest of the
    # curcumference measurements
    bpy.ops.object.mode_set(mode='EDIT')
    # we only resize in x and y directions
    orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
    for i in range(1, len(radius_list)):
        resize_ratio = (radius_list[i] / radius_list[i-1])
        resize_value = (resize_ratio, resize_ratio, resize_ratio)
        resize_selected_edges(resize_value, orient_matrix)
        extrude_selected_edges_co_by_z(circ_interval)

    # delete all inner faces
    bpy.ops.mesh.select_interior_faces()
    bpy.ops.mesh.delete(type='FACE')

    # set to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
