from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_thickness import OTApproveThickness


class OTApproveSocketTF(OTBaseTF, OTApproveThickness):
    """Tooltip"""
    bl_idname = "tf_operators.approve_socket"
    bl_label = "Approve Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_socket')

