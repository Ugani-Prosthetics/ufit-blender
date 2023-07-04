import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIPullBottom(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_pull_bottom, ot_pull_bottom_done):
        scene = context.scene
        layout = self.layout

        # box0
        box0 = layout.box()
        box0.prop(scene, 'ufit_extrude_amount')

        # box1
        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row0.operator(ot_pull_bottom)

        # separator
        layout.row().separator()

        # navigation box
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_pull_bottom_done)
