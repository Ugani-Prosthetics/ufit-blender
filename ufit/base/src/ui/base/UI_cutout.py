import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UICutoutPrep(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_cutout_plane):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_cutout_plane)


class UICutout(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_cutout):
        object = context.active_object
        scene = context.scene
        layout = self.layout

        # box0
        box0 = layout.box()
        box0.prop(scene, 'ufit_twist_method')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_cutout)
