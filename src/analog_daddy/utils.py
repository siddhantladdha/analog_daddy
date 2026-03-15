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

def look_upW(transistor,lut_root,length_increment=10e-9,ds=None):
    """
    Look up the value of a device width for the
    given gm_id, length, and id.
    Modify the transistor dictionary in place.
    The transistor dictionary should have the following
    transistor = {
        'type': "nmos_vth", # the key of device type within the device LUT dictionary.
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
    if ds is None:
        w_calc = transistor['id']/look_up(lut_root[transistor['type']],
                                        'id_w', gm_id=transistor['gm_id'],
                                        length=transistor['length'])
        while (w_calc < W_MIN) and (transistor['length'] < L_MAX):
            print(f"""A gm_id of {transistor['gm_id']} cannot be achieved for the length:
                {transistor['length']} and id: {transistor['id']}. Increasing the length.""")
            if IS_INTEGER:
                transistor['length'] += 1
            else:
                transistor['length'] += length_increment
            w_calc = transistor['id']/look_up(lut_root[transistor['type']],
                                            'id_w', gm_id=transistor['gm_id'],
                                            length=transistor['length'])

        transistor['w'] = round(w_calc) if IS_INTEGER else w_calc
        if transistor['length'] >= L_MAX:
            print(f"""The length has reached the maximum length of {L_MAX} for a gm_id of
                {transistor['gm_id']} and id of {transistor['id']}.""")
            return False
        return True
    else:
        w_calc = transistor['id']/look_up(lut_root[transistor['type']],
                                        'id_w', gm_id=transistor['gm_id'],
                                        length=transistor['length'], ds=ds)
        while (w_calc < W_MIN) and (transistor['length'] < L_MAX):
            print(f"""A gm_id of {transistor['gm_id']} cannot be achieved for the length:
                {transistor['length']} and id: {transistor['id']}. Increasing the length.""")
            if IS_INTEGER:
                transistor['length'] += 1
            else:
                transistor['length'] += length_increment
            w_calc = transistor['id']/look_up(lut_root[transistor['type']],
                                            'id_w', gm_id=transistor['gm_id'],
                                            length=transistor['length'], ds=ds)

        transistor['w'] = round(w_calc) if IS_INTEGER else w_calc
        if transistor['length'] >= L_MAX:
            print(f"""The length has reached the maximum length of {L_MAX} for a gm_id of
                {transistor['gm_id']} and id of {transistor['id']}.""")
            return False
        return True


def print_transistor(transistor_dict):
    """Print the transistor dictionary in a nice format."""
    print("-----------------------------------")
    for key in transistor_dict.keys():
        print(f"""{key}:{transistor_dict[key]}""")
    print("-----------------------------------\n")

def print_circuit(circuit_dict):
    """Print the circuit dictionary in a nice format."""
    print("----------BEGIN--------------------")
    for key in circuit_dict.keys():
        print_transistor(circuit_dict[key])
    print("------------END--------------------")

def look_upW_circuit(circuit_dict,lut_root,length_increment=10e-9):
    """Look up widths for the entire circuit."""
    if IS_INTEGER:
        length_increment = 1
    for key in circuit_dict.keys():
        if look_upW(circuit_dict[key],lut_root,length_increment=length_increment):
            return True
        else:
            return False

def write_expr_csv(filename, test_name_str, instance_name_str, circuit):
    """
    Writes expressions to a CSV file.
    We are not using CSV writer function and instead
    prefer to manually write the CSV file since
    CSV writer confirms to standard CSV formatting
    convention and escapes "
    We don't want additional " escapes since it is required
    in expressions to be imported by maestro.

    :param filename: The name of the CSV file to write to.
    :param test_name_str: A string representing the test name.
    :param instance_name_str: A string representing the instance name.
    :param circuit: A dictionary representing the circuit data.
    """
    header_row = ["Test", "Name", "Type", "Output", "EvalType", "Plot", "Save", "Spec"]

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        # Write the header manually
        file.write(','.join(header_row) + '\n')

        for device in circuit.keys():
            # This dictionary has core expressions.
            expr_dict = {
                "gm": f'OP("/{instance_name_str}/{device}" "gm")',
                "id": f'abs(OP("/{instance_name_str}/{device}" "id"))',
                "gds": f'OP("/{instance_name_str}/{device}" "gds")',
                "ro": f'(1/OP("/{instance_name_str}/{device}" "gds"))',
                "cgg": f'OP("/{instance_name_str}/{device}" "cgg")',
                "vth": f'abs(OP("/{instance_name_str}/{device}" "vth"))',
                "vds": f'abs(OP("/{instance_name_str}/{device}" "vds"))',
                "vgs": f'abs(OP("/{instance_name_str}/{device}" "vgs"))',
                "vdsat": f'abs(OP("/{instance_name_str}/{device}" "vdsat"))',
                "vdsat_margin": (
                    f'abs(OP("/{instance_name_str}/{device}" "vds")) - '
                    f'abs(OP("/{instance_name_str}/{device}" "vdsat"))'
                ),
                "veff": (
                    f'abs(OP("/{instance_name_str}/{device}" "vgs")) - '
                    f'abs(OP("/{instance_name_str}/{device}" "vth"))'
                ),
                "gm_id": (
                    f'OP("/{instance_name_str}/{device}" "gm") / '
                    f'abs(OP("/{instance_name_str}/{device}" "id"))'
                ),
                "gds_id": (
                    f'OP("/{instance_name_str}/{device}" "gds") / '
                    f'abs(OP("/{instance_name_str}/{device}" "id"))'
                ),
                "gm_gds": (
                    f'OP("/{instance_name_str}/{device}" "gm") / '
                    f'OP("/{instance_name_str}/{device}" "gds")'
                ),
            }

            for key,value in expr_dict.items():
                row = [
                    test_name_str,  # "Test"
                    f"{key}_{instance_name_str}_{device}",  # "Name"
                    "expr",  # "Type"
                    value,  # "Output"
                    "point",  # "EvalType"
                    "t",  # "Plot"
                    "",  # "Save"
                    ""   # "Spec"
                ]
                # Write the row manually
                file.write(','.join(row) + '\n')

    print(f"Data written to {filename}")
