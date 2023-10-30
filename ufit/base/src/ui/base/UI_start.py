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
    def draw_base(self, context, ot_import_scan):
        scene = context.scene
        layout = self.layout

        row1 = layout.row()
        row1.prop(scene, 'ufit_import_unit', expand=True)

        row2 = layout.row()
        row2.operator(ot_import_scan)

        nav_box = layout.box().row()
        nav_box.operator("ufit_operators.prev_step", text="Back")


