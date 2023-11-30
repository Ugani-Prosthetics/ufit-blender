import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIBorderChoice(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_border_choice):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.label(text="Would you like to add borders?")
        box0_row1.prop(scene, 'ufit_border_choice', expand=True)

        # separator
        layout.row().separator()

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_border_choice)