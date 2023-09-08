import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox


class UIPushPullRegions(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_push_pull_region, ot_smooth_region, ot_free_sculpt_checkpoint, ot_push_pull_smooth_done):
        scene = context.scene
        layout = self.layout

        row0 = layout.row()
        row0.alignment = 'LEFT'
        row0.label(text="Mode:")
        row0.prop(scene, 'ufit_sculpt_mode', expand=True)

        # separator
        layout.row().separator()

        # disable colors / preview extrusions
        row1 = layout.row()
        row1.alignment = 'LEFT'
        row1.label(text="Color Enable: ")
        row1.prop(scene, 'ufit_enable_colors', text='')

        # separator
        layout.row().separator()

        if context.scene.ufit_sculpt_mode == 'guided':
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row0.prop(scene, 'ufit_sculpt_tool', expand=True)

            if context.scene.ufit_sculpt_tool == 'push_pull':
                box0_row1 = box0.row()
                box0_row1.prop(scene, 'ufit_push_pull_circular')

                box0_row2 = box0.row()
                box0_row2.prop(scene, 'ufit_extrude_amount')

                box1 = layout.box()
                box1_row0 = box1.row()
                push_ot = box1_row0.operator(ot_push_pull_region, text='Push')
                push_ot.direction = 'Push'  # pass property value to operator
                pull_ot = box1_row0.operator(ot_push_pull_region, text='Pull')
                pull_ot.direction = 'Pull'  # pass property value to operator
            elif context.scene.ufit_sculpt_tool == 'smooth':
                box0_row1 = box0.row()
                box0_row1.prop(scene, 'ufit_smooth_factor')

                box1 = layout.box()
                box1.operator(ot_smooth_region)

        elif context.scene.ufit_sculpt_mode == 'free':
            box0 = layout.box()
            box0_row0 = box0.row()
            box0_row1 = box0.row()
            box0_row2 = box0.row()

            box0_row0.prop(scene, 'ufit_sculpt_brush', text='')
            box0_row1.prop(scene.tool_settings.unified_paint_settings, 'size')
            box0_row2.prop(scene.tool_settings.sculpt.brush, 'strength')

            box1 = layout.box()
            box1.operator(ot_free_sculpt_checkpoint)

        # separator
        layout.row().separator()

        # navigation box
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_push_pull_smooth_done)
