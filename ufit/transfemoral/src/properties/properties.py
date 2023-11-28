import bpy


#################################
# Properties
#################################
tf_scene_properties = [
    'tf_socket_source',
    'tf_circumference_interval',
    'tf_circumference_1',
    'tf_circumference_2',
    'tf_circumference_3',
    'tf_circumference_4',
    'tf_circumference_5',
    'tf_circumference_6',
    'tf_circumference_7',
    'tf_circumference_8',
    'tf_circumference_9',
    'tf_circumference_10',
    'tf_connector_type',
    'tf_foot_type',
    'tf_amputation_side',
]


def register():
    # model source
    bpy.types.Scene.tf_socket_source = bpy.props.EnumProperty(name="Socket Source", default=1,
                                                               items=[
                                                                   ("from_scan", "From scan", "", 1),
                                                                   ("from_measurement", "From measurement", "", 2),
                                                               ])
    
    bpy.types.Scene.tf_circumference_interval = bpy.props.FloatProperty(name="Circumference Interval",
                                                                      description="Distance between circumference measurements",
                                                                      default=30)

    bpy.types.Scene.tf_circumference_1 = bpy.props.FloatProperty(name="Circumference 1", default=438)

    bpy.types.Scene.tf_circumference_2 = bpy.props.FloatProperty(name="Circumference 2", default=419)

    bpy.types.Scene.tf_circumference_3 = bpy.props.FloatProperty(name="Circumference 3", default=400)

    bpy.types.Scene.tf_circumference_4 = bpy.props.FloatProperty(name="Circumference 4", default=390)

    bpy.types.Scene.tf_circumference_5 = bpy.props.FloatProperty(name="Circumference 5", default=390)

    bpy.types.Scene.tf_circumference_6 = bpy.props.FloatProperty(name="Circumference 6", default=385)

    bpy.types.Scene.tf_circumference_7 = bpy.props.FloatProperty(name="Circumference 7", default=372)

    bpy.types.Scene.tf_circumference_8 = bpy.props.FloatProperty(name="Circumference 8", default=340)

    bpy.types.Scene.tf_circumference_9 = bpy.props.FloatProperty(name="Circumference 9", default=240)

    bpy.types.Scene.tf_circumference_10 = bpy.props.FloatProperty(name="Circumference 10")

    # import connector
    bpy.types.Scene.tf_connector_type = bpy.props.EnumProperty(name="Connector Type", default=1,
                                                               items=[
                                                                   ("universal_no_hole_circ.blend", "Universal No-hole Circ", "", 1),
                                                                   ("universal_4_hole_circ.blend", "Universal 4-hole Circ", "", 2),
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
    del bpy.types.Scene.tf_socket_source
    del bpy.types.Scene.tf_circumference_interval
    del bpy.types.Scene.tf_circumference_1
    del bpy.types.Scene.tf_circumference_2
    del bpy.types.Scene.tf_circumference_3
    del bpy.types.Scene.tf_circumference_4
    del bpy.types.Scene.tf_circumference_5
    del bpy.types.Scene.tf_circumference_6
    del bpy.types.Scene.tf_circumference_7
    del bpy.types.Scene.tf_circumference_8
    del bpy.types.Scene.tf_circumference_9
    del bpy.types.Scene.tf_circumference_10
    del bpy.types.Scene.tf_connector_type
    del bpy.types.Scene.tf_foot_type
    del bpy.types.Scene.tf_amputation_side

