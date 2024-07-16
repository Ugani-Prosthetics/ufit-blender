import bpy
from .ST_0_start.UI_start_modeling import UIStartModelingTT
from .ST_10_import_scan.UI_import_scan import UIImportScanTT
from .ST_20_indicate.UI_indicate_patella import UIMoveScanTT
from .ST_30_clean_up.UI_clean_up import UICleanUpScanTT
from .ST_40_verify_clean_up.UI_verify_clean_up import UIVerifyCleanUpTT
from .ST_50_rotate.UI_rotate_scan import UIRotateTT
from .ST_60_circumferences.UI_circumferences import UIAddCircumferencesTT, UICircumferencesTT
from .ST_70_push_pull_smooth.UI_push_pull_smooth import UIPushPullRegionsTT
from .ST_80_pull_bottom.UI_pull_bottom import UIPullBottomTT
from .ST_90_cutout_prep.UI_cutout_prep import UICutoutPrepTT
from .ST_100_cutout.UI_cutout import UICutoutTT
from .ST_105_cutout_selection.UI_cutout_selection import UICutoutSelectionTT
from .ST_110_scale.UI_liner_scaling import UIScaleScanTT
from .ST_120_verify_scaling.UI_verify_scaling import UIVerifyScalingTT
from .ST_125_socket_milling.UI_socket_milling import UISocketMillingTT
from .ST_130_milling_model.UI_milling_model import UIMillingModelTT
from .ST_130_thickness.UI_thickness import UIThicknessTT
from .ST_132_custom_thickness.UI_custom_thickness import UICustomThicknessTT
from .ST_135_flare.UI_flare import UIFlareTT
from .ST_140_verify_socket.UI_verify_socket import UIVerifySocketTT
from .ST_150_import_connector.UI_import_connector import UIImportConnectorTT
from .ST_160_align.UI_alignment import UIMoveConnectorTT
from .ST_170_transition.UI_transition_connector import UITransitionConnectorTT
from .ST_180_export.UI_export_socket import UIExportSocketTT
from .ST_190_finish.UI_finish import UIFinishedTT


def register():
    bpy.utils.register_class(UIStartModelingTT)
    bpy.utils.register_class(UIImportScanTT)
    bpy.utils.register_class(UIMoveScanTT)
    bpy.utils.register_class(UICleanUpScanTT)
    bpy.utils.register_class(UIVerifyCleanUpTT)
    bpy.utils.register_class(UIRotateTT)
    bpy.utils.register_class(UICircumferencesTT)
    bpy.utils.register_class(UIAddCircumferencesTT)
    bpy.utils.register_class(UIPushPullRegionsTT)
    bpy.utils.register_class(UIPullBottomTT)
    bpy.utils.register_class(UICutoutPrepTT)
    bpy.utils.register_class(UICutoutTT)
    bpy.utils.register_class(UICutoutSelectionTT)
    bpy.utils.register_class(UIScaleScanTT)
    bpy.utils.register_class(UIVerifyScalingTT)
    bpy.utils.register_class(UISocketMillingTT)
    bpy.utils.register_class(UIMillingModelTT)
    bpy.utils.register_class(UIThicknessTT)
    bpy.utils.register_class(UICustomThicknessTT)
    bpy.utils.register_class(UIFlareTT)
    bpy.utils.register_class(UIVerifySocketTT)
    bpy.utils.register_class(UIImportConnectorTT)
    bpy.utils.register_class(UIMoveConnectorTT)
    bpy.utils.register_class(UITransitionConnectorTT)
    bpy.utils.register_class(UIExportSocketTT)
    bpy.utils.register_class(UIFinishedTT)


def unregister():
    bpy.utils.unregister_class(UIStartModelingTT)
    bpy.utils.unregister_class(UIImportScanTT)
    bpy.utils.unregister_class(UIMoveScanTT)
    bpy.utils.unregister_class(UICleanUpScanTT)
    bpy.utils.unregister_class(UIVerifyCleanUpTT)
    bpy.utils.unregister_class(UIRotateTT)
    bpy.utils.unregister_class(UICircumferencesTT)
    bpy.utils.unregister_class(UIAddCircumferencesTT)
    bpy.utils.unregister_class(UIPushPullRegionsTT)
    bpy.utils.unregister_class(UIPullBottomTT)
    bpy.utils.unregister_class(UICutoutPrepTT)
    bpy.utils.unregister_class(UICutoutTT)
    bpy.utils.unregister_class(UICutoutSelectionTT)
    bpy.utils.unregister_class(UIScaleScanTT)
    bpy.utils.unregister_class(UIVerifyScalingTT)
    bpy.utils.unregister_class(UISocketMillingTT)
    bpy.utils.unregister_class(UIMillingModelTT)
    bpy.utils.unregister_class(UIThicknessTT)
    bpy.utils.unregister_class(UICustomThicknessTT)
    bpy.utils.unregister_class(UIFlareTT)
    bpy.utils.unregister_class(UIVerifySocketTT)
    bpy.utils.unregister_class(UIImportConnectorTT)
    bpy.utils.unregister_class(UIMoveConnectorTT)
    bpy.utils.unregister_class(UITransitionConnectorTT)
    bpy.utils.unregister_class(UIExportSocketTT)
    bpy.utils.unregister_class(UIFinishedTT)
