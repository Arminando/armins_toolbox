if "bpy" in locals():
    import importlib
    importlib.reload(bl_class_registry)
    importlib.reload(property_class_registry)
else:
    from . import bl_class_registry
    from . import property_class_registry

import bpy
