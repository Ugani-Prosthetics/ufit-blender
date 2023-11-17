import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UICutoutPrep(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_cutout_plane):
        layout = self.layout

        row0 = layout.row()
        row0.prop(context.scene, 'ufit_cutout_style', expand=True)

        if context.scene.ufit_cutout_style == 'straight':
            row1 = layout.row()
            row1.prop(context.scene, 'ufit_plane_operation', expand=True)

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_cutout_plane)


class UICutout(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_cutout):
        object = context.active_object
        layout = self.layout

        # box0
        box0 = layout.box()

        box0.prop(object.data, 'extrude', text='Width')
        box0.prop(object.data, 'twist_mode')
        box0.prop(context.scene, 'ufit_mean_tilt')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_cutout)
