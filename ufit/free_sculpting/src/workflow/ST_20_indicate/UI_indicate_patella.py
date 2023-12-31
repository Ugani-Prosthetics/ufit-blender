from .....base.src.ui.base.UI_indicate import UIIndicate
from ...free_sculpting_constants import fs_ui_consts


class UIMoveScanFS(UIIndicate):
    bl_idname = "VIEW3D_PT_fs_move_scan"
    bl_label = fs_ui_consts['workflow']['indicate']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_move_scan="fs_operators.move_scan")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'indicate'
                and context.scene.ufit_device_type == 'free_sculpting')
