import os
import shutil
import zipfile
from datetime import datetime
import bpy
from .checkpoints import (
    recalc_ufit_paths,
    set_active_step,
    clear_checkpoints,
    get_workflow_step,
)
from ..utils.general import delete_scene, get_scale


#################################
# Start new / Start from existing
#################################
def start_modeling(context):
    # reset progress
    context.scene.ufit_progress = 0

    # set view_3d area full window
    # bpy.ops.wm.window_new()
    context.scene.ufit_full_screen = True


def start_from_existing(context, file_path_obj, path_consts, ui_consts, debug_step=None):
    modeling_folder = os.path.dirname(file_path_obj)
    checkpoints_dir = os.path.join(modeling_folder, "checkpoints")

    if os.path.isdir(checkpoints_dir):
        if context.scene.ufit_device_type not in modeling_folder:
            raise Exception(f"The chosen device type does not match the folder name")

        checkpoints_files = os.listdir(checkpoints_dir)
        checkpoints_files.reverse()
        latest_checkpoint = None
        active_step = None

        workflow = list(ui_consts['workflow'].keys())
        workflow.reverse()
        for step in workflow:
            for file in checkpoints_files:
                if file.startswith('ST_'):
                    wf_step = get_workflow_step(step, path_consts)
                    if wf_step \
                            and wf_step in file \
                            and 'blend1' not in file \
                            and (not debug_step or step == debug_step):
                        latest_checkpoint = os.path.join(checkpoints_dir, file)
                        active_step = step
                        break

            # also break out of big for loop
            if latest_checkpoint and active_step:
                break

        if latest_checkpoint:
            bpy.ops.wm.open_mainfile(filepath=latest_checkpoint)
            recalc_ufit_paths(context, modeling_folder, checkpoints_dir)
            set_active_step(context, active_step, path_consts, ui_consts)

            return None

    raise Exception(f"No checkpoint folder found. Please use 'Create New' for this scan.")


#################################
# Import Scan
#################################
def init_modeling_folders(context, filepath):
    file_name = os.path.basename(filepath)
    file_folder = os.path.dirname(filepath)

    # make sure you are not inside a modeling folder that already has checkpoints
    if not os.path.isdir(f'{file_folder}/checkpoints'):

        # define and create modeling folder
        ts = datetime.now().strftime("%y%m%d_%H%M%S")
        modeling_folder = f'{file_folder}/{context.scene.ufit_device_type}_{ts}'
        os.makedirs(modeling_folder)

        # scan file name and checkpoint folders
        context.scene.ufit_scan_filename = f'{file_name.split(".")[0]}'
        context.scene.ufit_folder_modeling = modeling_folder
        context.scene.ufit_folder_checkpoints = f'{modeling_folder}/checkpoints'

        # copy zip file to modeling folder
        shutil.copy2(filepath, f'{modeling_folder}/{file_name}')

        if file_name.endswith(".obj") or file_name.endswith(".stl"):
            obj_filepath = f'{modeling_folder}/{file_name}'  # not sure about the path
            context.scene.ufit_scan_filename = file_name.split(".")[0]
        else:
        # extract the zip file
            zip_extract_folder = f'{modeling_folder}/{file_name.replace(".zip", "")}'
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(zip_extract_folder)

        # store checkpoints folder and scan_filename
            obj_filepath = None
            for file in os.listdir(zip_extract_folder):
                if file.endswith(".obj") or file.endswith(".stl"):
                    obj_filepath = f'{zip_extract_folder}/{file}'
                    context.scene.ufit_scan_filename = file.split(".")[0]
                    break

        if not obj_filepath:
            raise Exception('Could not find an .obj or .stl file in scan folder')

        clear_checkpoints(context)

        return obj_filepath

    else:
        raise Exception(f"Found checkpoints folder. You can't use 'Create New' in this location.")


def import_zip(context, filepath):
    # delete everything from the scene
    delete_scene(context)

    # load the new object
    if filepath.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=filepath)
    elif filepath.endswith(".stl"):
        bpy.ops.import_scene.stl(filepath=filepath)

    # rename the object
    obj_scan = bpy.context.selected_objects[0]
    obj_scan.name = 'uFit'

    # remove any rotation, location and scaling changes
    obj_scan.rotation_euler = (0, 0, 0)
    obj_scan.location = (0, 0, 0)
    obj_scan.scale = (1, 1, 1)

    # Perform scaling by user defined unit
    unit = context.scene.ufit_import_unit
    obj_scan.scale = get_scale(unit)

    # activate object
    context.view_layer.objects.active = obj_scan

    # apply scaling
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
