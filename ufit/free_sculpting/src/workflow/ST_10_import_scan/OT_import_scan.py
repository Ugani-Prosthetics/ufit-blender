from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_import_scan import OTImportScan


class OTImportScanFS(OTBaseFS, OTImportScan):
    """Tooltip"""
    bl_idname = "operators.import_scan"
    bl_label = "Select Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_scan')
