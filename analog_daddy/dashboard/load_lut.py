"""
Module for LUT loading utilities for the Dracula-themed Analog Daddy dashboard.
"""

import numpy as np

def load_lut_from_file(file_path):
    """
    Load a LUT from a numpy .npy file and return the dictionary.
    """
    return np.load(file_path, allow_pickle=True).item()

def get_device_keys(lut_dict):
    """
    Return device keys (excluding 'corner', 'temp', 'info') from LUT dict.
    """
    return [k for k in lut_dict.keys() if k not in ("corner", "temperature", "info")]

def get_lut_details(lut_dict):
    """
    Return a dict with 'corner', 'temp', and 'info' from LUT dict (if present).
    """
    return {k: lut_dict.get(k, "-") for k in ("corner", "temperature", "info")}