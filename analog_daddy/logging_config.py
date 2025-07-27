"""
logging_config.py

Centralized logging configuration for the analog_daddy package.

This module provides a setup_logging() function to configure logging for the entire application.
If no log directory is specified, it defaults to ~/.analog_daddy/logs.
Call setup_logging() once at the entry point of your app.
Other modules should simply use the logging module; do not reconfigure logging elsewhere.
"""
import os
import logging
import streamlit as st

def setup_logging(log_dir: str = None) -> None:
    """
    Set up logging for the analog_daddy package.
    Logs are written to ~/.analog_daddy/logs/analog_daddy.log
    if no log_dir is specified.
    Call this once at the entry point of your application.
    Avoids adding duplicate handlers on Streamlit reruns.
    """
    if log_dir is None:
        log_dir = os.path.expanduser('~/.analog_daddy/logs')
    try:
        os.makedirs(log_dir, exist_ok=True)
    except PermissionError as e:
        msg = (
            f"Permission denied while creating log directory: {log_dir}.  \n"
            f"Complete error: {e}"
        )
        raise PermissionError(msg) from e
    except FileExistsError as e:
        msg = (
            f"A file (not a directory) exists at the log directory path: {log_dir}.  \n"
            f"Complete error: {e}"
        )
        raise FileExistsError(msg) from e
    except OSError as e:
        msg = (
            f"OS error while creating log directory: {log_dir}.  \n"
            f"Complete error: {e}"
        )
        raise OSError(msg) from e
    except Exception as e:
        msg = (
            f"An unexpected error occurred while creating log directory: {log_dir}  \n"
            f"Complete error: {e}"
            f"Please contact the developer for support using Get Help in the dropdown menu."
        )
        raise RuntimeError(msg) from e

    log_path = os.path.join(log_dir, 'analog_daddy.log')
    logger = logging.getLogger()
    # Only add handler if no handlers exist
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode='a')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    if logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)

def st_log_print(msg, msg_type="info", stop=False):
    """
    Log the message and display it in Streamlit with the appropriate style.
    type: 'info', 'success', 'warning', 'error', 'debug'
    stop: If True, call st.stop() after displaying the message.
    """
    if msg_type == "success":
        logging.info(msg)
        st.success(msg)
    elif msg_type == "error":
        logging.error(msg)
        st.error(msg)
    elif msg_type == "warning":
        logging.warning(msg)
        st.warning(msg)
    elif msg_type == "debug":
        logging.debug(msg)
        st.info(msg)
    else:
        logging.info(msg)
        st.info(msg)
    if stop:
        st.stop()
