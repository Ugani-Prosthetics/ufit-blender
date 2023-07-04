import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UITransitionConnector(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_transition_connector):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.prop(scene, 'ufit_try_perfect_print')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_transition_connector)

