from .....base.src.ui.base.UI_connector import UITransitionConnector
from ...transfemoral_constants import tf_ui_consts
from .....base.src.ui.utils.general import get_standard_navbox


class UITransitionConnectorTF(UITransitionConnector):
    bl_idname = "VIEW3D_PT_tf_transition_connector"
    bl_label = tf_ui_consts['workflow']['transition']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_transition_connector="tf_operators.transition_connector")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'transition'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
