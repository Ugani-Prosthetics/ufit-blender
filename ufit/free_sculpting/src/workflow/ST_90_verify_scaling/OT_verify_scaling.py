from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_scale import OTApproveScaling


class OTApproveScalingFS(OTBaseFS, OTApproveScaling):
    """Tooltip"""
    bl_idname = "fs_operators.approve_scaling"
    bl_label = "Approve Scaling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_scaling')
