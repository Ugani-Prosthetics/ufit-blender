from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_carve import OTSocketCarve


class OTSocketCarveTF(OTBaseTF, OTSocketCarve):
    """Tooltip"""
    bl_idname = "tf_operators.socket_carve"
    bl_label = "Approve Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='socket_carve')

