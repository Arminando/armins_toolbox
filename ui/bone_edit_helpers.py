import bpy

from ..utils.bl_class_registry import BlClassRegistry

@BlClassRegistry()
class AT_PT_View3D_Bone_Edit_Helpers(bpy.types.Panel):
    """
    Panel Class: Collection of tools for editing bones
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AT"
    bl_label = "Bone Edit Helpers"
    #bl_idname = "AT_PT_View3D_Template"


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        column = layout.column()
        row = column.row(align=True)
        row.label(text="Spread Bones:")
        row.operator("armature.spread_bones", text = "", icon = "SORTSIZE").spread_type = "FIBONACCI"
        row.operator("armature.spread_bones", text = "", icon = "ALIGN_JUSTIFY").spread_type = "EVEN"
