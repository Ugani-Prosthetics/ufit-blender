from ..OT_Base_TT import OTBaseTT
from .....base.src.operators.base.OT_connector import OTImportConnector
from .....base.src.operators.core.alignment import import_connector


class OTImportConnectorTT(OTBaseTT, OTImportConnector):
    """Tooltip"""
    bl_idname = "tt_operators.import_connector"
    bl_label = "Import Connector"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return self.execute_base(context,
                                 operator_name='import_connector')

    def main_func(self, context):
        import_connector(context,
                         self.get_path_consts(),
                         context.scene.tt_connector_type,
                         context.scene.tt_foot_type,
                         context.scene.tt_amputation_side)
