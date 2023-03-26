import bpy
from ..log import logger, log

def get_mode(context: bpy.types.Context) -> str:
    #logger.info(f"Current mode is {context.mode}.")
    return context.mode

def get_object(name: str) -> bpy.types.Object:
    if obj_exists(name):
        obj = bpy.data.objects[name]
        logger.debug(f"Returning object {obj}.")
        return obj
    else:
        logger.warning(f"{name} does not exist. Returning None.")
        return None
def get_edit_bone(obj: str, bone: str) -> bpy.types.EditBone:
    if bone_exists(obj, bone):
        edit_bone = bpy.data.objects[obj].data.edit_bones[bone]
        logger.debug(f"Return get edit bone {edit_bone} for {bone}.")
        return edit_bone
    else:
        logger.warning(f"{bone} does not exist. Returning None.")
        return None

def get_pose_bone(obj: str, bone: str) -> bpy.types.PoseBone:
    if bone_exists(obj, bone):
        pose_bone = bpy.data.objects[obj].pose.bones[bone]
        logger.debug(f"Return get pose bone {pose_bone} for {bone}.")
        return pose_bone
    else:
        logger.warning(f"{bone} does not exist. Returning None.")
        return None

def get_bone(obj: str, bone: str) -> bpy.types.Bone:
    if bone_exists(obj, bone):
        bone = bpy.data.objects[obj].data.bones[bone]
        logger.debug(f"Return get bone {bone} for {bone}.")
        return bone
    else:
        logger.warning(f"{bone} does not exist. Returning None.")
        return None

def get_active_object(context: bpy.types.Context) -> bpy.types.Object:
    obj = context.active_object
    logger.debug(f"Returning active object {obj}.")
    return obj

def set_mode(mode: str) -> None:
    bpy.ops.object.mode_set(mode = mode)
    logger.debug(f"Set mode to {mode}.")

def is_mode_edit_armature(context: bpy.types.Context) -> bool:
    return get_mode(context) == 'EDIT_ARMATURE'

def is_mode_edit(context: bpy.types.Context) -> bool:
    return get_mode(context) == 'EDIT'

def is_mode_object(context: bpy.types.Context) -> bool:
    return get_mode(context) == 'OBJECT'

def set_mode_edit() -> None:
    set_mode('EDIT')

def set_mode_object() -> None:
    set_mode('OBJECT')

def obj_exists(obj: str) -> bool:
    return obj in bpy.data.objects

def bone_exists(obj: str, bone: str) -> bool:
    return bone in bpy.data.objects[obj].data.edit_bones

def get_type(obj: str) -> str:
    return bpy.data.objects[obj].type

def is_type_armature(obj: str) -> bool:
    return get_type(obj) == 'ARMATURE'

def restore_selected_bones(context: bpy.types.Context, obj: str, bones: list[str]) -> None:
    if type(bones) is not list:
        logger.warning(f"{bones} is not a list. Returning None.")
        return None
    for bone in bones:
        get_edit_bone(obj, bone).select = True
    logger.debug(f"Restored selected bones: {bones}.")

def restore_active_bone(context: bpy.types.Context, obj: str, bone: str) -> None:
    get_edit_bone(obj, bone).select = True
    get_object(obj).data.bones.active = get_bone(obj, bone)
    logger.debug(f"Restored active bone: {bone}.")