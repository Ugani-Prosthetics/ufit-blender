from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_clean_up import OTCleanUp


class OTCleanUpFS(OTBaseFS, OTCleanUp):
    """Tooltip"""
    bl_idname = "fs_operators.clean_up"
    bl_label = "Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='clean_up')
