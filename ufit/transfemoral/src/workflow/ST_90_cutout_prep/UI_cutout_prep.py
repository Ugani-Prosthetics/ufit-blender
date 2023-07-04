from .....base.src.ui.base.UI_cutout import UICutoutPrep
from ...transfemoral_constants import tf_ui_consts


class UICutoutPrepTF(UICutoutPrep):
    bl_idname = "VIEW3D_PT_tf_cutout_prep"
    bl_label = tf_ui_consts['workflow']['cutout_prep']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_plane="tf_operators.cutout_plane")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_prep'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
