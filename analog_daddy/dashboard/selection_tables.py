import textwrap
import streamlit as st
from parse_si import format_si_or_scientific as fmt_str_si

def device_selection_table(lut_metadata=None):
    """
    Render the device selection table using Streamlit columns and selectboxes.
    """
    headers = ["Device Type", "Temperature/Corner", "Info"]
    table = [headers] + [
        [lut_metadata_entry["Device Type"],
         lut_metadata_entry["Temperature/Corner"],
         lut_metadata_entry["Info"]]
        for lut_metadata_entry in lut_metadata
    ]
    column_widths = [1, 1, 1]
    for row_idx, row_value in enumerate(table):
        columns = st.columns(column_widths, border=True, gap="small")
        for col_idx, (column, cell) in enumerate(zip(columns, row_value)):
            if row_idx == 0:
                column.markdown(f"**{cell}**")
            else:
                if col_idx == 0:
                    column.selectbox(
                        label="Lable_text",
                        options=lut_metadata[row_idx - 1]["Device Type"],
                        key=f"selected_device_type_{row_idx - 1}",
                        label_visibility="collapsed",
                        index=0
                    )
                else:
                    column.write(cell)
    return 0

def variable_selection_table(lut_metadata_elem=None, selected_device_type_elem=None):
    """
    Render the variable selection controls for independent and dependent variables.
    Take only one element of the lut_metadata and corresponding selected_device_type
    which is obtained using the session_state
    Mutual exclusivity is maintained for independent variables
    using st.multiselect.
    Mutual exclusivity between the independent and the dependent variable
    is maintained at top-level using st.stop()
    """
    st.multiselect(
        textwrap.dedent("""\
                        **Independent variables**
                        (Choose upto two variables)\n
                        **First** option is the **x-axis**.\n
                        **Second** option is the **parametric axis**."""),
        list(
            lut_metadata_elem["independent_vars"][selected_device_type_elem].keys()
        ),
        default=None,
        key="selected_independent_var",
        max_selections=2
    )
    st.selectbox(
        "**Dependent variable**",
        lut_metadata_elem["dependent_vars"][selected_device_type_elem],
        index=None,
        key="selected_dependent_var"
    )
    return 0

def input_range_table(lut_metadata=None, selected_device_type=None, selected_independent_var=None):
    """
    Render the input range controls for the selected independent variables.
    Returns a dictionary of default values for each variable.
    """
    if (lut_metadata and
        selected_device_type and
        selected_independent_var):

        st.markdown("**Range for variables:**")
        for idx, var in enumerate(selected_independent_var):
            # Setting the correct key for the step mode selector
            var_step_mode_key = st.session_state.get(f"var_step_mode_selector_{idx}")

            col1, col2, col3 = st.columns(3)
            col1.text_input(
                f"{var} start",
                key=f"{var}_start",
                value=fmt_str_si(
                    min(
                        lut_met_val["independent_vars"][selected_device_type[j]][var]["min"]
                        for j, lut_met_val in enumerate(lut_metadata))
                    )
                )
            col2.text_input(
                f"{var} stop",
                key=f"{var}_stop",
                value=fmt_str_si(
                    min(
                        lut_met_val["independent_vars"][selected_device_type[j]][var]["max"]
                        for j, lut_met_val in enumerate(lut_metadata))
                    )
                )
            col3.text_input(
                f"{var} {var_step_mode_key}",
                key=f"{var}_{var_step_mode_key}",
                value=fmt_str_si(
                    lut_metadata[0]["independent_vars"][
                        selected_device_type[0]][var][var_step_mode_key]
                )
            )
    else:
        st.error("Please select atleast one independent variable.")
        st.stop()
    return 0
