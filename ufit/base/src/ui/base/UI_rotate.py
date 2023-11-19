import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIRotate(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_save_rotation, ot_mirror=None):
        layout = self.layout

        if ot_mirror:
            row0 = layout.row()
            row0.operator(ot_mirror)

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_save_rotation)
