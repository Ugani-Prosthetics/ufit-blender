from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.prepare import clean_up, verify_clean_up


class OTCleanUp(OTBase):
    @classmethod
    def poll(cls, context):
        # check if the uFit object is active
        active_object = context.active_object

        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'EDIT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        clean_up(context)


class OTApproveCleanUp(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'EDIT':
            return True

    def main_func(self, context):
        verify_clean_up(context)
