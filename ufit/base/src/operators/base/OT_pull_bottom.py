from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.prepare import remeasure_circumferences
from .....base.src.operators.core.sculpt import pull_bottom


class OTPullBottom(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'EDIT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        # get property values
        extrusion = context.scene.ufit_extrude_amount / 1000

        # execute func
        pull_bottom(context, extrusion)

        # remeasure circumferences
        remeasure_circumferences(context)


class OTPullBottomDone(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        if active_object is not None \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        pass
