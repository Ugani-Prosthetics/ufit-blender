from ..OT_Base_TF import OTBaseTF
from .....base.src.operators.base.OT_connector import OTImportConnector
from .....base.src.operators.core.alignment import import_connector


class OTImportConnectorTF(OTBaseTF, OTImportConnector):
    """Tooltip"""
    bl_idname = "tf_operators.import_connector"
    bl_label = "Import Connector"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_connector')

    def main_func(self, context):
        import_connector(context,
                         self.get_path_consts(),
                         context.scene.tf_connector_type,
                         context.scene.tf_foot_type,
                         context.scene.tf_amputation_side)
