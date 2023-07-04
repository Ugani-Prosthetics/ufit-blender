import bpy
from abc import abstractmethod
from .....base.src.operators.core.checkpoints import set_active_step, add_checkpoint
from .....base.src.operators.utils.general import return_to_default_state
from ...base_constants import base_path_consts, base_ui_consts, base_operator_consts


class OTBase(bpy.types.Operator):
    def execute_base(self, context, operator_name):
        try:
            path_consts = self.get_path_consts()
            ui_consts = self.get_ui_consts()
            operator_consts = self.get_operator_consts(operator_name)
            checkpoint = operator_consts.get('checkpoint')
            prep_func = operator_consts.get('prep_func')
            next_step = operator_consts.get('next_step')
            default_state = operator_consts.get('default_state')

            # add checkpoint
            if checkpoint:
                if checkpoint.get('sub_steps'):
                    add_checkpoint(context, checkpoint['name'], path_consts, ui_consts, sub_step_nr=context.scene.ufit_substep)
                else:
                    add_checkpoint(context, checkpoint['name'], path_consts, ui_consts)

            # execute func
            self.main_func(context)

            # return to default state
            if default_state:
                return_to_default_state(context,
                                        object_name=default_state['object_name'],
                                        light=default_state['light'],
                                        color_type=default_state['color_type'])

            # prep and step
            if prep_func:
                prep_func(context)

            if next_step:
                set_active_step(context,
                                step=next_step['name'],
                                path_consts=path_consts,
                                ui_consts=ui_consts,
                                exec_save=next_step['exec_save'])

        except Exception as e:
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
