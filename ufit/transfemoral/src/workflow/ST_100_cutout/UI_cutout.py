from .....base.src.ui.base.UI_cutout import UICutout
from ...transfemoral_constants import tf_ui_consts


class UICutoutTF(UICutout):
    bl_idname = "VIEW3D_PT_tf_cutout_plane"
    bl_label = tf_ui_consts['workflow']['cutout']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout="tf_operators.cutout")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')