from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_clean_up import (OTApproveCleanUp, OTHighlightNonManifold, OTFillNonManifold,
                                                      OTDeleteNonManifold)


class OTHighlightNonManifoldTF(OTBaseTF, OTHighlightNonManifold):
    """Tooltip"""
    bl_idname = "tf_operators.highlight_non_manifold"
    bl_label = "Highlight Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='highlight_non_manifold')


class OTFillNonManifoldTF(OTBaseTF, OTFillNonManifold):
    """Tooltip"""
    bl_idname = "tf_operators.fill_non_manifold"
    bl_label = "Fix Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='fill_non_manifold')


class OTDeleteNonManifoldTF(OTBaseTF, OTDeleteNonManifold):
    """Tooltip"""
    bl_idname = "tf_operators.delete_non_manifold"
    bl_label = "Delete Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='delete_non_manifold')
    

class OTApproveCleanUpTF(OTBaseTF, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "tf_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')
