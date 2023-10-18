from .....base.src.ui.base.UI_flare import UIFlare
from ...transfemoral_constants import tf_ui_consts


class UIFlareTF(UIFlare):
    bl_idname = "VIEW3D_PT_tf_flare"
    bl_label = tf_ui_consts['workflow']['flare']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_flare="tf_operators.flare",
                       ot_flare_done="tf_operators.flare_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'flare'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
