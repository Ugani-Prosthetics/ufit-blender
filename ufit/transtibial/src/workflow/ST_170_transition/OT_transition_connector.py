from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_connector import OTTransitionConnector


class OTTransitionConnectorTT(OTBaseTT, OTTransitionConnector):
    """Tooltip"""
    bl_idname = "tt_operators.transition_connector"
    bl_label = "Transition Connector"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='transition')
