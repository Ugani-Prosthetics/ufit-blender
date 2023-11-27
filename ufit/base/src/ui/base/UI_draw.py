import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIDraw(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_apply_draw):
        ufit_obj = bpy.data.objects['uFit']
        layout = self.layout
        scene = context.scene

        row0 = layout.row()
        row0.prop(scene, 'ufit_draw_type', text="")

        # separator
        layout.row().separator()

        if context.scene.ufit_draw_type == 'free':
            row0 = layout.row()
            row0.prop(scene.tool_settings.unified_paint_settings, 'size')

            row1 = layout.row()
            row1.prop(scene, 'ufit_free_draw_thickness')
            
        elif context.scene.ufit_draw_type == 'automated':
            row0 = layout.row()
            row0.prop(scene, 'ufit_solidify_thickness')
            
        elif context.scene.ufit_draw_type == 'voronoi':
            row0 = layout.row()
            row0.prop(scene, 'ufit_voronoi_type', expand=True)

            if context.scene.ufit_voronoi_type == 'voronoi_one':
                node_tree = bpy.data.node_groups['Voronoi Nodes One']

                row1 = layout.row()
                row2 = layout.row()
                row3 = layout.row()
                row4 = layout.row()
                row1.prop(scene, 'ufit_voronoi_size', text='Size')
                row2.prop(scene, 'ufit_voronoi_one_thickness')
                row3.prop(node_tree.nodes['ufit_voronoi_node'].inputs[2], 'default_value', text='Quantity')
                row4.prop(node_tree.nodes['ufit_voronoi_node'].inputs[5], 'default_value', text='Randomness')
            elif context.scene.ufit_voronoi_type == 'voronoi_two':
                row1 = layout.row()
                row2 = layout.row()
                row1.prop(scene, 'ufit_voronoi_two_thickness')
                row2.prop(ufit_obj.modifiers['Decimate'], 'ratio', text='Ratio')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_apply_draw)
