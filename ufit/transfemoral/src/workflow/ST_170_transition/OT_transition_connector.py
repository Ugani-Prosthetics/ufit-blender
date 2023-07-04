from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_connector import OTTransitionConnector


class OTTransitionConnectorTF(OTBaseTF, OTTransitionConnector):
    """Tooltip"""
    bl_idname = "tf_operators.transition_connector"
    bl_label = "Transition Connector"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='transition')
