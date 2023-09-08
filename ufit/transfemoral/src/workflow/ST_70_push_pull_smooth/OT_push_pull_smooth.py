from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_push_pull_smooth import \
    OTPushPullRegion, OTSmoothRegion, OTPushPullSmoothDone, OTFreeSculptCheckpoint


class OTPushPullRegionTF(OTBaseTF, OTPushPullRegion):
    """Tooltip"""
    bl_idname = "tf_operators.push_pull_region"
    bl_label = "Push_Pull"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='push_pull_region')


class OTSmoothRegionTF(OTBaseTF, OTSmoothRegion):
    """Tooltip"""
    bl_idname = "tf_operators.smooth_region"
    bl_label = "Smooth"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='smooth_region')


class OTFreeSculptCheckpointTF(OTBaseTF, OTFreeSculptCheckpoint):
    """Tooltip"""
    bl_idname = "tf_operators.free_sculpt_checkpoint"
    bl_label = "Add Checkpoint"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='free_sculpt_checkpoint')


class OTPushPullSmoothDoneTF(OTBaseTF, OTPushPullSmoothDone):
    """Tooltip"""
    bl_idname = "tf_operators.push_pull_smooth_done"
    bl_label = "Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='push_pull_smooth_done')
