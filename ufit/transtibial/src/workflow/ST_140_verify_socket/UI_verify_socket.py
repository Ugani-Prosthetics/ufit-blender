from .....base.src.ui.base.UI_thickness import UIVerifyThickness
from ...transtibial_constants import tt_ui_consts


class UIVerifySocketTT(UIVerifyThickness):
    bl_idname = "VIEW3D_PT_tt_verify_socket"
    bl_label = tt_ui_consts['workflow']['verify_socket']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_approve_thickness="tt_operators.approve_socket")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_socket'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
