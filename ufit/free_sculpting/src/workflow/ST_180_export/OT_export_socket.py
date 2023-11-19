from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_finish import OTExportDevice


class OTExportSocketFS(OTBaseFS, OTExportDevice):
    """Tooltip"""
    bl_idname = "fs_operators.export_socket"
    bl_label = "Export Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='export')
