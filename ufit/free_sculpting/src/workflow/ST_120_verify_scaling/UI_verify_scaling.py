from .....base.src.ui.base.UI_scale import UIVerifyScaling
from ...free_sculpting_constants import fs_ui_consts


class UIVerifyScalingFS(UIVerifyScaling):
    bl_idname = "VIEW3D_PT_fs_verify_scaling"
    bl_label = fs_ui_consts['workflow']['verify_scaling']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_approve_scaling="fs_operators.approve_scaling")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_scaling'
                and context.scene.ufit_device_type == 'free_sculpting')
