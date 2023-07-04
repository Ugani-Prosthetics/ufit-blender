import bpy
from ....base.src.operators.core.checkpoints import rollback_to_checkpoint, previous_step
from ....transtibial.src.transtibial_constants import tt_path_consts, tt_ui_consts
from ....transfemoral.src.transfemoral_constants import tf_path_consts, tf_ui_consts


class OTCheckpointRollback(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ufit_operators.checkpoint_rollback"
    bl_label = "Rollback"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                rollback_to_checkpoint(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                rollback_to_checkpoint(context, tf_path_consts, tf_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))

        return {'FINISHED'}


class OTPreviousStep(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ufit_operators.prev_step"
    bl_label = "Previous Step"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                previous_step(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                previous_step(context, tf_path_consts, tf_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))

        return {'FINISHED'}



class OTNextStep(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ufit_operators.next_step"
    bl_label = "Previous Step"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # always make it possible
        return True

    def execute(self, context):
        try:
            if context.scene.ufit_device_type == 'transtibial':
                previous_step(context, tt_path_consts, tt_ui_consts)
            elif context.scene.ufit_device_type == 'transfemoral':
                previous_step(context, tf_path_consts, tf_ui_consts)
            else:
                self.report({'ERROR'}, f'Could not find a module with name {context.scene.ufit_device_type}')

        except Exception as e:
            self.report({'ERROR'}, str(e))

        return {'FINISHED'}