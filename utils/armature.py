from ..log import logger, log
import mathutils
from ..utils.context import is_mode_edit_armature, obj_exists, is_type_armature, bone_exists, get_edit_bone

import bpy
@log
def points_from_bone_list(obj: str, bones: list[str]) -> list[mathutils.Vector]:
    """
    Returns a list of points from a list of bones. The first points are the head of bones, the last point is the tail of the last bone.
    :param obj: The name of the armature object
    :param bones: A list of bone names
    :return: A list of xyz coordinates
    """
    if not obj_exists(obj):
        logger.warning(f"{obj} does not exist. Returning None.")
        return None

    armature = bpy.data.objects[obj]

    edit_bones = [armature.data.edit_bones[bone] for bone in bones if bone_exists(obj, bone)]
    if len(edit_bones) != len(bones):
        logger.warning(f"Some bones in {bones} do not exist. Returning None.")
        return None

    points = []
    for bone in edit_bones:
        if not points:
            points.append(((bone.head - bone.tail) + bone.head))

        points.append(bone.head)
        if bone == edit_bones[-1]:
            points.append(bone.tail)
            points.append(((bone.tail - bone.head) + bone.tail))

    logger.debug(f"Points from bone list: {points}.")
    return points

def get_bone_chain(obj: str, first: str, last: str) -> list[str]:
    """
    Returns a chain of bones from first to last.
    :param obj: The name of the armature object
    :param first: The name of the first bone
    :param last: The name of the last bone
    :return: List of bone names, or None if the chain is invalid
    """
    if not is_mode_edit_armature(bpy.context):
        logger.warning(f"{obj} not in edit mode. Returning None.")
        return None
    if not obj_exists(obj) or not is_type_armature(obj):
        logger.warning(f"{obj} object does not exist or is not an armature. Returning None.")
        return None
    if not bone_exists(obj, first) or not bone_exists(obj, last):
        logger.warning(f"{first} or {last} bone does not exist. Returning None.")
        return None

    armature = bpy.data.objects[obj]
    first_bone = armature.data.edit_bones[first]
    last_bone = armature.data.edit_bones[last]

    all_parents = last_bone.parent_recursive
    if first_bone not in all_parents:
        logger.warning(f"{first} is not in parent hierarchy of {last}. Returning None.")
        return None

    bone_chain = [last_bone] + all_parents[:all_parents.index(first_bone) + 1]
    bone_chain.reverse()
    bones = [x.name for x in bone_chain]

    logger.debug(f"Returning bone chain: {bones}")
    return bones

@log
def update_bone_pos(obj: str, bones: list[str], positions: list[mathutils.Vector]):
    """
    Updates the head and tail of a list of bones to a list of positions.
    Length of bones and positions must be len(bones)+1 == len(positions).
    :param obj: The name of the armature object
    :param bones: A list of bone names
    :param positions: A list of xyz coordinates
    :return: None
    """
    if not obj_exists(obj):
        logger.warning(f"{obj} does not exist. Returning None.")
        return None

    armature = bpy.data.objects[obj]
    if len(bones)+1 != len(positions):
        logger.warning(f"Bone list length ({len(bones)}) and position list lenght ({len(positions)}) are not compatible. Must be len(bones)+1 == len(positions). Returning None.")
        return None

    for i, bone in enumerate(bones):
        if not bone_exists(obj, bone):
            logger.debug(f"{bone} does not exist. Skipped it.")
        edit_bone = get_edit_bone(obj, bone)
        edit_bone.head = positions[i]
        edit_bone.tail = positions[i+1]