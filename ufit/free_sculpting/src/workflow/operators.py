import bpy
from .ST_0_start.OT_start_modeling import OTStartModelingFS, OTStartFromExistingFS
from .ST_10_import_scan.OT_import_scan import OTImportScanFS
from .ST_20_indicate.OT_indicate_patella import OTMoveScanFS
from .ST_30_clean_up.OT_clean_up import OTCleanUpFS
from .ST_40_verify_clean_up.OT_verify_clean_up import (
    OTHighlightNonManifoldFS,
    OTFillNonManifoldFS,
    OTDeleteNonManifoldFS,
    OTApproveCleanUpFS,
)
from .ST_50_rotate.OT_rotate_scan import OTMirrorFS, OTSaveRotationFS
from .ST_70_push_pull_smooth.OT_push_pull_smooth import (
    OTPushPullRegionFS,
    OTSmoothRegionFS,
    OTFreeSculptCheckpointFS,
    OTPushPullSmoothDoneFS
)
from .ST_90_cutout_prep.OT_cutout_prep import OTCutoutPlaneFS
from .ST_100_cutout.OT_cutout import OTCutoutFS
from .ST_105_new_cutout.OT_new_cutout import OTNewCutoutFS, OTCutoutDoneFS
from .ST_110_scale.OT_liner_scaling import OTLinerScaleFS
from .ST_120_verify_scaling.OT_verify_scaling import OTApproveScalingFS
from .ST_130_thickness.OT_thickness import OTThicknessFS
from .ST_132_custom_thickness.OT_custom_thickness import OTCustomThicknessFS, OTCustomThicknessDoneFS
from .ST_180_export.OT_export_socket import OTExportSocketFS
from .ST_190_finish.OT_finish import OTFinishFS


def register():
    bpy.utils.register_class(OTStartModelingFS)
    bpy.utils.register_class(OTStartFromExistingFS)
    bpy.utils.register_class(OTImportScanFS)
    bpy.utils.register_class(OTMoveScanFS)
    bpy.utils.register_class(OTCleanUpFS)
    bpy.utils.register_class(OTHighlightNonManifoldFS)
    bpy.utils.register_class(OTFillNonManifoldFS)
    bpy.utils.register_class(OTDeleteNonManifoldFS)
    bpy.utils.register_class(OTApproveCleanUpFS)
    bpy.utils.register_class(OTMirrorFS)
    bpy.utils.register_class(OTSaveRotationFS)
    bpy.utils.register_class(OTSmoothRegionFS)
    bpy.utils.register_class(OTPushPullRegionFS)
    bpy.utils.register_class(OTFreeSculptCheckpointFS)
    bpy.utils.register_class(OTPushPullSmoothDoneFS)
    bpy.utils.register_class(OTCutoutPlaneFS)
    bpy.utils.register_class(OTCutoutFS)
    bpy.utils.register_class(OTNewCutoutFS)
    bpy.utils.register_class(OTCutoutDoneFS)
    bpy.utils.register_class(OTLinerScaleFS)
    bpy.utils.register_class(OTApproveScalingFS)
    bpy.utils.register_class(OTThicknessFS)
    bpy.utils.register_class(OTCustomThicknessFS)
    bpy.utils.register_class(OTCustomThicknessDoneFS)
    bpy.utils.register_class(OTExportSocketFS)
    bpy.utils.register_class(OTFinishFS)


def unregister():
    bpy.utils.unregister_class(OTStartModelingFS)
    bpy.utils.unregister_class(OTStartFromExistingFS)
    bpy.utils.unregister_class(OTImportScanFS)
    bpy.utils.unregister_class(OTMoveScanFS)
    bpy.utils.unregister_class(OTCleanUpFS)
    bpy.utils.unregister_class(OTHighlightNonManifoldFS)
    bpy.utils.unregister_class(OTFillNonManifoldFS)
    bpy.utils.unregister_class(OTDeleteNonManifoldFS)
    bpy.utils.unregister_class(OTApproveCleanUpFS)
    bpy.utils.unregister_class(OTMirrorFS)
    bpy.utils.unregister_class(OTSaveRotationFS)
    bpy.utils.unregister_class(OTSmoothRegionFS)
    bpy.utils.unregister_class(OTPushPullRegionFS)
    bpy.utils.unregister_class(OTFreeSculptCheckpointFS)
    bpy.utils.unregister_class(OTPushPullSmoothDoneFS)
    bpy.utils.unregister_class(OTCutoutPlaneFS)
    bpy.utils.unregister_class(OTCutoutFS)
    bpy.utils.unregister_class(OTNewCutoutFS)
    bpy.utils.unregister_class(OTCutoutDoneFS)
    bpy.utils.unregister_class(OTLinerScaleFS)
    bpy.utils.unregister_class(OTApproveScalingFS)
    bpy.utils.unregister_class(OTThicknessFS)
    bpy.utils.unregister_class(OTCustomThicknessFS)
    bpy.utils.unregister_class(OTCustomThicknessDoneFS)
    bpy.utils.unregister_class(OTExportSocketFS)
    bpy.utils.unregister_class(OTFinishFS)
