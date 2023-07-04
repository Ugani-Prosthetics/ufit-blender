import bpy
from .....base.src.ui.utils.general import UFitPanel
from .....base.src.ui.utils.general import get_standard_navbox
from .....base.src.operators.core.checkpoints import get_workflow_step_nr


class UICircumferences(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, path_consts, init_step_nr, sculpt_step_nr, liner_step_nr, ot_circums_highlight):
        workflow_step_nr = get_workflow_step_nr(context.scene.ufit_active_step, path_consts)

        layout = self.layout

        box0 = layout.box()
        box0_row0 = box0.row()

        box0_row0.label(text=f"#")
        box0_row0.label(text=f"Init.")
        if workflow_step_nr > sculpt_step_nr:
            box0_row0.label(text=f"Sculpt")
        if workflow_step_nr > liner_step_nr:
            box0_row0.label(text=f"Liner")

        for i, circum in enumerate(context.scene.ufit_circumferences):
            if circum > 0:
                initial_circum = context.scene.ufit_init_circumferences[i]

                box = layout.box()
                box_row0 = box.row()

                box_row0.label(text=f"{i + 1}.")
                box_row0.label(text=f"{round(initial_circum*100, 1)}")

                if workflow_step_nr > liner_step_nr:
                    sculpt_circum = context.scene.ufit_sculpt_circumferences[i]
                    box_row0.label(text=f"{round(sculpt_circum*100, 1)}")  # sculpt circum
                    box_row0.label(text=f"{round(circum * 100, 1)}")  # liner circum
                elif workflow_step_nr > liner_step_nr:
                    box_row0.label(text=f"{round(circum*100, 1)}")  # sculpt circum

        # circumferences highlighting
        box1 = layout.box()
        box1_row0 = box1.row()
        if not context.scene.ufit_circums_highlighted:
            box1_row0.operator(ot_circums_highlight, text="Highlight Measurements")
        else:
            box1_row0.operator(ot_circums_highlight, text="Close Measurements")


class UIAddCircumferences(UFitPanel, bpy.types.Panel):
    def draw_base(self, context, ot_add_circums, ot_circums_calc, ot_circums_done):
        scene = context.scene
        layout = self.layout

        # box0
        box0 = layout.box()
        box0_row0 = box0.row()
        box0_row0.operator(ot_add_circums, text="Add first")

        # box1
        box1 = layout.box()
        box1_row0 = box1.row()
        box1_row1 = box1.row()

        box1.enabled = False
        if 'Circum_0' in bpy.data.objects and 'Circum_1' not in bpy.data.objects:
            box1.enabled = True

        box1_row0.prop(scene, 'ufit_circums_distance', expand=True)
        box1_row1.operator(ot_circums_calc)

        # separator
        layout.row().separator()

        # navigation box
        get_standard_navbox(self.layout, "ufit_operators.prev_step", ot_circums_done)
