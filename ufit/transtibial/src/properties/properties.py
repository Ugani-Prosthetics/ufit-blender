import bpy


#################################
# Properties
#################################
tt_scene_properties = [
    'tt_connector_type',
    'tt_foot_type',
    'tt_amputation_side',
]


def register():
    # import connector
    bpy.types.Scene.tt_connector_type = bpy.props.EnumProperty(name="Connector Type", default=1,
                                                                  items=[
                                                                      ("connector_cylinder.blend", "4-hole cylinder", "", 1),
                                                                      ("connector_cylinder_kid.blend", "4-hole cylinder (kid)", "", 2),
                                                                      ("connector_squared.blend", "4-hole squared", "", 3),
                                                                      ("connector_sl700p.blend", "SL 700-P", "", 4),
                                                                      # ("connector_cylinder_kid_small.blend", "cylinder (kid small)", "", 3),
                                                                      # # ("connector_pyramid.blend", "pyramid", "", 2),
                                                                      # ("connector_sl700p_circle.blend", "SL 700-P (circle)", "", 4),
                                                                  ])

    bpy.types.Scene.tt_foot_type = bpy.props.EnumProperty(name="Foot Type", default=1,
                                                                  items=[
                                                                      ("basic_foot.blend", "basic", "", 1),
                                                                  ])

    bpy.types.Scene.tt_amputation_side = bpy.props.EnumProperty(name="Side", default=1,
                                                                   items=[
                                                                       ("right", "right", "", 1),
                                                                       ("left", "left", "", 2),
                                                                   ])


def unregister():
    # import connector
    del bpy.types.Scene.tt_connector_type
    del bpy.types.Scene.tt_foot_type
    del bpy.types.Scene.tt_amputation_side

