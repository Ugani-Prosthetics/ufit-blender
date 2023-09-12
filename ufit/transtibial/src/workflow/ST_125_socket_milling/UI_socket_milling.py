from .....base.src.ui.base.UI_milling import UISocketMilling
from ...transtibial_constants import tt_ui_consts


class UISocketMillingTT(UISocketMilling):
    bl_idname = "VIEW3D_PT_tt_socket_milling"
    bl_label = tt_ui_consts['workflow']['socket_milling']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_socket_milling="tt_operators.socket_milling")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'socket_milling'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
