from .....base.src.ui.base.UI_custom_thickness import UICustomThickness
from ...transfemoral_constants import tf_ui_consts


class UICustomThicknessTF(UICustomThickness):
    bl_idname = "VIEW3D_PT_tf_custom_thickness"
    bl_label = tf_ui_consts['workflow']['custom_thickness']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_custom_thickness="tf_operators.custom_thickness",
                       ot_custom_thickness_done="tf_operators.custom_thickness_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'custom_thickness'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
