import bpy
from .utils.general import UFitPanel
from ....base.src.operators.utils.user_interface import get_addon_version


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

        ufit_version = get_addon_version('uFit')
        if ufit_version:
            row = layout.row()
            row.alignment = 'CENTER'
            row.label(text=f'Version: {ufit_version}')

        device_type = bpy.context.scene.bl_rna.properties['ufit_device_type'].enum_items[context.scene.ufit_device_type].name
        if context.scene.ufit_active_step not in ['platform_login', 'device_type']:
            row = layout.row()
            row.alignment = 'CENTER'
            row.label(text=f'{device_type}', icon='HAND')

    @classmethod
    def poll(cls, context):
        return True
