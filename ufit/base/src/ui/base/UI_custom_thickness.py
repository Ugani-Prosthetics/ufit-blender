import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UICustomThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_custom_thickness, ot_custom_thickness_done):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_print_thickness', text="Extra Thickness")
        box0_row1 = box0.row()
        box0_row1.operator(ot_custom_thickness, text="Apply")

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_custom_thickness_done)


class UIVerifyThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_thickness):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_thickness)
