import os
import bpy
import math
import addon_utils
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
from bl_ui.space_toolsystem_toolbar import VIEW3D_PT_tools_active, ToolDef, _defs_sculpt
from .....config_ufit import logger


def enable_addon(addon_module_name):
    loaded_defaults, loaded_state = addon_utils.check(addon_module_name)
    if not loaded_state:
        addon_utils.enable(addon_module_name, default_set=True)


def get_addon_version(addon_module_name):
    for mod in addon_utils.modules():
        if mod.bl_info.get('name') == addon_module_name:
            version = mod.bl_info.get('version')
            if version:
                return f'{version[0]}.{version[1]}.{version[2]}'

    return None


def set_theme_vertex_size(size):
    bpy.context.preferences.themes['Default'].view_3d.vertex_size = size


def set_theme_vertex_colour(r, g, b):
    c = bpy.context.preferences.themes['Default'].view_3d.vertex
    c.r = r
    c.g = g
    c.b = b


def set_input_preference(pref_name, pref_value):
    """
    Set the value of an input preference property dynamically (bpy.types.PreferencesInput).
    Args:
        pref_name (str): Name of the input preference property.
        pref_value: Value to set for the input preference property.
    """
    # Access the input preferences
    input_prefs = bpy.context.preferences.inputs
    # Check if the specified property exists in the input preferences
    if hasattr(input_prefs, pref_name):
        # Set the value of the specified property
        setattr(input_prefs, pref_name, pref_value)
    else:
        logger.debug(f"Input preference '{pref_name}' does not exist.")


def set_outliner_restriction(restr_name, restr_val):
    # Fetch the first outliner area in the screen
    # Will throw error if workspace doesn't contain any outliner editor.
    for a in bpy.context.screen.areas:
        if a.type == "OUTLINER":
            space = a.spaces[0]

            if hasattr(space, restr_name):
                setattr(space, restr_name, restr_val)
            else:
                logger.debug(f"Ouliner restriction '{restr_name}' does not exist.")

            break


def keep_workspaces(workspaces):
    for ws in bpy.data.workspaces:
        if ws.name not in workspaces:
            bpy.ops.workspace.delete({"workspace": ws})


def delete_tools(workspace, tool_ids, space_type='VIEW_3D', context_mode='EDIT'):
    bpy.context.window.workspace = bpy.data.workspaces[workspace]
    cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
    tools = cls._tools[context_mode]

    for idname in tool_ids:
        for i, tool_group in enumerate(tools):
            if tool_group:
                if all(isinstance(x, tuple) for x in tool_group):
                    tools[i] = tuple(x for x in tool_group if x.idname != idname)
                    if not tools[i]:  # all items from tool_group were removed
                        del tools[i]  # delete i
                else:
                    if tool_group.idname == idname:
                        del tools[i:i + 2]  # delete i and i+1


# todo: fix function - not working
def delete_brushes(workspace, brush_ids, space_type='VIEW_3D', context_mode='SCULPT'):
    bpy.context.window.workspace = bpy.data.workspaces[workspace]

    # Get all tooldefs for builtin brushes
    brushes = list(_defs_sculpt.generate_from_brushes(bpy.context))
    for idname in brush_ids:
        for i, brush in enumerate(brushes):
            if callable(brush):
                pass  #
            elif brush.idname == idname:
                del brush


def set_active_tool(tool_name):
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            override = bpy.context.copy()
            override["space_data"] = area.spaces[0]
            override["area"] = area
            bpy.ops.wm.tool_set_by_id(override, name=tool_name)


def get_space(space_type='VIEW_3D', screens=None):
    """
    Performs an action analogous to clicking on the display/shade button of
    the 3D view. Mode is one of "RENDERED", "MATERIAL", "SOLID", "WIREFRAME".
    The change is applied to the given collection of bpy.data.screens.
    If none is given, the function is applied to bpy.context.screen (the
    active screen) only. E.g. set all screens to rendered mode:
      set_shading_mode("RENDERED", bpy.data.screens)
    """
    screens = screens or [bpy.context.screen]
    for s in screens:
        for spc in s.areas:
            if spc.type == space_type:
                return spc.spaces[0] # we expect at most 1 VIEW_3D space


def set_shading_solid_mode(light='STUDIO', color_type='MATERIAL'):
    spc = get_space('VIEW_3D')
    spc.shading.type = 'SOLID'
    spc.shading.light = light
    spc.shading.color_type = color_type


def set_shading_wireframe_mode():
    spc = get_space('VIEW_3D')
    spc.shading.type = 'WIREFRAME'


def set_shading_material_preview_mode():
    spc = get_space('VIEW_3D')
    spc.shading.type = 'MATERIAL'


def set_xray(turn_on=True, screens=None, alpha=0.5):
    screens = screens or [bpy.context.screen]
    for s in screens:
        for spc in s.areas:
            if spc.type == "VIEW_3D":
                spc.spaces[0].shading.show_xray = turn_on
                spc.spaces[0].shading.xray_alpha = alpha
                break  # we expect at most 1 VIEW_3D space


def get_area_override(area_type='VIEW_3D'):
    override = None
    for area in bpy.context.screen.areas:
        if area.type == area_type:
            # override = bpy.context.copy()
            # override['area'] = area
            override = {
                'window': bpy.context.window,
                'screen': bpy.context.window.screen,
                'area': area,
                'region': [region for region in area.regions if region.type == 'WINDOW'][0],
            }

            break

    if not override:
        raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

    return override


def get_space_data(area_type='VIEW_3D'):
    space_data = None
    for area in bpy.context.screen.areas:
        if area.type == area_type:
            for space in area.spaces:
                if space.type == area_type:
                    space_data = space
                    break

    return space_data


def focus_on_selected():
    # then switch the orthographic
    override = get_area_override(area_type='VIEW_3D')
    bpy.ops.view3d.view_selected(override)


def change_orthographic(orthographic):
    # then switch the orthographic
    override = get_area_override(area_type='VIEW_3D')
    bpy.ops.view3d.view_axis(override, type=orthographic)


def change_view_orbit(angle_degrees, type='ORBITUP'):
    # then switch the orthographic
    override = get_area_override(area_type='VIEW_3D')
    bpy.ops.view3d.view_orbit(override, angle=math.radians(angle_degrees), type=type)


# reference: https://blender.stackexchange.com/questions/119407/failed-to-find-grease-pencil-data-to-draw-into-when-using-bpy-ops-gpencil-dra
def activate_new_grease_pencil(context, name, layer_name, thickness=10, color=(0.0325735, 0.78, 0.0565021)):
    set_active_tool('builtin.annotate')
    bpy.context.scene.tool_settings.annotation_stroke_placement_view3d = 'SURFACE'

    # add grease pencil to the scene
    scene = context.scene
    gp = scene.grease_pencil
    if gp:
        gp.clear()  # delete all layers
        gp.name = name
    else:
        gp = bpy.data.grease_pencils.new(name)
        scene.grease_pencil = gp

    # Reference grease pencil layer or create one of none exists
    gp.layers.new(layer_name, set_active=True)

    # set color and thickness
    bpy.data.grease_pencils[name].layers[layer_name].color = color
    bpy.data.grease_pencils[name].layers[layer_name].thickness = thickness
    bpy.data.grease_pencils[name].layers[layer_name].show_in_front = False


def cleanup_grease_pencil(context):
    scene = context.scene
    gp = scene.grease_pencil
    if gp:
        gp.clear()  # delete all layers


def set_full_screen(show_fs):
    override = get_area_override('VIEW_3D')
    to_full_screen = True

    # set default values for no-full screen (part of workaround)
    bpy.ops.wm.context_set_value(data_path="space_data.overlay.show_text", value='True')
    bpy.ops.wm.context_set_value(data_path="space_data.show_gizmo_navigate", value='True')

    # bug in blender: not possible to know if current situation is full screen or not
    with bpy.context.temp_override(**override):
        bpy.ops.screen.screen_full_area(use_hide_panels=True)  # hide the sidebar and the toolbar

        # workaround for bug
        if isinstance(bpy.context.space_data, bpy.types.SpaceView3D):
            # from no full screen to full screen
            # bpy.ops.wm.context_set_value(data_path="space_data.show_region_toolbar", value='False')  # toolbar (default off)
            bpy.ops.wm.context_set_value(data_path="space_data.show_region_ui", value='True')  # sidebar
            bpy.ops.wm.context_set_value(data_path="space_data.show_gizmo_navigate", value='False')  # gizmo
            # bpy.ops.wm.context_set_value(data_path="space_data.overlay.show_text", value='False')  # text info

        if isinstance(bpy.context.space_data, bpy.types.SpaceProperties):  # for some reason it switches to the properties space
            # from full screen to no full screen
            to_full_screen = False

    if (show_fs and not to_full_screen) or (not show_fs and to_full_screen):
        set_full_screen(show_fs)  # re-execute function


def set_quad_view(show_qv):
    quad_view_active = False
    override = get_area_override('VIEW_3D')

    if len(override['area'].spaces[0].region_quadviews) == 4:
        quad_view_active = True

    if (quad_view_active and not show_qv) or (not quad_view_active and show_qv):
        with bpy.context.temp_override(**override):
            bpy.ops.screen.region_quadview()  # toggle


def set_ortho_view(activate_ortho):
    space_data = get_space_data('VIEW_3D')

    if space_data:
        if space_data.region_3d.is_perspective and activate_ortho:
            space_data.region_3d.view_perspective = 'ORTHO'
        elif not space_data.region_3d.is_perspective and not activate_ortho:
            space_data.region_3d.view_perspective = 'PERSP'
    else:
        raise Exception('Could not find VIEW_3D space data.')


def enum_previews_from_directory_items(context, pcoll, directory):
    enum_items = []

    if context is None:
        return enum_items

    # check if the directory was changed
    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews

    # change in directory - load new items
    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews

