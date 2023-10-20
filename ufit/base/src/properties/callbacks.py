import os
import bpy
import math
import bpy.utils.previews
from ..operators.utils import general, user_interface
from ..operators.core import checkpoints


# We can store multiple preview collections here,
preview_collections = {}


#################################
# Callbacks
#################################
def full_screen(self, context):
    user_interface.set_full_screen(self.ufit_full_screen)
    # bpy.ops.wm.window_fullscreen_toggle()


def quad_view(self, context):
    user_interface.set_quad_view(self.ufit_quad_view)


def orthographic_view(self, context):
    user_interface.set_ortho_view(self.ufit_orthographic_view)


# function that dynamically sets the ufit_checkpoints enum
def checkpoint_items(self, context):
    enum_items = []
    for checkpoint in context.scene.ufit_checkpoint_collection:
        name = str(checkpoint.name)
        item = (name, name, name)
        enum_items.append(item)

    return enum_items


def show_prescale_update(self, context):
    obj = bpy.data.objects['uFit_Prescale']
    if self.ufit_show_prescale:
        obj.hide_set(False)
    else:
        obj.hide_set(True)


def show_original_update(self, context):
    ufit_original = bpy.data.objects['uFit_Original']
    if self.ufit_show_original:
        ufit_original.hide_set(False)
    else:
        ufit_original.hide_set(True)


def twist_method_update(self, context):
    ufit_cutout = bpy.data.curves['uFit_Cutout']
    ufit_cutout.twist_mode = self.ufit_twist_method


def update_colors_enable(self, context):
    if self.ufit_enable_colors:
        user_interface.set_shading_material_preview_mode()
    else:
        user_interface.set_shading_solid_mode(light='STUDIO', color_type='MATERIAL')


def sculpt_mode_update(self, context):
    if self.ufit_sculpt_mode == 'guided':
        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        context.scene.tool_settings.unified_paint_settings.size = 30
    else:
        bpy.ops.object.mode_set(mode='SCULPT')
        context.scene.ufit_sculpt_brush = self.ufit_sculpt_brush  # trigger the sculpt_brush_update_function
        checkpoints.fill_history_with_null_operations()  # fill the history with null operations so that the user cannot switch back to vertex paint mode using crtl-z


def sculpt_brush_update(self, context):
    if self.ufit_sculpt_brush == 'push_brush':
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")
        bpy.data.brushes["SculptDraw"].direction = 'SUBTRACT'
    elif self.ufit_sculpt_brush == 'pull_brush':
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Draw")
        bpy.data.brushes["SculptDraw"].direction = 'ADD'
    elif self.ufit_sculpt_brush == 'smooth_brush':
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Smooth")
        bpy.data.brushes["Smooth"].direction = 'SMOOTH'
    elif self.ufit_sculpt_brush == 'flatten_brush':
        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Flatten")
        bpy.data.brushes["Flatten/Contrast"].direction = 'FLATTEN'


def flare_tool_update(self, context):
    # (re)select vertices from cutout edge
    # when the user switches tool, it can be used as a reset to reselect the edge
    ufit_obj = bpy.data.objects['uFit']
    general.select_vertices_from_vertex_groups(context, ufit_obj, vg_names=['cutout_edge'])

    user_interface.set_active_tool(self.ufit_flare_tool)


def get_flare_height(self):
    return bpy.context.tool_settings.proportional_size*100


def set_flare_height(self, value):
    bpy.context.tool_settings.proportional_size = value/100
    self["flare_height"] = value


def xray_update(self, context):
    user_interface.set_xray(context.scene.ufit_x_ray)


def show_connector_update(self, context):
    conn_obj = bpy.data.objects['Connector']
    conn_obj.hide_set(not context.scene.ufit_show_connector)


def alignment_tool_update(self, context):
    user_interface.set_active_tool(self.ufit_alignment_tool)


def alignment_object_update(self, context):
    # unhide connector
    if self.ufit_alignment_object == 'Connector':
        context.scene.ufit_show_connector = True
        context.scene.ufit_alignment_tool = 'builtin.move'

    # activate object
    obj = bpy.data.objects[self.ufit_alignment_object]
    general.activate_object(context, obj, 'OBJECT')


def show_inner_part_update(self, context):
    # only hide the uFit object so that the inner part becomes visible
    ufit_obj = bpy.data.objects['uFit']
    ufit_obj.hide_set(context.scene.ufit_show_inner_part)

    # also hide ufit_original
    context.scene.ufit_show_original = False

    # ufit_inner_obj = bpy.data.objects['uFit_Inner']
    # ufit_inner_obj.hide_set(not context.scene.ufit_show_inner_part)


# # function is directly called from operator as callback
# def rotation_update(self, context):
#     objs = [obj for obj in bpy.data.objects if obj.name.startswith("uFit")]
#     ufit_circum_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Circum_")]
#
#     objs.extend(ufit_circum_objects)
#
#     for obj in objs:
#         obj.rotation_euler.x = math.radians(context.scene.ufit_x_rotation)
#         obj.rotation_euler.y = math.radians(context.scene.ufit_y_rotation)
#         obj.rotation_euler.z = math.radians(context.scene.ufit_z_rotation)
#
#
# def move_update(self, context):
#     objs = [obj for obj in bpy.data.objects if obj.name.startswith("uFit")]
#     ufit_circum_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Circum_")]
#
#     objs.extend(ufit_circum_objects)
#
#     default_z_loc = bpy.context.scene.bl_rna.properties['ufit_z_move'].default
#     for obj in objs:
#         obj.location.x = context.scene.ufit_x_move / 100
#         obj.location.y = -context.scene.ufit_y_move / 100
#         obj.location.z = context.scene.ufit_z_move / 100


# def connector_move_update(self, context):
#     conn_obj = bpy.data.objects['Connector']
#     conn_obj.location.z = context.scene.ufit_connector_move / 100


def enum_previews_for_assistance(self, context):
    if context.scene.ufit_assistance_previews_dir:
        # Get the preview collection, create new if not exists.
        pcoll = preview_collections.get('assistance')
        if not pcoll:
            pcoll = bpy.utils.previews.new()
            pcoll.my_previews_dir = ""
            pcoll.my_previews = ()
            preview_collections['assistance'] = pcoll

        enum_previews = user_interface.enum_previews_from_directory_items(context, pcoll,
                                                                          context.scene.ufit_assistance_previews_dir)

        return enum_previews

    return []
