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
from metadata_utils import build_lut_metadata

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
