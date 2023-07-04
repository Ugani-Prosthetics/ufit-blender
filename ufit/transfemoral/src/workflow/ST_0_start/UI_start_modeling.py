from .....base.src.ui.base.UI_start import UIStartModeling
from ...transfemoral_constants import tf_ui_consts


class UIStartModelingTF(UIStartModeling):
    bl_idname = "VIEW3D_PT_tf_start_modeling"
    bl_label = tf_ui_consts['workflow']['start']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_start="tf_operators.start_modeling",
                       ot_start_from_existing="tf_operators.start_from_existing")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'start'
                and context.scene.ufit_device_type == 'transfemoral')
