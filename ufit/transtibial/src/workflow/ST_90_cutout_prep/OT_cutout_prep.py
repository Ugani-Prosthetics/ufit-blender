from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_cutout import OTCutoutPlane


class OTCutoutPlaneTT(OTBaseTT, OTCutoutPlane):
    """Tooltip"""
    bl_idname = "tt_operators.cutout_plane"
    bl_label = "Create Cutout Plane"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_prep')
