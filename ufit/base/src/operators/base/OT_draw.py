import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.sculpt import apply_draw


class OTApplyDraw(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        apply_draw(context)
