from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.utils import annotations
from .....base.src.operators.core.prepare import move_scan


class OTMoveScan(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        # knee_vert = general.get_single_vert_co(context)
        all_points = annotations.get_all_points(anno_name='Selections', layer_name='Knee')
        if active_object is not None \
                and active_object.name == 'uFit' \
                and len(all_points) == 1:
            return True

    def main_func(self, context):
        move_scan(context)
