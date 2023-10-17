from .....base.src.operators.core.OT_base import OTBase
from mathutils import Vector
from .....base.src.operators.core.sculpt import create_custom_thickness
from .....base.src.operators.core.prepare import remeasure_circumferences
from .....base.src.operators.utils import color_attributes
from .....base.src.operators.core.sculpt import color_attr_select


class OTCustomThickness(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        selected_verts = color_attributes.get_vertices_by_color_exclude_simple(active_object, color_attr_select, Vector((1, 1, 1, 1)))
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'VERTEX_PAINT' \
                and len(selected_verts) > 25:
            return True

    def main_func(self, context):
        extrusion = context.scene.ufit_print_thickness / 1000

        create_custom_thickness(context, extrusion)

        remeasure_circumferences(context)


class OTCustomThicknessDone(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'VERTEX_PAINT':
            return True

    def main_func(self, context):
        pass
