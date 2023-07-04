import bpy
from ....base.src.operators.utils import user_interface


#################################
# Gizmo operators
#################################
def change_view(context, orthographic):
    mode = context.object.mode
    user_interface.change_orthographic(orthographic)
    bpy.ops.object.mode_set(mode=mode)


class OTuFitGizmo(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ufit_operators.ufit_gizmo"
    bl_label = "Gizmo"
    bl_options = {"REGISTER", "UNDO"}

    enum_items = (
        ("FRONT", "Front", ""),
        ("BACK", "Back", ""),
        ("LEFT", "Left", ""),
        ("RIGHT", "Right", ""),
        ("TOP", "Top", ""),
        ("BOTTOM", "Bottom", ""),
    )
    action: bpy.props.EnumProperty(items=enum_items)

    @classmethod
    def poll(cls, context):
        # always make it possible to import a scan
        return True

    def execute(self, context):
        change_view(context, self.action)

        return {'FINISHED'}
