from .....base.src.ui.base.UI_finish import UIExportDevice
from ...free_sculpting_constants import fs_ui_consts


class UIExportSocketFS(UIExportDevice):
    bl_idname = "VIEW3D_PT_fs_export_socket"
    bl_label = fs_ui_consts['workflow']['export']['ui_name']

    def draw(self, context):
        self.draw_base(context,
                       ot_export_device="fs_operators.export_socket")

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'export'
                and context.scene.ufit_device_type == 'free_sculpting')
