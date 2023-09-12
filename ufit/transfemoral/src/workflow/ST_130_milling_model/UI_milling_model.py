from .....base.src.ui.base.UI_milling import UIMillingModel
from ...transfemoral_constants import tf_ui_consts


class UIMillingModelTF(UIMillingModel):
    bl_idname = "VIEW3D_PT_tf_milling_model"
    bl_label = tf_ui_consts['workflow']['milling_model']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_milling_model="tf_operators.milling_model")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'milling_model'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
