"""
sidebar.py

Derived the file from the plotter_dashboard/sidebar.py
Key changes:
- Removed the step_mode_options_dict and its usage.
- load_lut_files called with accept_multiple_files set to False.
- Using show_sidebar_debug_info from designer_dashboard.debug instead
of plotter_dashboard.debug.

Defines the sidebar UI for the dashboard, including file upload, dashboard mode selection,
advanced preferences, and debug panel. Orchestrates LUT loading and sidebar controls.
"""

import streamlit as st
# Reuse the function from plotter_dashboard.
from analog_daddy.plotter_dashboard.data_loader import load_lut_files
# Need to create new clone since need a modified debug_info.
from analog_daddy.designer_dashboard.debug import show_sidebar_debug_info
# For loading the "live" config using config.CONFIG
import analog_daddy.config as config

def render_sidebar():
    """
    Render the sidebar controls and debug panel.
    Loads LUT files, sets dashboard mode, and advanced preferences.
    """
    dashboard_mode_options = [
                                "User Mode",
                                "Debug Mode",
    ]

    with st.sidebar:
        st.title("Sidebar")

        # File uploader
        lut_roots, status_msgs, lut_metadata = load_lut_files(accept_multiple_files=False)

        # Advanced Preferences section
        with st.expander("Advanced Preferences", expanded=True):
            st.radio(
                "Select Dashboard Mode:",
                [0, 1],
                format_func=lambda x: dashboard_mode_options[x],
                # 0 for "User Mode", 1 for "Debug Mode"
                index=1 if config.CONFIG.dashboard.debug_mode else 0, # pylint: disable=E1101
                key="debug_mode_selector"
            )

        if st.session_state.get("debug_mode_selector"):
            with st.expander("DEBUG Mode", expanded=True):
                show_sidebar_debug_info(
                    lut_roots,
                    lut_metadata,
                )

    return lut_roots, status_msgs, lut_metadata
