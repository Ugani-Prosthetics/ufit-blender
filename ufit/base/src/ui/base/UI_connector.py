import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UITransitionConnector(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_transition_connector):
        scene = context.scene
        layout = self.layout

        # todo: activate try perfect print again.
        # box0 = layout.box()
        # box0_row0 = box0.row()
        # box0_row0.prop(scene, 'ufit_try_perfect_print')

        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row0.prop(scene, 'ufit_total_contact_socket')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_transition_connector)

