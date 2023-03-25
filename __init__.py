bl_info = {
    "name": "Armins Toolbox",
    "description": "Mix of tools for Rigging and Animation",
    "author": "Armin Halac",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "warning": "In development, things may (and will) change.",
    "location": "",
    # "doc_url": "{BLENDER_MANUAL_URL}/addons/animation/pose_library.html",
    "category": "Animation",
}


if "bpy" in locals():
    import importlib
    importlib.reload(log)
    importlib.reload(utils)
    utils.bl_class_registry.BlClassRegistry.cleanup()
    importlib.reload(op)
    importlib.reload(ui)
    importlib.reload(properties)
    importlib.reload(preferences)
else:
    import bpy
    from . import log
    from . import utils
    from . import op
    from . import ui
    from . import properties
    from . import preferences

import bpy


def register():
    utils.bl_class_registry.BlClassRegistry.register()
    properties.init_props(bpy.types.Scene)



def unregister():
    properties.clear_props(bpy.types.Scene)
    utils.bl_class_registry.BlClassRegistry.unregister()


if __name__ == "__main__":
    register()