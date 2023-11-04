from .....base.src.ui.base.UI_custom_thickness import UICustomThickness
from ...free_sculpting_constants import fs_ui_consts


class UICustomThicknessFS(UICustomThickness):
    bl_idname = "VIEW3D_PT_fs_custom_thickness"
    bl_label = fs_ui_consts['workflow']['custom_thickness']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_custom_thickness="fs_operators.custom_thickness",
                       ot_custom_thickness_done="fs_operators.custom_thickness_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'custom_thickness'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'free_sculpting')
