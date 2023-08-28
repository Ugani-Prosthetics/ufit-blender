import bpy
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)
from . import callbacks


ufit_scene_properties = [
    'ufit_full_screen',
    'ufit_quad_view',
    'ufit_orthographic_view',
    'ufit_device_type',
    'ufit_progress',
    'ufit_scan_filename',
    'ufit_folder_modeling',
    'ufit_folder_checkpoints',
    'ufit_active_step',
    'ufit_substep',
    'ufit_checkpoints',
    'ufit_checkpoint_collection',
    'ufit_help_text',
    'ufit_import_unit',
    'ufit_circum_z_ixs',
    'ufit_init_circumferences',
    'ufit_sculpt_circumferences',
    'ufit_circumferences',
    'ufit_circums_highlighted',
    'ufit_circums_distance',
    'ufit_scaling_unit',
    'ufit_liner_scaling',
    'ufit_show_prescale',
    'ufit_show_original',
    'ufit_preview_extrusions',
    'ufit_smooth_factor',
    'ufit_push_pull_circular',
    'ufit_extrude_amount',
    'ufit_twist_method',
    'ufit_print_thickness',
    'ufit_show_connector',
    'ufit_x_ray',
    'ufit_anchor_point',
    'ufit_alignment_object',
    'ufit_alignment_tool',
    'ufit_connector_loc',
]


# property group that stores the step and file_path of a checkpoint
class CheckpointPG(bpy.types.PropertyGroup):
    step: StringProperty()
    step_nr: IntProperty()
    sub_step_nr: IntProperty()
    name: StringProperty()
    technical_name: StringProperty()
    file_path: StringProperty()


#################################
# Properties
#################################
def register():
    # platform
    bpy.types.Scene.ufit_platform = bpy.props.EnumProperty(name="Platform", default=1,
                                                           items=[
                                                               ("https://ufit.ugani.org", "uFit", "", 1),
                                                           ])
    bpy.types.Scene.ufit_user = bpy.props.StringProperty(name="User")
    bpy.types.Scene.ufit_password = bpy.props.StringProperty(name="Password", subtype='PASSWORD')

    # device type
    bpy.types.Scene.ufit_device_type = EnumProperty(name="Device Type", default=1,
                                                    items=[
                                                        ("transtibial", "Transtibial", "", 1),
                                                        # ("transfemoral", "Transfemoral", "", 2),
                                                    ])

    # settings
    bpy.types.Scene.ufit_full_screen = BoolProperty(name="Full Screen", default=False,
                                                    update=callbacks.full_screen)
    bpy.types.Scene.ufit_quad_view = BoolProperty(name="Quad View", default=False,
                                                  update=callbacks.quad_view)
    bpy.types.Scene.ufit_orthographic_view = BoolProperty(name="Ortho. View", default=False,
                                                          update=callbacks.orthographic_view)

    # progress
    bpy.types.Scene.ufit_progress = FloatProperty(name="Progress", subtype="PERCENTAGE", soft_min=0, soft_max=100,
                                                  precision=0)

    # files
    bpy.types.Scene.ufit_scan_filename = StringProperty(name="Scan File Name")
    bpy.types.Scene.ufit_folder_modeling = StringProperty(name="Folder Modeling")
    bpy.types.Scene.ufit_folder_checkpoints = StringProperty(name="Folder Checkpoints")

    # steps (overview)
    bpy.types.Scene.ufit_active_step = StringProperty(name="Active Step", default='platform_login')
    bpy.types.Scene.ufit_substep = IntProperty(name="Active Substep", default=0)

    # checkpoints
    bpy.utils.register_class(CheckpointPG)
    bpy.types.Scene.ufit_checkpoints = EnumProperty(items=callbacks.checkpoint_items)  # gets checkpoints dynamically
    bpy.types.Scene.ufit_checkpoint_collection = CollectionProperty(type=CheckpointPG)  # a collection of CheckpointPG items

    # assistance
    bpy.types.Scene.ufit_assistance_previews_dir = StringProperty(name="Assistance Folder Path")
    bpy.types.Scene.ufit_assistance_previews = EnumProperty(items=callbacks.enum_previews_for_assistance)
    bpy.types.Scene.ufit_help_text = StringProperty(name="Help Text")

    # import scan
    bpy.types.Scene.ufit_import_unit = EnumProperty(name="Scan Unit", default=3,
                                                    items=[
                                                        ("meter", "m", "", 1),
                                                        ("centimeter", "cm", "", 2),
                                                        ("millimeter", "mm", "", 3),
                                                    ])

    # circumferences
    max_num_circumferences = 15
    bpy.types.Scene.ufit_circum_z_ixs = FloatVectorProperty(name='Circumferences Heights', size=max_num_circumferences)
    bpy.types.Scene.ufit_init_circumferences = FloatVectorProperty(name='Init. Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_sculpt_circumferences = FloatVectorProperty(name='Sculpt. Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_circumferences = FloatVectorProperty(name='Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_circums_highlighted = BoolProperty(name='Circumferences Highlighted', default=False)
    bpy.types.Scene.ufit_circums_distance = EnumProperty(name="Distance", default=2,
                                                         items=[
                                                             ("0.020", "2 cm", "", 1),
                                                             ("0.030", "3 cm", "", 2),
                                                             ("0.040", "4 cm", "", 3),
                                                         ])

    # Scaling
    bpy.types.Scene.ufit_scaling_unit = EnumProperty(name="Scaling Unit", default=1,
                                                     items=[
                                                         ("millimeter", "mm", "", 1),
                                                         ("percentage", "%", "", 2)
                                                     ])
    bpy.types.Scene.ufit_liner_scaling = FloatProperty(name="Liner Scaling", min=-50.0, max=50.0, step=50, default=0)
    bpy.types.Scene.ufit_show_prescale = BoolProperty(name="Show Pre-scaling", default=True,
                                                      update=callbacks.show_prescale_update)
    bpy.types.Scene.ufit_show_original = BoolProperty(name="Show Original", default=True,
                                                      update=callbacks.show_original_update)

    # extrude/smooth regions
    bpy.types.Scene.ufit_preview_extrusions = BoolProperty(name="Disable Colors", default=False,
                                                           update=callbacks.update_preview)
    bpy.types.Scene.ufit_smooth_factor = IntProperty(name="Factor", min=0, max=50, step=1, default=15)
    bpy.types.Scene.ufit_push_pull_circular = BoolProperty(name="Circular", default=True)
    bpy.types.Scene.ufit_extrude_amount = FloatProperty(name="Amount", min=0, max=100.0, step=50, default=3.5)

    # Cutout
    bpy.types.Scene.ufit_twist_method = EnumProperty(name="Twist Method", default=2,
                                                     items=[
                                                         ("MINIMUM", "minimum", "", 1),
                                                         ("Z_UP", "z-up", "", 2),
                                                         ("TANGENT", "tangent", "", 3),
                                                     ],
                                                     update=callbacks.twist_method_update)

    bpy.types.Scene.ufit_print_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10,
                                                         default=4.2)

    # alignment
    bpy.types.Scene.ufit_x_ray = BoolProperty(name="X-Ray", default=False,
                                              update=callbacks.xray_update)
    bpy.types.Scene.ufit_anchor_point = FloatVectorProperty(name='Anchor Point')

    bpy.types.Scene.ufit_show_connector = BoolProperty(name="Show Connector", default=False,
                                                       update=callbacks.show_connector_update)

    bpy.types.Scene.ufit_alignment_object = EnumProperty(name="Object", default=1,
                                                         items=[
                                                             ("uFit", "socket", "", 1),
                                                             ("Connector", "connector", "", 2),
                                                         ],
                                                         update=callbacks.alignment_object_update)

    bpy.types.Scene.ufit_alignment_tool = EnumProperty(name="Tool", default=1,
                                                       items=[
                                                           ("builtin.rotate", "rotate", "", 1),
                                                           ("builtin.move", "translate", "", 2),
                                                       ],
                                                       update=callbacks.alignment_tool_update)
    bpy.types.Scene.ufit_connector_loc = FloatVectorProperty(name='Connector Location')

    # transition
    bpy.types.Scene.ufit_try_perfect_print = BoolProperty(name="Try Perfect Print", default=False)
    bpy.types.Scene.ufit_total_contact_socket = BoolProperty(name="Total Contact Socket", default=False)

    # export
    bpy.types.Scene.ufit_show_inner_part = BoolProperty(name="Show Inner Part", default=False,
                                                        update=callbacks.show_inner_part_update)


def unregister():
    # platform
    del bpy.types.Scene.ufit_platform
    del bpy.types.Scene.ufit_user
    del bpy.types.Scene.ufit_password

    # device type
    del bpy.types.Scene.ufit_device_type

    # settings
    del bpy.types.Scene.ufit_full_screen
    del bpy.types.Scene.ufit_quad_view
    del bpy.types.Scene.ufit_orthographic_view

    # progress
    del bpy.types.Scene.ufit_progress

    # files
    del bpy.types.Scene.ufit_scan_filename
    del bpy.types.Scene.ufit_folder_modeling
    del bpy.types.Scene.ufit_folder_checkpoints

    # steps (overview)
    del bpy.types.Scene.ufit_active_step
    del bpy.types.Scene.ufit_substep

    # checkpoints
    bpy.utils.unregister_class(CheckpointPG)
    del bpy.types.Scene.ufit_checkpoints
    del bpy.types.Scene.ufit_checkpoint_collection

    # assistance
    del bpy.types.Scene.ufit_help_text

    # import scan
    del bpy.types.Scene.ufit_import_unit

    # circumferences
    del bpy.types.Scene.ufit_circum_z_ixs
    del bpy.types.Scene.ufit_init_circumferences
    del bpy.types.Scene.ufit_sculpt_circumferences
    del bpy.types.Scene.ufit_circumferences
    del bpy.types.Scene.ufit_circums_highlighted
    del bpy.types.Scene.ufit_circums_distance

    # Scaling
    del bpy.types.Scene.ufit_scaling_unit
    del bpy.types.Scene.ufit_liner_scaling
    del bpy.types.Scene.ufit_show_prescale
    del bpy.types.Scene.ufit_show_original

    # extrude/smooth regions
    del bpy.types.Scene.ufit_smooth_factor
    del bpy.types.Scene.ufit_preview_extrusions
    del bpy.types.Scene.ufit_push_pull_circular
    del bpy.types.Scene.ufit_extrude_amount

    # cutout
    del bpy.types.Scene.ufit_twist_method
    del bpy.types.Scene.ufit_print_thickness

    # alignment
    del bpy.types.Scene.ufit_x_ray
    del bpy.types.Scene.ufit_show_connector
    del bpy.types.Scene.ufit_anchor_point
    del bpy.types.Scene.ufit_alignment_object
    del bpy.types.Scene.ufit_alignment_tool
    del bpy.types.Scene.ufit_connector_loc

    # transition
    del bpy.types.Scene.ufit_try_perfect_print
