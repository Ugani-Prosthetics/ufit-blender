from .core.OT_base import OTBase
from .core.platform import platform_login


class OTPlatformLogin(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.platform_login"
    bl_label = "Login"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.scene.ufit_user \
                and context.scene.ufit_password:
            return True

    def execute(self, context):
        return self.execute_base(context,
                                 'platform_login')

    def main_func(self, context):
        platform_login(context)
