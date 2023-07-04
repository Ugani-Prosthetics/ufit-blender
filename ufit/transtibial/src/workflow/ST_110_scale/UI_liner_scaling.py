from .....base.src.ui.base.UI_scale import UIScale
from ...transtibial_constants import tt_ui_consts


class UIScaleScanTT(UIScale):
    bl_idname = "VIEW3D_PT_tt_scale"
    bl_label = tt_ui_consts['workflow']['scale']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_scale_scan="tt_operators.liner_scale_scan")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'scale'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
