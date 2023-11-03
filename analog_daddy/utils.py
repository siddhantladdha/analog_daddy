"""
This module contains additional utility functions that can be used
to improve code quality.
"""
import numpy as np

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
