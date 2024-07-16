import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UISocketMilling(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_socket_milling):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.label(text="3D Printing or CNC Milling?")
        box0_row1.prop(scene, 'ufit_socket_or_milling', expand=True)

        # separator
        layout.row().separator()

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_socket_milling)


class UIMillingModel(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_milling_model):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.prop(scene, 'ufit_milling_flare')
        box0_row1.prop(scene, 'ufit_milling_margin', expand=True)

        # separator
        layout.row().separator()

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_milling_model)
