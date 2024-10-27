#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Package tests.

Author        : Vadim Titov
Created       : Di Okt 15 16:52:09 2024 +0200
Last modified : Di Okt 15 16:52:14 2024 +0200
"""

from movies_backend import __version__


def test_package_version() -> None:
    """Test that the package version is correct."""
    assert __version__ == "1.0.0"
