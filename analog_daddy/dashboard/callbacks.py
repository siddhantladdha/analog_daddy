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
        Output('device-dropdown', 'options'),
        Output('device-dropdown', 'value'),
        Output('lut-temp-cell', 'children'),
        Output('lut-corner-cell', 'children'),
        Output('lut-info-cell', 'children'),
        Input('lut-upload', 'filename'),
        Input('lut-upload', 'contents'),
    )
    def handle_lut_upload(filenames, contents):
        """
        Handle LUT upload, update toast, device dropdown, and LUT details table cells.
        """
        from .load_lut import load_lut_from_file, get_device_keys, get_lut_details
        import base64
        import tempfile
        if not filenames or not contents:
            raise PreventUpdate
        if isinstance(filenames, str):
            filenames = [filenames]
            contents = [contents]
        # Only handle the first LUT for now (single column)
        header, b64data = contents[0].split(',')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.npy') as tmp:
            tmp.write(base64.b64decode(b64data))
            tmp.flush()
            lut = load_lut_from_file(tmp.name)
        device_keys = get_device_keys(lut)
        details = get_lut_details(lut)
        dropdown_options = [{'label': k, 'value': k} for k in device_keys]
        dropdown_value = device_keys[0] if device_keys else None
        # Toast
        items = [html.Li(os.path.basename(f)) for f in filenames]
        filenames_display = html.Div([
            "Loaded:",
            html.Ul(items, style={"marginBottom": 0})
        ])
        return (
            True,
            filenames_display,
            dropdown_options,
            dropdown_value,
            details.get('temperature', '-'),
            details.get('corner', '-'),
            details.get('info', '-')
        )

    @app.callback(
        Output('debug-text', 'children'),
        Input('device-dropdown', 'value'),
    )
    def update_debug_text(selected_device):
        """
        Update the debug text to show the currently selected device.
        """
        if selected_device:
            return f"[DEBUG] Selected device: {selected_device}"
        return "[DEBUG] No device selected."
