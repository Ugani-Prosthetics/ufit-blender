import os
import sys
from datetime import datetime
import configparser
import bpy
from bpy.app.handlers import persistent
from .config_ufit import configure_logging, configure_full_debug, logger
from .base.src import base_globals
from .base.src.operators.utils import user_interface
from .base.src.operators.utils.general import set_ufit_logo
from .base.src.operators.utils.authenticate import platform_authenticate, is_authenticated, set_ufit_authetication_vars

bl_info = {
    "name": "uFit",
    "author": "Ugani Prosthetics",
    "blender": (3, 5, 0),
    "category": "O&P",
    "version": (2, 2, 2)
}

modulesNames = [
    'base',
    'transtibial',
    'transfemoral',
    'free_sculpting',
]

enable_addons = [
    'pose_library',
    'io_scene_fbx',
    'io_curve_svg',
    'io_mesh_ply',
    'io_mesh_stl',
    'io_mesh_uv_layout',
    'io_scene_obj',
    'io_scene_x3d',
    'io_scene_gltf2',
    'space_view3d_copy_attributes',
    'object_print3d_utils',
    'mesh_looptools',
    'mesh_tissue',
    'node_wrangler',
    'cycles',
]

modules_full_names = {}
for mod in modulesNames:
    modules_full_names[mod] = ('{}.{}'.format(__name__, mod))


def read_ini():
    # Get the current script's directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config_file_path = os.path.join(current_dir, 'ufit.ini')

    # Create a ConfigParser object and read the ini file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    return config


def load_ufit_config():
    config = read_ini()
    full_debug_mode = config.getboolean('full_debug', 'full_debug_mode')

    # configure full debug mode
    if full_debug_mode:
        configure_full_debug(
            context=bpy.context,
            workspace=config.get('full_debug', 'workspace'),
            ufit_device=config.get('full_debug', 'ufit_device'),
            ufit_step=config.get('full_debug', 'ufit_step')
        )


def reload_modules():
    import importlib

    for current_module_full_name in modules_full_names.values():
        if current_module_full_name in sys.modules.keys():
            logger.debug(f'reloading module now: {current_module_full_name}')
            importlib.reload(sys.modules[current_module_full_name])
        else:
            logger.debug(f'importing module now: {current_module_full_name}')
            globals()[current_module_full_name] = importlib.import_module(current_module_full_name)
            setattr(globals()[current_module_full_name], 'modulesNames', modules_full_names)


# function should only be executed once the scene is available (after Blender is fully loaded)
def init_ufit():
    # keep looping until the context is filled after opening a new file
    if bpy.context.window is None:
        bpy.app.timers.register(init_ufit, first_interval=0.1)

    user_interface.open_n_sidebar()
    # bpy.context.scene.ufit_full_screen = True  # as of Blender 3.5.1 - Blender crashes with full screen

    set_ufit_logo()
    bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'
    user_interface.set_outliner_restriction('show_restrict_column_select', True)

    if not base_globals.debug_enabled:
        platform_authenticate(bpy.context)
    else:
        set_ufit_authetication_vars(bpy.context)

    # jump to device_type step if authenticated OR last_authenticated is less than 10 days ago
    if bpy.context.scene.ufit_active_step == 'platform_login':
        ufit_prefs = bpy.context.preferences.addons['ufit'].preferences
        now = datetime.now()

        days_diff = 100  # more than 10
        if ufit_prefs.last_authentication:
            last_authenticated = datetime.strptime(ufit_prefs.last_authentication, "%Y%m%d_%H%M%S")
            delta = now - last_authenticated
            days_diff = delta.days

        if is_authenticated() and \
                (days_diff <= 10 and bpy.context.scene.ufit_user and bpy.context.scene.ufit_password):  # make sure authentication happens every 10 days
            bpy.context.scene.ufit_active_step = 'device_type'
            load_ufit_config()


# @persistent
# def handler_blender_loaded(scene):
#     init_ufit()


def register():
    for addon in enable_addons:
        user_interface.enable_addon(addon)
    user_interface.set_theme_vertex_size(1)
    user_interface.set_input_preference('use_rotate_around_active', True)
    user_interface.set_input_preference('use_zoom_to_mouse', True)
    user_interface.set_input_preference('use_auto_perspective', False)

    # configure logging (should be done here due to authentication logging)
    config = read_ini()
    enable_debug = config.getboolean('debug', 'enable_debug')
    configure_logging(enable_debug)

    # reload modules
    reload_modules()
    for current_module_name in modules_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], 'register'):
                sys.modules[current_module_name].register()

    # DON'T USE HANDLER!
    # bpy.app.handlers.load_post.append(handler_blender_loaded)  # wait until scene is loaded

    # use timer instead of handler so that it also works on installation of addon
    bpy.app.timers.register(init_ufit, first_interval=0.1)


def unregister():
    for current_module_name in modules_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], 'unregister'):
                sys.modules[current_module_name].unregister()


# if __name__ == "__main__":
#     register()
