import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_thickness, include_voronoi=False):
        ufit_obj = bpy.data.objects['uFit']
        scene = context.scene
        layout = self.layout

        if include_voronoi:
            row0 = layout.row()
            row0.prop(scene, 'ufit_thickness_voronoi', expand=True)

            if context.scene.ufit_thickness_voronoi == 'normal':
                box0 = layout.box()
                box0_row0 = box0.row()
                box0_row0.prop(ufit_obj.modifiers['Solidify'], 'thickness')
            elif context.scene.ufit_thickness_voronoi == 'voronoi':
                box0 = layout.box()
                box0_row0 = box0.row()
                box0_row0.prop(scene, 'ufit_voronoi_number', text='Holes #')

                box0_row1 = box0.row()
                box0_row1.prop(ufit_obj.modifiers['Wireframe'], 'thickness')

        else:
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row0.prop(scene, 'ufit_print_thickness')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_thickness)


class UIVerifyThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_thickness):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_thickness)
