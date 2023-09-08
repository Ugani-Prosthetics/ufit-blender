from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_carve import OTCarveModel


class OTCarveModelTF(OTBaseTF, OTCarveModel):
    """Tooltip"""
    bl_idname = "tf_operators.carve_model"
    bl_label = "Carve Model"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='carve_model')

