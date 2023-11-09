import bpy
from .utils.general import UFitPanel


class UIDeviceType(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_device_type"
    bl_label = 'Device Type'
    # bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        col = layout.row().column()

        row = layout.row(align=True)
        row.prop(context.scene, "ufit_device_type", text="")

        row1 = layout.row()
        row1.operator("ufit_operators.device_type", text="Next")

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step == 'device_type'
