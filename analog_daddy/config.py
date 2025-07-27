"""
config.py

Centralized configuration loader for the analog_daddy package.

This module loads the main TOML configuration file once at import time and exposes
it as the global variable CONFIG. Other modules should import CONFIG from this module
to access application-wide settings.

- The config file is only read once per process, regardless of how many times CONFIG is imported.
- Any exceptions during config loading should be handled at the application entry point, not here.
"""

import os
from analog_daddy.toml_utils import config_toml_reader
# try-catch handled at level where config is used
CONFIG = config_toml_reader(
    os.path.join(os.path.dirname(__file__), '..','.config','config.toml'))
