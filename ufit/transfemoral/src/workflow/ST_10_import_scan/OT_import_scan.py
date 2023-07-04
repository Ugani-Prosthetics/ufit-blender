from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_import_scan import OTImportScan


class OTImportScanTF(OTBaseTF, OTImportScan):
    """Tooltip"""
    bl_idname = "tf_operators.import_scan"
    bl_label = "Select Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_scan')
