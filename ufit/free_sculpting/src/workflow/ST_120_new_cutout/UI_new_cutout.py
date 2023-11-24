from .....base.src.ui.base.UI_cutout import UINewCutout
from ...free_sculpting_constants import fs_ui_consts


class UINewCutoutFS(UINewCutout):
    bl_idname = "VIEW3D_PT_fs_new_cutout"
    bl_label = fs_ui_consts['workflow']['new_cutout']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_new_cutout="fs_operators.new_cutout",
                       ot_cutout_done="fs_operators.cutout_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'new_cutout'
                and context.scene.ufit_device_type == 'free_sculpting')
