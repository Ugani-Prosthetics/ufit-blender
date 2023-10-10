from .....base.src.ui.base.UI_push_pull_smooth import UIPushPullRegions
from ...transtibial_constants import tt_ui_consts


class UIPushPullRegionsTT(UIPushPullRegions):
    bl_idname = "VIEW3D_PT_tt_push_pull_regions"
    bl_label = tt_ui_consts["workflow"]["push_pull_smooth"]["ui_name"]

    def draw(self, context):
        self.draw_base(context,
                       ot_push_pull_region="tt_operators.push_pull_region",
                       ot_smooth_region="tt_operators.smooth_region",
                       ot_free_sculpt_checkpoint="tt_operators.free_sculpt_checkpoint",
                       ot_push_pull_smooth_done="tt_operators.push_pull_smooth_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'push_pull_smooth'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
