
'''
This module contains the configuration/constants used throughout the project.
DO NOT WRITE THIS FILE MANUALLY. Instead use the write_config.py script
as follows:

from analog_daddy.write_config import write_config
write_config()
'''
# This file was generated on 03/11/2023 10:36:33 Zone: EDT by write_config.py
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
VDD = 0.9

# Length Range
L_MIN = 1e-06
L_MAX = 2e-06

# Width Range (Per-Finger)
W_MIN = 3.2e-07
W_MAX = 1e-05

# Voltage Step Size = 20 mV. This is the default step size
# which will be selected for our voltage sweeps.
# Note that decreasing sizes would not lead to more accurate results
# since the lookup function interpolates.
VOLTAGE_STEP_SIZE = 0.02

# Decides the verbosity of the importer. If set to True, the importer will
# output information about the imported data in real-time.
IMPORTER_VERBOSE = True
