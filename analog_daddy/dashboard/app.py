import streamlit as st
from sidebar import render_sidebar
from selection_tables import device_selection_table, variable_selection_table, input_range_table
from plotter import state_dict_creator, lookup_array_creator, plot_lookup_result
import numpy as np
from debug import show_page_debug_info
from variable_logic_checker import mutual_exclusivity_check, gm_id_id_w_mutual_exclusivity_check

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

mutual_exclusivity_check(
    st.session_state.get("selected_independent_var"),
    st.session_state.get("selected_dependent_var"),
)

gm_id_id_w_mutual_exclusivity_check(st.session_state.get("selected_independent_var"))

input_range_table(
    lut_metadata,
    [
        st.session_state.get("selected_device_type_0"),
        st.session_state.get("selected_device_type_1"),
    ],
    st.session_state.get("selected_independent_var"),
    )
# flow control for dependent variable selection.
# since the lookup cannot proceed without a dependent variable
if st.session_state.get("selected_dependent_var"):
    # create the state dictionary for the LUT roots
    # lookup the values
    # and plot the results.
    try:
        (
            indep_vars_range,
            dep_var_range_dict,
            indep_vars,
            dep_var,
        ) = lookup_array_creator(state_dict_creator(lut_roots))

    except ValueError as e:
        error_msg = str(e)
        if "below the interpolation range's minimum value" in error_msg:
            # Handle this specific ValueError
            st.error(f"Input is below the allowed range.{error_msg}")
            st.stop()
        else:
            # Re-raise or handle other ValueErrors
            raise


    show_page_debug_info(indep_vars_range, dep_var_range_dict, indep_vars, dep_var)
    plot_lookup_result(indep_vars_range, dep_var_range_dict, indep_vars, dep_var)
else:
    st.error(
            (
            "No dependent variable is selected, "
            "Please select a dependent variable."
            ))
    st.stop()
