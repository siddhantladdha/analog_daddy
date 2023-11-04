"""
The purpose of this script is to write a configuration file for analog_daddy.
It additionally sanitizes the user input to ensure that the configuration file
is valid and has no syntax errors.

DO NOT WRITE THIS FILE MANUALLY. Instead use the write_config.py script
as follows:
from analog_daddy.write_config import write_config
write_config()
"""
import time

def prompt_natural_number(message, default, min_val=None, max_val=None):
    """Prompt the user for a natural number and validate against optional bounds."""
    while True:
        try:
            value = input(f"{message} (default: {default}): ") or default
            value = int(value)
            if value < 1:
                raise ValueError("Natural numbers are greater than 0.")
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            print("Invalid input. Please provide a valid natural number.")

def prompt_float(message, default, min_val=None, max_val=None):
    """Prompt the user for a float and validate against optional bounds."""
    while True:
        try:
            value = input(f"{message} (default: {default}, in SI units): ") or default
            value = float(value)
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                raise ValueError
            return value
        except ValueError:
            print("Invalid input. Please provide a valid number in SI units.")

def prompt_bool(message, default):
    """Prompt the user for a boolean value (True or False)."""
    while True:
        value = input(f"{message} (default: {default}): ").lower() or str(default).lower()
        if value in ['true', 't', 'yes', 'y']:
            return True
        if value in ['false', 'f', 'no', 'n']:
            return False
        print("Invalid input. Please provide a valid boolean value (yes/no or true/false).")

def prompt_string(message, default):
    """Prompt the user for a string."""
    return input(f"{message} (default: {default}): ") or default

def write_config(config_path):
    """Write a configuration file for analog_daddy."""
    # Provide default values as examples
    default_values = {
        'PARAMETER_TAG': 'Parameters:',
        'GM_KEY_START': 'gm_',
        'LENGTH_KEY': 'length',
        'GS_KEY': 'gs',
        'DS_KEY': 'ds',
        'SB_KEY': 'sb',
        'DB_KEY': 'db',
        'GB_KEY': 'gb',
        'METHOD_KEY': 'METHOD',
        'WARNING_KEY': 'WARNING',
        'VDD': 0.9,
        'IS_INTEGER': False,
        'L_MIN': 1e-06,
        'L_MAX': 2e-06,
        'W_MIN': 320e-09,
        'W_MAX': 10e-06,
        'VOLTAGE_STEP_SIZE': 20e-03,
        'IMPORTER_VERBOSE': True
    }

    # Gather inputs using the default values
    parameter_tag = prompt_string("Enter the value for PARAMETER_TAG",
                                  default_values['PARAMETER_TAG'])
    gm_key_start = prompt_string("Enter the value for GM_KEY_START", default_values['GM_KEY_START'])
    length_key = prompt_string("Enter the value for LENGTH_KEY", default_values['LENGTH_KEY'])
    gs_key = prompt_string("Enter the value for GS_KEY", default_values['GS_KEY'])
    ds_key = prompt_string("Enter the value for DS_KEY", default_values['DS_KEY'])
    sb_key = prompt_string("Enter the value for SB_KEY", default_values['SB_KEY'])
    db_key = prompt_string("Enter the value for DB_KEY", default_values['DB_KEY'])
    gb_key = prompt_string("Enter the value for GB_KEY", default_values['GB_KEY'])
    method_key = prompt_string("Enter the value for METHOD_KEY", default_values['METHOD_KEY'])
    warning_key = prompt_string("Enter the value for WARNING_KEY", default_values['WARNING_KEY'])

    vdd = prompt_float("Enter the value for VDD",
                       default_values['VDD'], min_val=0.1, max_val=50)
    is_integer = prompt_bool("Enter the value for IS_INTEGER",
                                   default_values['IS_INTEGER'])
    if is_integer:
        l_min = prompt_natural_number("Enter the value for L_MIN",
                                      default_values['L_MIN'], min_val=1, max_val=5)
        l_max = prompt_natural_number("Enter the value for L_MAX. Must be greater than L_MIN",
                                      default_values['L_MAX'], min_val=1, max_val=100)
        w_min = prompt_natural_number("Enter the value for W_MIN",
                                      default_values['W_MIN'], min_val=1, max_val=5)
        w_max = prompt_natural_number("Enter the value for W_MAX. Must be greater than W_MIN",
                                      default_values['W_MAX'], min_val=1, max_val=100)
    else:
        l_min = prompt_float("Enter the value for L_MIN",
                            default_values['L_MIN'], min_val=1e-15, max_val=1e-3)
        l_max = prompt_float("Enter the value for L_MAX. Must be greater than L_MIN",
                            default_values['L_MAX'], min_val=1e-15, max_val=1e-3)
        w_min = prompt_float("Enter the value for W_MIN",
                            default_values['W_MIN'], min_val=1e-15, max_val=1e-3)
        w_max = prompt_float("Enter the value for W_MAX. Must be greater than W_MIN",
                            default_values['W_MAX'], min_val=1e-15, max_val=1e-3)

    voltage_step_size = prompt_float("Enter the value for VOLTAGE_STEP_SIZE",
                                    default_values['VOLTAGE_STEP_SIZE'], min_val=1e-3, max_val=10)

    importer_verbose = prompt_bool("Enter the value for IMPORTER_VERBOSE",
                                   default_values['IMPORTER_VERBOSE'])

    # Construct the configuration string
    conf_str = f"""
'''
This module contains the configuration/constants used throughout the project.
DO NOT WRITE THIS FILE MANUALLY. Instead use the write_config.py script
as follows:

from analog_daddy.write_config import write_config
write_config()
'''
# This file was generated on {time.strftime("%d/%m/%Y %H:%M:%S")} Zone: {time.localtime().tm_zone} by write_config.py
# DON'T YOU DARE EDIT THIS FILE MANUALLY.
# Constants to avoid magic strings
PARAMETER_TAG = "{parameter_tag}"
GM_KEY_START = "{gm_key_start}"
LENGTH_KEY = "{length_key}"
GS_KEY = "{gs_key}"
DS_KEY = "{ds_key}"
SB_KEY = "{sb_key}"
DB_KEY = "{db_key}"
GB_KEY = "{gb_key}"
METHOD_KEY = "{method_key}"
WARNING_KEY = "{warning_key}"

# Supply Voltage (Vdd)
VDD = {vdd}

# for technologies that only allow stacking and multipliers.
# Is the length/width an integer?
IS_INTEGER = {is_integer}

# Length Range
L_MIN = {l_min}
L_MAX = {l_max}

# Width Range (Per-Finger)
W_MIN = {w_min}
W_MAX = {w_max}

# Voltage Step Size = 20 mV. This is the default step size
# which will be selected for our voltage sweeps.
# Note that decreasing sizes would not lead to more accurate results
# since the lookup function interpolates.
VOLTAGE_STEP_SIZE = {voltage_step_size}

# Decides the verbosity of the importer. If set to True, the importer will
# output information about the imported data in real-time.
IMPORTER_VERBOSE = {importer_verbose}
"""

    # Write to conf.py
    with open(config_path, "w",encoding="utf-8") as f:
        f.write(conf_str)

    print("Configuration saved to conf.py!")
