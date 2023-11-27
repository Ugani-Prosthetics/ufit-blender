from .....base.src.operators.core.OT_base import OTBase


class OTBorderChoice(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'OBJECT':
            return True

    def main_func(self, context):
        pass