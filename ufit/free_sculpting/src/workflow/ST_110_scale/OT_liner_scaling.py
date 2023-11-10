from .....base.src.operators.base.OT_scale import OTScale
from ..OT_Base_FS import OTBaseFS
from ...free_sculpting_constants import fs_path_consts, fs_ui_consts
from .....base.src.operators.core.checkpoints import set_active_step
from .....base.src.operators.utils.general import return_to_default_state
from .....base.src.operators.core.prepare import remeasure_circumferences
from .....base.src.operators.core.sculpt import prep_verify_scaling, scale


class OTLinerScaleFS(OTBaseFS, OTScale):
    """Tooltip"""
    bl_idname = "fs_operators.liner_scale_scan"
    bl_label = "Add"
    bl_options = {"REGISTER", "UNDO"}

    def main_func(self, context):
        if context.scene.ufit_liner_scaling != 0:
            # execute func
            scale(context)
            remeasure_circumferences(context)  # remeasure circumferences

            # return to default state
            return_to_default_state(context, 'uFit', light='STUDIO', color_type='RANDOM')

            # prep and step
            prep_verify_scaling(context)
            set_active_step(context, 'verify_scaling', fs_path_consts, fs_ui_consts)
        else:
            # return to default state
            return_to_default_state(context, 'uFit', light='STUDIO', color_type='MATERIAL')

            # step (no prep needed)
            set_active_step(context, 'thickness', fs_path_consts, fs_ui_consts)

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='scale')
