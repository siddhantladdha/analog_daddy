"""
data_loader.py

This module provides functions for handling file uploads and LUT (Lookup Table) loading
for the Analog Daddy Streamlit dashboard. All file processing, session state management,
and error handling related to LUT files should be implemented here.
In addition, it includes functions to build metadata for the LUTs,
including device types, temperature/corner, independent and dependent variables,
and design variables with their min/max/step values.
"""

from typing import List, Tuple, Any
from io import BytesIO
import streamlit as st
import numpy as np

@st.cache_data(show_spinner=False)
def load_lut_from_bytes(file_bytes: bytes) -> Any:
    """
    Loads a LUT (Lookup Table) from bytes using numpy. Cached for performance.
    Args:
        file_bytes (bytes): The bytes of the .npy file.
    Returns:
        Any: The loaded LUT object.
    """
    return np.load(BytesIO(file_bytes), allow_pickle=True).item()

def load_lut_files() -> Tuple[List[Any], List[str], List[dict]]:
    """
    Handles file upload and LUT loading logic for the dashboard.
    Returns a tuple of (list of loaded LUT roots, list of status messages).
    Handles both new uploads and session restores, with error handling.
    Uses caching for LUT loading.
    """
    lut_roots = []
    status_msgs = []
    lut_metadata = []

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'lut_roots' not in st.session_state:
        st.session_state.lut_roots = []

    uploaded_files = st.file_uploader(
        "Upload up to two numpy (*.npy*) files",
        type=["npy"],
        accept_multiple_files=True,
        key="npy_uploader"
    )

    if uploaded_files:
        if len(uploaded_files) > 2:
            status_msgs.append("Please upload no more than two .npy files.")
        else:
            st.session_state.uploaded_files = uploaded_files
            st.session_state.lut_roots = []
            for file in uploaded_files:
                try:
                    file_bytes = file.read()
                    lut_root = load_lut_from_bytes(file_bytes)
                    st.session_state.lut_roots.append(lut_root)
                    lut_roots.append(lut_root)
                    status_msgs.append(f"Uploaded file: {file.name}")
                except EOFError as e:
                    status_msgs.append(
                    (f"Failed to load {file.name}: {e}."
                     "The session has been refreshed. Please re-upload the files."
                    )
                    )
                except ValueError as e:
                    status_msgs.append(f"Failed to load {file.name}: {e}")
                except Exception as e:
                    status_msgs.append(f"Failed to load {file.name}: {e}")
                del file
    elif st.session_state.uploaded_files:
        st.session_state.lut_roots = []
        for file in st.session_state.uploaded_files:
            try:
                file_bytes = file.read()
                lut_root = load_lut_from_bytes(file_bytes)
                st.session_state.lut_roots.append(lut_root)
                lut_roots.append(lut_root)
                status_msgs.append(f"(Session) File: {file.name}")
            except EOFError as e:
                status_msgs.append(
                (f"Failed to load {file.name}: {e}."
                    "The session has been refreshed. Please re-upload the files."
                )
                )
            except ValueError as e:
                status_msgs.append(f"Failed to load {file.name}: {e}")
            except Exception as e:
                status_msgs.append(f"Failed to load {file.name}: {e}")
            del file
    else:
        status_msgs.append("No LUT uploaded. Please upload the LUT.")

    if lut_roots:
        lut_metadata =  build_lut_metadata(lut_roots)
    return lut_roots, status_msgs, lut_metadata

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
                            "step": float(value[1] - value[0])
                        }
            # Add design vars (gm/id, id/w)
            # Fill in min/max/step for gm/id and id/w if possible
            # Currently, the min/max are set to some value.
            try:
                meta["independent_vars"][device]["gm/id"] = {
                    "min": 2,
                    "max": 30,
                    "step": 0.5
                }
                meta["independent_vars"][device]["id/w"] = {
                    "min": 1e-9,
                    "max": 1e-3,
                    "step": 1e-8
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
