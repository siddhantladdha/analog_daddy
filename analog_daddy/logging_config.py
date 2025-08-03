"""
logging_config.py

Centralized logging configuration and Exception handling for the analog_daddy package.

This module provides a setup_logging() function to configure logging for the entire application.
If no log directory is specified, it defaults to ~/.analog_daddy/logs.
Call setup_logging() once at the entry point of your app.
Other modules should simply use the logging module; do not reconfigure logging elsewhere.
"""
from pathlib import Path
import logging
import streamlit as st

class CustomFileError(Exception):
    """Custom exception for file errors with standardized messages."""
    ERROR_MESSAGES = {
        FileNotFoundError:
            "The file/directory is not found at the provided path. ",
        PermissionError:
            "Permission denied when reading/writing/creating file/directory at the provided path. "
            "Please ensure you have the necessary permissions. ",
        FileExistsError:
            "A file/directory already exists at the provided path. "
            "Either delete it or specify a different path. ",
        OSError:
            "An Operating System level error has occurred "
            "while reading/writing/accessing file/directory. "
            "Contact the developer for support. ",
        Exception:
            "An unexpected error has occured "
            "while reading/writing/accessing file/directory. "
            "Contact the developer for support. "
    }

    def __init__(self, filepath: str, exc: Exception):
        error_type = type(exc)
        msg = self.ERROR_MESSAGES.get(error_type, self.ERROR_MESSAGES[Exception])
        full_msg = (
            f"{msg}\n"
            f"File: {filepath}\n"
            f"Error type: {error_type.__name__}\n"
            f"Details: {exc}"
        )
        super().__init__(full_msg)

def setup_logging(
        log_dir: str = "~/.analog_daddy/logs"
        ) -> None:
    """
    Set up logging for the analog_daddy package.
    Logs are written to ~/.analog_daddy/logs/analog_daddy.log
    if no log_dir is specified.
    Call this once at the entry point of your application.
    DON'T decorate this function with @st.cache_resource.
    The program has checks to avoid adding duplicate handlers
    on Streamlit reruns.
    """
    log_dir_path = Path(log_dir).expanduser().resolve()
    try:
        log_dir_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise CustomFileError(str(log_dir_path), e) from e

    log_path = log_dir_path / 'analog_daddy.log'
    logger = logging.getLogger()
    # Only add handler if no handlers exist
    if not logger.handlers:
        file_handler = logging.FileHandler(str(log_path), mode='a')
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
