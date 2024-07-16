from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_cutout import OTCutoutSelection


class OTCutoutSelectionTF(OTBaseTF, OTCutoutSelection):
    """Tooltip"""
    bl_idname = "tf_operators.cutout_selection"
    bl_label = "Perform Cutout"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_selection')
