
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
        'report_problem': {
            'ui_name': 'Report Problem'
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
        'next_step': {
            'name': 'device_type',
            'default_state': None,
            'prep_func': None,
            'exec_save': False
        },
    },
    'device_type': {
        'checkpoint': None,
        'next_step': {
            'name': 'start',
            'default_state': None,
            'prep_func': None,
            'exec_save': False
        },
    },
    'report_problem': {
        'checkpoint': None,
        'next_step': None
    },
    'gizmo': {
        'checkpoint': None,
        'next_step': None
    },
    'checkpoint_rollback': {
        'checkpoint': None,
        'next_step': None
    },
    'prev_step': {
        'checkpoint': None,
        'next_step': None
    },
    'next_step': {
        'checkpoint': None,
        'next_step': None
    },
}
