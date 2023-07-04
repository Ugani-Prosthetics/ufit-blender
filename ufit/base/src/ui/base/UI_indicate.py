import bpy
from .....base.src.ui.utils.general import UFitPanel


class UIIndicate(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_move_scan):
        object = context.active_object
        layout = self.layout

        row0 = layout.row()
        row0.operator(ot_move_scan, text="Next")
