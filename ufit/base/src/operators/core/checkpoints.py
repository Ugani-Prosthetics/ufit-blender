import os
import re
import bpy
from ..utils.general import set_ufit_logo


#################################
# Steps
#################################
def fill_history_with_null_operations():
    # keep looping until the context is filled after opening a new file
    if bpy.context.window is None:
        bpy.app.timers.register(fill_history_with_null_operations, first_interval=0.1)

    for i in range(0, bpy.context.preferences.edit.undo_steps):
        bpy.ops.ed.undo_push(message="null operation")


def update_progress(context, step, workflow):
    for i, t in enumerate(workflow.keys()):
        if t == step:
            # do not include the "start" step
            context.scene.ufit_progress = (i - 2) / (len(workflow.keys()) - 3) * 100


def set_active_step(context, step, path_consts, ui_consts, exec_save=True):
    bpy.types.Scene.ufit_active_step = step

    if exec_save:
        # workaround to undo the history after each step
        file_path = f'{context.scene.ufit_folder_checkpoints}/{context.scene.ufit_scan_filename}.blend'

        bpy.ops.wm.save_as_mainfile(filepath=file_path, copy=True)
        bpy.ops.wm.open_mainfile(filepath=file_path)

        set_ufit_logo()  # reset logo because textures are removed when opening new files
        set_assistance(step, path_consts, ui_consts)

        update_progress(context, step, ui_consts['workflow'])

        # fill the history by pushing "null operation" undo steps
        # WORKAROUND: context is removed when opening a new main file
        bpy.app.timers.register(fill_history_with_null_operations, first_interval=0.1)
    else:
        set_ufit_logo()


def set_assistance(step, path_consts, ui_consts):
    if (ui_consts['workflow'].get(step) and ui_consts['workflow'][step].get('help_text')) or \
            (ui_consts['modal'].get(step) and ui_consts['modal'][step].get('help_text')):
        # set help text
        if ui_consts['workflow'].get(step):
            bpy.context.scene.ufit_help_text = ui_consts['workflow'][step]['help_text']
        else:
            bpy.context.scene.ufit_help_text = ui_consts['modal'][step]['help_text']

        # set paths to assistance image
        assistance_dir = os.path.join(os.path.dirname(__file__),
                                      f"../../../..{path_consts['paths']['assistance_path']}/{step}")
        if os.path.isdir(assistance_dir):
            bpy.context.scene.ufit_assistance_previews_dir = assistance_dir
        else:
            bpy.context.scene.ufit_assistance_previews_dir = ''


def set_modal_step(context, modal_func, name):
    # calculate paths
    current_file_path = f'{context.scene.ufit_folder_checkpoints}/{context.scene.ufit_scan_filename}.blend'
    modal_file_path = f'{context.scene.ufit_folder_checkpoints}/{name}.blend'

    bpy.ops.wm.save_as_mainfile(filepath=current_file_path, copy=True)  # first save the current file/step
    bpy.ops.wm.save_as_mainfile(filepath=modal_file_path, copy=True)  # then save the modal file/step
    bpy.ops.wm.open_mainfile(filepath=modal_file_path)  # open the modal file

    # WORKAROUND: context is removed when opening a new main file
    # 1. fill the history by pushing "null operation" undo steps
    # 2. execute the modal_func to prepare the scene
    bpy.app.timers.register(fill_history_with_null_operations, first_interval=0.1)
    bpy.app.timers.register(modal_func, first_interval=0.1)


def close_modal_step(context, path_consts, ui_consts):
    file_path = f'{context.scene.ufit_folder_checkpoints}/{context.scene.ufit_scan_filename}.blend'
    bpy.ops.wm.open_mainfile(filepath=file_path)  # open the modal file

    # reset step (assistance image)
    set_active_step(context, context.scene.ufit_active_step, path_consts, ui_consts)


def previous_step(context, path_consts, ui_consts):
    if context.scene.ufit_active_step == 'start':
        set_active_step(context,
                        step='device_type',
                        path_consts=None,
                        ui_consts=None,
                        exec_save=False)
    elif context.scene.ufit_active_step == 'import_scan':
        set_active_step(context,
                        step='start',
                        path_consts=None,
                        ui_consts=None,
                        exec_save=False)
    else:
        cp_rollback = context.scene.ufit_checkpoint_collection[-1]
        context.scene.ufit_checkpoints = cp_rollback.name

        rollback_to_checkpoint(context, path_consts, ui_consts)


#################################
# Checkpoints
#################################
# in case of working in a drive, the paths need to be recalculated
# todo: work with relative paths!
def recalc_ufit_paths(context, modeling_folder, checkpoints_dir):
    # make backwards compatible (when modeling folder was not defined yet)
    if not context.scene.ufit_folder_modeling:
        cp = context.scene.ufit_checkpoint_collection[0]
        old_checkpoints_folder = os.path.dirname(cp.file_path)
        context.scene.ufit_folder_modeling = os.path.dirname(old_checkpoints_folder)  # the old modeling folder

    # recalculate path variables
    for cp in context.scene.ufit_checkpoint_collection:
        cp.file_path = cp.file_path.replace(context.scene.ufit_folder_modeling, modeling_folder)

    # reset modeling and checkpoints folder
    context.scene.ufit_folder_modeling = modeling_folder
    context.scene.ufit_folder_checkpoints = checkpoints_dir


def clear_checkpoints(context):
    # clear or create checkpoint folder
    if not os.path.exists(context.scene.ufit_folder_checkpoints):
        os.makedirs(context.scene.ufit_folder_checkpoints)
    else:
        for fname in os.listdir(context.scene.ufit_folder_checkpoints):
            os.remove(f'{context.scene.ufit_folder_checkpoints}/{fname}')

    # remove checkpoint list
    context.scene.ufit_checkpoint_collection.clear()


def get_checkpoint_files(context, step_nr, sub_step_nr=0):
    # get all checkpoint files above a specific step
    files = []
    for cp in context.scene.ufit_checkpoint_collection:
        if int(cp.step_nr) > step_nr or \
                (int(cp.step_nr) == step_nr and int(cp.sub_step_nr) > sub_step_nr):
            files.append(str(cp.file_path))

    return files


def get_workflow_step(step, path_consts):
    # get list of steps from workflow
    workflow_dir = os.path.join(os.path.dirname(__file__), f'../../../..{path_consts["paths"]["workflow_path"]}')
    workflow_steps = os.listdir(workflow_dir)
    sorted(workflow_steps)

    # find step and assign to checkpoint filename
    workflow_step = None
    for ws in workflow_steps:
        if ws.startswith('ST_'):
            ws_splitted = ws.split('_', 2)  # splits on the first and second underscore
            if step == ws_splitted[2]:  # check if equal to the third split
                workflow_step = ws
                break

    return workflow_step


def get_workflow_step_nr(step, path_consts, raise_exception=True):
    workflow_step = get_workflow_step(step, path_consts)

    if workflow_step:
        # Define the regular expression pattern to match the number
        pattern = r'\d+'

        # Use the re.search() function to find the first match of the pattern in the string
        match = re.search(pattern, workflow_step)

        # Extract the matched substring and convert it to an integer
        return int(match.group())
    else:
        if raise_exception:
            raise Exception('Could not find a workflow step number.')
        return -1


def add_checkpoint(context, step, path_consts, ui_consts, sub_steps):
    workflow_step = get_workflow_step(step, path_consts)
    step_nr = get_workflow_step_nr(step, path_consts)

    if not sub_steps:
        context.scene.ufit_substep = 0

    if workflow_step:
        workflow = ui_consts['workflow']

        # save the file
        file_name = f"{workflow_step}_{context.scene.ufit_substep}.blend"
        file_path = f'{context.scene.ufit_folder_checkpoints}/{file_name}'
        bpy.ops.wm.save_as_mainfile(filepath=file_path)

        # add the checkpoint
        name = f'{workflow[step]["ui_name"]} {context.scene.ufit_substep}' if context.scene.ufit_substep != 0 else f'{workflow[step]["ui_name"]}'
        checkpoint_item = context.scene.ufit_checkpoint_collection.add()  # add an item to the property collection
        checkpoint_item.step = step
        checkpoint_item.step_nr = step_nr
        checkpoint_item.sub_step_nr = context.scene.ufit_substep
        checkpoint_item.name = name  # set the property 'step' of the Checkpoint_PG item
        checkpoint_item.file_path = file_path

        if sub_steps:
            context.scene.ufit_substep += 1
    else:
        raise Exception('Could not save the checkpoint.')


def rollback_to_checkpoint(context, path_consts, ui_consts):
    # add the current step so that the file will be removed
    add_checkpoint(context, context.scene.ufit_active_step, path_consts, ui_consts, context.scene.ufit_substep)

    cp_rollback = context.scene.ufit_checkpoints
    for cp in context.scene.ufit_checkpoint_collection:
        if cp.name == cp_rollback:
            step = str(cp.step)  # make a copy as cp is lost when loading file
            step_nr = get_workflow_step_nr(step, path_consts)
            sub_step_nr = int(cp.sub_step_nr)  # make a copy as cp is lost when loading file
            file_path = str(cp.file_path)  # make a copy as cp is lost when loading file

            files_to_remove = get_checkpoint_files(context, step_nr, sub_step_nr)

            for f in files_to_remove:
                if os.path.isfile(f):
                    os.remove(f)
                if os.path.isfile(f.replace('.blend', '.blend1')):  # also remove the blend1 file if it exists
                    os.remove(f.replace('.blend', '.blend1'))

            checkpoints_dir = os.path.dirname(file_path)
            modeling_folder = os.path.dirname(checkpoints_dir)

            bpy.ops.wm.open_mainfile(filepath=file_path)
            recalc_ufit_paths(context, modeling_folder, checkpoints_dir)
            set_active_step(context, step, path_consts, ui_consts)
