import bpy
from .utils.general import UFitPanel


class UIPlatformLogin(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_platform"
    bl_label = 'uFit Platform Login'
    # bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        col = layout.row().column()

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row2 = box0.row()
        box0_row0.prop(context.scene, "ufit_user")
        box0_row1.prop(context.scene, "ufit_password")
        box0_row2.operator("ufit_operators.platform_login")

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step == 'platform_login'