from ...base.src.operators.core.prepare import (
    prep_move_scan, prep_clean_up, prep_verify_clean_up, prep_rotate, prep_circumferences)
from ...base.src.operators.core.sculpt import (
    prep_push_pull_smooth, prep_cutout, prep_cutout_prep, prep_scaling, prep_pull_bottom,
    prep_verify_scaling, minimal_prep_pull_bottom, minimal_prep_push_pull_smooth, prep_flare)
from ...base.src.operators.core.alignment import (
    prep_import_connector, prep_alignment, prep_transition_connector)
from ...base.src.operators.core.finish import prep_export


tt_path_consts = {
    'name': 'Transtibial',
    'paths': {
        'images_path': '/transtibial/static/images',
        'assistance_path': '/transtibial/static/images/assistance',
        'connectors_path': '/transtibial/static/connectors',
        'feet_path': '/transtibial/static/feet',
        'workflow_path': '/transtibial/src/workflow'
    },
}

tt_ui_consts = {
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
    'modal': {
        'highlight_circumferences': {
            'ui_name': 'Circumferences',
            'help_text': 'The highlighted circumferences correspond to the measurements you find in the menu. '
                         'You can always activate or deactivate this step to follow-up the measurements.'},
    },
    # keys of workflow must be in the correct order!
    'workflow': {
        'start': {
            'ui_name': 'Start Modeling'},
        'import_scan': {
            'ui_name': 'Import Scan'},
        'indicate': {
            'ui_name': 'Infrapatellar Point',
            'help_text': 'Indicate carefully the infrapatellar point. The point will later be used for alignment.'},
        'clean_up': {
            'ui_name': 'Clean Up',
            'help_text': 'Hold Left-Click and move mouse to select the relevant area of the scan. '
                         'Hold SHIFT to add more selected area. Hold CTRL to remove selected area.'},
        'verify_clean_up': {
            'ui_name': 'Verify Clean Up',
            'help_text': 'Verify the clean up is what you expected. The potential issues are highlighted.'},
        'rotate': {
            'ui_name': 'Rotate',
            'help_text': 'Use the rotation tool to align the scan. Make sure it faces directly '
                         'towards you from the front view.'},
        'circumferences': {
            'ui_name': 'Circumferences',
            'help_text': 'Add the first circumference, the rest will be calculated automatically downwards. '
                         'Choose the distance between the measurements.'},
        'push_pull_smooth': {
            'ui_name': 'Smooth/Push/Pull',
            'help_text': 'Hold Left-Click and move mouse to select an area. Use CTRL-Click to remove selected area. '
                         'Once selected, change the smooth/push/pull parameters in the menu.'},
        'pull_bottom': {
            'ui_name': 'Pull Bottom',
            'help_text': 'Hold Left-Click and move mouse to select the area at the bottom of the leg that '
                         'should be pulled downwards. Once selected, set your pulling distance in the menu.'},
        'cutout_prep': {
            'ui_name': 'Prepare Cutout',
            'help_text': 'Indicate the cutout line by adding many points. '
                         'Deselect a point by clicking it again while holding CTRL.'},
        'cutout': {
            'ui_name': 'Cutout Corrections',
            'technical_name': 'cutout',
            'help_text': 'Make corrections to the cutout curve by selecting a point using Left-Click, '
                         'press G, move mouse to the destination and Left-Click again.'},
        'scale': {
            'ui_name': 'Liner Scaling',
            'help_text': 'Scale the scan in mm or % to increase or decrease its size.'},
        'verify_scaling': {
            'ui_name': 'Verify Scaling',
            'help_text': 'Verify the scaling is what you expected.'},
        'thickness': {
            'ui_name': 'Thickness',
            'help_text': 'Choose the print thickness in mm.'},
        'flare': {
            'ui_name': 'Flare',
            'help_text': 'Provide the flare height and flare percentage in the menu, or use the interactive tool, to '
                         'add flare to your socket.'},
        'verify_socket': {
            'ui_name': 'Verify Socket',
            'help_text': 'Verify the socket is what you expected.'},
        'import_connector': {
            'ui_name': 'Import Connector & Foot',
            'help_text': 'Select a point on the bottom of the socket. '
                         'Choose your type of connector and foot in the menu.'},
        'align': {
            'ui_name': 'Alignment',
            'help_text': 'Align the socket and connector using the available options.'},
        'transition': {
            'ui_name': 'Transition',
            'help_text': 'Move the plane up and down to make sure the connector transitions nicely with the socket.'},
        'export': {
            'ui_name': 'Export Socket',
            'help_text': 'Verify the results before exporting the socket.'},
        'finish': {
            'ui_name': 'Finished'},
    },
}

tt_operator_consts = {
    'start_modeling': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': {
            'name': 'import_scan',
            'exec_save': False
        },
    },
    'start_from_existing': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
    'import_scan': {
        'checkpoint': None,
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_move_scan,
        'next_step': {
            'name': 'indicate',
            'exec_save': True
        },

    },
    'move_scan': {
        'checkpoint': {
            'name': 'indicate',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_clean_up,
        'next_step': {
            'name': 'clean_up',
            'exec_save': True
        },
    },
    'clean_up': {
        'checkpoint': {
            'name': 'clean_up',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_verify_clean_up,
        'next_step': {
            'name': 'verify_clean_up',
            'exec_save': True
        },
    },
    'verify_clean_up': {
        'checkpoint': {
            'name': 'verify_clean_up',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_rotate,
        'next_step': {
            'name': 'rotate',
            'exec_save': True
        },
    },
    'rotate': {
        'checkpoint': {
            'name': 'rotate',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_circumferences,
        'next_step': {
            'name': 'circumferences',
            'exec_save': True
        },
    },
    'circumference_add': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
    'circumferences_calc': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
    'circumferences_done': {
        'checkpoint': {
            'name': 'circumferences',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_push_pull_smooth,
        'next_step': {
            'name': 'push_pull_smooth',
            'exec_save': True
        },
    },
    'circumferences_highlight': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
    'push_pull_region': {
        'checkpoint': {
            'name': 'push_pull_smooth',
            'sub_steps': True
        },
        'default_state': None,
        'prep_func': minimal_prep_push_pull_smooth,
        'next_step': {
            'name': 'push_pull_smooth',
            'exec_save': True
        },
    },
    'smooth_region': {
        'checkpoint': {
            'name': 'push_pull_smooth',
            'sub_steps': True
        },
        'default_state': None,
        'prep_func': minimal_prep_push_pull_smooth,
        'next_step': {
            'name': 'push_pull_smooth',
            'exec_save': True
        },
    },
    'push_pull_smooth_done': {
        'checkpoint': None,
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_pull_bottom,
        'next_step': {
            'name': 'pull_bottom',
            'exec_save': False
        },
    },
    'pull_bottom': {
        'checkpoint': {
            'name': 'pull_bottom',
            'sub_steps': True
        },
        'default_state': None,
        'prep_func': minimal_prep_pull_bottom,
        'next_step': {
            'name': 'pull_bottom',
            'exec_save': True
        },
    },
    'pull_bottom_done': {
        'checkpoint': None,
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_cutout_prep,
        'next_step': {
            'name': 'cutout_prep',
            'exec_save': True
        },
    },
    'cutout_prep': {
        'checkpoint': {
            'name': 'cutout_prep',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'TEXTURE'
        },
        'prep_func': prep_cutout,
        'next_step': {
            'name': 'cutout',
            'exec_save': True
        },
    },
    'cutout': {
        'checkpoint': {
            'name': 'cutout',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'VERTEX'
        },
        'prep_func': prep_scaling,
        'next_step': {
            'name': 'scale',
            'exec_save': True
        },
    },
    'scale': {
        'checkpoint': {
            'name': 'scale',
            'sub_steps': False
        },
        'default_state': None,  # replaced by custom main_func
        'prep_func': None,  # replaced by custom main_func
        'next_step': None,  # replaced by custom main_func
    },
    'verify_scaling': {
        'checkpoint': {
            'name': 'verify_scaling',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'MATERIAL'
        },
        'prep_func': None,
        'next_step': {
            'name': 'thickness',
            'exec_save': True
        },
    },
    'thickness': {
        'checkpoint': {
            'name': 'thickness',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'MATERIAL'
        },
        'prep_func': prep_flare,
        'next_step': {
            'name': 'flare',
            'exec_save': True
        },
    },
    'flare': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': None,
    },
    'flare_done': {
        'checkpoint': {
            'name': 'flare',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'MATERIAL'
        },
        'prep_func': None,
        'next_step': {
            'name': 'verify_socket',
            'exec_save': True
        },
    },
    'verify_socket': {
        'checkpoint': {
            'name': 'verify_socket',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'VERTEX'
        },
        'prep_func': prep_import_connector,
        'next_step': {
            'name': 'import_connector',
            'exec_save': True
        },
    },
    'import_connector': {
        'checkpoint': {
            'name': 'import_connector',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'FLAT',
            'color_type': 'VERTEX'
        },
        'prep_func': prep_alignment,
        'next_step': {
            'name': 'align',
            'exec_save': True
        },
    },
    'align': {
        'checkpoint': {
            'name': 'align',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'MATERIAL'
        },
        'prep_func': prep_transition_connector,
        'next_step': {
            'name': 'transition',
            'exec_save': True
        },
    },
    'transition': {
        'checkpoint': {
            'name': 'transition',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'RANDOM'
        },
        'prep_func': prep_export,
        'next_step': {
            'name': 'export',
            'exec_save': True
        },
    },
    'export': {
        'checkpoint': {
            'name': 'export',
            'sub_steps': False
        },
        'default_state': {
            'object_name': 'uFit',
            'light': 'STUDIO',
            'color_type': 'RANDOM'
        },
        'prep_func': None,
        'next_step': {
            'name': 'finish',
            'exec_save': True
        },
    },
    'restart': {
        'checkpoint': None,
        'default_state': None,
        'prep_func': None,
        'next_step': {
            'name': 'start',
            'exec_save': False
        },
    },
}
