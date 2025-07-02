import textwrap
import streamlit as st
import numpy as np
from parse_si import format_si_or_scientific as fmt_str_si
from sidebar import render_sidebar
from analog_daddy.look_up import look_up
from selection_tables import device_selection_table, variable_selection_table, input_range_table

st.set_page_config(
    page_title="Analog Daddy Dashboard",
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

device_selection_table(lut_metadata)
variable_selection_table(lut_metadata[0], st.session_state.get("selected_device_type_0"))

# Mutual exlusivity check for independent and dependent variables
if (
    st.session_state.get("selected_independent_var") and
    st.session_state.get("selected_dependent_var") and
    st.session_state.get("selected_dependent_var") in
    st.session_state.get("selected_independent_var")
):
    st.error(
            (
            "Dependent variable cannot be an independent variable. "
            "Please select a different variable."
            ))
    st.stop()

input_range_table(
    lut_metadata,
    [
        st.session_state.get("selected_device_type_0"),
        st.session_state.get("selected_device_type_1"),
    ],
    st.session_state.get("selected_independent_var"),
    )
