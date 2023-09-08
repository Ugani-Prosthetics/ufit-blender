import bpy
from .ST_0_start.OT_start_modeling import OTStartModelingTF, OTStartFromExistingTF
from .ST_10_import_scan.OT_import_scan import OTImportScanTF
from .ST_20_indicate.OT_indicate_patella import OTMoveScanTF
from .ST_30_clean_up.OT_clean_up import OTCleanUpTF
from .ST_40_verify_clean_up.OT_verify_clean_up import OTApproveCleanUpTF
from .ST_50_rotate.OT_rotate_scan import OTSaveRotationTF
from .ST_60_circumferences.OT_circumferences import (
    OTCircumferenceTF,
    OTCircumferencesCalcTF,
    OTCircumferencesDoneTF,
    OTCircumferencesHighlightTF
)
from .ST_70_push_pull_smooth.OT_push_pull_smooth import (
    OTPushPullRegionTF,
    OTSmoothRegionTF,
    OTFreeSculptCheckpointTF,
    OTPushPullSmoothDoneTF
)
from .ST_80_pull_bottom.OT_pull_bottom import OTPullBottomTF, OTPullBottomDoneTF
from .ST_90_cutout_prep.OT_cutout_prep import OTCutoutPlaneTF
from .ST_100_cutout.OT_cutout import OTCutoutTF
from .ST_110_scale.OT_liner_scaling import OTLinerScaleTF
from .ST_120_verify_scaling.OT_verify_scaling import OTApproveScalingTF
from .ST_125_socket_carve.OT_socket_carve import OTSocketCarveTF
from .ST_130_carve_model.OT_carve_model import OTCarveModelTF
from .ST_130_thickness.OT_thickness import OTThicknessTF
from .ST_140_verify_socket.OT_verify_socket import OTApproveSocketTF
from .ST_150_import_connector.OT_import_connector import OTImportConnectorTF
from .ST_160_align.OT_alignment import OTSaveAlignmentTF
from .ST_170_transition.OT_transition_connector import OTTransitionConnectorTF
from .ST_180_export.OT_export_socket import OTExportSocketTF
from .ST_190_finish.OT_finish import OTTinishTF


def register():
    bpy.utils.register_class(OTStartModelingTF)
    bpy.utils.register_class(OTStartFromExistingTF)
    bpy.utils.register_class(OTImportScanTF)
    bpy.utils.register_class(OTMoveScanTF)
    bpy.utils.register_class(OTCleanUpTF)
    bpy.utils.register_class(OTApproveCleanUpTF)
    bpy.utils.register_class(OTSaveRotationTF)
    bpy.utils.register_class(OTCircumferenceTF)
    bpy.utils.register_class(OTCircumferencesCalcTF)
    bpy.utils.register_class(OTCircumferencesDoneTF)
    bpy.utils.register_class(OTCircumferencesHighlightTF)
    bpy.utils.register_class(OTLinerScaleTF)
    bpy.utils.register_class(OTApproveScalingTF)
    bpy.utils.register_class(OTSocketCarveTF)
    bpy.utils.register_class(OTCarveModelTF)
    bpy.utils.register_class(OTSmoothRegionTF)
    bpy.utils.register_class(OTPushPullRegionTF)
    bpy.utils.register_class(OTFreeSculptCheckpointTF)
    bpy.utils.register_class(OTPushPullSmoothDoneTF)
    bpy.utils.register_class(OTPullBottomTF)
    bpy.utils.register_class(OTPullBottomDoneTF)
    bpy.utils.register_class(OTCutoutPlaneTF)
    bpy.utils.register_class(OTCutoutTF)
    bpy.utils.register_class(OTThicknessTF)
    bpy.utils.register_class(OTApproveSocketTF)
    bpy.utils.register_class(OTImportConnectorTF)
    bpy.utils.register_class(OTSaveAlignmentTF)
    bpy.utils.register_class(OTTransitionConnectorTF)
    bpy.utils.register_class(OTExportSocketTF)
    bpy.utils.register_class(OTTinishTF)


def unregister():
    bpy.utils.unregister_class(OTStartModelingTF)
    bpy.utils.unregister_class(OTStartFromExistingTF)
    bpy.utils.unregister_class(OTImportScanTF)
    bpy.utils.unregister_class(OTMoveScanTF)
    bpy.utils.unregister_class(OTCleanUpTF)
    bpy.utils.unregister_class(OTApproveCleanUpTF)
    bpy.utils.unregister_class(OTSaveRotationTF)
    bpy.utils.unregister_class(OTCircumferenceTF)
    bpy.utils.unregister_class(OTCircumferencesCalcTF)
    bpy.utils.unregister_class(OTCircumferencesDoneTF)
    bpy.utils.unregister_class(OTCircumferencesHighlightTF)
    bpy.utils.unregister_class(OTLinerScaleTF)
    bpy.utils.unregister_class(OTApproveScalingTF)
    bpy.utils.unregister_class(OTSocketCarveTF)
    bpy.utils.unregister_class(OTCarveModelTF)
    bpy.utils.unregister_class(OTSmoothRegionTF)
    bpy.utils.unregister_class(OTPushPullRegionTF)
    bpy.utils.unregister_class(OTFreeSculptCheckpointTF)
    bpy.utils.unregister_class(OTPushPullSmoothDoneTF)
    bpy.utils.unregister_class(OTPullBottomTF)
    bpy.utils.unregister_class(OTPullBottomDoneTF)
    bpy.utils.unregister_class(OTCutoutPlaneTF)
    bpy.utils.unregister_class(OTCutoutTF)
    bpy.utils.unregister_class(OTThicknessTF)
    bpy.utils.unregister_class(OTApproveSocketTF)
    bpy.utils.unregister_class(OTImportConnectorTF)
    bpy.utils.unregister_class(OTSaveAlignmentTF)
    bpy.utils.unregister_class(OTTransitionConnectorTF)
    bpy.utils.unregister_class(OTExportSocketTF)
    bpy.utils.unregister_class(OTTinishTF)
