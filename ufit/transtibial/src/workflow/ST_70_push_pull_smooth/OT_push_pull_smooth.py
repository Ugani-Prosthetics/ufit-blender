from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_push_pull_smooth import \
    OTPushPullRegion, OTSmoothRegion, OTPushPullSmoothDone, OTFreeSculptCheckpoint


class OTPushPullRegionTT(OTBaseTT, OTPushPullRegion):
    """Tooltip"""
    bl_idname = "tt_operators.push_pull_region"
    bl_label = "Push_Pull"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='push_pull_region')


class OTSmoothRegionTT(OTBaseTT, OTSmoothRegion):
    """Tooltip"""
    bl_idname = "tt_operators.smooth_region"
    bl_label = "Smooth"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='smooth_region')


class OTFreeSculptCheckpointTT(OTBaseTT, OTFreeSculptCheckpoint):
    """Tooltip"""
    bl_idname = "tt_operators.free_sculpt_checkpoint"
    bl_label = "Add Checkpoint"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='free_sculpt_checkpoint')


class OTPushPullSmoothDoneTT(OTBaseTT, OTPushPullSmoothDone):
    """Tooltip"""
    bl_idname = "tt_operators.push_pull_smooth_done"
    bl_label = "Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='push_pull_smooth_done')
