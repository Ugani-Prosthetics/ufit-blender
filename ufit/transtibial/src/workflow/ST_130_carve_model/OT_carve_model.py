from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_carve import OTCarveModel


class OTCarveModelTT(OTBaseTT, OTCarveModel):
    """Tooltip"""
    bl_idname = "tt_operators.carve_model"
    bl_label = "Carve Model"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='carve_model')

