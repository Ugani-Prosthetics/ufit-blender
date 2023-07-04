from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_indicate import OTMoveScan


class OTMoveScanTF(OTBaseTF, OTMoveScan):
    """Tooltip"""
    bl_idname = "tf_operators.move_scan"
    bl_label = "Move Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='move_scan')
