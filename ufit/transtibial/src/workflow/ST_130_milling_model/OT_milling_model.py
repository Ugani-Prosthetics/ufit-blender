from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_milling import OTMillingModel


class OTMillingModelTT(OTBaseTT, OTMillingModel):
    """Tooltip"""
    bl_idname = "tt_operators.milling_model"
    bl_label = "Milling Model"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='milling_model')

