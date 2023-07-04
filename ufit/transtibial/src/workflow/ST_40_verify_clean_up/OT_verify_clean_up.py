from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_clean_up import OTApproveCleanUp


class OTApproveCleanUpTT(OTBaseTT, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "tt_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')
