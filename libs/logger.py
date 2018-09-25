#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
import tempfile


LOG_FILENAME = os.path.join(tempfile.gettempdir(), 'zpython.log')

# Define the logging configuration
LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)s - %(message)s"
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": LOG_FILENAME
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "main": {
            "handlers": ["file", "console"],
            "level": "INFO"
        }
    }
}


def zero_logger(level=None):
    """
    Build and return the logger.
    :param level: logger level
    :return: logger -- Logger instance
    """
    _logger = logging.getLogger()
    # Load the configuration
    logging.config.dictConfig(LOGGING_CFG)

    if level is not None:
        _logger.setLevel(level=level)
    return _logger


logger = zero_logger()
