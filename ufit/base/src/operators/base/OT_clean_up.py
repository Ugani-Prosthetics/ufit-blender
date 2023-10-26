from ..utils import general
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.prepare import (clean_up, verify_clean_up, highlight_next_non_manifold,
                                                  fill_non_manifold, delete_non_manifold)


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


class OTHighlightNonManifold(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object

        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'EDIT':
            return True

    def main_func(self, context):
        highlight_next_non_manifold(context)


class OTFillNonManifold(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object

        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'EDIT':
            selected_vertices = general.get_selected_vertices(context)
            if len(selected_vertices) > 3:
                return True

    def main_func(self, context):
        fill_non_manifold(context)


class OTDeleteNonManifold(OTBase):
    @classmethod
    def poll(cls, context):
        active_object = context.active_object

        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.name == 'uFit' \
                and active_object.mode == 'EDIT':
            selected_vertices = general.get_selected_vertices(context)
            if len(selected_vertices) > 0:
                return True

    def main_func(self, context):
        delete_non_manifold(context)


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
