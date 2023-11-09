from ...base.src.operators.core.prepare import (
    prep_move_scan, prep_clean_up, prep_verify_clean_up, prep_rotate)
from ...base.src.operators.core.sculpt import (
    prep_push_pull_smooth, minimal_prep_push_pull_smooth, create_thickness, minimal_prep_free_sculpt,
    prep_custom_thickness, minimal_prep_custom_thickness)
from ...base.src.operators.core.finish import prep_export


fs_path_consts = {
    'name': 'Free_sculpting',
    'paths': {
        'images_path': '/free_sculpting/static/images',
        'assistance_path': '/free_sculpting/static/images/assistance',
        'workflow_path': '/free_sculpting/src/workflow'
    },
}

fs_ui_consts = {
    'persistent': {},
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
            'ui_name': 'Indicate',
            'help_text': 'Indicate carefully the point. The point will later be used for alignment.'},
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
        'push_pull_smooth': {
            'ui_name': 'Sculpt',
            'help_text': 'For guided sculpting, hold Left-Click and move mouse to highlight an area. '
                         'Use CTRL-Click to remove highlighted area. '
                         'Once the area is highlighted, use the options in the menu to perform an action'},
        'thickness': {
            'ui_name': 'Base Thickness',
            'help_text': 'Choose the base 3D printing thickness in mm.'},
        'custom_thickness': {
            'ui_name': 'Custom Thickness',
            'help_text': 'Highlight the region that you would like to give custom thickness. '
                         'Use the apply thickness button to see the result.'},
        'export': {
            'ui_name': 'Export Model',
            'help_text': 'Verify the results before exporting the model.'},
        'finish': {
            'ui_name': 'Finished'},
    },
}

fs_operator_consts = {
    'start_modeling': {
        'checkpoint': None,
        'next_step': {
            'name': 'import_scan',
            'default_state': None,
            'prep_func': None,
            'exec_save': False
        },
    },
    'start_from_existing': {
        'checkpoint': None,
        'next_step': None,
    },
    'import_scan': {
        'checkpoint': None,
        'next_step': {
            'name': 'indicate',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_move_scan,
            'exec_save': True
        },

    },
    'move_scan': {
        'checkpoint': {
            'name': 'indicate',
            'sub_steps': False
        },
        'next_step': {
            'name': 'clean_up',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_clean_up,
            'exec_save': True
        },
    },
    'clean_up': {
        'checkpoint': {
            'name': 'clean_up',
            'sub_steps': False
        },
        'next_step': {
            'name': 'verify_clean_up',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_verify_clean_up,
            'exec_save': True
        },
    },
    'highlight_non_manifold': {
        'checkpoint': None,
        'next_step': None,
    },
    'fill_non_manifold': {
        'checkpoint': {
            'name': 'verify_clean_up',
            'sub_steps': True
        },
        'next_step': {
            'name': 'verify_clean_up',
            'default_state': None,
            'prep_func': None,
            'exec_save': True
        },
    },
    'delete_non_manifold': {
        'checkpoint': {
            'name': 'verify_clean_up',
            'sub_steps': True
        },
        'next_step': {
            'name': 'verify_clean_up',
            'default_state': None,
            'prep_func': None,
            'exec_save': True
        },
    },
    'verify_clean_up': {
        'checkpoint': {
            'name': 'verify_clean_up',
            'sub_steps': False
        },
        'next_step': {
            'name': 'rotate',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE',
                'overlay_axes': (1, 1, 1),
                'overlay_text': True
            },
            'prep_func': prep_rotate,
            'exec_save': True
        },
    },
    'rotate': {
        'checkpoint': {
            'name': 'rotate',
            'sub_steps': False
        },
        'next_step': {
            'name': 'push_pull_smooth',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_push_pull_smooth,
            'exec_save': True,
        },
    },

    'push_pull_region': {
        'checkpoint': {
            'name': 'push_pull_smooth',
            'sub_steps': True
        },
        'next_step': {
            'name': 'push_pull_smooth',
            'default_state': None,
            'prep_func': minimal_prep_push_pull_smooth,
            'exec_save': True
        },
    },
    'smooth_region': {
        'checkpoint': {
            'name': 'push_pull_smooth',
            'sub_steps': True
        },
        'next_step': {
            'name': 'push_pull_smooth',
            'default_state': None,
            'prep_func': minimal_prep_push_pull_smooth,
            'exec_save': True
        },
    },
    'free_sculpt_checkpoint': {
        'checkpoint': {
            'name': 'push_pull_smooth',
            'sub_steps': True
        },
        'next_step': {
            'name': 'push_pull_smooth',
            'default_state': None,
            'prep_func': minimal_prep_free_sculpt,
            'exec_save': True
        },
    },
    'push_pull_smooth_done': {
        'checkpoint': {
            'name': 'push_pull_smooth',  # also add a checkpoint once done
            'sub_steps': True
        },
        'next_step': {
            'name': 'thickness',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL'
            },
            'prep_func': create_thickness,
            'exec_save': True
        },
    },
    'thickness': {
        'checkpoint': {
            'name': 'thickness',
            'sub_steps': False
        },
        'next_step': {
            'name': 'custom_thickness',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL'
            },
            'prep_func': prep_custom_thickness,
            'exec_save': True
        },
    },
    'custom_thickness': {
        'checkpoint': {
            'name': 'custom_thickness',
            'sub_steps': True
        },
        'next_step': {
            'name': 'custom_thickness',
            'default_state': None,
            'prep_func': minimal_prep_custom_thickness,
            'exec_save': True
        },
    },
    'custom_thickness_done': {
        'checkpoint': {
            'name': 'custom_thickness',
            'sub_steps': True
        },
        'next_step': {
            'name': 'export',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'RANDOM'
            },
            'prep_func': prep_export,
            'exec_save': True
        },
    },
    'export': {
        'checkpoint': {
            'name': 'export',
            'sub_steps': False
        },
        'next_step': {
            'name': 'finish',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'RANDOM'
            },
            'prep_func': None,
            'exec_save': True
        },
    },
    'restart': {
        'checkpoint': None,
        'next_step': {
            'name': 'start',
            'default_state': None,
            'prep_func': None,
            'exec_save': False
        },
    },
}
