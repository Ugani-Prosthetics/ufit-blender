from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_thickness import OTThickness


class OTThicknessTT(OTBaseTT, OTThickness):
    """Tooltip"""
    bl_idname = "tt_operators.thickness"
    bl_label = "Choose Print Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='thickness')
