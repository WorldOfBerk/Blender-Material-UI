import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty

# Version
version = "0.0.1"

class CustomUITab(bpy.types.Panel):
    bl_label = "Berks UI"
    bl_idname = "PT_CustomUITab"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Berks UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Dropdown menu for material selection
        layout.label(text="Select Material:")
        layout.prop(obj, "active_material")

        # Button to create a new material
        layout.operator("material.new_material", text="Create New Material")

        # Button for color changing
        layout.label(text="Change Color:")
        layout.operator("material.change_color", text="Change Color")

        # Info section
        layout.separator()
        layout.label(text="Info:")

        # GitHub repository link
        repo_row = layout.row(align=True)
        repo_row.operator("wm.url_open", text="GitHub").url = "https://github.com/WorldOfBerk/Blender-Material-UI"

        # Version display
        layout.label(text=f"Version: {version}")

class NewMaterialOperator(Operator):
    bl_idname = "material.new_material"
    bl_label = "Create New Material"

    def execute(self, context):
        bpy.ops.material.new()
        return {'FINISHED'}

class ChangeColorOperator(Operator):
    bl_idname = "material.change_color"
    bl_label = "Change Color"

    def invoke(self, context, event):
        # Get the initial color of the selected material
        active_material = context.object.active_material
        if active_material:
            bsdf = active_material.node_tree.nodes.get('Principled BSDF')
            if bsdf:
                self.color = bsdf.inputs['Base Color'].default_value
        context.window_manager.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        active_material = context.object.active_material

        # Access the Principled BSDF shader
        bsdf = active_material.node_tree.nodes.get('Principled BSDF')

        # Change the Base Color
        if bsdf:
            bsdf.inputs['Base Color'].default_value = self.color

        return {'FINISHED'}

    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=4,  # Set the size to 4
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0)  # Set the default alpha value to 1, can be visible in SOLID mode
    )

def register():
    bpy.utils.register_class(CustomUITab)
    bpy.utils.register_class(NewMaterialOperator)
    bpy.utils.register_class(ChangeColorOperator)

def unregister():
    bpy.utils.unregister_class(CustomUITab)
    bpy.utils.unregister_class(NewMaterialOperator)
    bpy.utils.unregister_class(ChangeColorOperator)

if __name__ == "__main__":
    register()