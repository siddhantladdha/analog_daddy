"""
Derived the file from the plotter_dashboard/debug.py
debug.py

Provides functions for displaying debug information in the dashboard and sidebar.
Includes utilities for pretty-printing LUT structures, session state, and metadata.
Handles debug mode UI and diagnostic output.
"""

import streamlit as st
# Reuse to keep file small.
from analog_daddy.plotter_dashboard.debug import st_pretty_print_lut
# Redefine to use the designer_dashboard version.
from analog_daddy.designer_dashboard.circuit_lookup import state_dict_creator

# @st.cache_data
# Disabling caching since need to support session state updates.
def show_sidebar_debug_info(lut_roots=None,
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

# Might reuse later.
# def show_page_debug_info(indep_vars_range=None,
#                          dep_var_range_dict=None,
#                          indep_vars=None,
#                          dep_var=None):
#     """
#     Show debug information on the main page,
#     since the sidebar is already created and the lookup_array_creator
#     which can be computation intensive
#     function is called after the sidebar is rendered.
#     Hence calling it twice does not make sense.
#     """
#     if st.session_state.get("debug_mode_selector"):
#         with st.expander("Debug Info", expanded=True):
#             st.write(f"Variables: {indep_vars}, {dep_var}")
#             st.write(f"Independent variable Array shape: {indep_vars_range}")
#             st.write("Independent variable Array value:", indep_vars_range)
#             st.write(f"Dependent variable Array shape: {dep_var_range_dict}")
#             st.write("Dependent variable Array value: ",dep_var_range_dict)
