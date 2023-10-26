from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_custom_thickness import OTCustomThickness, OTCustomThicknessDone


class OTCustomThicknessTT(OTBaseTT, OTCustomThickness):
    """Tooltip"""
    bl_idname = "tt_operators.custom_thickness"
    bl_label = "Apply Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='custom_thickness')


class OTCustomThicknessDoneTT(OTBaseTT, OTCustomThicknessDone):
    """Tooltip"""
    bl_idname = "tt_operators.custom_thickness_done"
    bl_label = "Next"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='custom_thickness_done')
