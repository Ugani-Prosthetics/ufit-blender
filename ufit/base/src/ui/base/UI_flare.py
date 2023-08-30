import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIFlare(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_flare, ot_flare_done):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_flare_tool', expand=True)

        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row0.prop(scene, 'ufit_flare_height')

        if context.scene.ufit_flare_tool == 'builtin.select_box':  # input mode
            box1_row1 = box1.row()
            box1_row1.prop(scene, 'ufit_flare_percentage')

            # box3
            box2 = layout.box()
            box2_row0 = box2.row()
            box2_row0.operator(ot_flare, text='Apply Flare')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_flare_done)
