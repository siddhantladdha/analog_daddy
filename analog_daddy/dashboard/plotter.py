from typing import Any, Dict, List
import streamlit as st
import numpy as np
import plotly.graph_objs as go
from parse_si import parse_text_for_scientific_or_si_prefix as parse_si
from parse_si import format_si_or_scientific as disp_si
from analog_daddy.look_up import look_up

def state_dict_creator(lut_roots: List[Any]) -> Dict[str, Any]:
    """
    Create a dictionary of LUT roots and session state variables
    for use in the lookup_array_creator function.
    """
    state_dict = {
        "lut_roots": lut_roots,
        "selected_device_type": [
        st.session_state.get(f"selected_device_type_{idx}") for idx in range(2)
            ],
        "selected_independent_var": st.session_state.get("selected_independent_var"),
        "selected_dependent_var": st.session_state.get("selected_dependent_var"),
    }
    try:
        for idx, indep_var in enumerate(state_dict.get("selected_independent_var", [])):
            state_dict[f"{indep_var}_start"] = parse_si(st.session_state.get(f"{indep_var}_start"))
            state_dict[f"{indep_var}_stop"] = parse_si(st.session_state.get(f"{indep_var}_stop"))
            state_dict[f"{indep_var}_step_mode"] = st.session_state.get(f"var_step_mode_selector_{idx}")
            step_mode = state_dict[f"{indep_var}_step_mode"]
            state_dict[f"{indep_var}_step_or_n"] = parse_si(st.session_state.get(f"{indep_var}_{step_mode}"))
    except ValueError as e:
        st.error(f"Check input field: {e}")
        st.stop()

    return state_dict

@st.cache_data
def indep_array_creator(state_dict: Dict[str, Any] = None) -> List[np.ndarray]:
    """
    Generate arrays for the selected independent variables using the provided state dictionary.

    This function retrieves the start, stop, step/number-of-elements, and step mode.
    for each independent variable from the state_dict and generates the corresponding
    arrays using array_creator.
    Any ValueError encountered during array creation is reported to the user and stops execution.

    Args:
        state_dict (Dict[str, Any]): Dictionary containing session state
        and user selections for array generation.

    Returns:
        List[np.ndarray]: A list of numpy arrays for each independent variable.
    """
    indep_vars = state_dict.get("selected_independent_var", [])
    indep_vars_range = []

    for var in indep_vars:
        try:
            arr = array_creator(
                state_dict[f"{var}_start"],
                state_dict[f"{var}_stop"],
                state_dict[f"{var}_step_or_n"],
                state_dict[f"{var}_step_mode"],
            )
        except ValueError as e:
            st.error(f"Check input field for {var}: {e}")
            st.stop()
        indep_vars_range.append(arr)

    return indep_vars_range

def ratio_slash_to_underscore(s: str) -> str:
    """
    Convert a string with slashes to underscores.
    Used for formatting variable to be ready for use
    in look_up utility.
    """
    return s.replace("/", "_")

def array_creator(start, stop, step_or_n, step_mode):
    """
    Create an array based on the provided parameters.
    Used for generating arrays for plotting.
    """
    if step_mode == "step":
        return np.arange(start, stop + step_or_n, step_or_n)
    elif step_mode == "N-elements":
        if int(step_or_n) < 2:
            raise ValueError("N-elements must be at least 2.")
        else:
            return np.linspace(start, stop, int(step_or_n))
    else:
        raise ValueError(f"Unknown step mode: {step_mode}")

@st.cache_data
def lookup_array_creator(state_dict: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """
    Generate a look_up string.

    Args:
        device (str): The device or LUT variable.
        param (str): The dependent variable to look up.
        x_var (str): The independent variable (x-axis).
        x_range (str): The name of the array for the x-axis.
        **kwargs: Any additional keyword arguments for fixed variables.

    Returns:
        str: The look_up string.
    """
    lut_roots = state_dict.get("lut_roots", [])
    indep_vars = [
        ratio_slash_to_underscore(val) for val in state_dict.get("selected_independent_var", [])
        ]
    indep_vars_range = indep_array_creator(state_dict)
    dep_var = ratio_slash_to_underscore(state_dict.get("selected_dependent_var", []))
    dep_var_range = {}

    # need to pass a default value for gs since the look_up
    # function defaults it to a 1-D array.
    # this will get overwritten if the indep_vars has a "gs" key.
    kwargs = {}
    kwargs.update({"gs": 0})
    kwargs.update({indep_vars[0]: indep_vars_range[0]})
    # iterate over each LUT root
    for idx, lut_root_val in enumerate(lut_roots):
        if len(indep_vars) == 1:
            dep_var_range[f"{idx}"] = look_up(
                        # device selection.
                        lut_root_val[state_dict.get("selected_device_type")[idx]],
                        # dependent variable selection.
                        dep_var,
                        **kwargs)
        elif len(indep_vars) == 2:
            dep_var_range[f"{idx}"] = []
            for param_var in indep_vars_range[1]:
                kwargs.update({indep_vars[1]: param_var})
                dep_var_range[f"{idx}"].append(
                    look_up(
                        # device selection.
                        lut_root_val[state_dict.get("selected_device_type")[idx]],
                        # dependent variable selection.
                        dep_var,
                        **kwargs))
            dep_var_range[f"{idx}"] = np.array(dep_var_range[f"{idx}"])
    return indep_vars_range, dep_var_range, indep_vars, dep_var

@st.cache_data
def plot_lookup_result(
    indep_vars_range,
    dep_var_range,
    indep_vars: List[str],
    dep_var: str
) -> None:
    """
    Plot dep_var_range vs indep_var_range using Plotly in Streamlit.

    Args:
        indep_vars_range: 1D or 2D array-like, independent variable(s).
        dep_var_range: 1D or 2D array-like, dependent variable(s).
        indep_vars: Label for the independent variable.
        dep_var: Label for the dependent variable.
    """
    dep_var_range = dep_var_range["0"]
    fig = go.Figure()
    if len(indep_vars) == 1:
        fig.add_trace(
            go.Scatter(
                x=indep_vars_range[0],
                y=dep_var_range,
                mode='lines'
                ))
        # Add metadata to the figure
        fig.update_layout(
            title=f'Plot of {dep_var} vs {indep_vars[0]}',
            xaxis_title=f'{indep_vars[0]}',
            yaxis_title=f'{dep_var}'
            )
    elif len(indep_vars) == 2:
        for idx, param_var in enumerate(indep_vars_range[1]):
            fig.add_trace(
                go.Scatter(
                    x=indep_vars_range[0],
                    y=dep_var_range[idx],
                    mode='lines',
                    name=f'{indep_vars[1]}={disp_si(param_var, precision=3)}'
                    ))
        # Add metadata to the figure
        fig.update_layout(
            title=f'Plot of {dep_var} vs {indep_vars[0]} for Parametric {indep_vars[1]}',
            xaxis_title=f'{indep_vars[0]}',
            yaxis_title=f'{dep_var}')

    st.plotly_chart(fig, use_container_width=True)
