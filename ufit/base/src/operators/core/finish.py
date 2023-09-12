import json
from datetime import datetime
import bpy
from ..utils import general, user_interface
from ....src.properties.properties import ufit_scene_properties
from ....src import base_globals


#################################
# Export Socket
#################################
def prep_export(context):
    # show the uFit Original Object
    context.scene.ufit_show_original = True

    # unshow the z-axis
    context.space_data.overlay.show_axis_z = False


def apply_remesh_modifiers(context, ufit_obj):
    # voxel remesh object to remove material between inner and outer shell
    voxel_remesh = ufit_obj.modifiers.new("Voxel Remesh", type='REMESH')
    voxel_remesh.mode = 'VOXEL'
    voxel_remesh.voxel_size = 0.0005  # Set the voxel size

    # Add a corrective smooth modifier to round corners
    corrective_smooth = ufit_obj.modifiers.new("Corrective Smooth", type='CORRECTIVE_SMOOTH')
    corrective_smooth.factor = 1
    corrective_smooth.iterations = 5  # Set the number of iterations (repeat parameter)
    corrective_smooth.smooth_type = 'LENGTH_WEIGHTED'
    corrective_smooth.use_only_smooth = True

    # apply modifiers
    # bug in blender - you have to use an override to apply the modifier
    override = {"object": ufit_obj, "active_object": ufit_obj}
    bpy.ops.object.modifier_apply(override, modifier="Voxel Remesh")
    bpy.ops.object.modifier_apply(override, modifier="Corrective Smooth")

    # decimate geometry to reduce vertices
    general.activate_object(context, ufit_obj, mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.decimate(ratio=0.05)


def upload_ufit_statistic(context):
    # update the offline count
    ufit_prefs = context.preferences.addons['ufit'].preferences
    if context.scene.ufit_device_type == 'transtibial':
        ufit_prefs.offline_transtibial_count += 1
    elif context.scene.ufit_device_type == 'transfemoral':
        ufit_prefs.offline_transfemoral_count += 1

    # create ufit statistic
    try:
        url_ufit_statistic = f'{context.scene.ufit_platform}/ugani/create/ufit_statistic'
        data = {
            "params": {
                "transtibial_count": ufit_prefs.offline_transtibial_count,
                "transfemoral_count": ufit_prefs.offline_transfemoral_count
            }
        }

        r = base_globals.platform_session.post(url=url_ufit_statistic,
                                               data=json.dumps(data),
                                               headers=base_globals.headers)

        if r.ok and r.json()['result']['success']:
            ufit_prefs.offline_transtibial_count = 0
            ufit_prefs.offline_transfemoral_count = 0
        else:
            pass

    except Exception as e:
        pass


def export_device(context):
    # only select uFit object
    ufit_obj = bpy.data.objects['uFit']
    general.activate_object(context, ufit_obj, mode='OBJECT')

    # apply remesh modifiers
    apply_remesh_modifiers(context, ufit_obj)

    # get the data name
    data_name = ufit_obj.data.name

    # get the timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if context.scene.ufit_socket_or_milling == 'socket':
        # export stl of device to checkpoints folder
        socket_name = f'{data_name}_finished_socket_{ts}.stl'
        filepath_socket = f'{context.scene.ufit_folder_modeling}/{socket_name}'
        bpy.ops.export_mesh.stl(filepath=filepath_socket, check_existing=True, filter_glob='*.stl',
                                use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False,
                                use_mesh_modifiers=True, batch_mode='OFF', axis_forward='Y', axis_up='Z')

        # export stl of the inner part to checkpoints folder
        if context.scene.ufit_total_contact_socket:
            ufit_inner_obj = bpy.data.objects['uFit_Inner']
            general.activate_object(context, ufit_inner_obj, mode='OBJECT')
            inner_part_name = f'{data_name}_finished_inner_part_{ts}.stl'
            filepath_inner_part = f'{context.scene.ufit_folder_modeling}/{inner_part_name}'
            bpy.ops.export_mesh.stl(filepath=filepath_inner_part, check_existing=True, filter_glob='*.stl',
                                    use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False,
                                    use_mesh_modifiers=True, batch_mode='OFF', axis_forward='Y', axis_up='Z')

    else:
        # export stl of device to checkpoints folder
        milling_name = f'{data_name}_finished_milling_model_{ts}.stl'
        filepath_milling = f'{context.scene.ufit_folder_modeling}/{milling_name}'
        bpy.ops.export_mesh.stl(filepath=filepath_milling, check_existing=True, filter_glob='*.stl',
                                use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False,
                                use_mesh_modifiers=True, batch_mode='OFF', axis_forward='Y', axis_up='Z')

    upload_ufit_statistic(context)


#################################
# Finish/Restart
#################################
def restart_ufit(context, custom_scene_props):
    exclude_props = [
        'ufit_full_screen',
        'ufit_active_step',
    ]

    scene_props_to_reset = list(set(ufit_scene_properties).union(custom_scene_props) - set(exclude_props))
    general.reset_ufit_properties(context, scene_props=scene_props_to_reset)

    general.delete_scene(context)
