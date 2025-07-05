"""
variable_logic_checker.py

Utility functions for checking
1. Mutual exclusivity of dependent and independent variables.
2. Making sure that gm_id and id_w are not together as independent variables since
fixing one, selects the other's value.

"""
import numpy as np
import streamlit as st

def mutual_exclusivity_check(selected_independent_var, selected_dependent_var) -> None:
    """
    Check if the dependent variable is in the list of independent variables.
    Returns True if they are mutually exclusive, False otherwise.
    """

    # Mutual exlusivity check for independent and dependent variables
    if (
        selected_independent_var and
        selected_dependent_var and
        selected_dependent_var in selected_independent_var
    ):
        st.error(
                (
                "Dependent variable cannot be an independent variable. "
                "Please select a different variable."
                ))
        st.stop()

def gm_id_id_w_mutual_exclusivity_check(selected_independent_var) -> None:
    """
    Check if gm_id and id_w are both selected as independent variables.
    """
    if (
        selected_independent_var and
        "gm/id" in selected_independent_var and
        "id/w" in selected_independent_var
    ):
        st.error(
            (
                "gm_id and id_w cannot be selected together as independent variables. "
                "Please select one of them."
            )
        )
        st.stop()
