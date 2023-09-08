import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UISocketCarve(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_socket_carve):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.label(text="Full socket or carve model?")
        box0_row1.prop(scene, 'ufit_socket_or_carve', expand=True)

        # separator
        layout.row().separator()

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_socket_carve)


class UICarveModel(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_carve_model):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        # box0 = layout.box()
        # box0_row0 = box0.row()
        # box0_row1 = box0.row()
        # box0_row0.label(text="Full socket or carve model?")
        # box0_row1.prop(scene, 'ufit_socket_or_carve', expand=True)

        # separator
        layout.row().separator()

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_carve_model)
