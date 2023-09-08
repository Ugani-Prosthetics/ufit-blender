from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_carve import OTSocketCarve


class OTSocketCarveTT(OTBaseTT, OTSocketCarve):
    """Tooltip"""
    bl_idname = "tt_operators.socket_carve"
    bl_label = "Socket or Carve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='socket_carve')

