from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_clean_up import (OTApproveCleanUp, OTHighlightNonManifold, OTFillNonManifold,
                                                      OTDeleteNonManifold)


class OTHighlightNonManifoldTT(OTBaseTT, OTHighlightNonManifold):
    """Tooltip"""
    bl_idname = "tt_operators.highlight_non_manifold"
    bl_label = "Highlight Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='highlight_non_manifold')


class OTFillNonManifoldTT(OTBaseTT, OTFillNonManifold):
    """Tooltip"""
    bl_idname = "tt_operators.fill_non_manifold"
    bl_label = "Fix Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='fill_non_manifold')


class OTDeleteNonManifoldTT(OTBaseTT, OTDeleteNonManifold):
    """Tooltip"""
    bl_idname = "tt_operators.delete_non_manifold"
    bl_label = "Delete Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='delete_non_manifold')


class OTApproveCleanUpTT(OTBaseTT, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "tt_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')



