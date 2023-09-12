from .....base.src.ui.base.UI_milling import UISocketMilling
from ...transfemoral_constants import tf_ui_consts


class UISocketMillingTF(UISocketMilling):
    bl_idname = "VIEW3D_PT_tf_socket_milling"
    bl_label = tf_ui_consts['workflow']['socket_milling']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_socket_milling="tf_operators.socket_milling")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'socket_milling'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
