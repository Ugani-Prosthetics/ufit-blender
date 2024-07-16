from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_cutout import OTCutoutSelection


class OTCutoutSelectionTT(OTBaseTT, OTCutoutSelection):
    """Tooltip"""
    bl_idname = "tt_operators.cutout_selection"
    bl_label = "Perform Cutout"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_selection')
