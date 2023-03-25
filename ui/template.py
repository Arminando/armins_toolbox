import bpy

from ..utils.bl_class_registry import BlClassRegistry

@BlClassRegistry()
class AT_PT_View3D_Template(bpy.types.Panel):
    """
    Panel class: Main on Property Panel on View3D
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AT"
    bl_label = "Armin's Template"
    bl_idname = "AT_PT_View3D_Template"


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.label(text="Hello World")
        layout.operator('object.template_operator')