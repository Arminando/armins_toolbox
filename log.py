import logging
import sys
import bpy

class _CustomFormatter(logging.Formatter):
    """ Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """

    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(_CustomFormatter, self).format(record)

__log_level = 20

logger = logging.getLogger("Armin's Toolbox")
try:
    logger.setLevel(bpy.context.preferences.addons['armins_toolbox'].preferences['logging_level'])
except:
    logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("armins_toolbox.log")
stream_handler = logging.StreamHandler(sys.stdout)

file_handler.setFormatter(_CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s, l.%(lineno)d - %(message)s'))
stream_handler.setFormatter(_CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s, l.%(lineno)d - %(message)s'))

logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def set_log_level(value):
    global __log_level
    global logger
    logger.setLevel(value)
    logger.debug("Log level set to " + str(value))

def get_log_level():
    return __log_level