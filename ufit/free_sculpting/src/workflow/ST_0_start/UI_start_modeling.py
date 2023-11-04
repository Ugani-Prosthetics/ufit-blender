from .....base.src.ui.base.UI_start import UIStartModeling
from ...free_sculpting_constants import fs_ui_consts


class UIStartModelingFS(UIStartModeling):
    bl_idname = "VIEW3D_PT_fs_start_modeling"
    bl_label = fs_ui_consts['workflow']['start']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_start="fs_operators.start_modeling",
                       ot_start_from_existing="fs_operators.start_from_existing")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'start'
                and context.scene.ufit_device_type == 'free_sculpting')
