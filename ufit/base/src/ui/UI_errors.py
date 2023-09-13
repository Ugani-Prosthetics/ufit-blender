import bpy
from .utils.general import UFitPanel, get_label_multiline
from ..base_constants import base_ui_consts


class UIReportProblem(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_ufit_report_problem"
    bl_label = base_ui_consts['persistent']['report_problem']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box0 = layout.box()
        get_label_multiline(
            context=context,
            text='Checkpoint files and the 3D scan will be send to the uFit team via WeTransfer '
                 'and an automated email will be initiated. The process usually takes about 2 minutes.',
            parent=box0
        )

        row = layout.row()
        row.operator('ufit_operators.report_problem')

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan']
