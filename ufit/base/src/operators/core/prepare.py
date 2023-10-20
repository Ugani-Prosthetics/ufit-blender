import bpy
from ..utils import annotations, general, user_interface
from ..utils.general import select_vertices_from_vertex_group, highlight_next_vertex_group


#########################################
# Move to center
#########################################




def prep_move_scan(context):
    # switch to annotation tool
    user_interface.activate_new_grease_pencil(context, name='Selections', layer_name='Knee')


def move_scan(context):
    # set ufit object
    ufit_obj = bpy.data.objects['uFit']

    # switch to edit mode
    general.activate_object(context, ufit_obj, mode='EDIT')

    # select single vertex based on annotations
    annotations.select_single_vert(ufit_obj, 'Selections', 'Knee')

    # move the scan to the center
    knee_vert = general.get_single_vert_co(context)
    general.set_object_origin(knee_vert)
    general.move_object(ufit_obj, -knee_vert)

    # apply location
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    # cleanup annotations
    user_interface.cleanup_grease_pencil(context)


###############################
# Clean Up
###############################
def prep_clean_up(context):
    ufit_obj = bpy.data.objects['uFit']

    # go to edit mode
    general.activate_object(context, ufit_obj, mode='EDIT')
    user_interface.set_shading_wireframe_mode()

    # activate tools
    user_interface.set_active_tool('builtin.select_circle')


def clean_up(context):
    selected_verts = general.get_selected_vertices_ix(context)
    if not len(selected_verts) > 100:  # there shoul
        raise Exception(f"Please select enough vertices. You only selected {len(selected_verts)} vertices, which is not possible in this step")

    # delete non-selected vertices
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')

    # toggle edit mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    # select all
    bpy.ops.mesh.select_all(action='SELECT')

    # remove edges with no length and faces with no area
    bpy.ops.mesh.dissolve_degenerate()

    # merge by distance to only keep relevant vertices
    bpy.ops.mesh.remove_doubles(threshold=0.001)

    # some extra clean up
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.fill_holes(sides=100)


###############################
# Verify Clean Up
###############################
def prep_verify_clean_up(context):
    ufit_obj = bpy.data.objects['uFit']
    general.activate_object(context, ufit_obj, mode='EDIT')
    non_manifold_areas = general.get_non_manifold_areas(context, ufit_obj)
    bpy.ops.object.mode_set(mode='OBJECT')

    for nma in non_manifold_areas:
        vertex_group = ufit_obj.vertex_groups.new(name=nma)
        vertex_group.add(list(non_manifold_areas[nma]), 1, 'REPLACE')

    context.scene.ufit_non_manifold_highlighted = 0

    select_vertices_from_vertex_group(context, ufit_obj,
                                      ufit_obj.vertex_groups[context.scene.ufit_non_manifold_highlighted].name)


def highlight_next_non_manifold(context):

    ufit_obj = bpy.data.objects['uFit']
    if len(ufit_obj.vertex_groups) != 0:
        highlight_next_vertex_group(context, ufit_obj)
        user_interface.focus_on_selected()


def auto_fix_non_manifold(context):

    ufit_obj = bpy.data.objects['uFit']
    if len(ufit_obj.vertex_groups) != 0:
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_remove()


def verify_clean_up(context):
    ufit_obj = bpy.data.objects['uFit']

    general.subdivide_until_vertex_count(ufit_obj, 30000)  # make sure to have more than 30000 vertices


###############################
# Rotate
###############################
def prep_rotate(context):
    # activate quad and orthographic view
    context.scene.ufit_quad_view = True
    context.scene.ufit_orthographic_view = True

    # cursor to world center and snap cursor as rotaion point, make rotation around global axis
    bpy.ops.view3d.snap_cursor_to_center()
    context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    context.scene.transform_orientation_slots[0].type = 'GLOBAL'

    # activate rotation tool
    user_interface.set_active_tool('builtin.rotate')


def save_rotation(context):
    ufit_obj = bpy.data.objects['uFit']

    # make sure the ufit object is selected
    general.apply_transform(ufit_obj, use_location=True, use_rotation=True, use_scale=True)


#################################
# Circumferences
#################################
def prep_circumferences(context):
    # reset substep
    context.scene.ufit_substep = 0


def add_circumference(context, i, z=0.0):
    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_circle_add(radius=0.2, enter_editmode=False, align='WORLD', location=(0, 0, z),
                                      scale=(1, 1, 1))

    # Fill the circle with a face
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.edge_face_add()

    # name the circumference object
    circum_obj = bpy.context.active_object
    circum_obj.name = f"Circum_{i}"

    # lock to y direction movement
    circum_obj.lock_location[0] = True
    circum_obj.lock_location[1] = True

    # add a boolean modifier to find the intersection with the ufit object
    general.activate_object(context, circum_obj, mode='OBJECT')
    boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'INTERSECT'
    boolean_mod.solver = 'FAST'
    boolean_mod.object = measure_obj

    # Set the origin to the median point of the object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

    # set the move tool
    bpy.ops.wm.tool_set_by_id(name="builtin.move")
    context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'


# you cannot immediately apply after adding circumference because the user first moves it to the correct position
def apply_circumference(context):
    z_coord = None
    circumference = None

    # ONLY APPLIES ONE AT THE TIME (for-loop breaks!)
    for obj in bpy.data.objects:
        if "Circum_" in obj.name and obj.modifiers:
            # bug in blender - you have to use an override to apply the modifier
            override = {"object": obj, "active_object": obj}
            bpy.ops.object.modifier_apply(override, modifier="Boolean")

            # get the z coord
            z_coord = obj.location.z

            # get the circumference
            general.activate_object(context, obj, mode='EDIT')
            circumference = general.get_mesh_circumference(obj)
            general.activate_object(context, obj, mode='OBJECT')

            # move the origin of the object back to the median point (origin is dislocated after boolean operator)
            # completely changes the location of the object. Perform this after storing the z-ix
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

            # scale so that the object is visible
            obj.scale = (1.01, 1.01, 1.0)

            # apply transformations (resets origin of object to center of world!)
            general.apply_transform(obj, use_location=True, use_rotation=True, use_scale=True)

            break

    return z_coord, circumference


def hide_circumferences(context):
    for obj in bpy.data.objects:
        if "Circum_" in obj.name:
            obj.hide_set(True)


def calc_circumferences(context, z_coord, circumference, distance=0.02):
    i = 0
    new_z_coord = z_coord
    new_circum = circumference
    while new_circum > 0.025:
        context.scene.ufit_circum_z_ixs[i] = new_z_coord
        context.scene.ufit_circumferences[i] = new_circum
        i += 1

        new_z_coord -= distance
        add_circumference(context, i, new_z_coord)
        new_z_coord, new_circum = apply_circumference(context)

    general.delete_obj_by_name_contains(f'Circum_{i}')  # delete the last added circum because it is too small

    # hide the circumferences
    hide_circumferences(context)


def add_other_circumferences(context):
    # apply the first circumference
    z_coord, circumference = apply_circumference(context)

    # calculate the other circumferences
    dist = float(context.scene.ufit_circums_distance)
    calc_circumferences(context, z_coord, circumference, distance=dist)

    # set the initial circumferences
    context.scene.ufit_init_circumferences = context.scene.ufit_circumferences

    # increase substep
    context.scene.ufit_substep += 1


# function called in other steps to remeasure circumferences when ufit object changed
def remeasure_circumferences(context):
    general.delete_obj_by_name_contains('Circum_')  # remove circum objects
    for i, z in enumerate(context.scene.ufit_circum_z_ixs):
        if context.scene.ufit_circumferences[i] > 0:  # only recalculate if it was calculated before
            add_circumference(context, i, z)  # remeasure circumferences
            new_z_coord, new_circum = apply_circumference(context)
            context.scene.ufit_circumferences[i] = new_circum

    # hide the circumferences
    hide_circumferences(context)


def highlight_circumferences():
    # keep looping until the context is filled after opening a new file
    if bpy.context.window is None:
        bpy.app.timers.register(highlight_circumferences, first_interval=0.1)

    # get the ufit or ufit_original object
    ufit_obj = bpy.data.objects['uFit']
    active_obj = ufit_obj
    if 'uFit_Measure' in bpy.data.objects:
        ufit_obj.hide_set(True)
        active_obj = bpy.data.objects['uFit_Measure']
        active_obj.hide_set(False)
        active_obj.hide_select = False

    # Object mode, show colors and orbit up the viewpoint to avoid frontal view
    general.activate_object(bpy.context, active_obj, mode='OBJECT')
    user_interface.change_orthographic('FRONT')
    user_interface.set_shading_solid_mode(light='FLAT', color_type='TEXTURE')
    user_interface.set_active_tool('builtin.select_box')

    # un-hide and select all Circum objects
    for obj in bpy.data.objects:
        if "Circum_" in obj.name:
            obj.hide_set(False)
            obj.hide_select = False
            obj.select_set(True)
        elif not obj == active_obj:
            obj.hide_set(True)  # hide all objects except the active object and the circumferences

    # deselect the UFit object
    active_obj.select_set(False)

    # set the property that indicates the circums are highlighted
    bpy.context.scene.ufit_circums_highlighted = True
