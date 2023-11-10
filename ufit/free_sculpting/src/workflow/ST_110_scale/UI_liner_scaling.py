from .....base.src.ui.base.UI_scale import UIScale
from ...free_sculpting_constants import fs_ui_consts


class UIScaleScanFS(UIScale):
    bl_idname = "VIEW3D_PT_fs_scale"
    bl_label = fs_ui_consts['workflow']['scale']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_scale_scan="fs_operators.liner_scale_scan")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'scale'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'free_sculpting')
