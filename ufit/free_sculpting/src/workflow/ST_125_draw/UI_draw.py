from .....base.src.ui.base.UI_draw import UIDraw
from ...free_sculpting_constants import fs_ui_consts


class UIDrawFS(UIDraw):
    bl_idname = "VIEW3D_PT_fs_draw"
    bl_label = fs_ui_consts['workflow']['draw']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_apply_draw="fs_operators.apply_draw")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'draw'
                and context.scene.ufit_device_type == 'free_sculpting')
