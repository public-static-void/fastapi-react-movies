#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : DB restoration module.

Author        : Vadim Titov
Created       : Di Okt 01 18:14:07 2024 +0200
Last modified : Di Okt 15 18:35:10 2024 +0200
"""

import sys
from typing import Dict, List, Optional

from .config import get_logger, setup_logging
from .crud import add_actor, add_category, add_movie, add_series, add_studio
from .database import get_db_session, init_db
from .exceptions import ListFilesException
from .util import PathType, get_movie_path, list_files, parse_filename


# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def main() -> None:
    """Restore the database from the files in the movies directory."""
    setup_logging()
    logger = get_logger()
    init_db()
    db = next(get_db_session())
    try:
        path = get_movie_path(PathType.MOVIE)
        movie_files = list_files(path)
    except ListFilesException as e:
        logger.critical(repr(e))
        sys.exit(1)
    actors: List[str] = []
    categories: List[str] = []
    series: List[str] = []
    studios: List[str] = []
    for path_type in (
        PathType.ACTOR,
        PathType.CATEGORY,
        PathType.SERIES,
        PathType.STUDIO,
    ):
        files: List[str] = locals()[path_type.value]
        path = get_movie_path(path_type)
        try:
            files.extend(list_files(path))
            logger.info("Loaded %s from link directory %s", path_type, path)
        except ListFilesException:
            logger.warning(
                "Failed to load %s from link directory %s", path_type, path
            )
    if ".keep" in movie_files:
        movie_files.remove(".keep")
    movie_actors: Dict[str, List[str]] = {
        filename: [] for filename in movie_files
    }
    movie_categories: Dict[str, List[str]] = {
        filename: [] for filename in movie_files
    }
    movie_series: Dict[str, List[str]] = {
        filename: [] for filename in movie_files
    }
    movie_studios: Dict[str, List[str]] = {
        filename: [] for filename in movie_files
    }
    for path_type in (
        PathType.ACTOR,
        PathType.CATEGORY,
        PathType.SERIES,
        PathType.STUDIO,
    ):
        names: List[str] = locals()[path_type.value]
        path = get_movie_path(path_type)
        name: Optional[str]
        for name in names:
            full_path = f"{path}/{name}"
            try:
                files = list_files(full_path)
                logger.info("Loaded link files from %s", full_path)
            except ListFilesException as e:
                logger.error(
                    "Unable to read files in %s. %s", full_path, repr(e)
                )
                continue
            properties: Dict[str, List[str]] = locals()[
                f"movie_{path_type.value}"
            ]
            for file in files:
                if file in properties:
                    properties[file].append(name)
                    logger.info(
                        "Associated movie %s with %s in %s",
                        file,
                        name,
                        path_type,
                    )
                else:
                    logger.warning("Broken link file %s/%s", full_path, file)

    movie_name: Dict[str, Optional[str]] = {
        filename: None for filename in movie_files
    }
    movie_series_number: Dict[str, Optional[str]] = {
        filename: None for filename in movie_files
    }
    for file in movie_files:
        name, studio_name, series_name, series_number, actor_names = (
            parse_filename(file)
        )
        if name is not None:
            movie_name[file] = name
            logger.info("Parsed name %s from file %s", name, file)
        if actor_names is not None:
            file_actors = actor_names.split(", ")
            actors.extend(file_actors)
            movie_actors[file].extend(file_actors)
            logger.info("Parsed actors (%s) from file %s", actor_names, file)
        if series_name is not None:
            series.append(series_name)
            movie_series[file].append(series_name)
            logger.info("Parsed series %s from file %s", series_name, file)
        if series_number is not None:
            movie_series_number[file] = series_number
            logger.info(
                "Parsed series number %s from file %s", series_number, file
            )
        if studio_name is not None:
            studios.append(studio_name)
            movie_studios[file].append(studio_name)
            logger.info("Parsed studio %s from file %s", studio_name, file)
    actors = sorted(set(actors))
    categories = sorted(set(categories))
    series = sorted(set(series))
    studios = sorted(set(studios))
    actor_by_name = {
        actor.name: actor
        for actor in [add_actor(db=db, name=actor) for actor in actors]
    }
    logger.info("Imported actors into database")
    category_by_name = {
        category.name: category
        for category in [
            add_category(db=db, name=category) for category in categories
        ]
    }
    logger.info("Imported categories into database")
    series_by_name = {
        series.name: series
        for series in [add_series(db=db, name=series) for series in series]
    }
    logger.info("Imported series into database")
    studio_by_name = {
        studio.name: studio
        for studio in [add_studio(db=db, name=studio) for studio in studios]
    }
    logger.info("Imported studios into database")
    for filename in movie_files:
        name = movie_name[filename]
        if name is None:
            name = ""
        series_number = movie_series_number[filename]
        series_number_int: Optional[int] = None
        if series_number is not None:
            series_number_int = int(series_number)
        series_id = None
        studio_id = None
        actors_list = []
        category_list = []
        if len(movie_series[filename]) > 0:
            series_name = list(set(movie_series[filename]))[0]
            series_id = series_by_name[series_name].id
        if len(movie_studios[filename]) > 0:
            studio_name = list(set(movie_studios[filename]))[0]
            studio_id = studio_by_name[studio_name].id
        movie_actors_set = set(movie_actors[filename])
        if len(movie_actors_set) > 0:
            actors_list = [
                actor_by_name[actor_name] for actor_name in movie_actors_set
            ]
        movie_categories_set = set(movie_categories[filename])
        if len(movie_categories_set) > 0:
            category_list = [
                category_by_name[category_name]
                for category_name in movie_categories_set
            ]
        add_movie(
            db=db,
            filename=filename,
            name=name,
            studio_id=studio_id,
            series_id=series_id,
            series_number=series_number_int,
            actors=actors_list,
            categories=category_list,
            processed=True,
        )
        logger.info("Imported movie %s into database", filename)


if __name__ == "__main__":
    main()
