import bpy
from .....base.src.ui.utils.general import UFitPanel
from ...transfemoral_constants import tf_ui_consts
from .....base.src.ui.utils.general import get_standard_navbox


class UIImportConnectorTF(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_tf_import_connector"
    bl_label = tf_ui_consts['workflow']['import_connector']['ui_name']

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box0 = layout.box()
        box0.prop(scene, 'tf_connector_type')
        box0.prop(scene, 'tf_foot_type')
        box0.prop(scene, 'tf_amputation_side')

        get_standard_navbox(self.layout, "ufit_operators.prev_step", "tf_operators.import_connector")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'import_connector'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
