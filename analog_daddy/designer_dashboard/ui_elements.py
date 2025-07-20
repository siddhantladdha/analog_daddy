"""
Contains Streamlit UI functions for device info table,
circuit dict editor form.
"""

import streamlit as st
import pandas as pd
from analog_daddy.plotter_dashboard.parse_si import (
    format_si_or_scientific as fmt_str_si)

def lut_info_table(lut_metadata=None):
    """
    Render a data fram of lut_info_table.
    """
    headers = ["Device Type", "Temperature/Corner", "Info"]
    # Convert to DataFrame (first row as header)
    df = pd.DataFrame(
        lut_metadata,
        columns=headers)
    st.dataframe(df, hide_index=True)
    return 0
