import bpy


#################################
# Properties
#################################
tf_scene_properties = [
    'tf_connector_type',
    'tf_foot_type',
    'tf_amputation_side',
]


def register():
    # import connector
    bpy.types.Scene.tf_connector_type = bpy.props.EnumProperty(name="Connector Type", default=1,
                                                               items=[
                                                                   ("universal_no_hole_circ.blend", "Universal No-hole Circ", "", 1),
                                                                   ("universal_4_hole_circ.blend", "Universal 4-hole Circ", "", 2),
                                                                   ("universal_circ_regal_base_65mm.blend", "Regal Base 65mm", "", 3),
                                                               ])

    bpy.types.Scene.tf_foot_type = bpy.props.EnumProperty(name="Foot Type", default=1,
                                                          items=[
                                                              ("basic_foot.blend", "basic", "", 1),
                                                          ])

    bpy.types.Scene.tf_amputation_side = bpy.props.EnumProperty(name="Side", default=1,
                                                                items=[
                                                                    ("right", "right", "", 1),
                                                                    ("left", "left", "", 2),
                                                                ])


def unregister():
    # import connector
    del bpy.types.Scene.tf_connector_type
    del bpy.types.Scene.tf_foot_type
    del bpy.types.Scene.tf_amputation_side

