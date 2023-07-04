from .....base.src.ui.base.UI_cutout import UICutoutPrep
from ...transtibial_constants import tt_ui_consts


class UICutoutPrepTT(UICutoutPrep):
    bl_idname = "VIEW3D_PT_tt_cutout_prep"
    bl_label = tt_ui_consts['workflow']['cutout_prep']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_plane="tt_operators.cutout_plane")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_prep'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
