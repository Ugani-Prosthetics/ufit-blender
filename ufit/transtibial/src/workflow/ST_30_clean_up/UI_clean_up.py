from .....base.src.ui.base.UI_clean_up import UICleanUpScan
from ...transtibial_constants import tt_ui_consts


class UICleanUpScanTT(UICleanUpScan):
    bl_idname = "VIEW3D_PT_tt_clean_up_scan"
    bl_label = tt_ui_consts['workflow']['clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_clean_up="tt_operators.clean_up")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'clean_up'
                and context.scene.ufit_device_type == 'transtibial')
