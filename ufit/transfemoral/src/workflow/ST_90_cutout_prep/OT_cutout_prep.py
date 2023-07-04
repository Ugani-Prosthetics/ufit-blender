from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_cutout import OTCutoutPlane


class OTCutoutPlaneTF(OTBaseTF, OTCutoutPlane):
    """Tooltip"""
    bl_idname = "tf_operators.cutout_plane"
    bl_label = "Create Cutout Plane"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_prep')
