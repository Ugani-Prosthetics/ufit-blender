from .....base.src.ui.base.UI_clean_up import UIVerifyCleanUp
from ...transtibial_constants import tt_ui_consts


class UIVerifyCleanUpTT(UIVerifyCleanUp):
    bl_idname = "VIEW3D_PT_tt_verify_clean_up"
    bl_label = tt_ui_consts['workflow']['verify_clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_approve_clean_up="tt_operators.approve_clean_up",
                       ot_highlight_non_manifold="tt_operators.highlight_non_manifold",
                       ot_fix_non_manifold="tt_operators.fix_non_manifold",
                       ot_delete_non_manifold="tt_operators.delete_non_manifold")



    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_clean_up'
                and context.scene.ufit_device_type == 'transtibial')
