from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_milling import OTMillingModel


class OTMillingModelTF(OTBaseTF, OTMillingModel):
    """Tooltip"""
    bl_idname = "tf_operators.milling_model"
    bl_label = "CNC Milling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='milling_model')

