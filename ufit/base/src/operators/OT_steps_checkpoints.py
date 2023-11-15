import bpy
from .core.OT_base import OTBase
from ....base.src.operators.core.checkpoints import rollback_to_checkpoint, previous_step
from ....transtibial.src.transtibial_constants import tt_path_consts, tt_ui_consts
from ....transfemoral.src.transfemoral_constants import tf_path_consts, tf_ui_consts
from ....free_sculpting.src.free_sculpting_constants import fs_path_consts, fs_ui_consts


class OTCheckpointRollback(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.checkpoint_rollback"
    bl_label = "Rollback"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'checkpoint_rollback')

    def main_func(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                rollback_to_checkpoint(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                rollback_to_checkpoint(context, tf_path_consts, tf_ui_consts)
            elif context.scene.ufit_device_type == 'free_sculpting':
                rollback_to_checkpoint(context, fs_path_consts, fs_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))


class OTPreviousStep(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.prev_step"
    bl_label = "Previous Step"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'prev_step')

    def main_func(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                previous_step(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                previous_step(context, tf_path_consts, tf_ui_consts)
            elif context.scene.ufit_device_type == 'free_sculpting':
                previous_step(context, fs_path_consts, fs_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))


class OTNextStep(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.next_step"
    bl_label = "Previous Step"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'prev_step')

    def main_func(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                previous_step(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                previous_step(context, tf_path_consts, tf_ui_consts)
            elif context.scene.ufit_device_type == 'free_sculpting':
                previous_step(context, fs_path_consts, fs_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))
