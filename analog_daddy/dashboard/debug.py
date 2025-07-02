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
    if lut_roots:
        with st.expander("LUT Root Structure", expanded=False):
            st_pretty_print_lut(lut_roots)
    else:
        st.error("No LUT roots available. Please upload .npy files.")
        return 0
    # LUT Metadata Structure
    if lut_metadata:
        with st.expander("LUT Metadata Structure", expanded=False):
            st.write(lut_metadata)

    # Selected device type, Independent and Dependent Variable
    # if the ui elements are not created, then the state value is None.
    # Hence assigning an [] to the values in None.
    with st.expander(
        "Selected Values",
        expanded=True):
        st.write(
                (
                f"- Device Type: "
                f"{[x for x in (selected_device_type or []) if x is not None]}\n"
                f"- Independent variable: "
                f"{[x for x in (selected_independent_var or []) if x is not None]}\n"
                f"- Dependent Variable: "
                f"{selected_dependent_var if selected_dependent_var is not None else ''}\n"
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
