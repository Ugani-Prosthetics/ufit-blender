from .....base.src.ui.base.UI_finish import UIFinished
from ...free_sculpting_constants import fs_ui_consts


class UIFinishedFS(UIFinished):
    bl_idname = "VIEW3D_PT_fs_finished"
    bl_label = fs_ui_consts['workflow']['finish']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_restart="fs_operators.restart")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'finish'
                and context.scene.ufit_device_type == 'free_sculpting')
