"""
Derived the file from the plotter_dashboard/debug.py
debug.py

Provides functions for displaying debug information in the dashboard and sidebar.
Includes utilities for pretty-printing LUT structures, session state, and metadata.
Handles debug mode UI and diagnostic output.
"""

import streamlit as st
import pandas as pd
# Reuse to keep file small.
from analog_daddy.plotter_dashboard.debug import st_pretty_print_lut
# Redefine to use the designer_dashboard version.
from analog_daddy.designer_dashboard.circuit_lookup import state_dict_creator
import analog_daddy.config as config
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
    with st.expander("CONFIG file", expanded=False):
        st.write(config.CONFIG.__dict__)
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

def show_page_debug_info(edited_df: pd.DataFrame):
    """
    Show debug information on the main page,
    since the sidebar is already created and the lookup_array_creator
    which can be computation intensive
    function is called after the sidebar is rendered.
    Hence calling it twice does not make sense.
    """
    if st.session_state.get("debug_mode_selector"):
        with st.expander("Debug Info", expanded=True):
            st.dataframe(edited_df)
