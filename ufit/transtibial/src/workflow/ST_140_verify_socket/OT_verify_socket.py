from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_thickness import OTApproveThickness


class OTApproveSocketTT(OTBaseTT, OTApproveThickness):
    """Tooltip"""
    bl_idname = "tt_operators.approve_socket"
    bl_label = "Approve Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_socket')

