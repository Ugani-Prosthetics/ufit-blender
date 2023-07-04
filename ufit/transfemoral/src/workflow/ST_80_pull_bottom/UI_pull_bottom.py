from .....base.src.ui.base.UI_pull_bottom import UIPullBottom
from ...transfemoral_constants import tf_ui_consts


class UIPullBottomTF(UIPullBottom):
    bl_idname = "VIEW3D_PT_tf_pull_bottom"
    bl_label = tf_ui_consts['workflow']['pull_bottom']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       "tf_operators.pull_bottom",
                       "tf_operators.pull_bottom_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'pull_bottom'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
