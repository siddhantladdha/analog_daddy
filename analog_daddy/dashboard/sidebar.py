import streamlit as st
from data_loader import load_lut_files
from debug import show_debug_info

def render_sidebar():
    """
    Render the sidebar controls and debug panel.
    Loads LUT files, sets dashboard mode, and advanced preferences.
    """
    step_mode_options_dict = {
                                "step": "Start:Stop:Step Mode",
                                "N-elements": "Start:Stop:N-Elements Mode",
    }

    with st.sidebar:
        st.title("Sidebar")

        # File uploader
        lut_roots, status_msgs, lut_metadata = load_lut_files()

        # Advanced Preferences section
        with st.expander("Advanced Preferences", expanded=True):
            st.radio(
                "Select Dashboard Mode:",
                ("User Mode", "Debug Mode"),
                index=1,  # 0 for "User Mode", 1 for "Debug Mode"
                key="debug_mode_selector"
            )
            st.radio(
                "Select Mode for Array creation for X-axis:",
                options=list(step_mode_options_dict.keys()),
                format_func=lambda x: step_mode_options_dict[x],
                index=0,
                key="var_step_mode_selector_0"
            )
            st.radio(
                "Select Mode for Array creation for Parametric axis:",
                options=list(step_mode_options_dict.keys()),
                format_func=lambda x: step_mode_options_dict[x],
                index=1,
                key="var_step_mode_selector_1"
            )

        if st.session_state.get("debug_mode_selector") == "Debug Mode":
            with st.expander("DEBUG Mode", expanded=True):
                show_debug_info(
                    lut_roots,
                    lut_metadata,
                    [
                        st.session_state.get("selected_device_type_0"),
                        st.session_state.get("selected_device_type_1"),
                    ],
                    st.session_state.get("selected_independent_var"),
                    st.session_state.get("selected_dependent_var"),
                )

    return lut_roots, status_msgs, lut_metadata
