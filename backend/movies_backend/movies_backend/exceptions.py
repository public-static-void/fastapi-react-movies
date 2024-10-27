#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Exception handling.

Author        : Vadim Titov
Created       : Mo Sep 29 15:57:36 2024 +0200
Last modified : Do Okt 03 15:40:03 2024 +0200
"""


class InvalidIDException(Exception):
    """Raised when an ID is not found in the4 DB."""

    # pylint:disable=unnecessary-ellipsis
    ...


class DuplicateEntryException(Exception):
    """Raised when an entry already exists in the DB."""

    # pylint:disable=unnecessary-ellipsis
    ...


class ListFilesException(Exception):
    """Raised when files in a given path cannon be listed."""

    # pylint:disable=unnecessary-ellipsis
    ...


class PathException(Exception):
    """Raised when a path is invalid."""

    # pylint:disable=unnecessary-ellipsis
    ...


class IntegrityConstraintException(Exception):
    """Raised when a constraint is violated."""

    # pylint:disable=unnecessary-ellipsis
    ...
