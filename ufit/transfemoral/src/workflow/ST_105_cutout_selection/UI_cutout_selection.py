from .....base.src.ui.base.UI_cutout import UICutoutSelection
from ...transfemoral_constants import tf_ui_consts


class UICutoutSelectionTF(UICutoutSelection):
    bl_idname = "VIEW3D_PT_tf_cutout_selection"
    bl_label = tf_ui_consts['workflow']['cutout_selection']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_selection="tf_operators.cutout_selection")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_selection'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
