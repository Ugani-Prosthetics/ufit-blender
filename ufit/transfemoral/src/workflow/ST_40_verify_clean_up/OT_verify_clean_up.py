from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_clean_up import OTApproveCleanUp


class OTApproveCleanUpTF(OTBaseTF, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "tf_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')
