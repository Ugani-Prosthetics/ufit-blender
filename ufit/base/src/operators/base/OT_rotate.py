import bpy
from .....base.src.operators.core.OT_base import OTBase
from .....base.src.operators.core.prepare import save_rotation


class OTMirror(OTBase):
    @classmethod
    def poll(cls, context):
        # check if the uFit object is active
        active_object = context.active_object
        if active_object.select_get() \
                and active_object.type == 'MESH' \
                and active_object.mode == 'OBJECT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        # mirror using x-axis direction
        bpy.ops.transform.mirror(
            orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type='GLOBAL',
            constraint_axis=(True, False, False)
        )


class OTSaveRotation(OTBase):
    @classmethod
    def poll(cls, context):
        # check if the uFit object is active
        active_object = context.active_object
        if active_object is not None \
                and active_object.type == 'MESH' \
                and active_object.mode == 'OBJECT' \
                and active_object.name == 'uFit':
            return True

    def main_func(self, context):
        save_rotation(context)
