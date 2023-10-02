from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_flare import OTFlare, OTFlareDone


class OTFlareTF(OTBaseTF, OTFlare):
    """Tooltip"""
    bl_idname = "tt_operators.flare"
    bl_label = "Flare"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='flare')


class OTFlareDoneTF(OTBaseTF, OTFlareDone):
    """Tooltip"""
    bl_idname = "tt_operators.flare_done"
    bl_label = "Done"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='flare_done')
