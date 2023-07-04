from .....base.src.ui.base.UI_thickness import UIThickness
from ...transfemoral_constants import tf_ui_consts


class UIThicknessTF(UIThickness):
    bl_idname = "VIEW3D_PT_tf_thickness"
    bl_label = tf_ui_consts['workflow']['thickness']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_thickness="tf_operators.thickness")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'thickness'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
