import os
import streamlit as st
from analog_daddy.designer_dashboard.sidebar import render_sidebar
from analog_daddy.designer_dashboard.ui_elements import lut_info_table, circuit_bulk_editor
from analog_daddy.logging_config import setup_logging, st_log_print
from analog_daddy.designer_dashboard.debug import show_page_debug_info

try:
    # define CONFIG as a global variable to be used in the app
    # and within submodules.
    # import within try-catch to handle any import errors gracefully.
    # you can now just use
    # from analog_daddy.config import CONFIG
    # everywhere else since the exception handling is done here.
    from analog_daddy.config import CONFIG
    setup_logging(
        os.path.join(os.path.dirname(__file__), '..', '.logs'))
except Exception as e:
    st_log_print(str(e), msg_type="error", stop=True)

st.set_page_config(
    page_title="Designer Dashboard",
    page_icon="🧑‍🔬",
    layout=CONFIG["dashboard"]["layout"],
    initial_sidebar_state=CONFIG["dashboard"]["initial_sidebar_state"],
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

