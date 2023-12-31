from .....base.src.ui.base.UI_clean_up import UICleanUpScan
from ...transfemoral_constants import tf_ui_consts


class UICleanUpScanTF(UICleanUpScan):
    bl_idname = "VIEW3D_PT_tf_clean_up_scan"
    bl_label = tf_ui_consts['workflow']['clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_clean_up="tf_operators.clean_up")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'clean_up'
                and context.scene.ufit_device_type == 'transfemoral')
