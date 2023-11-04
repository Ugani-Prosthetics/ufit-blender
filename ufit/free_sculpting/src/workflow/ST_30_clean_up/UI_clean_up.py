from .....base.src.ui.base.UI_clean_up import UICleanUpScan
from ...free_sculpting_constants import fs_ui_consts


class UICleanUpScanFS(UICleanUpScan):
    bl_idname = "VIEW3D_PT_fs_clean_up_scan"
    bl_label = fs_ui_consts['workflow']['clean_up']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_clean_up="fs_operators.clean_up")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'clean_up'
                and context.scene.ufit_device_type == 'free_sculpting')
