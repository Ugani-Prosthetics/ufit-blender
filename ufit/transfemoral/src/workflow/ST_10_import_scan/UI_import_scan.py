from .....base.src.ui.base.UI_start import UIImportScan
from ...transfemoral_constants import tf_ui_consts


class UIImportScanTF(UIImportScan):
    bl_idname = "VIEW3D_PT_tf_import_scan"
    bl_label = tf_ui_consts['workflow']['import_scan']['ui_name']

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row1 = layout.row()
        row1.prop(scene, 'tf_socket_source', expand=True)

        if scene.tf_socket_source == 'from_scan':
            self.draw_base(context,
                           ot_import_scan="tf_operators.import_scan")
        elif scene.tf_socket_source == 'from_measurement':
            self.draw_measurement_panel(scene, layout)
        else:
            pass

    def draw_measurement_panel(self, scene, layout):
        row2 = layout.row()
        row2.prop(scene, 'ufit_import_unit', expand=True)

        row3 = layout.row()
        row3.prop(scene, 'tf_circumference_interval')

        layout.row().separator()

        box0 = layout.box()

        for i in range(1, 11):
            row = box0.row()
            row.prop(scene, 'tf_circumference_{}'.format(i))

        row = layout.row()
        row.operator("ufit_operators.prev_step", text="Back")
        row.operator('tf_operators.generate_model')

    @classmethod
    def poll(cls, context):
        return (context.scene.ufit_active_step == 'import_scan'
                and context.scene.ufit_device_type == 'transfemoral')
