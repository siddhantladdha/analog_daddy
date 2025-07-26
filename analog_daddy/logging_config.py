"""
logging_config.py

Centralized logging configuration for the analog_daddy package.

This module provides a setup_logging() function to configure logging for the entire application.
All logs are written to .logs/analog_daddy.log. Call setup_logging() once at the entry
point of your app.
Other modules should simply use the logging module; do not reconfigure logging elsewhere.
"""
import os
import logging
import streamlit as st

def setup_logging():
    """
    Set up logging for the analog_daddy package. Logs are written to .logs/analog_daddy.log.
    Call this once at the entry point of your application.
    Avoids adding duplicate handlers on Streamlit reruns.
    """
    log_dir = os.path.join(os.path.dirname(__file__), '..', '.logs')
    os.makedirs(log_dir, exist_ok=True)
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
