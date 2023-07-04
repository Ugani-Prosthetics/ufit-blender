from .....base.src.ui.base.UI_start import UIStartModeling
from ...transtibial_constants import tt_ui_consts


class UIStartModelingTT(UIStartModeling):
    bl_idname = "VIEW3D_PT_tt_start_modeling"
    bl_label = tt_ui_consts['workflow']['start']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_start="tt_operators.start_modeling",
                       ot_start_from_existing="tt_operators.start_from_existing")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'start'
                and context.scene.ufit_device_type == 'transtibial')
