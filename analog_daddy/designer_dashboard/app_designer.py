"""
Designer Dashboard Streamlit App

This module implements the main dashboard page for the Analog Daddy designer interface.
This is the launch point. It sets up configuration, logging, and page layout.

Main Features:
- Loads configuration and logging settings from environment and config files.
- Renders a sidebar for file upload, debug mode, and advanced preferences.
- Displays status messages and handles error flow control to prevent further execution on failure.
- Provides a form for bulk editing circuit data, with submission handling and debug info display.

Error Handling:
- Gracefully handles configuration and logging setup errors, displaying them in the UI.
"""
import os
import streamlit as st
from analog_daddy.designer_dashboard.sidebar import render_sidebar
from analog_daddy.designer_dashboard.ui_elements import lut_info_table, circuit_bulk_editor
from analog_daddy.logging_config import setup_logging, st_log_print
from analog_daddy.designer_dashboard.debug import show_page_debug_info
from analog_daddy.config import load_config_in_st
import analog_daddy.config as config

try:
    # define CONFIG as a global variable to be used in the app
    # and within submodules.
    # import within try-catch to handle any import errors gracefully.
    # you can now just use
    # import analog_daddy.config as config
    # and use config.CONFIG for accessing the "live" config
    # everywhere else since the exception handling is done here.

    # environment variables are used to allow user to use the launcher
    # script and run streamlit in its own process.
    config_path = os.environ.get("ANALOG_DADDY_CONFIG_PATH")
    logdir_path = os.environ.get("ANALOG_DADDY_LOGDIR_PATH")
    devel_mode = os.environ.get("ANALOG_DADDY_DEVEL_MODE")
    # Load config and setup logging.
    load_config_in_st(config_path)
    setup_logging(logdir_path)
except Exception as e:
    st_log_print(str(e), msg_type="error", stop=True)

st.set_page_config(
    page_title="Designer Dashboard",
    page_icon="🧑‍🔬",
    layout=config.CONFIG.dashboard.layout, # pylint: disable=E1101
    initial_sidebar_state=config.CONFIG.dashboard.initial_sidebar_state, # pylint: disable=E1101
    menu_items={
        'Get Help':
        'https://github.com/siddhantladdha/analog_daddy?tab=readme-ov-file#provide-helpfeedback',
        'About':
        'Find more information about the Analog Daddy project at '
        'https://github.com/siddhantladdha/analog_daddy'
    }
)

# Sidebar: Dashboard Controls
# Handles file_uploader, debug mode, and advanced preferences.
lut_roots, status_msgs, lut_metadata_list = render_sidebar()
st.title("Dashboard")

# Show status messages in main area
# This flow control with st.stop() ensures that if the LUT is not loaded
# or if there are errors, the rest of the dashboard does not execute.
# This is important to prevent errors in the rest of the dashboard
# as try:catch is not used in the rest of the code.
for msg in status_msgs:
    if msg.startswith("Uploaded file") or msg.startswith("(Session) File"):
        st_log_print(msg, msg_type="success")
    elif (
        msg.startswith("Please upload no more") or
        msg.startswith("Failed to load") or
        msg.startswith("No LUT uploaded")
    ):
        st_log_print(msg, msg_type="error", stop=True)
    else:
        st_log_print(msg, msg_type="info")

# lut_metadata is a single dictionary since it contains only one LUT.
# It will always be an non-empty list due to for loop in metadata_utils.py
# Doing this after file status check for better error handling.
lut_metadata = lut_metadata_list[0]

lut_info_table(lut_metadata)
with st.form("my_form"):
    edited_df = circuit_bulk_editor(lut_metadata,filepath = os.path.join(
                            os.path.dirname(__file__),
                            "..", "..", ".config", "demo_circuit.toml"
                            # "..", "..", ".config", "demo_circuit_different.toml"
                            ))
    submit_clicked = st.form_submit_button('Lookup Circuit')

if submit_clicked:
    st_log_print("Circuit lookup submitted.", msg_type="success")
    show_page_debug_info(edited_df)
