from typing import List
import numpy as np
import streamlit as st

def build_lut_metadata(lut_roots: List[dict]) -> List[dict]:
    """
    Build metadata for each LUT root including device types, temperature/corner, info,
    independent/dependent variables, design variables, and min/max for each independent variable.
    Returns a list of metadata dicts for each LUT.
    Each independent variable is a dict with keys: name, min, max, step.
    """
    lut_metadata = []
    design_vars = ["gm/id", "id/w"]

    # iterate through each LUT in the list LUT_root which is the number of LUTs uploaded
    for lut in lut_roots:
        # extract device_types which would be the Dictionary in the top-level of the LUT
        device_types = [k for k, v in lut.items() if isinstance(v, dict)]
        # create metadata dictionary for the LUT
        # populate as much as possible else initialize empty dicts.
        meta = {
            "Device Type": device_types, # List of device types in the LUT
            "Temperature/Corner": f"{lut.get('temperature')}°C : {lut.get('corner')}",
            "Info": lut.get('info'),
            "independent_vars": {},
            "dependent_vars": {},
        }
        # iterate through each device type in the LUT
        for device in device_types:
            # Explicitly initialize nested dicts/lists for each device
            if device not in meta["independent_vars"]:
                meta["independent_vars"][device] = {}
            if device not in meta["dependent_vars"]:
                meta["dependent_vars"][device] = []
            device_data_dict = lut.get(device, {})
            # iterate through the device data dictionary
            # to find independent and dependent variables.
            # these variables are the keys of the device data dictionary.
            for key, value in device_data_dict.items():
                if isinstance(value, np.ndarray):
                    # 4D-numpy array is a dependent variable
                    if value.ndim == 4:
                        meta["dependent_vars"][device].append(key)
                    # 1D-numpy array with more than one element is an independent variable
                    elif value.ndim == 1 and value.size > 1:
                        meta["independent_vars"][device][key] = {
                            "min": float(np.min(value)),
                            "max": float(np.max(value)),
                            "step": float(value[1] - value[0]),
                            "N-elements": value.size
                        }
            # Add design vars (gm/id, id/w)
            # Fill in min/max/step for gm/id and id/w if possible
            # Currently, the min/max are set to some value.
            try:
                meta["independent_vars"][device]["gm/id"] = {
                    "min": 2,
                    "max": 30,
                    "step": 0.5,
                    "N-elements": 57
                }
                # for id/w entering some value which makes sense.
                # ideally you would want a log space array
                # for default values using linear spacing.
                # and using 100 elements as an example.
                meta["independent_vars"][device]["id/w"] = {
                    "min": 1e-9,
                    "max": 1e-3,
                    "step": 1e-8,
                    "N-elements": 100
                }
            except KeyError as e:
                # gm, id or w not found, set design vars to None
                for v in design_vars:
                    st.warning(f"KeyError: {e}. Setting to None.")
                    meta["independent_vars"][device][v] = {
                            "min": None,
                            "max": None,
                            "step": None
                            }
            # Create ratios of dependent variables
            # Currently creating all possible ratios of dependent variables
            # Eventually will try to trim this down to only ratios that make sense
            # Create a shallow copy of the dependent_vars list
            temp_dependent_vars = meta["dependent_vars"][device][:]
            for i in temp_dependent_vars: # iteraing over a copy of the list
                # modifying the original list
                meta["dependent_vars"][device].append(f"{i}/w")
                for j in temp_dependent_vars: # iteraing over a copy of the list
                    if i != j:
                        # modifying the original list
                        meta["dependent_vars"][device].append(f"{i}/{j}")

        lut_metadata.append(meta)

    if len(lut_metadata) == 2: # Only compare if two LUTs are selected
        reference_keys = {}
        for var_type in ["dependent_vars", "independent_vars"]:
            reference_keys[var_type] = lut_metadata[0][var_type][lut_metadata[0]["Device Type"][0]]
            for i in range(1, len(lut_metadata)):
                for device in lut_metadata[i]["Device Type"]:
                    if set(lut_metadata[i][var_type][device]) != set(reference_keys[var_type]):
                        st.error((
                            f"{var_type} do not match for LUT: {i}, device: {device}. "
                            "Please correct the LUT keys."))
                        st.stop()
    return lut_metadata
