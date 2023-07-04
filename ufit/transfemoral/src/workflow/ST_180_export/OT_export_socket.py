from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_finish import OTExportDevice


class OTExportSocketTF(OTBaseTF, OTExportDevice):
    """Tooltip"""
    bl_idname = "tf_operators.export_socket"
    bl_label = "Export Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='export')
