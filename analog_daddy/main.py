"""
main.py

Entry point for launching the analog daddy tools.

Usage:
    Use the wrapper script to run the main module.
    The wrapper script should be "./ad"
"""

import argparse
import sys
import os
import subprocess

def main():
    """
    Parses command-line arguments to configure and launch an Analog Daddy dashboard using Streamlit.

    Arguments:
        Use --help to see available options.

    Intended to do the following:
        - Loads the specified configuration file.
        - set up logging directory.
        - selects the appropriate dashboard script.
        - Run the dashboard using Streamlit.
    Exits with an error message if an unknown dashboard is specified.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Launch Analog daddy tool-suite with custom arguments.\n"
            "Analog daddy helps with transistor sizing for Integrated Circuit Design.\n"
            "\n"
            "Note: To run multiple dashboard instances, launch each instance in a \n"
            "separate shell or terminal window.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,  # Disable default help
        epilog="",
    )
    parser.add_argument(
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help=(
            "\nShow this help message and exit.\n"
        ))
    parser.add_argument(
        "--dashboard",
        type=str,
        default="plotter",
        help=(
            "\n(Optional) Choose which dashboard to launch.\n"
            "Valid entries are 'plotter' (Default) or 'designer'.\n"
            "\n"
        ))
    parser.add_argument(
        "--config",
        type=str,
        default="~/.analog_daddy/config/config.toml",
        help=(
            "\n(Optional) Path to the TOML config file.\n"
            "Defaults to ~/.analog_daddy/config/config.toml\n"
            "\n"
        ))
    parser.add_argument(
        "--logging-dir",
        type=str,
        default="~/.analog_daddy/logs",
        help=(
            "\n(Optional) Path to the log directory.\n"
            "Defaults to ~/.analog_daddy/logs\n"
            "\n"
        ))
    parser.add_argument(
        "--devel-mode",
        action="store_true",
        help=(
            "\n(Optional) When this flag is set, the application will run in development mode.\n"
            "Intended for development purposes only.\n"
            "\n"
        ))
    args = parser.parse_args()

    # Streamlit dashboard map to resolve dashboard names to scripts
    dashboard_map = {
        "designer": "analog_daddy/designer_dashboard/app_designer.py",
        "plotter": "analog_daddy/plotter_dashboard/app_plotter.py"
    }
    # Allow case-insensitive dashboard names
    dashboard_script = dashboard_map.get((args.dashboard).lower())
    if dashboard_script is None:
        print(f"Unknown dashboard: {args.dashboard}. Choose 'designer' or 'plotter'.")
        sys.exit(1)
    # Share the paths with Streamlit process using environment variables
    # Despite my doubts, this seems to be the best way for interprocess communication
    # https://github.com/streamlit/streamlit/issues/337
    env = os.environ.copy()
    env["ANALOG_DADDY_CONFIG_PATH"] = args.config
    env["ANALOG_DADDY_LOGDIR_PATH"] = args.logging_dir
    env["ANALOG_DADDY_DEVEL_MODE"] = str(args.devel_mode).lower()
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", dashboard_script
    ]
    try:
        subprocess.run(streamlit_cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error: Streamlit dashboard failed to launch.\nExit code: {e.returncode}\n{e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
