import io
import contextlib
import streamlit as st
from analog_daddy.utils import pretty_print_structure, describe_structure

@st.cache_data
# Caching is used to avoid recomputing the debug information
def show_debug_info(lut_roots=None,
                    lut_metadata=None,
                    selected_device_type=None,
                    selected_independent_var=None,
                    selected_dependent_var=None):
    """
    Display debug information in the sidebar.
    This function is called when the debug mode is enabled.
    """
    # since we are printing the list just use the LUT 0 (which always exists.)
    # LUT root display.
    with st.expander("LUT Root Structure", expanded=False):
        st_pretty_print_lut(lut_roots)
    # LUT Metadata Structure
    with st.expander("LUT Metadata Structure", expanded=False):
        st.write(lut_metadata)
    # Independent and Dependent Variable list
    for idx in len(lut_metadata):
        with st.expander(
            f"Independent and Dependent Variable List for LUT {idx}",
            expanded=False):

            st.write(list(
                lut_metadata[idx]["independent_vars"][
                    selected_device_type[idx]
                ].keys()))
            st.write(
                lut_metadata[idx]["dependent_vars"][
                    selected_device_type[idx]
                ])

    # Selected Independent and Dependent Variable
    with st.expander(
        "Selected Independent and Dependent Variable",
        expanded=False):
        st.write(
                (
                f"- Independent variable: {selected_independent_var}\n"
                f"- Dependent Variable: {selected_dependent_var}"
                )
        )
    return 0

# Caching used since this function traverses the entire LUT
# and mostly does not change once the file is uploaded.
@st.cache_data
def st_pretty_print_lut(lut_roots=None):
    """
    Display the structure of each LUT root as st.code element.
    This captures whatever is printed by the utils function
    and display in a Streamlit expander.
    Currently using YAML syntax highlighting, which is not
    entirely accurate.

    Args:
        lut_roots (list, optional): List of LUT root objects
        Each LUT will be summarized and printed.
        If None, nothing is displayed.

    Returns:
        int: Always returns 0 (for compatibility or chaining).
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        for i, lut in enumerate(lut_roots):
            print(f"LUT Root {i} structure:")
            pretty_print_structure(describe_structure(lut))
    st.code(buf.getvalue(), language="yaml")
    return 0
