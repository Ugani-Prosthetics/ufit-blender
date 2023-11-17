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
                node_tree = bpy.data.node_groups['Voronoi Nodes']

                box0 = layout.box()
                box0_row0 = box0.row()
                box0_row1 = box0.row()
                box0_row2 = box0.row()
                box0_row3 = box0.row()
                box0_row4 = box0.row()
                # box0_row0.prop(scene, 'ufit_voronoi_size', text='Size')
                # box0_row1.prop(node_tree.nodes['ufit_voronoi_node'].inputs[2], 'default_value', text='Quantity')
                # box0_row2.prop(node_tree.nodes['ufit_voronoi_node'].inputs[5], 'default_value', text='Randomness')
                # box0_row3.prop(node_tree.nodes['ufit_extrude_node'].inputs[3], 'default_value', text='Thickness')
                # box0_row4.prop(node_tree.nodes['ufit_smooth_node'].inputs[4], 'default_value', text='Smooth')

                # box0_row1 = box0.row()
                # box0_row1.prop(ufit_obj.modifiers['Wireframe'], 'thickness')

        else:
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row0.prop(scene, 'ufit_print_thickness')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_thickness)


class UIVerifyThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_thickness):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_thickness)
