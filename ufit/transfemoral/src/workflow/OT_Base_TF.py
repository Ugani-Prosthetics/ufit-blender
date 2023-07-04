from ....base.src.operators.core.OT_base import OTBase
from ..transfemoral_constants import tf_path_consts, tf_ui_consts, tf_operator_consts


class OTBaseTF(OTBase):
    def get_path_consts(self):
        return tf_path_consts

    def get_ui_consts(self):
        return tf_ui_consts

    def get_operator_consts(self, operator_name):
        operator_vars = tf_operator_consts.get(operator_name)
        if operator_vars:
            return operator_vars
        else:
            raise ValueError(f"Unknown operator name: {operator_name}")

