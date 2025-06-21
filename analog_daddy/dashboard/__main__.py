import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from .app import app
from .layout import layout

app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)
