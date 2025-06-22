"""
Entry point for the Analog Daddy Dash dashboard.

This module sets up the Dash app, applies the layout, registers callbacks,
and runs the server if executed as a script.
"""
import warnings
from .app import app
from .layout import layout
from .callbacks import register_callbacks

warnings.filterwarnings("ignore", category=DeprecationWarning)

app.layout = layout
register_callbacks()

if __name__ == "__main__":
    app.run(debug=True)
