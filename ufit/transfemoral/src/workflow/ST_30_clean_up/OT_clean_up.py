from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_clean_up import OTCleanUp


class OTCleanUpTF(OTBaseTF, OTCleanUp):
    """Tooltip"""
    bl_idname = "tf_operators.clean_up"
    bl_label = "Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='clean_up')
