from .core.OT_base import OTBase
from .core.finish import restart_ufit
from ...src.properties.properties import ufit_scene_properties
from ....transtibial.src.properties.properties import tt_scene_properties
from ....transfemoral.src.properties.properties import tf_scene_properties


class OTRestart(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.restart"
    bl_label = "New Restart"
    bl_options = {"REGISTER", "UNDO"}

    def main_func(self, context):
        scene_props = list(set(tt_scene_properties + tf_scene_properties + ufit_scene_properties))
        restart_ufit(context, custom_scene_props=scene_props)

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='restart')
