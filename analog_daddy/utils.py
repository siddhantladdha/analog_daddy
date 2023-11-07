"""
This module contains additional utility functions that can be used
to improve code quality.
"""
import numpy as np
from analog_daddy.look_up import look_up
from analog_daddy.conf import * # import all the config variables

def pretty_print_structure(d, indent=0):
    """Pretty print the structure of a dictionary containing numpy arrays and strings."""
    if isinstance(d, dict):
        for key, value in d.items():
            print(' ' * indent + str(key) + ":")
            pretty_print_structure(value, indent + 4)
    else:
        print(' ' * indent + str(d))

def describe_structure(d):
    """Describe the structure of a dictionary containing numpy arrays and strings."""
    if isinstance(d, dict):
        return {key: describe_structure(value) for key, value in d.items()}
    if isinstance(d, np.ndarray):
        if d.ndim == 0:  # Numpy Scalar
            return d.item()
        if d.ndim == 1:  # 1D array
            if len(d) <= 4:
                # print the whole array
                return [val.item() for val in d]
            # print the first two and last two elements
            return [d[0].item(), d[1].item(), "...", f"total: {len(d)} items", d[-2].item(), d[-1].item()]
        else:  # Multidimensional array
            return f"numpy.ndarray(shape={d.shape}, dtype={d.dtype})"
    elif isinstance(d, (int, float, complex)):  # Python native scalars
        return d
    elif isinstance(d, str):  # Strings
        return f'string: "{d}"'
    else:
        return type(d).__name__

def look_upW(transistor,length_increment=10e-9):
    """
    Look up the value of a device width for the
    given gm_id, length, and id.
    Modify the transistor dictionary in place.
    The transistor dictionary should have the following
    transistor = {
        'type': nmos, # actual dictionary of the device LUT
        'length': L_MIN, # starting value of the length
        'w': W_MIN, # does not matter, will be overwritten
        "id": 10e-6, # current value to look up the width for.
        "gm_id" : 15 # gm_id value to look up the width for.
    }
    If the width is less than the minimum width,
    start increasing the length until the width
    is greater than the minimum width.
    We don't put checks for maximum width because
    we can stack it and most likely this iteration
    is required in strong inversion cases where
    we won't increase the width anyway.
    """
    w_calc = transistor['id']/look_up(transistor['type'],
                                      'id_w', gm_id=transistor['gm_id'],
                                      length=transistor['length'])
    while (w_calc < W_MIN) and (transistor['length'] < L_MAX):
        print(f"""A gm_id of {transistor['gm_id']} cannot be achieved for the length:
              {transistor['length']} and id: {transistor['id']}. Increasing the length.""")
        if IS_INTEGER:
            transistor['length'] += 1
        else:
            transistor['length'] += length_increment
        w_calc = transistor['id']/look_up(transistor['type'],
                                        'id_w', gm_id=transistor['gm_id'],
                                        length=transistor['length'])

    transistor['w'] = round(w_calc) if IS_INTEGER else w_calc
    if transistor['length'] >= L_MAX:
        print(f"""The length has reached the maximum length of {L_MAX} for a gm_id of
              {transistor['gm_id']} and id of {transistor['id']}.""")
        return False
    return True

def print_transistor(transistor_dict):
    """Print the transistor dictionary in a nice format."""
    print("\n-----------------------------------\n")
    for key in transistor_dict.keys():
        if key == "type":
            print("Type: Refer dictionary.")
        else:
            print(f"""{key}:{transistor_dict[key]}""")
    print("\n-----------------------------------\n")

def print_circuit(circuit_dict):
    """Print the circuit dictionary in a nice format."""
    print("\n----------BEGIN--------------------\n")
    for key in circuit_dict.keys():
        print_transistor(circuit_dict[key])
    print("\n------------END--------------------\n")

def look_upW_circuit(circuit_dict,length_increment=10e-9):
    """Look up widths for the entire circuit."""
    for key in circuit_dict.keys():
        if look_upW(circuit_dict[key],length_increment=length_increment):
            return True
        else:
            return False