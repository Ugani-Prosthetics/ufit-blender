from .....base.src.ui.base.UI_start import UIImportScan
from ...transfemoral_constants import tf_ui_consts


class UIImportScanTF(UIImportScan):
    bl_idname = "VIEW3D_PT_tf_import_scan"
    bl_label = tf_ui_consts['workflow']['import_scan']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_import_scan="tf_operators.import_scan")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'import_scan'
                and context.scene.ufit_device_type == 'transfemoral')
