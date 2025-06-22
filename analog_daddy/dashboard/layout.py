"""
Defines the main layout for the Analog Daddy dashboard.

This module sets up the dashboard container, file upload, and toast notification components.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Analog Daddy Dashboard'),
            html.H2('LUT Import'),
            dcc.Upload(
                id='lut-upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select LUT File(s)')
                ]),
                multiple=True,
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '8px',
                    'textAlign': 'center',
                    'background': 'var(--dracula-current-line)',
                    'color': 'var(--dracula-foreground)',
                    'margin': '1em 0'
                }
            ),
            dbc.Toast(
                id='lut-toast',
                header='LUT Import Successful',
                is_open=False,
                duration=5000,
                dismissable=True,
                icon='success',
                style={
                    'position': 'fixed',
                    'top': 20,
                    'right': 20,
                    'minWidth': '250px',
                    'background': 'var(--dracula-current-line)',
                    'color': 'var(--dracula-foreground)'
                }
            ),
            html.Div(id='lut-upload-output'),
            # LUT details table with device dropdown in the second column of the first row
            dbc.Table(
                [
                    html.Thead(
                        html.Tr([
                            html.Th("LUT Details"),
                            html.Th("LUT 1"),
                        ])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td("Device Type"),
                            html.Td(
                                dcc.Dropdown(
                                    id='device-dropdown',
                                    options=[],
                                    value=None,
                                    clearable=False,
                                    placeholder='Select device',
                                    style={'maxWidth': '400px'}
                                )
                            )
                        ]),
                        html.Tr([html.Td("Temperature"), html.Td(id='lut-temp-cell')]),
                        html.Tr([html.Td("Corner"), html.Td(id='lut-corner-cell')]),
                        html.Tr([html.Td("Info."), html.Td(id='lut-info-cell')]),
                    ])
                ],
                bordered=True,
                hover=True,
                responsive=True,
                id='lut-details-table',
                style={
                    'marginTop': '1em'
                },
            ),
            # Debug text for development (shows selected device)
            html.Div(id='debug-text', style={'marginTop': '1em', 'color': '#ffb86c', 'fontFamily': 'monospace', 'width': '100%', 'wordBreak': 'break-word'}),
        ], width=12)
    ]),
], fluid=True)
