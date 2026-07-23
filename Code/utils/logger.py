"""
Utility module for configuring and creating application loggers.
"""

import logging
import os
from datetime import datetime


def get_logger(name: str):
    """
    Create and configure a logger.

    The logger writes log messages to both the console and a log file.
    If the logger has already been configured, the existing instance is
    returned to avoid adding duplicate handlers.

    Parameters
    ----------
    name : str
        Name of the logger, typically __name__.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    # Create logs directory if not exists
    os.makedirs("logs", exist_ok=True)

    log_file = f"logs/app_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.log"

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
