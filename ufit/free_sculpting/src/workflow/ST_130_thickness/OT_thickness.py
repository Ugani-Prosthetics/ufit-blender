import bpy
from ..OT_Base_FS import OTBaseFS
from .....base.src.operators.base.OT_thickness import OTThickness
from .....base.src.operators.utils.general import apply_all_modifiers


class OTThicknessFS(OTBaseFS, OTThickness):
    """Tooltip"""
    bl_idname = "fs_operators.thickness"
    bl_label = "Choose Print Thickness"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='thickness')

    # override the main_func from OTThickness
    def main_func(self, context):
        ufit_obj = bpy.data.objects['uFit']
        apply_all_modifiers(context, ufit_obj)
