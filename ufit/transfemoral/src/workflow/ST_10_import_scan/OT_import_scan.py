import bpy
from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_import_scan import OTImportScan
from .....base.src.operators.core.start import start_from_dimensions

class OTImportScanTF(OTBaseTF, OTImportScan):
    """Tooltip"""
    bl_idname = "tf_operators.import_scan"
    bl_label = "Select Scan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_scan')

class OTGenerateModelFromDimTF(OTBaseTF):
    """Tooltip"""
    bl_idname = "tf_operators.generate_model"
    bl_label = "Generate Model"
    bl_options = {"REGISTER", "UNDO"}

    def append_circ_measurement(self, circ_list, circ_measurement):
        if (circ_measurement > 0):
            circ_list.append(circ_measurement)

    def execute(self, context):
        print("now generate model from dimensions")
        length_unit = context.scene.ufit_import_unit.upper() + "S"
        circ_interval = context.scene.tf_circumference_interval
        circ_list = []

        self.append_circ_measurement(circ_list, context.scene.tf_circumference_1)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_2)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_3)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_4)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_5)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_6)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_7)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_8)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_9)
        self.append_circ_measurement(circ_list, context.scene.tf_circumference_10)

        print("units:", length_unit, "circ_interval", circ_interval, "circ_list", circ_list)

        start_from_dimensions(context, length_unit, circ_interval, circ_list)
        return {'FINISHED'}
