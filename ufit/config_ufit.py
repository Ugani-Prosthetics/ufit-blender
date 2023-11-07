import os
import logging
import shutil


def configure_logging(enable_debug):
    if enable_debug:
        logging.basicConfig(level=logging.DEBUG)
        # You can configure other logging options for debugging here
    else:
        # Configure the default logging level for non-debug mode
        logging.basicConfig(level=logging.INFO)



def configure_full_debug(context, workspace, ufit_device, ufit_step):
    # avoid circular imports
    from .base.src.operators.core.start import start_from_existing
    from .transtibial.src.transtibial_constants import tt_path_consts, tt_ui_consts
    from .transfemoral.src.transfemoral_constants import tf_path_consts, tf_ui_consts

    # get the path to the debug patient folder
    current_dir = os.path.abspath(os.path.dirname(__file__))
    patient_folder = f'debug_patient/{ufit_device}_000000_debug/'
    debug_path = f'debug/{ufit_device}/{patient_folder}'
    debug_abs_path = os.path.join(current_dir, debug_path)

    # define the destination folder
    destination_folder = os.path.join(workspace, patient_folder)

    # copy the content of the debug patient folder to the destination folder
    if os.path.exists(destination_folder):
        try:
            shutil.rmtree(destination_folder)
            shutil.copytree(debug_abs_path, destination_folder)
            logger.debug(f"Created the destination folder: {destination_folder}")
        except Exception as e:
            logger.warning(f"Error creating destination folder: {e}")

    if ufit_device == 'transtibial':
        start_from_existing(context, destination_folder, tt_path_consts, tt_ui_consts, debug_step=ufit_step)
    elif ufit_device == 'transfemoral':
        start_from_existing(context, destination_folder, tf_path_consts, tf_ui_consts, debug_step=ufit_step)


logger = logging.getLogger('ufit.logger')
