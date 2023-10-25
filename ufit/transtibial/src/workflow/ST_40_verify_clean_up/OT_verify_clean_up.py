from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_clean_up import OTApproveCleanUp, OTHighlightNonManifold, OTFixNonManifold


class OTHighlightNonManifoldTT(OTBaseTT, OTHighlightNonManifold):
    """Tooltip"""
    bl_idname = "tt_operators.highlight_non_manifold"
    bl_label = "Highlight NonManifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='highlight_non_manifold')


class OTFixNonManifoldTT(OTBaseTT, OTFixNonManifold):
    """Tooltip"""
    bl_idname = "tt_operators.fix_non_manifold"
    bl_label = "Auto Fix Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='fix_non_manifold')


class OTApproveCleanUpTT(OTBaseTT, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "tt_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')



