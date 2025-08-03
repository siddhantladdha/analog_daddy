"""
Contains Streamlit UI functions for device info table,
circuit dict editor form.
"""
from typing import Dict, Any
import streamlit as st
import pandas as pd
from analog_daddy.toml_utils import circuit_toml_reader
from analog_daddy.logging_config import st_log_print
from analog_daddy.plotter_dashboard.parse_si import (
    format_si_or_scientific as float_to_si
)
from analog_daddy.config import CONFIG

def lut_info_table(lut_metadata: Dict[str,Any] = None):
    """
    Render dataframe of lut_info_table.
    """
    headers = ["Device Type", "Temperature/Corner", "Info"]
    # Convert to DataFrame (first row as header)
    df = pd.DataFrame(
        lut_metadata,
        columns=headers)
    st.dataframe(df, hide_index=True)
    return 0

def circuit_bulk_editor(lut_metadata: Dict[str,Any] = None, filepath: str = None) -> pd.DataFrame:
    """
    Display a Streamlit data editor for bulk editing circuit/transistor data.

    Args:
        circuit_dict (dict): The circuit data, keys are names, values are dicts of parameters.
        allowed_types (dict): Dict of column: type, e.g. {"w": float, "l": float, "type": str}
        key (str): Streamlit widget key.

    Returns:
        dict: The updated circuit dictionary.
    """
    default_device_type = lut_metadata["Device Type"][0]
    default_length = float_to_si(
                        lut_metadata["independent_vars"][default_device_type]["length"]["min"]
                    )
    default_gm_id = "15"

    # ^ ... $: Anchors the match to the start and end of the string (full match).
    # The rest of the pattern is identical to Python.
    REGEX_STR_SI_PREFIX_JS = r"^([-+]?[0-9]*\.?[0-9]+)\s*([fpnumkMGT]?)$"

    column_config_dict = {
        "transistor_name": st.column_config.TextColumn(
                "Transistor Name",
                help="(Required) Name of the transistor. It must start "
                "with a letter and can contain letters, numbers"
                "and underscores. Max 50 characters.",
                required=True,
                pinned=True,
                default="gm_pair",
                max_chars=50,
                # Must start with a letter and
                # can contain letters, numbers, and underscores
                validate="^[A-Za-z][A-Za-z0-9_]*$"
            ),
        "type": st.column_config.SelectboxColumn(
                "Device Type",
                help="(Required) Type of the device, e.g. NMOS, PMOS",
                options=lut_metadata["Device Type"],
                required=True,
                pinned=True,
                default=default_device_type,
            ),
        "length": st.column_config.TextColumn(
                "L",
                help="(Required) Length of the transistor",
                required=True,
                pinned=False,
                default=default_length,
                max_chars=5,
                validate=REGEX_STR_SI_PREFIX_JS
            ),
        "gm_id": st.column_config.TextColumn(
                "gm/id",
                help="(Required) Gm/ID of the transistor",
                required=True,
                pinned=False,
                default=default_gm_id,
                max_chars=5,
                validate=REGEX_STR_SI_PREFIX_JS
            ),
        "id": st.column_config.TextColumn(
                "id",
                help="(Required) Current flowing through the transistor",
                required=True,
                pinned=False,
                default="1u",
                max_chars=5,
                validate=REGEX_STR_SI_PREFIX_JS
            ),
        "w": st.column_config.TextColumn(
                "W",
                help="Calculated width of the transistor",
                disabled=True,
                default="1u",
            ),
        "description": st.column_config.TextColumn(
                "Description",
                help="More information about the transistor",
                default="Enter more details here.",
            ),
        }
    # "transistor_name" won't be found at the device_level.
    required_keys = set(column_config_dict.keys()) - {"transistor_name"}
    st.write("**Circuit Data Editor**")
    try:
        circuit_df = circuit_toml_reader(lut_metadata, filepath, required_keys)
        filtered_circuit_df = circuit_df[circuit_df.columns.intersection(column_config_dict.keys())]
    except (FileNotFoundError, ValueError) as e:
        st_log_print(str(e), msg_type="error", stop=True)
    edited_df = st.data_editor(
        filtered_circuit_df,
        column_config=column_config_dict,
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        key="circuit_dict_editor",
    )
    return edited_df
