from .core.OT_base import OTBase


class OTDeviceType(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.device_type"
    bl_label = "Device Type"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'device_type')

    def main_func(self, context):
        pass



