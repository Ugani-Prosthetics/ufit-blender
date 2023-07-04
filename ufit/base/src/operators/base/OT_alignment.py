from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.alignment import save_alignment, scale_connector_scale_groups


class OTSaveAlignment(OTBase):
    @classmethod
    def poll(cls, context):
        # check if the uFit object is active
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name in ['uFit', 'Connector']:
            return True

    def main_func(self, context):
        # execute func
        save_alignment(context)

        # Todo: investigate why blender crashes when executed in prep functionality
        # Blender bug: we need to perform scaling before all the other prep functionality
        scale_connector_scale_groups(context)
