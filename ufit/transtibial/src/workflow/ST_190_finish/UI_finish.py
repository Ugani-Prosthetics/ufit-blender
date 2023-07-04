from .....base.src.ui.base.UI_finish import UIFinished
from ...transtibial_constants import tt_ui_consts


class UIFinishedTT(UIFinished):
    bl_idname = "VIEW3D_PT_tt_finished"
    bl_label = tt_ui_consts['workflow']['finish']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_restart="tt_operators.restart")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'finish'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
