import bpy
from mathutils import Vector
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.utils import color_attributes
from .....base.src.operators.core.prepare import remeasure_circumferences
from .....base.src.operators.core.sculpt import (
    color_attr_select,
    smooth_region,
    push_pull_region,
    push_pull_region_circular,
    push_pull_smooth_done,
)


class OTPushPullRegion(OTBase):
    direction: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        selected_verts = color_attributes.get_vertices_by_color_exclude_simple(active_object, color_attr_select, Vector((1, 1, 1, 1)))
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'VERTEX_PAINT' \
                and active_object.name == 'uFit' \
                and len(selected_verts) > 25:
            return True

    def main_func(self, context):
        # get property values
        extrusion = context.scene.ufit_extrude_amount / 1000
        if self.direction == 'Push':
            extrusion = -extrusion

        # execute func
        if context.scene.ufit_push_pull_circular:
            push_pull_region_circular(context, extrusion)
        else:
            push_pull_region(context, extrusion)

        # remeasure circumferences
        remeasure_circumferences(context)


class OTSmoothRegion(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        selected_verts = color_attributes.get_vertices_by_color_exclude_simple(active_object, color_attr_select, Vector((1, 1, 1, 1)))
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'VERTEX_PAINT' \
                and active_object.name == 'uFit' \
                and len(selected_verts) > 25:
            return True

    def main_func(self, context):
        # execute func
        smooth_region(context)

        # remeasure circumferences
        remeasure_circumferences(context)


class OTFreeSculptCheckpoint(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        if active_object is not None \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        # remeasure circumferences
        remeasure_circumferences(context)


class OTPushPullSmoothDone(OTBase):
    @classmethod
    def poll(cls, context):
        # check if there is an ufit object and a vertex is selected
        active_object = context.active_object
        if active_object is not None \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        # execute func
        push_pull_smooth_done(context)

        # remeasure circumferences
        remeasure_circumferences(context)
