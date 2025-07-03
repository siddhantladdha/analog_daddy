from typing import Any, Dict, List
import streamlit as st
import numpy as np
from parse_si import parse_text_for_scientific_or_si_prefix as parse_si
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

def lookup_array_creator(state_dict: Dict[str, Any] = None) -> List[np.ndarray]:
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
