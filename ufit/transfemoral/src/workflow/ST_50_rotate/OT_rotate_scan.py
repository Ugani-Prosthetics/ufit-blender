from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_rotate import OTSaveRotation


class OTSaveRotationTF(OTBaseTF, OTSaveRotation):
    """Tooltip"""
    bl_idname = "tf_operators.save_rotation"
    bl_label = "Save Rotation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='rotate')


