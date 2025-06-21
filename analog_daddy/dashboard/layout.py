from dash import html

layout = html.Div([
    html.H1('Hello, Analog Daddy Dashboard!'),
    html.P('This is a minimal Dash app.'),
    html.H2('Dracula Color Demo'),
    html.Div([
        html.Div('Background', style={'background': 'var(--dracula-background)', 'color': 'var(--dracula-foreground)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Current Line', style={'background': 'var(--dracula-current-line)', 'color': 'var(--dracula-foreground)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Foreground', style={'background': 'var(--dracula-foreground)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Comment', style={'background': 'var(--dracula-comment)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Cyan', style={'background': 'var(--dracula-cyan)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Green', style={'background': 'var(--dracula-green)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Orange', style={'background': 'var(--dracula-orange)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Pink', style={'background': 'var(--dracula-pink)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Purple', style={'background': 'var(--dracula-purple)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Red', style={'background': 'var(--dracula-red)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
        html.Div('Yellow', style={'background': 'var(--dracula-yellow)', 'color': 'var(--dracula-background)', 'padding': '1em', 'margin': '0.5em', 'borderRadius': '6px'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),
])
