from .....base.src.ui.base.UI_thickness import UIThickness
from ...free_sculpting_constants import fs_ui_consts


class UIThicknessFS(UIThickness):
    bl_idname = "VIEW3D_PT_fs_thickness"
    bl_label = fs_ui_consts['workflow']['thickness']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_thickness="fs_operators.thickness")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'thickness'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'free_sculpting')
