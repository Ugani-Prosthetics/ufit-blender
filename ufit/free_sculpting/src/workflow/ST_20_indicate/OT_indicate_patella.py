from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_indicate import OTMoveScan


class OTMoveScanFS(OTBaseFS, OTMoveScan):
    """Tooltip"""
    bl_idname = "operators.move_scan"
    bl_label = "Move Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='move_scan')
