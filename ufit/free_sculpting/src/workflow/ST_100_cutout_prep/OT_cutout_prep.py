from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_cutout import OTCutoutPlane


class OTCutoutPlaneFS(OTBaseFS, OTCutoutPlane):
    """Tooltip"""
    bl_idname = "fs_operators.cutout_plane"
    bl_label = "Create Cutout Plane"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_prep')
