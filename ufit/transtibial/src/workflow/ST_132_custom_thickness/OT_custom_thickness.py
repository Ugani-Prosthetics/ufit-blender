from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_custom_thickness import OTCustomThickness


class OTCustomThicknessTT(OTBaseTT, OTCustomThickness):
    """Tooltip"""
    bl_idname = "tt_operators.custom_thickness"
    bl_label = "Choose Print Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='custom_thickness')
