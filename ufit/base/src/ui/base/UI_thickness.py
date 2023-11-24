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
            row0.prop(scene, 'ufit_thickness_type')

            box0 = layout.box()
            box0_row0 = box0.row()

            if context.scene.ufit_thickness_type == 'normal':
                box0_row0.prop(scene, 'ufit_solidify_thickness')

            elif context.scene.ufit_thickness_type == 'draw':
                node_tree = bpy.data.node_groups['Voronoi Nodes Empty']

                box0_row0.prop(scene, 'ufit_draw_thickness')

                # box1 = layout.box()
                # box1_row0 = box1.row()
                # box1_row0.prop(node_tree.nodes['ufit_smooth_node'].inputs[4], 'default_value', text='Smooth')

            elif context.scene.ufit_thickness_type == 'voronoi_one':
                node_tree = bpy.data.node_groups['Voronoi Nodes One']

                box0_row0.prop(scene, 'ufit_voronoi_one_thickness')

                box1 = layout.box()
                box1_row0 = box1.row()
                box1_row1 = box1.row()
                box1_row2 = box1.row()
                # box1_row3 = box1.row()
                box1_row0.prop(scene, 'ufit_voronoi_size', text='Size')
                box1_row1.prop(node_tree.nodes['ufit_voronoi_node'].inputs[2], 'default_value', text='Quantity')
                box1_row2.prop(node_tree.nodes['ufit_voronoi_node'].inputs[5], 'default_value', text='Randomness')
                # box1_row2.prop(node_tree.nodes['ufit_smooth_node'].inputs[4], 'default_value', text='Smooth')

                # box1_row1 = box0.row()
                # box1_row1.prop(ufit_obj.modifiers['Wireframe'], 'thickness')
            elif context.scene.ufit_thickness_type == 'voronoi_two':
                node_tree = bpy.data.node_groups['Voronoi Nodes Two']

                box0_row0.prop(scene, 'ufit_voronoi_two_thickness')

                box1 = layout.box()
                box1_row0 = box1.row()
                box1_row0.prop(ufit_obj.modifiers['Decimate'], 'ratio', text='Ratio')

        else:
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row0.prop(scene, 'ufit_print_thickness')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_thickness)


class UIVerifyThickness(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_approve_thickness):
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_approve_thickness)
