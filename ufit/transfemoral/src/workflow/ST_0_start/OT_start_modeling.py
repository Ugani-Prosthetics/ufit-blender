from .....base.src.operators.base.OT_start import OTStartModeling, OTStartFromExisting
from ..OT_Base_TF import OTBaseTF


class OTStartModelingTF(OTBaseTF, OTStartModeling):
    """Tooltip"""
    bl_idname = "tf_operators.start_modeling"
    bl_label = "Start New"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='start_modeling')


class OTStartFromExistingTF(OTBaseTF, OTStartFromExisting):
    """Tooltip"""
    bl_idname = "tf_operators.start_from_existing"
    bl_label = "Start From Existing"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='start_from_existing')
