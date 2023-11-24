import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIDraw(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_apply_draw):
        layout = self.layout
        scene = context.scene

        row0 = layout.row()
        row0.prop(scene.tool_settings.unified_paint_settings, 'size')

        row1 = layout.row()
        row1.prop(scene, 'ufit_draw_thickness')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_apply_draw)
