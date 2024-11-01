#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : FastAPI backend template project.

Author        : Vadim Titov
Created       : Di Okt 15 16:57:03 2024 +0200
Last modified : Mi Okt 27 18:24:34 2024 +0200
"""

__version__ = "1.0.0"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import (actors, categories, movie_actor, movie_category, movies,
                     root, series, studios)


def create_app() -> FastAPI:
    """
    Create FastAPI application.

    Returns
    -------
    FastAPI
        FastAPI application
    """
    description = """# Movie Manager Backend

    FastAPI backend template project"""
    app = FastAPI(
        title="Movie Manager Backend",
        description=description,
        version="1.0.0",
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=(
            r"https?://(?:127\.0\.0\.1|localhost)(?::300[0-9])?"
        ),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(root.router)
    app.include_router(actors.router)
    app.include_router(categories.router)
    app.include_router(movie_actor.router)
    app.include_router(movie_category.router)
    app.include_router(movies.router)
    app.include_router(series.router)
    app.include_router(studios.router)
    return app
