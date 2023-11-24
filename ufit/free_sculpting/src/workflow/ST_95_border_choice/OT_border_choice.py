from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_border_choice import OTBorderChoice


class OTBorderChoiceFS(OTBaseFS, OTBorderChoice):
    """Tooltip"""
    bl_idname = "fs_operators.border_choice"
    bl_label = "Border Choice"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='border_choice')

