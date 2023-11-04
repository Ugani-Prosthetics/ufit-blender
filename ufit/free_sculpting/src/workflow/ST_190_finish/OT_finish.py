from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_finish import OTRestart
from .....base.src.operators.core.finish import restart_ufit
from ....src.properties.properties import tt_scene_properties


class OTFinishFS(OTBaseFS, OTRestart):
    """Tooltip"""
    bl_idname = "operators.restart"
    bl_label = "Create New"
    bl_options = {"REGISTER", "UNDO"}

    def main_func(self, context):
        restart_ufit(context, custom_scene_props=tt_scene_properties)

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='restart')
