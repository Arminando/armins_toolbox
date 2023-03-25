if "bpy" in locals():
    import importlib
    importlib.reload(template)
else:
    from . import template
import bpy
