from .....base.src.ui.base.UI_carve import UICarveModel
from ...transfemoral_constants import tf_ui_consts


class UICarveModelTF(UICarveModel):
    bl_idname = "VIEW3D_PT_tf_carve_model"
    bl_label = tf_ui_consts['workflow']['carve_model']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_carve_model="tf_operators.carve_model")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'carve_model'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
