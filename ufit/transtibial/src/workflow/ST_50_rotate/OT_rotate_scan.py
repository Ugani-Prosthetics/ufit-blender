from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_rotate import OTSaveRotation


class OTSaveRotationTT(OTBaseTT, OTSaveRotation):
    """Tooltip"""
    bl_idname = "tt_operators.save_rotation"
    bl_label = "Save Rotation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='rotate')


