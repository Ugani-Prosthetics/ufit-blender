import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.sculpt import flare, flare_done


class OTFlare(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'EDIT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        # execute func
        flare(context)


class OTFlareDone(OTBase):
    @classmethod
    def poll(cls, context):
        return True

    def main_func(self, context):
        flare_done(context)
