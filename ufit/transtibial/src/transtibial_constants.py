from ...base.src.operators.core.prepare import (
    prep_move_scan, prep_clean_up, prep_verify_clean_up, prep_rotate, prep_circumferences)
from ...base.src.operators.core.sculpt import (
    prep_push_pull_smooth, prep_cutout, prep_cutout_prep, prep_scaling, prep_pull_bottom,
    prep_verify_scaling, minimal_prep_pull_bottom, minimal_prep_push_pull_smooth, minimal_prep_free_sculpt,
    prep_custom_thickness, prep_flare)
from ...base.src.operators.core.alignment import (
    prep_import_connector, prep_alignment, prep_transition_connector)
from ...base.src.operators.core.finish import prep_export


def socket_condition(context):
    return context.scene.ufit_socket_or_milling == "socket"


def milling_condition(context):
    return context.scene.ufit_socket_or_milling == "milling"


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
            'ui_name': 'Sculpt',
            'help_text': 'For guided sculpting, hold Left-Click and move mouse to highlight an area. '
                         'Use CTRL-Click to remove highlighted area. '
                         'Once the area is highlighted, use the options in the menu to perform an action'},
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
            'ui_name': 'Scaling',
            'help_text': 'Scale the scan in mm or % to increase or decrease its size.'},
        'verify_scaling': {
            'ui_name': 'Verify Scaling',
            'help_text': 'Verify the scaling is what you expected.'},
        'socket_milling': {
            'ui_name': 'Socket or Milling',
            'help_text': 'Choose "Socket" if you would you like to create a full 3D socket. '
                         'Choose "Milling" if you would like to create a positive model for CNC carving?'},
        'milling_model': {
            'ui_name': 'Milling Model',
            'help_text': 'Create your milling model by choosing your parameters in the menu and clicking next.'},
        'thickness': {
            'ui_name': 'Base Thickness',
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
            'ui_name': 'Export Model',
            'help_text': 'Verify the results before exporting the model.'},
        'finish': {
            'ui_name': 'Finished'},
    },
}

tt_operator_consts = {
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
            'name': 'circumferences',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE',
            },
            'prep_func': prep_circumferences,
            'exec_save': True
        },
    },
    'circumference_add': {
        'checkpoint': None,
        'next_step': None,
    },
    'circumferences_calc': {
        'checkpoint': None,
        'next_step': None,
    },
    'circumferences_done': {
        'checkpoint': {
            'name': 'circumferences',
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
            'exec_save': True
        },
    },
    'circumferences_highlight': {
        'checkpoint': None,
        'next_step': None,
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
            'name': 'pull_bottom',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_pull_bottom,
            'exec_save': False
        },
    },
    'pull_bottom': {
        'checkpoint': {
            'name': 'pull_bottom',
            'sub_steps': True
        },
        'next_step': {
            'name': 'pull_bottom',
            'default_state': None,
            'prep_func': minimal_prep_pull_bottom,
            'exec_save': True
        },
    },
    'pull_bottom_done': {
        'checkpoint': None,
        'next_step': {
            'name': 'cutout_prep',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_cutout_prep,
            'exec_save': True
        },
    },
    'cutout_prep': {
        'checkpoint': {
            'name': 'cutout_prep',
            'sub_steps': False
        },
        'next_step': {
            'name': 'cutout',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'TEXTURE'
            },
            'prep_func': prep_cutout,
            'exec_save': True
        },
    },
    'cutout': {
        'checkpoint': {
            'name': 'cutout',
            'sub_steps': False
        },
        'next_step': {
            'name': 'scale',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'VERTEX'
            },
            'prep_func': prep_scaling,
            'exec_save': True
        },
    },
    'scale': {
        'checkpoint': {
            'name': 'scale',
            'sub_steps': False
        },
        'next_step': None,  # replaced by custom main_func
    },
    'verify_scaling': {
        'checkpoint': {
            'name': 'verify_scaling',
            'sub_steps': False
        },
        'next_step': {
            'name': 'socket_milling',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL'
            },
            'prep_func': None,
            'exec_save': True
        }
    },
    'socket_milling': {
        'checkpoint': {
            'name': 'socket_milling',
            'sub_steps': False
        },
        'next_step': {
            'conditions': [
                {
                    'condition_func': socket_condition,
                    'name': 'thickness',
                    'default_state': {
                        'object_name': 'uFit',
                        'light': 'STUDIO',
                        'color_type': 'MATERIAL'
                    },
                    'prep_func': None,
                    'exec_save': True
                },
                {
                    'condition_func': milling_condition,
                    'name': 'milling_model',
                    'default_state': {
                        'object_name': 'uFit',
                        'light': 'STUDIO',
                        'color_type': 'MATERIAL'
                    },
                    'prep_func': None,
                    'exec_save': True
                }
            ]
        },
    },
    'milling_model': {
        'checkpoint': {
            'name': 'milling_model',
            'sub_steps': False
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
    'thickness': {
        'checkpoint': {
            'name': 'thickness',
            'sub_steps': False
        },
        'next_step': {
            'name': 'custom_thickness',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
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
            'prep_func': None,
            'exec_save': True
        },
    },
    'custom_thickness_done': {
        'checkpoint': {
            'name': 'custom_thickness',
            'sub_steps': True
        },
        'next_step': {
            'name': 'flare',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL'
            },
            'prep_func': prep_flare,
            'exec_save': True
        },
    },
    'flare': {
        'checkpoint': {
            'name': 'flare',
            'sub_steps': True
        },
        'next_step': {
            'name': 'flare',
            'default_state': None,
            'prep_func': None,
            'exec_save': True
        },
    },
    'flare_done': {
        'checkpoint': {
            'name': 'flare',
            'sub_steps': True
        },
        'next_step': {
            'name': 'verify_socket',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL'
            },
            'prep_func': None,
            'exec_save': True
        },
    },
    'verify_socket': {
        'checkpoint': {
            'name': 'verify_socket',
            'sub_steps': False
        },
        'next_step': {
            'name': 'import_connector',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'VERTEX'
            },
            'prep_func': prep_import_connector,
            'exec_save': True
        },
    },
    'import_connector': {
        'checkpoint': {
            'name': 'import_connector',
            'sub_steps': False
        },
        'next_step': {
            'name': 'align',
            'default_state': {
                'object_name': 'uFit',
                'light': 'FLAT',
                'color_type': 'VERTEX',
                'overlay_axes': (1, 1, 1),
                'overlay_text': True
            },
            'prep_func': prep_alignment,
            'exec_save': True
        },
    },
    'align': {
        'checkpoint': {
            'name': 'align',
            'sub_steps': False
        },
        'next_step': {
            'name': 'transition',
            'default_state': {
                'object_name': 'uFit',
                'light': 'STUDIO',
                'color_type': 'MATERIAL',
            },
            'prep_func': prep_transition_connector,
            'exec_save': True
        },
    },
    'transition': {
        'checkpoint': {
            'name': 'transition',
            'sub_steps': False
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
