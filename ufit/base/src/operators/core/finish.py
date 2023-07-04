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


def upload_ufit_statistic(context):
    print('in upload statistic')
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

    # get the data name
    data_name = ufit_obj.data.name

    # export stl to checkpoints folder
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    socket_name = f'{data_name}_finished_socket_{ts}.stl'

    if context.scene.ufit_folder_modeling:
        filepath = f'{context.scene.ufit_folder_modeling}/{socket_name}'
    else:
        filepath = f'{context.scene.ufit_folder_checkpoints}/{socket_name}'

    bpy.ops.export_mesh.stl(filepath=filepath, check_existing=True, filter_glob='*.stl',
                            use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False,
                            use_mesh_modifiers=True, batch_mode='OFF', axis_forward='Y', axis_up='Z')

    print('calling upload statistic')
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
