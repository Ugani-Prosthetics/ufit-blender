from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_alignment import OTSaveAlignment


class OTSaveAlignmentTF(OTBaseTF, OTSaveAlignment):
    """Tooltip"""
    bl_idname = "tf_operators.save_alignment"
    bl_label = "Save Alignment"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='align')
