"""
This module contains functions for importing data from a pseudo CSV file.
"""
import csv
import numpy as np
from analog_daddy.conf import (LENGTH_KEY, GS_KEY,
                               DS_KEY, SB_KEY, GM_KEY_START,
                               PARAMETER_TAG, IMPORTER_VERBOSE)

def nest_populated_dictionary(y: dict, x: dict) -> dict:
    """
    Takes a dictionary y with device-related keys, processes it to rearrange
    keys based on unique devices, and nests dictionary x within each device key.

    Parameters:
    - y (dict): Dictionary with device-related keys.
    - x (dict): Dictionary of independent variables.

    Returns:
    - dict: Dictionary with independent variables nested within each device key.
    """
    # Start by filtering keys that start with 'gm'
    gm_keys = [key for key in y.keys() if key.startswith(GM_KEY_START)]

    # Extract the device names by removing the 'gm_' prefix
    unique_devices = {key.split(GM_KEY_START)[1] for key in gm_keys}

    y_rearranged = {}

    for device in unique_devices:
        y_rearranged[device] = x.copy()  # Nesting x within each device
        for key in y.keys():
            if device in key:
                # Strip the device name (plus preceding underscore) to avoid redundancy
                new_key = key.replace(f"_{device}", "")
                y_rearranged[device][new_key] = y[key]

    return y_rearranged

def extract_parameters_from_comment(comment: list) -> dict:
    """
    Extract parameters from a comment list and return them as a dictionary.

    Parameters:
    - comment (list): The comment list containing the PARAMETER_TAG and the parameters.

    Returns:
    - dict: A dictionary of extracted parameters.
    """
    parameters = {}

    if not comment:
        raise ValueError("The list is empty!")

    if comment[0] == PARAMETER_TAG:
        parts = comment[1].split(', ')
        for part in parts:
            try:
                key, value = part.split('=')
                parameters[key] = value.strip()
            except ValueError:
                raise ValueError("There are no parameters specified at all")
    return parameters

def parse_value(value: str) -> float:
    """
    Convert a string value with possible SI (International System of Units) prefixes
    to its corresponding float value.

    For instance:
    - "1k" becomes 1000.0
    - "1M" becomes 1000000.0
    - "1u" becomes 0.000001

    Parameters:
    - value (str): The string value to parse. It may end with an SI prefix.

    Returns:
    - float: The parsed float value.
    """
    # Dictionary to map SI prefixes to their multiplier values.
    si_prefixes = {
        'T': 1e12,  # Tera
        'G': 1e9,   # Giga
        'M': 1e6,   # Mega
        'k': 1e3,   # Kilo
        'm': 1e-3,  # Milli
        'u': 1e-6,  # Micro
        'n': 1e-9,  # Nano
        'p': 1e-12, # Pico
        'f': 1e-15, # Femto
        'a': 1e-18, # Atto (added)
    }

    # If the last character in the string is an SI prefix, multiply
    # the number with the corresponding multiplier.
    if value[-1] in si_prefixes:
        return float(value[:-1]) * si_prefixes[value[-1]]
    # If there's no SI prefix, simply convert the string to a float.
    return float(value)

def strip_empty_strings(data: list) -> list:
    """
    Remove empty strings, trim whitespaces, and adjust sublists based on the first element.

    This function processes each inner list within the main data list,
    removes empty string entries, trims whitespaces from non-empty strings,
    and adjusts sublists by removing the first two elements if the first element
    is not PARAMETER_TAG.

    Parameters:
    - data (list): The data list containing rows with possibly empty strings.

    Returns:
    - list: The processed data list with empty strings removed and sublists adjusted.
    """
    cleaned_data = []
    for sublist in data:
        # Remove empty strings, trim whitespaces, and check the first element
        cleaned_sublist = [item.strip() for item in sublist if item.strip() != '']
        if cleaned_sublist and cleaned_sublist[0] != PARAMETER_TAG:
            # If the first element is not PARAMETER_TAG, remove the first two elements
            cleaned_sublist = cleaned_sublist[2:]
        cleaned_data.append(cleaned_sublist)
    return cleaned_data

class CSVReadingError(Exception):
    pass

def read_pseudo_csv_file(file_path: str) -> list:
    """
    Read the pseudo CSV file and return its data as a list of lists.

    Parameters:
    - file_path (str): Path to the pseudo CSV file.

    Returns:
    - list: A list of rows, where each row is a list of string values.
    """
    data = []

    try:
        with open(file_path, 'r',encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            # Skip the first row (headers)
            next(reader, None)

            is_inside_parameters_section = False
            current_parameters = None

            for row in reader:
                if len(row) == 0:
                    continue  # Skip empty lines

                if PARAMETER_TAG in row[0]:
                    is_inside_parameters_section = True
                    current_parameters = row[0].split(":")[1].strip()
                elif is_inside_parameters_section:
                    data.append([PARAMETER_TAG, current_parameters])
                    is_inside_parameters_section = False
                    data.append(row)
                else:
                    data.append(row)

    except FileNotFoundError:
        raise CSVReadingError(f"The file '{file_path}' was not found.")
    except Exception as e:
        raise CSVReadingError(f"Error reading the CSV file: {str(e)}")

    return data

def separate_lines(data: list) -> (list, list):
    """
    Separate the provided data into parameter lines and data lines.
    Parameters:
    - data (list): The data list to process.

    Returns:
    - tuple: A tuple containing two lists - parameter lines and data lines.
    """
    param_lines = [line for line in data if PARAMETER_TAG in line[0]]
    data_lines = [line for line in data if PARAMETER_TAG not in line[0]]
    return param_lines, data_lines

def process_parameters(param_lines: list) -> dict:
    """
    Process the parameter lines to populate the x dictionary.
    Parameters:
    - param_lines (list): List of parameter lines.

    Returns:
    - dict: The x dictionary populated with parameters.
    """
    x = {DS_KEY: [], GS_KEY: [], LENGTH_KEY: [], SB_KEY: []}
    for line in param_lines:
        _, params = line
        for param in params.split(", "):
            key, value = param.split("=")
            parsed_value = parse_value(value)  # Assuming values are floating point numbers
            if parsed_value not in x[key]:
                x[key].append(parsed_value)
    return x

def create_data_structure(data_lines: list, x: dict) -> dict:
    """
    Create the structure of the y dictionary based on x values.
    Parameters:
    - data_lines (list): List of data lines.
    - x (dict): The x dictionary populated with parameters.

    Returns:
    - dict: The initialized y dictionary.
    """
    y = {}
    for key, _ in data_lines:
        if key not in y:
            y[key] = [
                [
                    [
                        [None for _ in x[SB_KEY]]
                        for _ in x[LENGTH_KEY]
                    ]
                    for _ in x[GS_KEY]
                ]
                for _ in x[DS_KEY]
            ]
    return y

def populate_data_values(combined_lines: list, param_lines: list, x: dict, y: dict) -> None:
    """
    Populate the y dictionary with data values using combined lines while leveraging
    param_lines and data_lines for context.
    Parameters:
    - combined_lines (list): Combined list of parameter and data lines.
    - param_lines (list): The separated parameter lines.
    - data_lines (list): The separated data lines.
    - x (dict): The x dictionary populated with parameters.
    - y (dict): The initialized y dictionary.
    """
    current_parameters = None
    # go through the data line by line.
    idx = 0
    for line in combined_lines:
        if IMPORTER_VERBOSE:
            print(f"Processing line {idx}")
            idx += 1
        try:
            #  Check if it's a parameter line
            if line in param_lines:
                current_parameters = extract_parameters_from_comment(line)
                ds_index = x[DS_KEY].index(parse_value(current_parameters[DS_KEY]))
                gs_index = x[GS_KEY].index(parse_value(current_parameters[GS_KEY]))
                length_index = x[LENGTH_KEY].index(parse_value(current_parameters[LENGTH_KEY]))
                sb_index = x[SB_KEY].index(parse_value(current_parameters[SB_KEY]))
            # else it's a data line.
            else:
                key, value = line
                y[key][ds_index][gs_index][length_index][sb_index] = float(value)
        except Exception as e:
            if 'value' in locals():
                raise ValueError(f"Error processing line {line} with value {value}: {e}")
            else:
                raise ValueError(f"Error processing line {line}: {e}")

def process_data(file_path: str) -> (dict, dict):
    """
    Process the data from the provided file path to extract and organize parameters
    and their associated values.
    Parameters:
    - file_path (str): The path to the pseudo CSV file containing the data.

    Returns:
    - tuple: A tuple containing two dictionaries (x, y) representing parameters
             and their associated values.
    """
    # Read the data from the file and strip empty strings
    combined_lines = strip_empty_strings(read_pseudo_csv_file(file_path))
    # Separate parameter lines and data lines
    param_lines, data_lines = separate_lines(combined_lines)
    # Process parameter lines to get x dictionary
    x = process_parameters(param_lines)
    if IMPORTER_VERBOSE:
        print("Done Processing Parameters")
    # Initialize the y dictionary based on x values
    y = create_data_structure(data_lines, x)
    if IMPORTER_VERBOSE:
        print("Done Initializing Data Structure")
    # Populate the y dictionary with data values
    populate_data_values(combined_lines, param_lines, x, y)
    return x, y

def lists_to_arrays(data):
    """
    Recursively converts all lists in a dictionary to numpy arrays.
    Args:
    - data (dict): The dictionary to process.

    Returns:
    - dict: The processed dictionary with lists converted to numpy arrays.
    """
    if isinstance(data, list):  # Base case: if it's a list, convert to np.array
        return np.array(data)
    if isinstance(data, dict):  # If it's a dictionary, process each key-value pair
        return {key: lists_to_arrays(value) for key, value in data.items()}
    return data  # If it's neither a list nor a dictionary, return it as is
