import bpy
from .utils.general import UFitPanel
from ..base_constants import base_ui_consts
from ....base.src.ui.utils.general import get_label_multiline


class UICheckpoints(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_checkpoints"
    bl_label = base_ui_consts['persistent']['checkpoints']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(context.scene, "ufit_checkpoints", text="")

        row1 = layout.row()
        row1.operator("ufit_operators.checkpoint_rollback")

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan']


class UIAssistance(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_assistance"
    bl_label = base_ui_consts['persistent']['assistance']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        if context.scene.ufit_assistance_previews_dir:
            col = layout.row().column()
            try:
                col.template_icon_view(context.scene, "ufit_assistance_previews", scale=10, scale_popup=5)
            except Exception as e:
                pass  # do nothing

        box0 = layout.box()
        get_label_multiline(
            context=context,
            text=context.scene.ufit_help_text,
            parent=box0
        )

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan', 'finish']


class UIProgress(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_progress"
    bl_label = base_ui_consts['persistent']['progress']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}
    # bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, "ufit_progress")

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan'] \
               and not context.scene.ufit_circums_highlighted
