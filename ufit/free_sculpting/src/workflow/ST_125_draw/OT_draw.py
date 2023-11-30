from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_draw import OTApplyDraw


class OTApplyDrawFS(OTBaseFS, OTApplyDraw):
    """Tooltip"""
    bl_idname = "fs_operators.apply_draw"
    bl_label = "Apply Draw"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='apply_draw')



