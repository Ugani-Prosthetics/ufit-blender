from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_milling import OTSocketMilling


class OTSocketMillingTF(OTBaseTF, OTSocketMilling):
    """Tooltip"""
    bl_idname = "tf_operators.socket_milling"
    bl_label = "Approve Socket"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='socket_milling')

