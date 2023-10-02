import bpy
from .ST_0_start.UI_start_modeling import UIStartModelingTF
from .ST_10_import_scan.UI_import_scan import UIImportScanTF
from .ST_20_indicate.UI_indicate_patella import UIMoveScanTF
from .ST_30_clean_up.UI_clean_up import UICleanUpScanTF
from .ST_40_verify_clean_up.UI_verify_clean_up import UIVerifyCleanUpTF
from .ST_50_rotate.UI_rotate_scan import UIRotateTF
from .ST_60_circumferences.UI_circumferences import UIAddCircumferencesTF, UICircumferencesTF
from .ST_70_push_pull_smooth.UI_push_pull_smooth import UIPushPullRegionsTF
from .ST_80_pull_bottom.UI_pull_bottom import UIPullBottomTF
from .ST_90_cutout_prep.UI_cutout_prep import UICutoutPrepTF
from .ST_100_cutout.UI_cutout import UICutoutTF
from .ST_110_scale.UI_liner_scaling import UIScaleScanTF
from .ST_120_verify_scaling.UI_verify_scaling import UIVerifyScalingTF
from .ST_125_socket_milling.UI_socket_milling import UISocketMillingTF
from .ST_130_milling_model.UI_milling_model import UIMillingModelTF
from .ST_130_thickness.UI_thickness import UIThicknessTF
from .ST_135_flare.UI_flare import UIFlareTF
from .ST_140_verify_socket.UI_verify_socket import UIVerifySocketTF
from .ST_150_import_connector.UI_import_connector import UIImportConnectorTF
from .ST_160_align.UI_alignment import UIMoveConnectorTF
from .ST_170_transition.UI_transition_connector import UITransitionConnectorTF
from .ST_180_export.UI_export_socket import UIExportSocketTF
from .ST_190_finish.UI_finish import UIFinishedTF


def register():
    bpy.utils.register_class(UIStartModelingTF)
    bpy.utils.register_class(UIImportScanTF)
    bpy.utils.register_class(UIMoveScanTF)
    bpy.utils.register_class(UICleanUpScanTF)
    bpy.utils.register_class(UIVerifyCleanUpTF)
    bpy.utils.register_class(UIRotateTF)
    bpy.utils.register_class(UICircumferencesTF)
    bpy.utils.register_class(UIAddCircumferencesTF)
    bpy.utils.register_class(UIPushPullRegionsTF)
    bpy.utils.register_class(UIPullBottomTF)
    bpy.utils.register_class(UICutoutPrepTF)
    bpy.utils.register_class(UICutoutTF)
    bpy.utils.register_class(UIScaleScanTF)
    bpy.utils.register_class(UIVerifyScalingTF)
    bpy.utils.register_class(UISocketMillingTF)
    bpy.utils.register_class(UIMillingModelTF)
    bpy.utils.register_class(UIThicknessTF)
    bpy.utils.register_class(UIFlareTF)
    bpy.utils.register_class(UIVerifySocketTF)
    bpy.utils.register_class(UIImportConnectorTF)
    bpy.utils.register_class(UIMoveConnectorTF)
    bpy.utils.register_class(UITransitionConnectorTF)
    bpy.utils.register_class(UIExportSocketTF)
    bpy.utils.register_class(UIFinishedTF)


def unregister():
    bpy.utils.unregister_class(UIStartModelingTF)
    bpy.utils.unregister_class(UIImportScanTF)
    bpy.utils.unregister_class(UIMoveScanTF)
    bpy.utils.unregister_class(UICleanUpScanTF)
    bpy.utils.unregister_class(UIVerifyCleanUpTF)
    bpy.utils.unregister_class(UIRotateTF)
    bpy.utils.unregister_class(UICircumferencesTF)
    bpy.utils.unregister_class(UIAddCircumferencesTF)
    bpy.utils.unregister_class(UIPushPullRegionsTF)
    bpy.utils.unregister_class(UIPullBottomTF)
    bpy.utils.unregister_class(UICutoutPrepTF)
    bpy.utils.unregister_class(UICutoutTF)
    bpy.utils.unregister_class(UIScaleScanTF)
    bpy.utils.unregister_class(UIVerifyScalingTF)
    bpy.utils.unregister_class(UISocketMillingTF)
    bpy.utils.unregister_class(UIMillingModelTF)
    bpy.utils.unregister_class(UIThicknessTF)
    bpy.utils.unregister_class(UIFlareTF)
    bpy.utils.unregister_class(UIVerifySocketTF)
    bpy.utils.unregister_class(UIImportConnectorTF)
    bpy.utils.unregister_class(UIMoveConnectorTF)
    bpy.utils.unregister_class(UITransitionConnectorTF)
    bpy.utils.unregister_class(UIExportSocketTF)
    bpy.utils.unregister_class(UIFinishedTF)
