from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_indicate import OTMoveScan


class OTMoveScanTT(OTBaseTT, OTMoveScan):
    """Tooltip"""
    bl_idname = "tt_operators.move_scan"
    bl_label = "Move Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='move_scan')
