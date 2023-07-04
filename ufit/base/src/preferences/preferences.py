import bpy
from .PF_ufit_preferences import PFuFit


def register():
    bpy.utils.register_class(PFuFit)


def unregister():
    bpy.utils.unregister_class(PFuFit)
