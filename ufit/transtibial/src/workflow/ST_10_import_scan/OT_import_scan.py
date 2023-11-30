from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_import_scan import OTImportScan


class OTImportScanTT(OTBaseTT, OTImportScan):
    """Tooltip"""
    bl_idname = "tt_operators.import_scan"
    bl_label = "Select Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_scan')


