import bpy
from .....base.src.ui.utils.general import UFitPanel


class UIStartModeling(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_start, ot_start_from_existing):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row1 = box0.row()
        box0_row0.operator(ot_start)
        box0_row1.operator(ot_start_from_existing)

        nav_box = layout.box().row()
        nav_box.operator("ufit_operators.prev_step", text="Back")


class UIImportScan(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_import_scan, ot_generate_socket=None):
        scene = context.scene
        layout = self.layout

        if context.scene.device_type == 'transfemoral':


        if context.scene.socket_generation == 'by_scan':
            row1 = layout.row()
            row1.prop(scene, 'ufit_import_unit', expand=True)

            row2 = layout.row()
            row2.operator(ot_import_scan)

            nav_box = layout.box().row()
            nav_box.operator("ufit_operators.prev_step", text="Back")

        elif context.scene.socket_generation == 'by_numbers':
            row1 = layout.row()
            row1.prop(scene, 'tf_socket_length', expand=True)





