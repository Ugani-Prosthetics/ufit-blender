import bpy


#######################################
# Shader Nodes
#######################################
def set_push_pull_smooth_shader_nodes(ufit_obj, color_attr_name):
    if ufit_obj.data.materials:
        material = ufit_obj.data.materials[ufit_obj.active_material_index]

        # check if there was a colored scan loaded
        node_tex_image = None
        node_output_mat = None
        node_bsdf_princ = None
        if len(material.node_tree.nodes) == 3:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    node_tex_image = node
                if node.type == 'OUTPUT_MATERIAL':
                    node_output_mat = node
                if node.type == 'BSDF_PRINCIPLED':
                    node_bsdf_princ = node

            if node_tex_image and node_output_mat and node_bsdf_princ:
                # Add new nodes
                node_rgb = material.node_tree.nodes.new('ShaderNodeRGB')
                node_color_attr = material.node_tree.nodes.new('ShaderNodeVertexColor')
                node_color_invert = material.node_tree.nodes.new('ShaderNodeInvert')
                node_separate_color = material.node_tree.nodes.new('ShaderNodeSeparateColor')
                node_mix = material.node_tree.nodes.new('ShaderNodeMix')

                # set variables of new nodes
                node_color_attr.layer_name = color_attr_name
                node_separate_color.mode = 'RGB'
                node_mix.data_type = 'RGBA'
                node_mix.blend_type = 'BURN'
                node_mix.clamp_result = True
                node_mix.clamp_factor = False
                node_rgb.outputs['Color'].default_value = (0.0, 1.0, 0.0, 1.0)  # selection in green

                # make node links
                material.node_tree.links.new(
                    node_color_attr.outputs['Color'],
                    node_color_invert.inputs['Color']
                )
                material.node_tree.links.new(
                    node_color_invert.outputs['Color'],
                    node_separate_color.inputs['Color']
                )
                material.node_tree.links.new(
                    node_separate_color.outputs['Red'],
                    node_mix.inputs['Factor']
                )
                material.node_tree.links.new(
                    node_tex_image.outputs['Color'],
                    node_mix.inputs[6]  # multiple 'A' inputs, we need to select type RGBA which is at index 6
                )
                material.node_tree.links.new(
                    node_rgb.outputs['Color'],
                    node_mix.inputs[7]  # multiple 'B' inputs, we need to select type RGBA which is at index 7
                )
                material.node_tree.links.new(
                    node_mix.outputs[2],  # multiple 'Result' output, we need to select type RGBA which is at index 2
                    node_bsdf_princ.inputs['Base Color']
                )


#######################################
# Geometry Nodes
#######################################
def set_voronoi_geometry_nodes_one(ufit_obj, tree_name, color_attr_name):
    # Check if the node tree already exists
    if tree_name not in bpy.data.node_groups:
        # Create a new geometry nodes modifer (automatically creates a node_group with name "Geometry Nodes"
        bpy.ops.node.new_geometry_nodes_modifier()

        # Rename the new node tree
        bpy.data.node_groups[0].name = tree_name

        # Access the geometry nodes tree
        node_tree = bpy.data.node_groups[tree_name]

        in_node = node_tree.nodes["Group Input"]
        out_node = node_tree.nodes["Group Output"]

        named_attribute = node_tree.nodes.new(type="GeometryNodeInputNamedAttribute")
        named_attribute.data_type = 'FLOAT_COLOR'
        named_attribute.inputs[0].default_value = color_attr_name

        equal_node = node_tree.nodes.new(type="FunctionNodeCompare")
        equal_node.data_type = 'RGBA'
        equal_node.operation = 'EQUAL'
        equal_node.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
        equal_node.inputs[12].default_value = 0.1

        voronoi_node = node_tree.nodes.new(type="ShaderNodeTexVoronoi")
        voronoi_node.name = 'ufit_voronoi_node'  # provide name so we can access it for UI
        voronoi_node.voronoi_dimensions = '3D'
        voronoi_node.feature = 'DISTANCE_TO_EDGE'
        voronoi_node.inputs[2].default_value = 15.0  # scale
        voronoi_node.inputs[5].default_value = 1  # random

        greater_than_node = node_tree.nodes.new(type="FunctionNodeCompare")
        greater_than_node.name = 'ufit_compare_node'  # provide name so we can access it for UI
        greater_than_node.data_type = 'FLOAT'
        greater_than_node.operation = 'GREATER_THAN'
        greater_than_node.inputs[1].default_value = 0.2

        boolean_and_node = node_tree.nodes.new(type="FunctionNodeBooleanMath")
        boolean_and_node.operation = 'AND'

        delete_geometry_node = node_tree.nodes.new(type="GeometryNodeDeleteGeometry")
        delete_geometry_node.domain = 'POINT'
        delete_geometry_node.mode = 'ALL'

        position_node_one = node_tree.nodes.new(type="GeometryNodeInputPosition")

        blur_attribute_one = node_tree.nodes.new(type="GeometryNodeBlurAttribute")
        blur_attribute_one.data_type = 'FLOAT_VECTOR'
        blur_attribute_one.inputs[4].default_value = 20  # iterations
        blur_attribute_one.inputs[5].default_value = 1  # weight

        named_attribute_two = node_tree.nodes.new(type="GeometryNodeInputNamedAttribute")
        named_attribute_two.data_type = 'FLOAT_COLOR'
        named_attribute_two.inputs[0].default_value = color_attr_name

        equal_node_two = node_tree.nodes.new(type="FunctionNodeCompare")
        equal_node_two.data_type = 'RGBA'
        equal_node_two.operation = 'NOT_EQUAL'
        equal_node_two.inputs[7].default_value = (1.0, 1.0, 0.0, 1.0)
        equal_node_two.inputs[12].default_value = 0.1

        set_position_node_one = node_tree.nodes.new(type="GeometryNodeSetPosition")

        extrude_mesh_node = node_tree.nodes.new(type="GeometryNodeExtrudeMesh")
        extrude_mesh_node.name = 'ufit_extrude_node'
        extrude_mesh_node.inputs[3].default_value = bpy.context.scene.ufit_voronoi_one_thickness/1000
        extrude_mesh_node.inputs[4].default_value = False  # individual

        flip_faces_node = node_tree.nodes.new(type="GeometryNodeFlipFaces")

        join_geometry_node = node_tree.nodes.new(type="GeometryNodeJoinGeometry")

        merge_by_dist_node = node_tree.nodes.new(type="GeometryNodeMergeByDistance")
        merge_by_dist_node.inputs[2].default_value = 0.0001  # 0.01cm

        position_node_two = node_tree.nodes.new(type="GeometryNodeInputPosition")

        blur_attribute_two = node_tree.nodes.new(type="GeometryNodeBlurAttribute")
        blur_attribute_two.name = 'ufit_smooth_node'
        blur_attribute_two.data_type = 'FLOAT_VECTOR'
        blur_attribute_two.inputs[4].default_value = 1  # smoothing iterations
        blur_attribute_two.inputs[5].default_value = 0.5

        set_position_node_two = node_tree.nodes.new(type="GeometryNodeSetPosition")

        node_tree.links.new(named_attribute.outputs[2], equal_node.inputs[6])
        node_tree.links.new(equal_node.outputs['Result'], boolean_and_node.inputs[1])
        node_tree.links.new(voronoi_node.outputs['Distance'], greater_than_node.inputs[0])
        node_tree.links.new(greater_than_node.outputs['Result'], boolean_and_node.inputs[0])

        # node_tree.links.new(greater_than_node.inputs[1], in_node.outputs[-1])  # TODO: FIGURE OUT
        node_tree.links.new(in_node.outputs['Geometry'], delete_geometry_node.inputs['Geometry'])
        node_tree.links.new(boolean_and_node.outputs['Boolean'], delete_geometry_node.inputs['Selection'])

        node_tree.links.new(named_attribute_two.outputs[2], equal_node_two.inputs[6])

        node_tree.links.new(position_node_one.outputs['Position'], blur_attribute_one.inputs[2])
        node_tree.links.new(blur_attribute_one.outputs[2], set_position_node_one.inputs['Position'])
        node_tree.links.new(equal_node_two.outputs['Result'], set_position_node_one.inputs['Selection'])
        node_tree.links.new(delete_geometry_node.outputs['Geometry'], set_position_node_one.inputs['Geometry'])

        node_tree.links.new(set_position_node_one.outputs['Geometry'], extrude_mesh_node.inputs['Mesh'])
        node_tree.links.new(set_position_node_one.outputs['Geometry'], flip_faces_node.inputs['Mesh'])

        node_tree.links.new(extrude_mesh_node.outputs['Mesh'], join_geometry_node.inputs['Geometry'])
        node_tree.links.new(flip_faces_node.outputs['Mesh'], join_geometry_node.inputs['Geometry'])

        node_tree.links.new(join_geometry_node.outputs['Geometry'], merge_by_dist_node.inputs['Geometry'])
        node_tree.links.new(position_node_two.outputs['Position'], blur_attribute_two.inputs[2])
        node_tree.links.new(equal_node_two.outputs['Result'], set_position_node_two.inputs['Selection'])
        node_tree.links.new(blur_attribute_two.outputs[2], set_position_node_two.inputs['Position'])
        node_tree.links.new(merge_by_dist_node.outputs['Geometry'], set_position_node_two.inputs['Geometry'])

        node_tree.links.new(set_position_node_two.outputs['Geometry'], out_node.inputs['Geometry'])

    else:
        geometry_modifier = ufit_obj.modifiers.new(name="Geometry Nodes", type='NODES')
        geometry_modifier.node_group = bpy.data.node_groups[tree_name]


def set_voronoi_geometry_nodes_two(ufit_obj, tree_name, color_attr_name):
    # Check if node tree already exists
    if tree_name not in bpy.data.node_groups:
        # Create a new geometry nodes modifer (automatically creates a node_group with name "Geometry Nodes"
        bpy.ops.node.new_geometry_nodes_modifier()

        # Rename the new node tree to "Voronoi Nodes Two"
        bpy.data.node_groups[0].name = tree_name

        # Access the "Voronoi Nodes Two" geometry nodes tree
        node_tree = bpy.data.node_groups[tree_name]

        in_node = node_tree.nodes["Group Input"]
        out_node = node_tree.nodes["Group Output"]

        named_attribute = node_tree.nodes.new(type="GeometryNodeInputNamedAttribute")
        named_attribute.data_type = 'FLOAT_COLOR'
        named_attribute.inputs[0].default_value = color_attr_name

        equal_node = node_tree.nodes.new(type="FunctionNodeCompare")
        equal_node.data_type = 'RGBA'
        equal_node.operation = 'EQUAL'
        equal_node.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
        equal_node.inputs[12].default_value = 0.1

        dual_mesh_node = node_tree.nodes.new(type="GeometryNodeDualMesh")
        dual_mesh_node.inputs[1].default_value = True  # keep boundaries

        extrude_mesh_node_one = node_tree.nodes.new(type="GeometryNodeExtrudeMesh")
        extrude_mesh_node_one.mode = 'FACES'
        extrude_mesh_node_one.inputs[3].default_value = 0

        scale_elements_node = node_tree.nodes.new(type="GeometryNodeScaleElements")
        scale_elements_node.inputs[2].default_value = 0.7

        # scale_elements_node = node_tree.nodes.new(type="GeometryNodeScaleElements")

        delete_geometry_node = node_tree.nodes.new(type="GeometryNodeDeleteGeometry")
        delete_geometry_node.domain = 'FACE'
        delete_geometry_node.mode = 'ALL'

        extrude_mesh_node_two = node_tree.nodes.new(type="GeometryNodeExtrudeMesh")
        extrude_mesh_node_two.name = 'ufit_extrude_node'
        extrude_mesh_node_two.inputs[3].default_value = bpy.context.scene.ufit_voronoi_two_thickness/1000  # thickness
        extrude_mesh_node_two.inputs[4].default_value = False  # individual

        flip_faces_node = node_tree.nodes.new(type="GeometryNodeFlipFaces")

        join_geometry_node = node_tree.nodes.new(type="GeometryNodeJoinGeometry")

        merge_by_dist_node = node_tree.nodes.new(type="GeometryNodeMergeByDistance")
        merge_by_dist_node.inputs[2].default_value = 0.0001

        subdivision_surface_node = node_tree.nodes.new(type="GeometryNodeSubdivisionSurface")
        subdivision_surface_node.inputs[1].default_value = 1

        shade_smooth_node = node_tree.nodes.new(type="GeometryNodeSetShadeSmooth")

        node_tree.links.new(in_node.outputs['Geometry'], dual_mesh_node.inputs['Mesh'])
        node_tree.links.new(named_attribute.outputs[2], equal_node.inputs[6])
        node_tree.links.new(equal_node.outputs['Result'], extrude_mesh_node_one.inputs['Selection'])
        node_tree.links.new(dual_mesh_node.outputs['Dual Mesh'], extrude_mesh_node_one.inputs['Mesh'])
        node_tree.links.new(extrude_mesh_node_one.outputs['Mesh'], scale_elements_node.inputs['Geometry'])
        node_tree.links.new(extrude_mesh_node_one.outputs['Top'], scale_elements_node.inputs['Selection'])
        node_tree.links.new(extrude_mesh_node_one.outputs['Top'], delete_geometry_node.inputs['Selection'])
        node_tree.links.new(scale_elements_node.outputs['Geometry'], delete_geometry_node.inputs['Geometry'])
        node_tree.links.new(delete_geometry_node.outputs['Geometry'], extrude_mesh_node_two.inputs['Mesh'])
        node_tree.links.new(delete_geometry_node.outputs['Geometry'], flip_faces_node.inputs['Mesh'])
        node_tree.links.new(extrude_mesh_node_two.outputs['Mesh'], join_geometry_node.inputs['Geometry'])
        node_tree.links.new(flip_faces_node.outputs['Mesh'], join_geometry_node.inputs['Geometry'])
        node_tree.links.new(join_geometry_node.outputs['Geometry'], merge_by_dist_node.inputs['Geometry'])
        node_tree.links.new(merge_by_dist_node.outputs['Geometry'], subdivision_surface_node.inputs['Mesh'])
        node_tree.links.new(subdivision_surface_node.outputs['Mesh'], shade_smooth_node.inputs['Geometry'])
        node_tree.links.new(shade_smooth_node.outputs['Geometry'], out_node.inputs['Geometry'])

    else:
        geometry_modifier = ufit_obj.modifiers.new(name="Geometry Nodes", type='NODES')
        geometry_modifier.node_group = bpy.data.node_groups[tree_name]
