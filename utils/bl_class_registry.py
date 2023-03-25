import bpy
from ..log import logger

class BlClassRegistry:
    class_list = []

    def __init__(self, *_, **kwargs):
        pass

    def __call__(self, cls):
        if hasattr(cls, "bl_idname"):
            BlClassRegistry.add_class(cls.bl_idname, cls)
        elif hasattr(cls, "bl_context"):
            bl_idname = "{}{}{}{}".format(cls.bl_space_type,
                                          cls.bl_region_type,
                                          cls.bl_context, cls.bl_label)
            BlClassRegistry.add_class(bl_idname, cls)
        else:
            bl_idname = "{}{}{}".format(cls.bl_space_type,
                                        cls.bl_region_type,
                                        cls.bl_label)
            BlClassRegistry.add_class(bl_idname, cls)
        return cls

    @classmethod
    def add_class(cls, bl_idname, op_class):
        for class_ in cls.class_list:
            if (class_["bl_idname"] == bl_idname):
                logger.error(f"{bl_idname} is already registered")
                raise RuntimeError("{} is already registered"
                                   .format(bl_idname))

        new_op = {
            "bl_idname": bl_idname,
            "class": op_class,
        }
        cls.class_list.append(new_op)
        logger.debug(f"{bl_idname} is registered.")

    @classmethod
    def register(cls):
        for class_ in cls.class_list:
            bpy.utils.register_class(class_["class"])
            logger.debug(f"{class_['bl_idname']} is registered")

    @classmethod
    def unregister(cls):
        for class_ in cls.class_list:
            bpy.utils.unregister_class(class_["class"])
            logger.debug(f"{class_['bl_idname']} is unregistered")

    @classmethod
    def cleanup(cls):
        cls.class_list = []
        logger.debug("Cleanup registry")







