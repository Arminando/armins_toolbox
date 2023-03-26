import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    EnumProperty,
)
from . import log
from . import common
from .utils.bl_class_registry import BlClassRegistry

def set_debug_mode(self, value):
    self['enable_debug_mode'] = value

def get_debug_mode(self):
    enabled = self.get('enable_debug_mode', False)
    if enabled:
        common.enable_debug_mode()
    else:
        common.disable_debug_mode()
    return enabled

def set_logging_level(self, value):
    self['logging_level'] = value

def get_logging_level(self):
    level = self.get('logging_level', 10)
    log.set_log_level(level)
    return level


@BlClassRegistry()
class AT_Preferences(AddonPreferences):
    """Preferences class: Preferences for this add-on"""

    bl_idname = "armins_toolbox"

    # enable debug mode
    enable_debug_mode : BoolProperty(
        name="Debug Mode",
        description="Enable debugging mode",
        default=True,
    )

    logging_level : EnumProperty(
        name = "Logging Level",
        description = "Set the log output level",
        items=(('NOTSET', 'NOTSET', 'NOTSET', 0),
               ('DEBUG', 'DEBUG', 'DEBUG', 10),
               ('INFO', 'INFO', 'INFO', 20),
               ('WARNING', 'WARNING', 'WARNING', 30),
               ('ERROR', 'ERROR', 'ERROR', 40),
               ('CRITICAL', 'CRITICAL', 'CRITICAL', 50)),
        default = 'DEBUG',

    )


    # for UI
    category : EnumProperty(
        name="Category",
        description="Preferences Category",
        items=[
            ('INFO', "Information", "Information about this add-on"),
            ('CONFIG', "Configuration", "Configuration about this add-on"),
        ],
        default='INFO'
    )
    info_desc_expanded : BoolProperty(
        name="Description",
        description="Description",
        default=False
    )
    info_loc_expanded : BoolProperty(
        name="Location",
        description="Location",
        default=False
    )
    conf_uv_sculpt_expanded : BoolProperty(
        name="UV Sculpt",
        description="UV Sculpt",
        default=False
    )

    def draw(self, _):
        layout = self.layout
        layout.row(align = True).prop(self, "category", expand=True)

        if self.category == 'INFO':
            layout.separator()


            layout.prop(
                self, "info_desc_expanded", text="Description",
                icon='DISCLOSURE_TRI_DOWN' if self.info_desc_expanded
                else 'DISCLOSURE_TRI_RIGHT')
            if self.info_desc_expanded:
                col = layout.column(align=True)
                col.label(text="Add some info here. Duplicate label to add more lines.")


            layout.prop(
                self, "info_loc_expanded", text="Location",
                icon='DISCLOSURE_TRI_DOWN' if self.info_loc_expanded
                else 'DISCLOSURE_TRI_RIGHT')
            if self.info_loc_expanded:
                col = layout.column(align=True)
                col.label(text="Add some info here. Duplicate label to add more lines.")

        elif self.category == 'CONFIG':
            layout.separator()
            layout.use_property_split = True
            layout.use_property_decorate = False
            layout.prop(self, "enable_debug_mode", text="Debug Mode")
            layout.prop(self, "logging_level", text = "Logging Level")