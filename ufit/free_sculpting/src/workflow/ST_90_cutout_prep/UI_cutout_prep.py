from .....base.src.ui.base.UI_cutout import UICutoutPrep
from ...free_sculpting_constants import fs_ui_consts


class UICutoutPrepFS(UICutoutPrep):
    bl_idname = "VIEW3D_PT_fs_cutout_prep"
    bl_label = fs_ui_consts['workflow']['cutout_prep']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout_plane="fs_operators.cutout_plane")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout_prep'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'free_sculpting')
