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

def setup_logging():
    """
    Set up logging for the analog_daddy package. Logs are written to .logs/analog_daddy.log.
    Call this once at the entry point of your application.
    """
    log_dir = os.path.join(os.path.dirname(__file__), '..', '.logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'analog_daddy.log')
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a'
    )
