from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_milling import OTSocketMilling


class OTSocketMillingTT(OTBaseTT, OTSocketMilling):
    """Tooltip"""
    bl_idname = "tt_operators.socket_milling"
    bl_label = "Socket or Milling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='socket_milling')

