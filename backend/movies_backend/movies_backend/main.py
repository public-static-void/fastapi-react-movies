#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Main entry point for the FastAPI backend template project.

Author        : Vadim Titov
Created       : Mo Sep 23 14:40:23 2024 +0200
Last modified : Di Okt 15 18:25:26 2024 +0200
"""


import uvicorn

from . import create_app
from .config import get_db_path, setup_logging
from .database import init_db

setup_logging()
init_db()
app = create_app()


def main() -> None:
    """Run the FastAPI app using uvicorn."""
    uvicorn.run(
        "movies_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=f"{get_db_path()}/logging.yaml",
    )


if __name__ == "__main__":
    main()
