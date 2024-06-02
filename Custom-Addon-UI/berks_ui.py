bl_info = {
    "name": "Berks UI",
    "description": "Create a Berks UI for simple material managing.",
    "author": "B. Berk Şengül",
    "version": (1, 1, 0),
    "blender": (4, 0, 2),
    "warning": "",
    "doc_url": "https://github.com/WorldOfBerk/Blender-Material-UI",
    "category": "User Interface",
}

import bpy
from bpy.types import Operator, Panel

# Version
version = "1.1.0"

def update_shader(self, context):
    mat = context.object.active_material
    if mat:
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Remove all existing nodes
        for node in nodes:
            nodes.remove(node)

        # Add new shader node and material output node
        shader_node = nodes.new(type=self.shader_type)
        output_node = nodes.new(type='ShaderNodeOutputMaterial')

        # Link new shader node to material output node
        links.new(shader_node.outputs[0], output_node.inputs[0])

        # Set the name for easy access later
        shader_node.name = self.shader_type

class CustomUITab(Panel):
    bl_label = "Berks UI"
    bl_idname = "PT_CustomUITab"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Berks UI"

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.active_material is not None

    def invoke(self, context, event):
        update_shader(context.scene, context)
        return self.execute(context)

    def execute(self, context):
        layout = self.layout
        obj = context.object

        # Dropdown menu for material selection
        layout.label(text="Select Material:")
        layout.prop(obj, "active_material")

        # Button to create a new material
        layout.operator("material.new_material", text="Create New Material")

        # Surface shader selection
        #layout.label(text="Surface:")
        layout.prop(context.scene, "shader_type", text="Shader")

        if obj.active_material:
            node_tree = obj.active_material.node_tree
            nodes = node_tree.nodes

            shader_node = nodes.get(context.scene.shader_type)

            if shader_node:
                if context.scene.shader_type == 'ShaderNodeBsdfPrincipled':
                    layout.prop(shader_node.inputs['Base Color'], "default_value", text="Base Color")
                    layout.prop(shader_node.inputs['Metallic'], "default_value", text="Metallic")
                    layout.prop(shader_node.inputs['Roughness'], "default_value", text="Roughness")
                elif context.scene.shader_type == 'ShaderNodeBsdfDiffuse':
                    layout.prop(shader_node.inputs['Color'], "default_value", text="Color")
                    layout.prop(shader_node.inputs['Roughness'], "default_value", text="Roughness")
                elif context.scene.shader_type == 'ShaderNodeBsdfGlossy':
                    layout.prop(shader_node.inputs['Color'], "default_value", text="Color")
                    layout.prop(shader_node.inputs['Roughness'], "default_value", text="Roughness")

        # Info section
        layout.separator()
        layout.label(text="Info:")

        # GitHub repository link
        repo_row = layout.row(align=True)
        repo_row.operator("wm.url_open", text="GitHub").url = "https://github.com/WorldOfBerk/Blender-Material-UI"

        # Version display
        layout.label(text=f"Version: {version}")

    def draw(self, context):
        self.execute(context)

class NewMaterialOperator(Operator):
    bl_idname = "material.new_material"
    bl_label = "Create New Material"

    def execute(self, context):
        bpy.ops.material.new()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CustomUITab)
    bpy.utils.register_class(NewMaterialOperator)
    bpy.types.Scene.shader_type = bpy.props.EnumProperty(
        items=[
            ('ShaderNodeBsdfPrincipled', 'Principled BSDF', ''),
            ('ShaderNodeBsdfDiffuse', 'Diffuse BSDF', ''),
            ('ShaderNodeBsdfGlossy', 'Glossy BSDF', '')
        ],
        name="Shader",
        default='ShaderNodeBsdfPrincipled',
        update=update_shader
    )

def unregister():
    bpy.utils.unregister_class(CustomUITab)
    bpy.utils.unregister_class(NewMaterialOperator)
    del bpy.types.Scene.shader_type

if __name__ == "__main__":
    register()
