import sys
from datetime import datetime
import bpy
from bpy.app.handlers import persistent
from .base.src.operators.utils import user_interface
from .base.src.operators.utils.general import set_ufit_logo
from .base.src.operators.utils.authenticate import platform_authenticate, is_authenticated

bl_info = {
    "name": "uFit",
    "author": "Ugani Prosthetics",
    "blender": (3, 5, 0),
    "category": "O&P",
    "version": (1, 1, 0)
}

modulesNames = [
    'base',
    'transtibial',
    'transfemoral',
]

modules_full_names = {}
for mod in modulesNames:
    modules_full_names[mod] = ('{}.{}'.format(__name__, mod))


def reload_modules():
    import importlib

    for current_module_full_name in modules_full_names.values():
        if current_module_full_name in sys.modules.keys():
            print(f'reloading module now: {current_module_full_name}')
            importlib.reload(sys.modules[current_module_full_name])
        else:
            print(f'importing module now: {current_module_full_name}')
            globals()[current_module_full_name] = importlib.import_module(current_module_full_name)
            setattr(globals()[current_module_full_name], 'modulesNames', modules_full_names)


# function should only be executed once the scene is available (after Blender is fully loaded)
def init_ufit():
    # keep looping until the context is filled after opening a new file
    if bpy.context.window is None:
        bpy.app.timers.register(init_ufit, first_interval=0.1)

    set_ufit_logo()
    bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'
    user_interface.set_outliner_restriction('show_restrict_column_select', True)
    platform_authenticate(bpy.context)

    # jump to device_type step if authenticated OR last_authenticated is less than 10 days ago
    if bpy.context.scene.ufit_active_step == 'platform_login':
        ufit_prefs = bpy.context.preferences.addons['ufit'].preferences
        now = datetime.now()

        days_diff = 100  # more than 10
        if ufit_prefs.last_authentication:
            last_authenticated = datetime.strptime(ufit_prefs.last_authentication, "%Y%m%d_%H%M%S")
            delta = now - last_authenticated
            days_diff = delta.days

        if is_authenticated() or days_diff <= 10:  # make sure authentication happens every 10 days
            bpy.context.scene.ufit_active_step = 'device_type'


@persistent
def handler_blender_loaded(scene):
    init_ufit()


def register():
    user_interface.enable_addon('mesh_looptools')
    user_interface.enable_addon('object_print3d_utils')
    user_interface.set_theme_vertex_size(1)
    user_interface.set_input_preference('use_rotate_around_active', True)
    user_interface.set_input_preference('use_zoom_to_mouse', True)
    user_interface.set_input_preference('use_auto_perspective', False)

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
