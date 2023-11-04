from .....base.src.ui.base.UI_clean_up import UIVerifyCleanUp
from ...free_sculpting_constants import fs_ui_consts


class UIVerifyCleanUpFS(UIVerifyCleanUp):
    bl_idname = "VIEW3D_PT_fs_verify_clean_up"
    bl_label = fs_ui_consts['workflow']['verify_clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_highlight_non_manifold="fs_operators.highlight_non_manifold",
                       ot_fill_non_manifold="fs_operators.fill_non_manifold",
                       ot_delete_non_manifold="fs_operators.delete_non_manifold",
                       ot_approve_clean_up="fs_operators.approve_clean_up")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'verify_clean_up'
                and context.scene.ufit_device_type == 'free_sculpting')
