from .....base.src.ui.base.UI_carve import UISocketCarve
from ...transtibial_constants import tt_ui_consts


class UISocketCarveTT(UISocketCarve):
    bl_idname = "VIEW3D_PT_tt_socket_carve"
    bl_label = tt_ui_consts['workflow']['socket_carve']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_socket_carve="tt_operators.socket_carve")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'socket_carve'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
