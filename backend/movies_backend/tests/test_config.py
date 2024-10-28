#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Config tests.

Author        : Vadim Titov
Created       : Di Okt 28 16:44:07 2024 +0200
Last modified : Di Okt 28 17:33:48 2024 +0200
"""

import pytest

from movies_backend.config import (DEFAULT_DB_PATH, get_db_path,
                                   get_log_config, get_sqlite_path)


def test_default_db_path():
    """Test default db path."""
    assert DEFAULT_DB_PATH == "./../db"


def test_get_db_path():
    """Test get_db_path."""
    assert get_db_path() == "./../db"
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setenv("MM_DB_PATH", "/custom/db/path")
        assert get_db_path() == "/custom/db/path"


def test_get_sqlite_path():
    """Test get_sqlite_path."""
    assert get_sqlite_path() == "./../db/sqlite.db"
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setenv("MM_SQLITE_PATH", "/custom/sqlite/path")
        assert get_sqlite_path() == "/custom/sqlite/path"


def test_get_log_config():
    """Test get_log_config."""
    assert get_log_config() == "./../db/logging.yaml"
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setenv("MM_LOG_CONFIG_PATH", "/custom/log/config/path")
        assert get_log_config() == "/custom/log/config/path"
