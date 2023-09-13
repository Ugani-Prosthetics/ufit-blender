from .core.OT_base import OTBase
from .core.errors import report_problem


class OTReportProblem(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.report_problem"
    bl_label = "Report Problem"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible to report a problem
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'report_problem')

    def main_func(self, context):
        report_problem(context)
