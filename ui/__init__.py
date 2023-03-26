if "bpy" in locals():
    import importlib
    importlib.reload(template)
    importlib.reload(bone_edit_helpers)
else:
    from . import template
    from . import bone_edit_helpers
import bpy
