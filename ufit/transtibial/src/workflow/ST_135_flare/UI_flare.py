from .....base.src.ui.base.UI_flare import UIFlare
from ...transtibial_constants import tt_ui_consts


class UIFlareTT(UIFlare):
    bl_idname = "VIEW3D_PT_tt_flare"
    bl_label = tt_ui_consts['workflow']['flare']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_flare="tt_operators.flare",
                       ot_flare_done="tt_operators.flare_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'flare'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
