from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_finish import OTExportDevice


class OTExportSocketTT(OTBaseTT, OTExportDevice):
    """Tooltip"""
    bl_idname = "tt_operators.export_socket"
    bl_label = "Export Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='export')
