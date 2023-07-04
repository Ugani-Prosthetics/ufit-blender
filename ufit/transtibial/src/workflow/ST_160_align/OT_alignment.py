from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_alignment import OTSaveAlignment


class OTSaveAlignmentTT(OTBaseTT, OTSaveAlignment):
    """Tooltip"""
    bl_idname = "tt_operators.save_alignment"
    bl_label = "Save Alignment"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='align')
