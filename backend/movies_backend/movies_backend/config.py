#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Config module.

Author        : Vadim Titov
Created       : Mo Sep 23 15:59:47 2024 +0200
Last modified : Mo Okt 14 19:33:38 2024 +0200
"""

import os
import sys
from logging import Logger, getLogger
from logging.config import dictConfig

import yaml

DEFAULT_DB_PATH = "./../db"


def get_db_path() -> str:
    """
    Get the database path.

    Returns
    -------
    str
        The database path.
    """
    return os.getenv("MM_DB_PATH", DEFAULT_DB_PATH)


def get_sqlite_path() -> str:
    """
    Get the sqlite database path.

    Returns
    -------
    str
        The sqlite database path.
    """
    path_override = os.getenv("MM_SQLITE_PATH")
    if path_override is not None:
        return path_override
    return f"{get_db_path()}/sqlite.db"


def get_log_config() -> str:
    """
    Get the log config path.

    Returns
    -------
    str
        The log config path.
    """
    path_override = os.getenv("MM_LOG_CONFIG_PATH")

    if path_override is not None:
        path = path_override
    else:
        path = f"{get_db_path()}/logging.yaml"

    return path


def setup_logging() -> None:
    """Configure logging for the application using the yaml config file."""
    path = get_log_config()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except OSError:
        logger = getLogger()
        logger.critical("Failed to read the logging config file %s", path)

        sys.exit(1)

    dictConfig(data)


def get_logger() -> Logger:
    """
    Get the logger.

    Returns
    -------
    Logger
        The logger.
    """
    return getLogger("moviemanager")
