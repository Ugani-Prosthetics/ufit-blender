import bpy
from bpy_extras.io_utils import ImportHelper
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.start import init_modeling_folders, import_3d_file


class OTImportScan(OTBase, ImportHelper):
    filename_ext = '.zip'

    filter_glob: bpy.props.StringProperty(
        default='*.zip;*.stl;*.obj',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        # always make it possible to import a scan
        return True

    def main_func(self, context):
        # execute func
        obj_filepath = init_modeling_folders(context, self.filepath)
        import_3d_file(context, obj_filepath)

