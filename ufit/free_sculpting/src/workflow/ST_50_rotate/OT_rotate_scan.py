from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_rotate import OTSaveRotation


class OTSaveRotationFS(OTBaseFS, OTSaveRotation):
    """Tooltip"""
    bl_idname = "operators.save_rotation"
    bl_label = "Save Rotation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='rotate')


