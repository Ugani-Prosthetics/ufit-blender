import bpy
import os
from bpy_extras.io_utils import ImportHelper
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.start import start_modeling, start_from_existing


class OTStartModeling(OTBase):
    @classmethod
    def poll(cls, context):
        # always make it possible to import a scan
        return True

    def main_func(self, context):
        start_modeling(context)


class OTStartFromExisting(OTBase, ImportHelper):
    # Only show folders to the user
    filter_folder: bpy.props.BoolProperty(
        default=True,
        options={"HIDDEN"}
    )

    @classmethod
    def poll(self, context):
        # always make it possible to start from existing
        return True

    def check(self, context):
        # Ensure the operator behaves as expected

        if os.path.isdir(self.filepath):
            folder_name = os.path.basename(os.path.dirname(self.filepath))
            for dt in bpy.context.scene.bl_rna.properties['ufit_device_type'].enum_items:
                if folder_name.startswith(f'{dt.identifier}_'):
                    bpy.ops.file.cancel()
        return True

    def cancel(self, context):
        # This method is used to close the modal operator
        start_from_existing(context, self.filepath, self.get_path_consts(), self.get_ui_consts())

    def invoke(self, context, event):
        # Open a file dialog to select a directory
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def main_func(self, context):
        pass
        # start_from_existing(context, self.filepath, self.get_path_consts(), self.get_ui_consts())
