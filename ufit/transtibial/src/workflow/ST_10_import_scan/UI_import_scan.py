from .....base.src.ui.base.UI_start import UIImportScan
from ...transtibial_constants import tt_ui_consts


class UIImportScanTT(UIImportScan):
    bl_idname = "VIEW3D_PT_tt_import_scan"
    bl_label = tt_ui_consts['workflow']['import_scan']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_import_scan="tt_operators.import_scan")



    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'import_scan'
                and context.scene.ufit_device_type == 'transtibial')



