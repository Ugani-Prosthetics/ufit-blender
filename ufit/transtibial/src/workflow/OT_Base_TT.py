from ....base.src.operators.core.OT_base import OTBase
from ..transtibial_constants import tt_path_consts, tt_ui_consts, tt_operator_consts


class OTBaseTT(OTBase):
    def get_path_consts(self):
        return tt_path_consts

    def get_ui_consts(self):
        return tt_ui_consts

    def get_operator_consts(self, operator_name):
        operator_vars = tt_operator_consts.get(operator_name)
        if operator_vars:
            return operator_vars
        else:
            raise ValueError(f"Unknown operator name: {operator_name}")

