import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIRotate(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_save_rotation):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_save_rotation)
