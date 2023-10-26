from .....base.src.ui.base.UI_clean_up import UIVerifyCleanUp
from ...transfemoral_constants import tf_ui_consts


class UIVerifyCleanUpTF(UIVerifyCleanUp):
    bl_idname = "VIEW3D_PT_tf_verify_clean_up"
    bl_label = tf_ui_consts['workflow']['verify_clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_highlight_non_manifold="tf_operators.highlight_non_manifold",
                       ot_fill_non_manifold="tf_operators.fill_non_manifold",
                       ot_delete_non_manifold="tf_operators.delete_non_manifold",
                       ot_approve_clean_up="tf_operators.approve_clean_up")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_clean_up'
                and context.scene.ufit_device_type == 'transfemoral')
