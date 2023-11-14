import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.sculpt import create_cutout_plane, cutout


class OTCutoutPlane(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        create_cutout_plane(context)


class OTCutout(OTBase):
    @classmethod
    def poll(cls, context):
        all_objects = bpy.data.objects
        object_names_types = [(obj.name, obj.type) for obj in all_objects]
        if ('uFit', 'MESH') in object_names_types \
                and ('uFit_Cutout', 'CURVE') in object_names_types:
            return True

    def main_func(self, context):
        cutout(context)


class OTNewCutout(OTBase):
    @classmethod
    def poll(cls, context):
        return True

    def main_func(self, context):
        pass
