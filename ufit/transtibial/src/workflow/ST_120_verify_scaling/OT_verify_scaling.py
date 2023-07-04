from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_scale import OTApproveScaling


class OTApproveScalingTT(OTBaseTT, OTApproveScaling):
    """Tooltip"""
    bl_idname = "tt_operators.approve_scaling"
    bl_label = "Approve Scaling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_scaling')
