from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_clean_up import (OTApproveCleanUp, OTHighlightNonManifold, OTFillNonManifold,
                                                      OTDeleteNonManifold)


class OTHighlightNonManifoldFS(OTBaseFS, OTHighlightNonManifold):
    """Tooltip"""
    bl_idname = "fs_operators.highlight_non_manifold"
    bl_label = "Highlight Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='highlight_non_manifold')


class OTFillNonManifoldFS(OTBaseFS, OTFillNonManifold):
    """Tooltip"""
    bl_idname = "fs_operators.fill_non_manifold"
    bl_label = "Fix Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='fill_non_manifold')


class OTDeleteNonManifoldFS(OTBaseFS, OTDeleteNonManifold):
    """Tooltip"""
    bl_idname = "fs_operators.delete_non_manifold"
    bl_label = "Delete Non Manifold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='delete_non_manifold')


class OTApproveCleanUpFS(OTBaseFS, OTApproveCleanUp):
    """Tooltip"""
    bl_idname = "fs_operators.approve_clean_up"
    bl_label = "Approve Clean Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='verify_clean_up')



