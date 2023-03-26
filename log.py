import logging, sys, functools, os
from inspect import getframeinfo, stack
from typing import Union
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

default_formatter = _CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s, l.%(lineno)d - %(message)s')
file_handler.setFormatter(default_formatter)
stream_handler.setFormatter(default_formatter)

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

# Function decorator to log function details
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        py_file_caller = getframeinfo(stack()[1][0])
        file_handler.setFormatter(_CustomFormatter('%(asctime)s - %(levelname)-10s - %(message)s'))
        stream_handler.setFormatter(_CustomFormatter('%(asctime)s - %(levelname)-10s - %(message)s'))
        logger.debug(f"{os.path.basename(py_file_caller.filename)} - {func.__name__} - Args: {signature}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Returned: {result!r}")
            file_handler.setFormatter(default_formatter)
            stream_handler.setFormatter(default_formatter)
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. Exception: {str(e)}")
            file_handler.setFormatter(default_formatter)
            stream_handler.setFormatter(default_formatter)
            raise e

    return wrapper