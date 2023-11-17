import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.sculpt import create_cutout_plane, cutout, cutout_straight


class OTCutoutPlane(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if (active_object is not None and
                ((active_object.name == 'uFit' and context.scene.ufit_cutout_style == 'free') or
                 (active_object.name == 'uFit_Cutout' and context.scene.ufit_cutout_style == 'straight'))):
            return True

    def main_func(self, context):
        if context.scene.ufit_cutout_style == "free":
            create_cutout_plane(context)
        elif context.scene.ufit_cutout_style == "straight":
            cutout_straight(context)



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
