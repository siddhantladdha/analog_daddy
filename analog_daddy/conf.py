
'''
This module contains the configuration/constants used throughout the project.
DO NOT WRITE THIS FILE MANUALLY. Instead use the write_config.py script
as follows:

from analog_daddy.write_config import write_config
write_config()
'''
# This file was generated on 10/11/2023 19:54:43 Zone: EST by write_config.py
# DON'T YOU DARE EDIT THIS FILE MANUALLY.
# Constants to avoid magic strings
PARAMETER_TAG = "Parameters:"
GM_KEY_START = "gm_"
LENGTH_KEY = "length"
GS_KEY = "gs"
DS_KEY = "ds"
SB_KEY = "sb"
DB_KEY = "db"
GB_KEY = "gb"
METHOD_KEY = "METHOD"
WARNING_KEY = "WARNING"

# Supply Voltage (Vdd)
VDD = 1.0

# for technologies that only allow stacking and multipliers.
# Is the length/width an integer?
IS_INTEGER = False

# Length Range
L_MIN = 4.5e-08
L_MAX = 1e-05
LENGTH_INCREMENT = 1e-08
# Width Range (Per-Finger)
W_MIN = 9e-08
W_MAX = 0.001

# Voltage Step Size = 20 mV. This is the default step size
# which will be selected for our voltage sweeps.
# Note that decreasing sizes would not lead to more accurate results
# since the lookup function interpolates.
VOLTAGE_STEP_SIZE = 0.02

# Decides the verbosity of the importer. If set to True, the importer will
# output information about the imported data in real-time.
IMPORTER_VERBOSE = True
