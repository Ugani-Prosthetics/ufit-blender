import bpy
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
    filename_ext = '.zip'

    filter_glob: bpy.props.StringProperty(
        default='*.zip',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        # always make it possible to start from existing
        return True

    def main_func(self, context):
        start_from_existing(context, self.filepath, self.get_path_consts(), self.get_ui_consts())
