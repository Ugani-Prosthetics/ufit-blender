from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.utils import annotations
from .....base.src.operators.core.alignment import transition_connector


class OTImportConnector(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        # tt_connector_vertex = general.get_single_vert_co(context)
        all_points = annotations.get_all_points(anno_name='Selections', layer_name='Connector_Loc')
        if active_object is not None \
                and active_object.name == 'uFit' \
                and len(all_points) == 1:
            return True

    def main_func(self, context):
        raise NotImplementedError("Subclasses must implement main_func")


class OTTransitionConnector(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'Cutter':
            return True

    def main_func(self, context):
        transition_connector(context)
