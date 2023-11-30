import bpy
from bpy_extras.io_utils import ImportHelper
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.start import init_modeling_folders, import_3d_file


class OTImportScan(OTBase, ImportHelper):
    filename_ext = ''
    filter_glob: bpy.props.StringProperty(
        default='*.zip;*.stl;*.obj',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        # always make it possible to import a scan
        return True

    def invoke(self, context, event):
        if context.scene.ufit_file_type == 'zip':
            self.filter_glob = '*.zip;'
        elif context.scene.ufit_file_type == 'stl':
            self.filter_glob = '*.stl;'
        elif context.scene.ufit_file_type == 'obj':
            self.filter_glob = '*.obj;'
        else:
            self.filter_glob = '*.zip;*.stl;*.obj'

        return super().invoke(context, event)

    def main_func(self, context):
        obj_filepath = init_modeling_folders(context, self.filepath)
        import_3d_file(context, obj_filepath)







