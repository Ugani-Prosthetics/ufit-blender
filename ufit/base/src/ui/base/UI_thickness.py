import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_thickness):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_print_thickness')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_thickness)


class UIVerifyThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_thickness):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_thickness)
