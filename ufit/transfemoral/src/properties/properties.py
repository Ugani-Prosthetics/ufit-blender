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
                                                                      ("connector_flatened_4_prong.blend", "flatened 4 prong", "", 1),
                                                                      ("connector_cylinder.blend", "cylinder", "", 2),
                                                                      # ("connector_cylinder_kid_small.blend", "cylinder (kid small)", "", 3),
                                                                      # # ("connector_pyramid.blend", "pyramid", "", 2),
                                                                      # ("connector_sl700p_circle.blend", "SL 700-P (circle)", "", 4),
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

