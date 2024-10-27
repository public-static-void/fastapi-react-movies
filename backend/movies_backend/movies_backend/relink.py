#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Relink property files.

Description   : Invoke with `python -m moviemanager.relink`

Author        : Vadim Titov
Created       : Mo Okt 14 19:17:21 2024 +0200
Last modified : Di Okt 15 18:35:47 2024 +0200
"""


from movies_backend.database import get_db_session, init_db

from .config import get_logger, setup_logging
from .crud import get_all_movies
from .models import Actor, Category
from .util import (update_actor_link, update_category_link, update_series_link,
                   update_studio_link)


def relink_property_files() -> None:
    """Recreates property link files from database."""
    setup_logging()
    logger = get_logger()
    init_db()
    db = next(get_db_session())
    movies = get_all_movies(db)
    for movie in movies:
        logger.info("Processing %s", movie.filename)
        actor: Actor
        for actor in movie.actors:
            logger.info("Adding %s actor link", actor.name)
            update_actor_link(movie.filename, actor.name, True)
        category: Category
        for category in movie.categories:
            logger.info("Adding %s category link", category.name)
            update_category_link(movie.filename, category.name, True)
        if movie.series is not None:
            logger.info("Adding %s series link", movie.series.name)
            update_series_link(movie.filename, movie.series.name, True)
        if movie.studio is not None:
            logger.info("Adding %s studio link", movie.studio.name)
            update_studio_link(movie.filename, movie.studio.name, True)


def main() -> None:
    """Recreate property link files from database."""
    relink_property_files()


if __name__ == "__main__":
    main()
