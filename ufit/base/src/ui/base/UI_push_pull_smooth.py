import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIPushPullRegions(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_push_pull_region, ot_push_pull_smooth_done):
        scene = context.scene
        layout = self.layout

        # box 1
        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row0.prop(scene, 'ufit_push_pull_circular')

        # box2
        box2 = layout.box()
        box2.prop(scene, 'ufit_extrude_amount')

        # box3
        box3 = layout.box()
        box3_row0 = box3.row()
        push_ot = box3_row0.operator(ot_push_pull_region, text='Push')
        push_ot.direction = 'Push'  # pass property value to operator
        pull_ot = box3_row0.operator(ot_push_pull_region, text='Pull')
        pull_ot.direction = 'Pull'  # pass property value to operator

        # separator
        layout.row().separator()

        # navigation box
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_push_pull_smooth_done)


class UISmoothRegions(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_smooth_region):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box1 = layout.box()

        box0_row0.prop(scene, 'ufit_preview_extrusions')
        box0_row1.prop(scene, 'ufit_smooth_factor')
        box1.operator(ot_smooth_region)
