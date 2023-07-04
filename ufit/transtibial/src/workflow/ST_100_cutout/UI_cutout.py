from .....base.src.ui.base.UI_cutout import UICutout
from ...transtibial_constants import tt_ui_consts


class UICutoutTT(UICutout):
    bl_idname = "VIEW3D_PT_tt_cutout_plane"
    bl_label = tt_ui_consts['workflow']['cutout']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout="tt_operators.cutout")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
