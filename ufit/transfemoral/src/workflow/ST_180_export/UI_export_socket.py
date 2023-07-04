from .....base.src.ui.base.UI_finish import UIExportDevice
from ...transfemoral_constants import tf_ui_consts


class UIExportSocketTF(UIExportDevice):
    bl_idname = "VIEW3D_PT_tf_export_socket"
    bl_label = tf_ui_consts['workflow']['export']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_export_device="tf_operators.export_socket")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'export'
                and not context.scene.ufit_circums_highlighted
                and context.scene.ufit_device_type == 'transfemoral')
