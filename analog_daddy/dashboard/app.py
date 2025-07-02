import textwrap
import streamlit as st
import numpy as np
from parse_si import format_si_or_scientific as fmt_str_si
from sidebar import render_sidebar
from analog_daddy.look_up import look_up

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
for msg in status_msgs:
    if msg.startswith("Uploaded file") or msg.startswith("(Session) File"):
        st.success(msg)
    elif msg.startswith("Please upload no more"):
        st.error(msg)
    elif msg.startswith("Failed to load"):
        st.error(msg)
    elif msg.startswith("No LUT uploaded"):
        st.error(msg)
        st.stop()
    else:
        st.info(msg)

# region Device Selection Table
headers = ["Device Type", "Temperature/Corner", "Info"]
st.markdown("## Device Selection Table")

# Prepare table: first row is headers, then the data rows
table = [headers] + [
    [lut_metadata_entry["Device Type"],
     lut_metadata_entry["Temperature/Corner"],
     lut_metadata_entry["Info"]]
    for lut_metadata_entry in lut_metadata
]

column_widths = [1, 1, 1]  # Adjust widths for each column
for row_idx, row_value in enumerate(table):
    columns = st.columns(column_widths, border=True, gap="small")
    for col_idx, (column, cell) in enumerate(zip(columns, row_value)):
        if row_idx == 0: # Header row
            column.markdown(f"**{cell}**")
        else: # Data rows
            if col_idx == 0:  # Device Type column
                selected = column.selectbox(
                    label="Lable_text",
                    options=lut_metadata[row_idx - 1]["Device Type"],
                    key=f"selected_device_type_{row_idx - 1}",
                    label_visibility="collapsed",
                    index=0
                )
            else:
                column.write(cell)
# endregion

# region Variable Selection and Display
st.markdown("## Variable Selection and Display")
try:
    # --- Mutually Exclusive Selection for Independent Vars using st.multiselect ---
    selected_independent_var = st.multiselect(
        textwrap.dedent("""\
                        **Independent variables**\n
                        Choose upto two variables.\n
                        The **first** option is used as the **x-axis**.\n
                        The **second** option is used for the **parametric axis**."""),
        # Use the first LUT's independent variables for the selectbox
        # Check is anyway performed to make sure the independent variables
        # are the same for both LUTs.
        list(
            lut_metadata[0]["independent_vars"][
                st.session_state.get("selected_device_type_0")
                ].keys()),
        default=None,
        key="selected_independent_var",
        max_selections=2
    )

    selected_dependent_var = st.selectbox(
                                        "**Dependent variable**",
                                        lut_metadata[0]["dependent_vars"][
                                        st.session_state.get("selected_device_type_0")],
                                        index=None,
                                        key="selected_dependent_var"
                                        )

    if selected_dependent_var and selected_independent_var:
        if selected_dependent_var in selected_independent_var:
            st.error(
                (
                "Dependent variable cannot be an independent variable. "
                "Please select a different variable."
                ))
            st.stop()

except IndexError:
    # If no LUTs are uploaded, show an error message and stop execution.
    # Safeguard required when the file is removed from the uploader,
    # after the selectbox and other elements are created.
    # Currently the created widgets cannot be removed,
    # as streamlit does not support dynamic widget removal.
    st.error("No LUT uploaded. Please upload a LUT file to continue.")
    st.stop()
# endregion

var_default = { }
# create input fields for the independent variables.
# Assume 'selected' is your list of selected independent variables from st.multiselect
if selected_independent_var:
    for idx, var in enumerate(selected_independent_var):
        st.markdown(f"**Range for {var}:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            start = st.text_input(
                    f"{var} start",
                    key=f"{var}_start",
                    value=fmt_str_si(
                    min(
                    lut_metadata[j]["independent_vars"][
                    st.session_state.get(f"selected_device_type_{j}")
                    ][var]["min"]
                    for j in range(len(lut_metadata))
                    )))
        with col2:
            stop = st.text_input(
                    f"{var} stop",
                    key=f"{var}_stop",
                    value=fmt_str_si(
                    min(
                    lut_metadata[j]["independent_vars"][
                    st.session_state.get(f"selected_device_type_{j}")
                    ][var]["max"]
                    for j in range(len(lut_metadata))
                    )))
        with col3:
            # Use the idx to determine between X-var and Parametric var
            # we don't bother comparing step size/ elements between two LUTs, just use the first one
            if st.session_state.get(f"var_step_mode_selector_{idx}") == "Start:Stop:Step Mode":
                step = st.text_input(
                f"{var} step",
                key=f"{var}_step",
                value=fmt_str_si(
                lut_metadata[0]["independent_vars"][
                st.session_state.get("selected_device_type_0")
                ][var]["step"]
                ))
            elif st.session_state.get(
                f"var_step_mode_selector_{idx}"
                ) == "Start:Stop:N-Elements Mode":
                # In this mode, we don't use step, but rather the number of elements
                n_elements = st.text_input(
                f"{var} N-elements",
                key=f"{var}_n_elements",
                value=fmt_str_si(
                lut_metadata[0]["independent_vars"][
                st.session_state.get("selected_device_type_0")
                ][var]["N-elements"]
                ))
