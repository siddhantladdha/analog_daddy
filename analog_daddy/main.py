"""
main.py

Entry point for launching the analog daddy tools.

Usage:
    python -m analog_daddy.main --config /path/to/config.toml
"""

import argparse
import sys
import subprocess
from analog_daddy.config import load_config

def main():
    """
    Parses command-line arguments to configure and launch an Analog Daddy dashboard using Streamlit.

    Arguments:
        --config (str, optional): Path to the TOML configuration file.
        --dashboard (str, optional): Dashboard to launch ('designer' or 'plotter').
        Defaults to 'plotter'.

    Loads the specified configuration file, selects the appropriate dashboard script,
    and runs it via Streamlit.
    Exits with an error message if an unknown dashboard is specified.
    """
    parser = argparse.ArgumentParser(
        description="Launch Analog daddy tools with custom arguments.")
    parser.add_argument(
        "--config",
        type=str,
        default="~/.analog_daddy/config/config.toml",
        help="Path to the TOML config file (optional)."
    )
    parser.add_argument(
        "--dashboard",
        type=str,
        default="plotter",
        help="Choose which dashboard to launch 'designer' or 'plotter' (Default)"
    )
    args = parser.parse_args()

    try:
        # define CONFIG as a global variable to be used in the app
        # and within submodules.
        # import within try-catch to handle any import errors gracefully.
        # you can now just use
        # from analog_daddy.config import CONFIG
        # everywhere else since the exception handling is done here.
        # Load config before launching Streamlit
        load_config(args.config)
    except Exception as e:
        print(f"\n{str(e)}\n")
        sys.exit(1)

    # Run Streamlit dashboard
    dashboard_map = {
        "designer": "analog_daddy/designer_dashboard/app_designer.py",
        "plotter": "analog_daddy/plotter_dashboard/app_plotter.py"
    }
    dashboard_script = dashboard_map.get((args.dashboard).lower())
    if dashboard_script is None:
        print(f"Unknown dashboard: {args.dashboard}. Choose 'designer' or 'plotter'.")
        sys.exit(1)
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", dashboard_script
    ]
    subprocess.run(streamlit_cmd, check=True)

if __name__ == "__main__":
    main()
