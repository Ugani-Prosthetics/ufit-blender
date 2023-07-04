from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_scale import OTApproveScaling


class OTApproveScalingTF(OTBaseTF, OTApproveScaling):
    """Tooltip"""
    bl_idname = "tf_operators.approve_scaling"
    bl_label = "Approve Scaling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_scaling')
