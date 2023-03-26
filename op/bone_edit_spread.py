import bpy
from bpy.props import BoolProperty
from ..log import logger, log

from ..utils.bl_class_registry import BlClassRegistry
from ..utils.fibonacci import fibonacci
from ..utils.spline import point_on_catmull_rom
from ..utils.context import is_mode_edit_armature, get_active_object, restore_selected_bones, restore_active_bone
from ..utils.armature import points_from_bone_list, get_bone_chain, update_bone_pos


SPREAD_TYPES = [
    ("FIBONACCI", "Fibonacci", "", 0),
    ("EVEN", "Even", "", 1),
]

@BlClassRegistry()
class AT_OT_Operator_Spread_Bones(bpy.types.Operator):
    """
        Takes a chain of bones and spreads them out along a catmull rom spline. The first and last bone in the chain must be selected.
        Offers two options for distribution: Fibonacci and Even.
    """
    bl_idname = "armature.spread_bones"
    bl_label = "Spread bones"
    bl_description = "Spread bones in a chain, using fibonacci or even distribution.\nSelect the first and last bone in the chain. Last bone must be the active bone"
    bl_options = {'REGISTER', 'UNDO'}

    # Operator properties (these will show up after the operator is executed)
    spread_type: bpy.props.EnumProperty(items=SPREAD_TYPES, default="FIBONACCI")

    @classmethod
    def poll(cls, context) -> bool:
        if is_mode_edit_armature(context) and len(context.selected_bones) > 1:
            return True
        else:
            cls.poll_message_set("Must be in edit mode with at least 2 bone selected")
            return False


    def execute(self, context):
        logger.debug("Executing operator: %s", self.bl_idname)
        armature = get_active_object(context)

        last_bone = bpy.context.active_bone
        prunned_selection = bpy.context.selected_editable_bones
        prunned_selection.remove(last_bone)
        first_bone = prunned_selection[0]

        bones = get_bone_chain(armature.name, first_bone.name, last_bone.name)
        points = points_from_bone_list(armature.name, bones)

        if self.spread_type == "FIBONACCI":
            fibonacci_seq = fibonacci(len(bones), start=3)
            fibonacci_seq.reverse()
            scale_factor = 1.0 / sum(fibonacci_seq)
            lengths = [x * scale_factor for x in fibonacci_seq]
        else:
            lengths = [1 / len(bones) for _ in range(len(bones))]

        updated_pos = [point_on_catmull_rom(points, 0)]
        t = 0
        for x in lengths:
            t += x
            updated_pos.append(point_on_catmull_rom(points, t))

        update_bone_pos(armature.name, bones, updated_pos)

        restore_selected_bones(context, armature.name, [first_bone.name])
        restore_active_bone(context, armature.name, last_bone.name)

        logger.debug("Operator executed successfully: %s", self.bl_idname)
        self.report({'INFO'}, "Operator executed successfully.")
        return {'FINISHED'}


