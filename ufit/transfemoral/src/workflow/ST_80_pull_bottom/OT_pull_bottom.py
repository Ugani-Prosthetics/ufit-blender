from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_pull_bottom import OTPullBottom, OTPullBottomDone


class OTPullBottomTF(OTBaseTF, OTPullBottom):
    """Tooltip"""
    bl_idname = "tf_operators.pull_bottom"
    bl_label = "Pull Bottom"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='pull_bottom')


class OTPullBottomDoneTF(OTBaseTF, OTPullBottomDone):
    """Tooltip"""
    bl_idname = "tf_operators.pull_bottom_done"
    bl_label = "Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='pull_bottom_done')

