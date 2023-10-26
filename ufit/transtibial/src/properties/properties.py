import bpy


#################################
# Properties
#################################
tt_scene_properties = [
    'tt_connector_type',
    'tt_foot_type',
    'tt_amputation_side',
    'tt_non_manifold_highlighted'
]


def register():
    # import connector
    bpy.types.Scene.tt_connector_type = bpy.props.EnumProperty(name="Connector Type", default=1,
                                                               items=[
                                                                   ("universal_4_hole_quad.blend", "Universal 4-hole Quad", "", 1),
                                                                   ("universal_4_hole_circ.blend", "Universal 4-hole Circ", "", 2),
                                                                   ("universal_4_hole_circ_small.blend", "Universal 4-hole Circ (Small)", "", 3),
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
    del bpy.types.Scene.tt_non_manifold_highlighted

