from .....base.src.ui.base.UI_scale import UIVerifyScaling
from ...transfemoral_constants import tf_ui_consts


class UIVerifyScalingTF(UIVerifyScaling):
    bl_idname = "VIEW3D_PT_tf_verify_scaling"
    bl_label = tf_ui_consts['workflow']['verify_scaling']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_approve_scaling="tf_operators.approve_scaling")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_scaling'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
