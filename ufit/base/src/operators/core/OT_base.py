import bpy
from abc import abstractmethod
from .....base.src.operators.core.checkpoints import set_active_step, add_checkpoint, rollback_to_checkpoint
from .....base.src.operators.utils.general import return_to_default_state
from ...base_constants import base_path_consts, base_ui_consts, base_operator_consts


class OTBase(bpy.types.Operator):
    def execute_base(self, context, operator_name):
        path_consts = self.get_path_consts()
        ui_consts = self.get_ui_consts()
        operator_consts = self.get_operator_consts(operator_name)

        checkpoint = operator_consts.get('checkpoint')
        next_step = operator_consts.get('next_step')

        print(f'next step: {next_step}')

        # reset the error message
        context.scene.ufit_error_message = ""

        try:
            # add checkpoint
            if checkpoint:
                add_checkpoint(context, checkpoint['name'], path_consts, ui_consts, checkpoint.get('sub_steps'))

            # execute func
            self.main_func(context)

            # move to next step
            if next_step:
                if not next_step.get('conditions'):
                    prep_func = next_step.get('prep_func')
                    default_state = next_step.get('default_state')

                    if default_state:
                        return_to_default_state(context,
                                                **default_state)

                    if prep_func:
                        prep_func(context)

                    set_active_step(context,
                                    step=next_step['name'],
                                    path_consts=path_consts,
                                    ui_consts=ui_consts,
                                    exec_save=next_step['exec_save'])

                else:  # conditions
                    for step in next_step.get('conditions'):
                        condition_func = step.get('condition_func')
                        if condition_func(context):
                            prep_func = step.get('prep_func')
                            default_state = step.get('default_state')

                            if default_state:
                                return_to_default_state(context,
                                                        **default_state)

                            if prep_func:
                                prep_func(context)

                            set_active_step(context,
                                            step=step['name'],
                                            path_consts=path_consts,
                                            ui_consts=ui_consts,
                                            exec_save=step['exec_save'])
                            break

        except Exception as e:
            if checkpoint:
                # a checkpoint has been saved while an exception appeared (remove the last checkpoint from collection)
                collection = context.scene.ufit_checkpoint_collection
                positive_index = collection.find(context.scene.ufit_checkpoint_collection[-1].name)
                collection.remove(positive_index)  # can only remove positive indexes

            context.scene.ufit_error_message = str(e)

            self.report({'ERROR'}, str(e))

        return {'FINISHED'}

    def get_path_consts(self):
        return base_path_consts

    def get_ui_consts(self):
        return base_ui_consts

    def get_operator_consts(self, operator_name):
        operator_vars = base_operator_consts.get(operator_name)
        if operator_vars:
            return operator_vars
        else:
            raise ValueError(f"Unknown operator name: {operator_name}")

    @abstractmethod
    def main_func(self, context):
        # Modify this method to implement the main functionality of this operator
        pass
