#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Utility functions.

Author        : Vadim Titov
Created       : Mo Sep 23 16:56:42 2024 +0200
Last modified : Mo Okt 14 19:44:51 2024 +0200
"""
import os
import re
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

from .config import get_db_path
from .exceptions import ListFilesException, PathException
from .models import Actor, Category, Movie


# pylint: disable=too-few-public-methods
class PathType(Enum):
    """
    Path type.

    Attributes
    ----------
    ACTOR : str
        Actor
    CATEGORY : str
        Category
    MOVIE : str
        Movie
    IMPORT : str
        Import
    SERIES : str
        Series
    STUDIO : str
        Studio
    """

    ACTOR = "actors"
    CATEGORY = "categories"
    MOVIE = "movies"
    IMPORT = "imports"
    SERIES = "series"
    STUDIO = "studios"


def generate_movie_filename(movie: Movie) -> str:
    """
    Generate a filename for a movie.

    Parameters
    ----------
    movie : Movie
        The movie

    Returns
    -------
    str
        The generated filename
    """
    filename = ""
    _, ext = os.path.splitext(movie.filename)
    if movie.studio is not None:
        filename += f"[{movie.studio.name}]"
    if movie.series is not None:
        if len(filename) > 0:
            filename += " "
        filename += f"{{{movie.series.name}"  # }}

        if movie.series_number is not None:
            filename += f" {movie.series_number}"
        filename += "}"
    if movie.name is not None:
        if len(filename) > 0:
            filename += " "
        filename += f"{movie.name}"
    if len(movie.actors) > 0:
        actor_names = [actor.name for actor in movie.actors]
        actors = f"({', '.join(actor_names)})"
        if len(filename) + len(actors) < 250:
            if len(filename) > 0:
                filename += " "
            filename += actors
    filename += ext
    if filename == ext:
        filename = movie.filename
    return filename


def generate_sort_name(name: str | None) -> str:
    """
    Generate a sort name.

    Parameters
    ----------
    name : str
        The name

    Returns
    -------
    str
        The generated sort name
    """
    if name is not None:
        return re.sub(
            r"^(?:a|an|the) ", "", re.sub(r"[^a-z0-9 ]", "", name.lower())
        )
    return ""


def list_files(path: str) -> List[str]:
    """
    List files in the given path.

    Parameters
    ----------
    path : str
        The path to list the files in.

    Returns
    -------
    List[str]
        The list of files in the path.
    """
    try:
        files = sorted(os.listdir(path))
    except FileNotFoundError as e:
        raise ListFilesException(
            f"Directory {path} does not exist", repr(e)
        ) from e
    except PermissionError as e:
        raise ListFilesException(
            f"No permission to list files in {path}", repr(e)
        ) from e
    except NotADirectoryError as e:
        raise ListFilesException(f"{path} is not a directory", repr(e)) from e
    except OSError as e:
        raise ListFilesException(
            f"An OS error occurred while listing files in {path}", repr(e)
        ) from e
    return files


def get_movie_path(path_type: PathType, full: bool = True) -> str:
    """Get the a relative or full path to the movie files.

    Parameters
    ----------
    path_type : PathType
        The type of path to get.
    full : bool
        Whether to return the full path or relative to the movie directory.

    Returns
    -------
    str
        The path to the movie files.
    """
    path = get_db_path() if full else "../.."

    return f"{path}/{path_type.value}"


def rename_movie_file(
    movie: Movie,
    actor_current: Optional[str] = None,
    category_current: Optional[str] = None,
    series_current: Optional[str] = None,
    studio_current: Optional[str] = None,
) -> None:
    """
    Rename a movie file.

    Parameters
    ----------
    movie : Movie
        Movie to rename
    actor_current : Optional[str]
        Current actor
    category_current : Optional[str]
        Current category
    series_current : Optional[str]
        Current series
    studio_current : Optional[str]
        Current studio
    """
    filename_current = movie.filename
    filename_new = generate_movie_filename(movie=movie)
    path_base = get_movie_path(PathType.MOVIE)
    path_current = f"{path_base}/{filename_current}"
    path_new = f"{path_base}/{filename_new}"

    if path_current != path_new:
        if os.path.exists(path_new):
            raise PathException(
                f"Renaming {movie.filename} -> {filename_new} conflicts with"
                " existing"
            )
        os.rename(src=path_current, dst=path_new)
        movie.filename = filename_new

        actor: Actor
        for actor in movie.actors:
            if actor_current is None:
                actor_current = actor.name
            update_actor_link(
                filename=filename_current,
                actor_name=actor_current,
                selected=False,
            )
            update_actor_link(
                filename=filename_new,
                actor_name=actor.name,
                selected=True,
            )

        category: Category
        for category in movie.categories:
            if category_current is None:
                category_current = category.name
            update_category_link(
                filename=filename_current,
                category_name=category_current,
                selected=False,
            )
            update_category_link(
                filename=filename_new,
                category_name=category.name,
                selected=True,
            )

        if movie.series is not None:
            if series_current is None:
                series_current = movie.series.name
            update_series_link(
                filename=filename_current,
                series_name=series_current,
                selected=False,
            )
            update_series_link(
                filename=filename_new,
                series_name=movie.series.name,
                selected=True,
            )

        if movie.studio is not None:
            if studio_current is None:
                studio_current = movie.studio.name
            update_studio_link(
                filename=filename_current,
                studio_name=studio_current,
                selected=False,
            )
            update_studio_link(
                filename=filename_new,
                studio_name=movie.studio.name,
                selected=True,
            )


def remove_movie(movie: Movie) -> None:
    """
    Remove a movie.

    Parameters
    ----------
    movie : Movie
        The movie to remove
    """
    migrate_file(filename=movie.filename, adding=False)
    for actor in movie.actors:
        update_actor_link(
            filename=movie.filename, actor_name=actor.name, selected=False
        )
    for category in movie.categories:
        update_category_link(
            filename=movie.filename,
            category_name=category.name,
            selected=False,
        )
    if movie.series is not None:
        update_series_link(
            filename=movie.filename,
            series_name=movie.series.name,
            selected=False,
        )
    if movie.studio is not None:
        update_studio_link(
            filename=movie.filename,
            studio_name=movie.studio.name,
            selected=False,
        )


def migrate_file(filename: str, adding: bool = True) -> None:
    """
    Migrate a movie file.

    Parameters
    ----------
    filename : str
        The movie to migrate.
    adding : bool
        Whether to add or remove the movie from the database.
    """
    imports = get_movie_path(PathType.IMPORT)
    movies = get_movie_path(PathType.MOVIE)

    base_current = imports if adding else movies
    base_new = movies if adding else imports

    path_current = f"{base_current}/{filename}"
    path_new = f"{base_new}/{filename}"

    if os.path.exists(path_new):
        raise PathException(
            f"Moving {filename} to {base_new} conflicts with existing"
        )
    try:
        os.rename(path_current, path_new)
    except FileNotFoundError as e:
        raise PathException(
            f"File {filename} not found in {base_current}", repr(e)
        ) from e
    except PermissionError as e:
        raise PathException(
            f"No permission to move {filename} from {base_current} to"
            f" {base_new}",
            repr(e),
        ) from e
    except OSError as e:
        raise PathException(
            f"An OS error occurred while moving {filename} from"
            f" {base_current} to {base_new}"
        ) from e


def parse_filename(
    filename: str,
) -> Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Parse a filename.

    Parameters
    ----------
    filename : str
        Filename

    Returns
    -------
    Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]
        Name, studio, series, number, actors
    """
    name, _ = os.path.splitext(filename)
    regex = (
        r"^"
        r"(?:\[([A-Za-z0-9 .,\'-]+)\])?"
        r" ?"
        r"(?:{([A-Za-z0-9 .,\'-]+?)(?: ([0-9]+))?})?"
        r" ?"
        r"([A-Za-z0-9 .,\'-]+)?"
        r" ?"
        r"(?:\(([A-Za-z0-9 .,\'-]+)\))?"
        r"$"
    )
    studio_name = None
    series_name = None
    series_number = None
    actor_names = None
    matches = re.search(regex, name)
    if matches is not None:
        studio_name, series_name, series_number, name, actor_names = (
            matches.groups()
        )
    return (name.strip(), studio_name, series_name, series_number, actor_names)


def update_link(
    filename: str, path_link_base: str, name: str | None, selected: bool
) -> None:
    """
    Update a movie category link.

    Parameters
    ----------
    filename : str
        Filename of the movie
    path_link_base : str
        Base path for the link
    name : str | None
        Name
    selected : bool
        Whether the category is selected
    """
    path_movies = get_movie_path(PathType.MOVIE, False)
    path_file = f"{path_movies}/{filename}"
    path_base = f"{path_link_base}/{name}"
    path_link = f"{path_base}/{filename}"

    if selected:
        if not os.path.isdir(path_base):
            try:
                path = Path(path_base)
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise PathException(
                    f"Link directory {path_base} could not be created"
                ) from e

        if not os.path.lexists(path_link):
            try:
                os.symlink(path_file, path_link)
            except Exception as e:
                raise PathException(
                    f"Link {path_file} -> {path_link} could not be created"
                ) from e

    else:
        if os.path.lexists(path_link):
            try:
                os.remove(path_link)
            except Exception as e:
                raise PathException(
                    f"Link {path_file} -> {path_link} could not be removed"
                ) from e

            try:
                os.rmdir(path_base)
            except FileNotFoundError as e:
                print(f"Directory not found: {path_base}, {repr(e)}")
            except PermissionError as e:
                print(
                    f"Permission denied for directory: {path_base}, {repr(e)}"
                )
            except OSError as e:
                print(
                    f"OS error occurred while removing directory {path_base}:"
                    f" {repr(e)}"
                )


def update_category_link(
    filename: str, category_name: str, selected: bool
) -> None:
    """
    Update a category link.

    Parameters
    ----------
    filename : str
        Filename of the movie
    category_name : str
        Category
    selected : bool
        Whether the category is selected
    """
    update_link(
        filename=filename,
        path_link_base=get_movie_path(PathType.CATEGORY),
        name=category_name,
        selected=selected,
    )


def update_actor_link(filename: str, actor_name: str, selected: bool) -> None:
    """
    Update an actor link.

    Parameters
    ----------
    filename : str
        Filename of the movie
    actor_name : str
        Actor
    selected : bool
        Whether the actor is selected
    """
    update_link(
        filename=filename,
        path_link_base=get_movie_path(PathType.ACTOR),
        name=actor_name,
        selected=selected,
    )


def update_series_link(
    filename: str, series_name: str | None, selected: bool
) -> None:
    """
    Update a series link.

    Parameters
    ----------
    filename : str
        Filename of the movie
    series_name : str | None
        Series
    selected : bool
        Whether the series is selected
    """
    update_link(
        filename=filename,
        path_link_base=get_movie_path(PathType.SERIES),
        name=series_name,
        selected=selected,
    )


def update_studio_link(
    filename: str, studio_name: str | None, selected: bool
) -> None:
    """
    Update a studio link.

    Parameters
    ----------
    filename : str
        Filename of the movie
    studio_name : str | None
        Studio
    selected : bool
        Whether the studio is selected
    """
    update_link(
        filename=filename,
        path_link_base=get_movie_path(PathType.STUDIO),
        name=studio_name,
        selected=selected,
    )
