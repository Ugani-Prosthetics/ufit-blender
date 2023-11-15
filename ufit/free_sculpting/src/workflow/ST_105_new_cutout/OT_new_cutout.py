from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_cutout import OTNewCutout


class OTNewCutoutFS(OTBaseFS, OTNewCutout):
    """Tooltip"""
    bl_idname = "fs_operators.new_cutout"
    bl_label = "Another Cutout"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='new_cutout')


class OTCutoutDoneFS(OTBaseFS, OTNewCutout):
    """Tooltip"""
    bl_idname = "fs_operators.cutout_done"
    bl_label = "Cutout Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='cutout_done')
