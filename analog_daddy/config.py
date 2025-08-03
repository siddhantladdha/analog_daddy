"""
config.py

Centralized configuration loader for the analog_daddy package.

This module loads the main TOML configuration file once at import time and exposes
it as the global variable CONFIG. Other modules should import CONFIG from this module
to access application-wide settings.

Config sections:
- DashboardConfig: Dashboard UI and behavior settings
- ToolConfig: Tool-specific settings
- TechnologyConfig: Technology settings, including defaults and per-technology configs

Usage:
    from analog_daddy.config import CONFIG
    layout = CONFIG.dashboard.layout
    gpdk_settings = CONFIG.technology['gpdk45']
    default_tech = CONFIG.technology.default

Notes:
- The config file is only read once per process, regardless of how many times CONFIG is imported.
- Any exceptions during config loading should be handled at the application entry point, not here.
"""
from typing import Dict, Any
from pathlib import Path
import tomlkit
from analog_daddy.logging_config import CustomFileError
CONFIG = None

class BaseConfigSection:
    """
    Base class for config sections. Sets only allowed keys as attributes.
    """
    allowed_keys = []
    def __init__(self, config_dict):
        for key in self.allowed_keys:
            setattr(self, key, config_dict.get(key))

class DashboardConfig(BaseConfigSection):
    """
    Dashboard-specific configuration.
    Only allowed keys are set as attributes for safety.
    """
    allowed_keys = [
        "layout", "initial_sidebar_state", "debug_mode"
    ]

class ToolConfig(BaseConfigSection):
    """
    Tool-specific configuration.
    Only allowed keys are set as attributes for safety.
    """
    allowed_keys = [
        "method_key", "warning_key", "importer_verbose"
    ]

class TechnologySettings(BaseConfigSection):
    """
    Settings for a single technology.
    Only allowed keys are set as attributes for safety.
    """
    allowed_keys = [
        "technology_info", "parameter_tag",
        "gm_key_start", "length_key",
        "gs_key", "ds_key", "sb_key",
        "db_key", "gb_key", "vdd",
        "is_integer",
        "l_min", "l_max", "length_increment",
        "w_min", "w_max", "voltage_step_size",
    ]

class TechnologyConfig:
    """
    Technology configuration, with a default and per-technology settings.
    Loads default technology settings and all named technology sections from config.
    Supports arbitrary technology keys.
    """
    def __init__(self, config_dict):
        tech_dict = config_dict.copy()
        self.default = TechnologySettings(tech_dict.pop("default_technology_settings", {}))
        self.technologies = {k: TechnologySettings(v) for k, v in tech_dict.items()}
    def __getitem__(self, key):
        return self.technologies[key]
    def get(self, key, default=None):
        """Safer get method to avoid KeyError."""
        return self.technologies.get(key, default)

class AppConfig:
    """
    Main application config, aggregating all sections.
    Provides access to dashboard, tool, and technology configs, plus raw dict fallback.
    Immutable after initialization.
    """
    def __init__(self, config_dict):
        object.__setattr__(self, '_initialized', False)
        self.dashboard = DashboardConfig(config_dict.get("dashboard", {}))
        self.tool = ToolConfig(config_dict.get("tool", {}))
        # Remove non-technology keys for TechnologyConfig
        tech_config = config_dict.copy()
        tech_config.pop("tool", None)
        tech_config.pop("dashboard", None)
        self.technology = TechnologyConfig(tech_config)
        object.__setattr__(self, '_initialized', True)
    def __setattr__(self, name, value):
        if getattr(self, '_initialized', False):
            raise AttributeError(f"Cannot modify immutable AppConfig: '{name}'")
        object.__setattr__(self, name, value)

# Load config as object
# The function will be decorated for resource caching when using with streamlit at the top level.
def load_config(config_path):
    """
    Loads the application configuration from the specified TOML file path.

    This function reads the configuration file, parses its contents, and initializes
    a global CONFIG object of type AppConfig, making it accessible to submodules.

    Args:
        config_path (str): The file path to the TOML configuration file.

    Raises:
        Passes along exceptions raised from config_toml_reader.
    """
    config_dict = config_toml_reader(config_path)
    # Need a global config to make it accessible for submodules.
    global CONFIG # pylint: disable=global-statement
    CONFIG = AppConfig(config_dict)

def config_toml_reader(
        filepath: str = "~/.analog_daddy/config/config.toml"
        ) -> Dict[str, Any]:
    """
    Read the TOML configuration file and return it as a dictionary.
    If no filepath is provided, defaults to a standard config path
    at ~/.analog_daddy/config/config.toml
    If there are issues with opening files raises a CustomFileError.
    TODO: Deal with tomlkit loading exceptions.
    """
    path = Path(filepath).expanduser()
    try:
        with path.open("r", encoding="utf-8") as f:
            # toml file is now loaded as a TOMLDocument (preserves comments)
            toml_doc = tomlkit.load(f)
            # Convert to dict for downstream compatibility
            return dict(toml_doc)
    except Exception as e:
        raise CustomFileError(str(path), e) from e
