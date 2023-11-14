from .....base.src.ui.base.UI_push_pull_smooth import UIPushPullRegions
from ...free_sculpting_constants import fs_ui_consts


class UIPushPullRegionsFS(UIPushPullRegions):
    bl_idname = "VIEW3D_PT_fs_push_pull_regions"
    bl_label = fs_ui_consts["workflow"]["push_pull_smooth"]["ui_name"]

    def draw(self, context):
        self.draw_base(context,
                       ot_push_pull_region="fs_operators.push_pull_region",
                       ot_smooth_region="fs_operators.smooth_region",
                       ot_free_sculpt_checkpoint="fs_operators.free_sculpt_checkpoint",
                       ot_push_pull_smooth_done="fs_operators.push_pull_smooth_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'push_pull_smooth'
                and context.scene.ufit_device_type == 'free_sculpting')
