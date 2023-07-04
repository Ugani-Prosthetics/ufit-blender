from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.prepare import save_rotation


class OTSaveRotation(OTBase):
    @classmethod
    def poll(cls, context):
        # check if the uFit object is active
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'OBJECT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        save_rotation(context)
