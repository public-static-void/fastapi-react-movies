#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Root endpoint.

Author        : Vadim Titov
Created       : Di Okt 15 17:07:49 2024 +0200
Last modified : Di Okt 15 17:09:02 2024 +0200
"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """
    Redirect to /docs.

    Returns
    -------
    RedirectResponse
        Redirect to /docs
    """
    return RedirectResponse("/docs")
