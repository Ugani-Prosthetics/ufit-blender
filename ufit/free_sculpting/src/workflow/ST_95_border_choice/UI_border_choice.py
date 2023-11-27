from .....base.src.ui.base.UI_border_choice import UIBorderChoice
from ...free_sculpting_constants import fs_ui_consts


class UIBorderChoiceFS(UIBorderChoice):
    bl_idname = "VIEW3D_PT_fs_border_choice"
    bl_label = fs_ui_consts['workflow']['border_choice']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_border_choice="fs_operators.border_choice")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'border_choice'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'free_sculpting')
