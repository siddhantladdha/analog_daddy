"""
Dash app instance for the Analog Daddy dashboard.

This module creates and configures the Dash app with Bootstrap and Bootstrap Icons.
"""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)
