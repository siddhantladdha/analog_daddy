import io
import contextlib
import streamlit as st
from analog_daddy.utils import pretty_print_structure, describe_structure
from plotter import state_dict_creator

# @st.cache_data
# Disabling caching since need to support session state updates.
def show_debug_info(lut_roots=None,
                    lut_metadata=None,
                    ):
    """
    Display debug information in the sidebar.
    This function is called when the debug mode is enabled.
    """
    # since we are printing the list just use the LUT 0 (which always exists.)
    # LUT root display.
    if lut_roots:
        with st.expander("LUT Root Structure", expanded=False):
            st_pretty_print_lut(lut_roots)
    else:
        st.error("No LUT roots available. Please upload .npy files.")
        return 0
    # LUT Metadata Structure
    if lut_metadata:
        with st.expander("LUT Metadata Structure", expanded=False):
            st.write(lut_metadata)

    with st.expander(
        "Session State",
        expanded=True):
        # Get the live session state and filter out lut_roots
        # since it is already displayed in the LUT Root Structure.
        session_state_dict = state_dict_creator(
            lut_roots=lut_roots,
            debug_mode=True
        )
        filtered_dict = {k: v for k, v in session_state_dict.items() if k != "lut_roots"}
        st.json(filtered_dict)
    return 0

# Caching used since this function traverses the entire LUT
# and mostly does not change once the file is uploaded.
@st.cache_data
def st_pretty_print_lut(lut_roots=None):
    """
    Display the structure of each LUT root as st.code element.
    This captures whatever is printed by the utils function
    and display in a Streamlit expander.
    Currently using YAML syntax highlighting, which is not
    entirely accurate.

    Args:
        lut_roots (list, optional): List of LUT root objects
        Each LUT will be summarized and printed.
        If None, nothing is displayed.

    Returns:
        int: Always returns 0 (for compatibility or chaining).
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        for i, lut in enumerate(lut_roots):
            print(f"LUT Root {i} structure:")
            pretty_print_structure(describe_structure(lut))
    st.code(buf.getvalue(), language="yaml")
    return 0
