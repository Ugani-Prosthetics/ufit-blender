from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_cutout import OTCutout


class OTCutoutFS(OTBaseFS, OTCutout):
    """Tooltip"""
    bl_idname = "fs_operators.cutout"
    bl_label = "Perform Cutout"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout')
