import streamlit as st
from analog_daddy.designer_dashboard.sidebar import render_sidebar
from analog_daddy.designer_dashboard.ui_elements import lut_info_table

st.set_page_config(
    page_title="Designer Dashboard",
    page_icon="🧑‍🔬",
    layout="centered"
)

# Sidebar: Dashboard Controls
# Handles file_uploader, debug mode, and advanced preferences.
lut_roots, status_msgs, lut_metadata = render_sidebar()

st.title("Dashboard")

# Show status messages in main area
# This flow control with st.stop() ensures that if the LUT is not loaded
# or if there are errors, the rest of the dashboard does not execute.
# This is important to prevent errors in the rest of the dashboard
# as try:catch is not used in the rest of the code.
for msg in status_msgs:
    if msg.startswith("Uploaded file") or msg.startswith("(Session) File"):
        st.success(msg)
    elif (
        msg.startswith("Please upload no more") or
        msg.startswith("Failed to load") or
        msg.startswith("No LUT uploaded")
    ):
        st.error(msg)
        st.stop()
    else:
        st.info(msg)


lut_info_table(lut_metadata)
