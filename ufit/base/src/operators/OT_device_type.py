from .core.OT_base import OTBase
from .core.checkpoints import set_active_step


class OTDeviceType(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.device_type"
    bl_label = "Device Type"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        set_active_step(context,
                        step='start',
                        path_consts=None,
                        ui_consts=None,
                        exec_save=False)

        return {'FINISHED'}

