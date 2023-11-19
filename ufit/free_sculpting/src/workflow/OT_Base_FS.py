from ....base.src.operators.core.OT_base import OTBase
from ..free_sculpting_constants import fs_path_consts, fs_ui_consts, fs_operator_consts


class OTBaseFS(OTBase):
    def get_path_consts(self):
        return fs_path_consts

    def get_ui_consts(self):
        return fs_ui_consts

    def get_operator_consts(self, operator_name):
        operator_vars = fs_operator_consts.get(operator_name)
        if operator_vars:
            return operator_vars
        else:
            raise ValueError(f"Unknown operator name: {operator_name}")

