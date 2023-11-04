from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_thickness import OTThickness


class OTThicknessFS(OTBaseFS, OTThickness):
    """Tooltip"""
    bl_idname = "operators.thickness"
    bl_label = "Choose Print Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='thickness')
