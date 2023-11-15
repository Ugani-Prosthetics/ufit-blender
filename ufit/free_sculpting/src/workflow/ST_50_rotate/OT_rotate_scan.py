from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_rotate import OTMirror, OTSaveRotation


class OTMirrorFS(OTBaseFS, OTMirror):
    """Tooltip"""
    bl_idname = "fs_operators.mirror"
    bl_label = "Mirror"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='mirror')


class OTSaveRotationFS(OTBaseFS, OTSaveRotation):
    """Tooltip"""
    bl_idname = "fs_operators.save_rotation"
    bl_label = "Save Rotation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='rotate')


