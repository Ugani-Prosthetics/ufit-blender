from .....base.src.ui.base.UI_cutout import UICutoutSelection
from ...transtibial_constants import tt_ui_consts


class UICutoutSelectionTT(UICutoutSelection):
    bl_idname = "VIEW3D_PT_tt_cutout_selection"
    bl_label = tt_ui_consts['workflow']['cutout_selection']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_selection="tt_operators.cutout_selection")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_selection'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
