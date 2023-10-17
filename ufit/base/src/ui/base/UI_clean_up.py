import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UICleanUpScan(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_clean_up):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_clean_up)


class UIVerifyCleanUp(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_clean_up, ot_highlight_non_manifold):
        scene = context.scene
        layout = self.layout

        # box0
        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.operator(ot_highlight_non_manifold, text="Highlight NonManifold")

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_clean_up)
