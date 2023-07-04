import bpy
from .OT_platform_login import OTPlatformLogin
from .OT_steps_checkpoints import OTPreviousStep, OTCheckpointRollback
from .OT_gizmo import OTuFitGizmo
from .OT_device_type import OTDeviceType


def register():
    bpy.utils.register_class(OTPlatformLogin)
    bpy.utils.register_class(OTCheckpointRollback)
    bpy.utils.register_class(OTPreviousStep)
    bpy.utils.register_class(OTuFitGizmo)
    bpy.utils.register_class(OTDeviceType)


def unregister():
    bpy.utils.unregister_class(OTPlatformLogin)
    bpy.utils.unregister_class(OTCheckpointRollback)
    bpy.utils.unregister_class(OTPreviousStep)
    bpy.utils.unregister_class(OTuFitGizmo)
    bpy.utils.unregister_class(OTDeviceType)
