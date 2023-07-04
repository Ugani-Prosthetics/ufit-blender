from .....base.src.ui.base.UI_finish import UIFinished
from ...transfemoral_constants import tf_ui_consts


class UIFinishedTF(UIFinished):
    bl_idname = "VIEW3D_PT_tf_finished"
    bl_label = tf_ui_consts['workflow']['finish']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_restart="tf_operators.restart")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'finish'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
