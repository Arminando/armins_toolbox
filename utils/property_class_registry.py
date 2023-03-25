from ..log import logger

class PropertyClassRegistry:
    class_list = []

    def __init__(self, *_, **kwargs):
        pass

    def __call__(self, cls):
        PropertyClassRegistry.add_class(cls.idname, cls)
        return cls

    @classmethod
    def add_class(cls, idname, prop_class):
        for class_ in cls.class_list:
            if (class_["idname"] == idname):
                logger.error(f"{idname} is already registered")
                raise RuntimeError("{} is already registered".format(idname))

        new_op = {
            "idname": idname,
            "class": prop_class,
        }
        cls.class_list.append(new_op)
        logger.debug(f"{idname} is registered.")

    @classmethod
    def init_props(cls, scene):
        for class_ in cls.class_list:
            class_["class"].init_props(scene)
            logger.debug(f"{class_['idname']} is initialized")

    @classmethod
    def del_props(cls, scene):
        for class_ in cls.class_list:
            class_["class"].del_props(scene)
            logger.debug(f"{class_['idname']} is cleared")

    @classmethod
    def cleanup(cls):
        cls.class_list = []
        logger.debug("Cleanup registry")