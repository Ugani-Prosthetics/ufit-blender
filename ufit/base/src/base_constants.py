
base_path_consts = {
    'name': 'Base',
    'paths': {
        'images_path': '/base/static/images',
    },
}

base_ui_consts = {
    'persistent': {
        'view': {
            'ui_name': 'View'
        },
        'ufit_gizmo': {
            'ui_name': 'View Modes'
        },
        'checkpoints': {
            'ui_name': 'Checkpoints'
        },
        'assistance': {
            'ui_name': 'Assistance'
        },
        'progress': {
            'ui_name': 'Progress'
        },
    },
    'workflow': {
        'device_type': {
            'ui_name': 'Device Type'
        }
    }
}


base_operator_consts = {
    'platform_login': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': {
            'name': 'device_type',
            'exec_save': False
        },
    },
    'device_type': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
}
