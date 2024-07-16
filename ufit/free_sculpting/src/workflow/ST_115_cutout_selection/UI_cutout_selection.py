from .....base.src.ui.base.UI_cutout import UICutoutSelection
from ...free_sculpting_constants import fs_ui_consts


class UICutoutSelectionFS(UICutoutSelection):
    bl_idname = "VIEW3D_PT_fs_cutout_selection"
    bl_label = fs_ui_consts['workflow']['cutout_selection']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_selection="fs_operators.cutout_selection")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_selection'
                and context.scene.ufit_device_type == 'free_sculpting')
