import bpy
from .utils.general import UFitPanel
from ..base_constants import base_ui_consts


class UIUFitView(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_view"
    bl_label = base_ui_consts['persistent']['view']['ui_name']
    # bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.prop(scene, 'ufit_full_screen')
        box0_row0.prop(scene, 'ufit_quad_view')
        box0_row1.prop(scene, 'ufit_orthographic_view')

    @classmethod
    def poll(cls, context):
        # return context.scene.ufit_active_step != 'start'
        return True


class UIUFitGizmo(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_gizmo"
    bl_label = base_ui_consts['persistent']['ufit_gizmo']['ui_name']

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row1 = box1.row()
        box1_row2 = box1.row()
        box2 = layout.box()
        box2_row0 = box2.row()

        box0_row0.operator('ufit_operators.ufit_gizmo', text="Top").action = 'TOP'
        box1_row0.operator('ufit_operators.ufit_gizmo', text="Front").action = 'FRONT'
        box1_row1.operator('ufit_operators.ufit_gizmo', text="Left").action = 'LEFT'
        box1_row1.operator('ufit_operators.ufit_gizmo', text="Right").action = 'RIGHT'
        box1_row2.operator('ufit_operators.ufit_gizmo', text="Back").action = 'BACK'
        box2_row0.operator('ufit_operators.ufit_gizmo', text="Bottom").action = 'BOTTOM'

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan']
