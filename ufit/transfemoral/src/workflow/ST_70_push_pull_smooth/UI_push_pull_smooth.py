from .....base.src.ui.base.UI_push_pull_smooth import UIPushPullRegions, UISmoothRegions
from ...transfemoral_constants import tf_ui_consts


class UIPushPullRegionsTF(UIPushPullRegions):
    bl_idname = "VIEW3D_PT_tf_push_pull_regions"
    bl_label = tf_ui_consts['workflow']['push_pull_smooth']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_push_pull_region="tf_operators.push_pull_region",
                       ot_push_pull_smooth_done="tf_operators.push_pull_smooth_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'push_pull_smooth'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')


class UISmoothRegionsTF(UISmoothRegions):
    bl_idname = "VIEW3D_PT_tf_smooth_regions"
    bl_label = "Smooth"

    def draw(self, context):
        self.draw_base(context,
                       ot_smooth_region="tf_operators.smooth_region")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'push_pull_smooth'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
