import bpy.types

from .utils.property_class_registry import PropertyClassRegistry


# Properties used in this add-on.
class AT_Properties():
    pass

def init_props(scene):
    scene.at_props = AT_Properties()
    PropertyClassRegistry.init_props(scene)


def clear_props(scene):
    PropertyClassRegistry.del_props(scene)
    del scene.at_props
