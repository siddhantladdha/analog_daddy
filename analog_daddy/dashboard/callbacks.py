"""
Callback registration for the Analog Daddy dashboard.

This module defines and registers Dash callbacks
"""

import os
from dash import Input, Output, html
from dash.exceptions import PreventUpdate
from .app import app

def register_callbacks():
    """
    Register all Dash callbacks for the dashboard.

    This function attaches all necessary callbacks to the Dash app instance.
    """
    @app.callback(
        Output('lut-toast', 'is_open'),
        Output('lut-toast', 'children'),
        Input('lut-upload', 'filename'),
    )
    def show_lut_toast(filenames):
        """
        Show a toast notification listing all uploaded LUT filenames.

        Args:
            filenames (str or list): The uploaded LUT filename(s).

        Returns:
            tuple: (is_open, toast content as a bulleted list)
        """
        if not filenames:
            raise PreventUpdate
        # Support both single and multiple file uploads
        if isinstance(filenames, str):
            filenames = [filenames]
        # Show all uploaded filenames as a bulleted list using Dash html components
        items = [html.Li(os.path.basename(f)) for f in filenames]
        filenames_display = html.Div([
            "Loaded:",
            html.Ul(items, style={"marginBottom": 0})
        ])
        return True, filenames_display
