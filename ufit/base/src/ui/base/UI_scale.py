import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIScale(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_scale_scan):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.prop(scene, 'ufit_scaling_unit', expand=True)
        box0_row1.prop(scene, 'ufit_liner_scaling')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_scale_scan)


class UIVerifyScaling(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_scaling):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_show_prescale')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_scaling)


