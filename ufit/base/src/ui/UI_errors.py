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
            text='Reporting a problem usually takes about 2 minutes processing!',
            parent=box0
        )
        box1 = layout.box()
        get_label_multiline(
            context=context,
            text='By clicking the Report Problem button you will be reporting the current status to the uFit team. '
                 'Your last two checkpoints and the scan will be uploaded to WeTransfer and an automated email will '
                 'be created for you to send.',
            parent=box1
        )

        row = layout.row()
        row.operator('ufit_operators.report_problem')

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan']
