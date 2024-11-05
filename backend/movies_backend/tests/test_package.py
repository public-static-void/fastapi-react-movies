#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Package tests.

Author        : Vadim Titov
Created       : Di Okt 15 16:52:09 2024 +0200
Last modified : Di Nov 05 14:57:02 2024 +0100
"""

from fastapi import FastAPI

from movies_backend import create_app


def test_create_app() -> None:
    """Test that the app is created correctly."""
    app: FastAPI = create_app()
    assert isinstance(app, FastAPI)
    assert app.title == "Movie Manager Backend"
    assert app.version == "1.0.1"
    assert "FastAPI backend template project" in app.description
