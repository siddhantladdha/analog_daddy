from typing import List, Dict, Any, Optional
import streamlit as st
import pandas as pd
from analog_daddy.plotter_dashboard.parse_si import (
    parse_text_for_scientific_or_si_prefix as parse_si,
    format_si_or_scientific as fmt_str_si
)

def state_dict_creator(lut_roots: List[Any], debug_mode: Optional[bool] = False) -> Dict[str, Any]:
    """
    Create a dictionary of LUT roots and session state variables
    for use in the lookup_array_creator function.
    """
    state_dict = {
        "lut_roots": lut_roots,
    }
    return state_dict


def validate_inputs():
    """
    Validate the name, length, gm/id, and id inputs,
    given to the circuit data editor.
    """
    st.write("Validating inputs...")
