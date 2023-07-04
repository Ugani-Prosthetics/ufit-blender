from .....base.src.ui.base.UI_circumferences import UICircumferences, UIAddCircumferences
from ...transtibial_constants import tt_path_consts, tt_ui_consts
from .....base.src.operators.core.checkpoints import get_workflow_step_nr


class UICircumferencesTT(UICircumferences):
    bl_idname = "VIEW3D_PT_tt_circumferences"
    bl_label = tt_ui_consts['workflow']['circumferences']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       path_consts=tt_path_consts,
                       init_step_nr=50,
                       sculpt_step_nr=60,
                       liner_step_nr=100,
                       ot_circums_highlight="tt_operators.circumferences_highlight")

    @classmethod
    def poll(cls, context):
        workflow_step_nr = get_workflow_step_nr(context.scene.ufit_active_step, tt_path_consts, raise_exception=False)
        return (workflow_step_nr >= 60
                and context.scene.ufit_circumferences[0] > 0
                and context.scene.ufit_device_type == 'transtibial')


class UIAddCircumferencesTT(UIAddCircumferences):
    bl_idname = "VIEW3D_PT_tt_calc_circumferences"
    bl_label = "Add Circumferences"

    def draw(self, context):
        self.draw_base(context,
                       ot_add_circums="tt_operators.add_circumference",
                       ot_circums_calc="tt_operators.circumferences_calc",
                       ot_circums_done="tt_operators.circumferences_done")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'circumferences'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transtibial')
