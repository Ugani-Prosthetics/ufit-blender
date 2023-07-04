from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_thickness import OTThickness


class OTThicknessTF(OTBaseTF, OTThickness):
    """Tooltip"""
    bl_idname = "tf_operators.thickness"
    bl_label = "Choose Print Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='thickness')
