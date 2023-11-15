from .....base.src.ui.base.UI_cutout import UICutout
from ...free_sculpting_constants import fs_ui_consts


class UICutoutFS(UICutout):
    bl_idname = "VIEW3D_PT_fs_cutout_plane"
    bl_label = fs_ui_consts['workflow']['cutout']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_cutout="fs_operators.cutout")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'cutout'
                and context.scene.ufit_device_type == 'free_sculpting')
