from . log import logger

__debug_mode = False

def enable_debug_mode():
    global __debug_mode
    global logger
    __debug_mode = True
    logger.debug("Debug mode enabled")


def disable_debug_mode():
    global __debug_mode
    global logger
    __debug_mode = False
    logger.debug("Debug mode disabled")

def get_debug_mode():
    return __debug_mode