"""
analog_daddy: This library is an attempt to make transistor sizing for Analog Design less painful.

This module dynamically loads package metadata from setup.cfg for a single point of truth.
"""
import os
import configparser

# Path to setup.cfg (assumes analog_daddy/ is a subdir of the project root)
_cfg_path = os.path.join(os.path.dirname(__file__), '..', 'setup.cfg')
_cfg_path = os.path.abspath(_cfg_path)

_cfg = configparser.ConfigParser()
_cfg.read(_cfg_path, encoding="utf-8")
meta = _cfg["metadata"]

__version__ = meta.get("version", "unknown")
__author__ = meta.get("author", "")
__author_email__ = meta.get("author_email", "")
__license__ = meta.get("license", "")
__url__ = meta.get("url", "")
__description__ = meta.get("description", "")

# __all__ = [
#     "look_up",
#     "importer",
#     "utils",
#     "write_config",
#     # Add other public modules/classes/functions here as needed
# ]

# from . import look_up, importer, utils, write_config
# Optionally, import key functions/classes for top-level access
# from .look_up import look_up_function
# from .importer import import_function
