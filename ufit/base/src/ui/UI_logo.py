import bpy
from .utils.general import UFitPanel


class UIUFitLogo(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_logo"
    bl_label = 'ufit_logo'
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        layout = self.layout
        col = layout.row().column()

        try:
            col.template_preview(bpy.data.textures['ufit_logo'])
        except Exception as e:
            print(e)
            pass  # do nothing

    @classmethod
    def poll(cls, context):
        return True
