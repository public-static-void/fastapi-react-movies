#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Utility functions tests.

Author        : Vadim Titov
Created       : Mi Okt 29 13:28:00 2024 +0200
Last modified : Do Okt 31 14:15:18 2024 +0100
"""

import pytest
from pytest_mock import MockerFixture

from movies_backend.config import get_db_path
from movies_backend.exceptions import ListFilesException
from movies_backend.models import Actor, Movie, Series, Studio
from movies_backend.util import (PathType, generate_movie_filename,
                                 get_movie_path, list_files)


def test_generate_movie_filename(mocker: MockerFixture) -> None:
    """
    Test generate_movie_filename.

    Parameters
    ----------
    mocker : MockerFixture
        Mocker
    """
    mocker.patch("movies_backend.models.Actor")
    actor1 = Actor()
    actor1.id = 1
    actor1.name = "Al Pacino"
    actor2 = Actor()
    actor2.id = 2
    actor2.name = "Diane Keaton"
    actor3 = Actor()
    actor3.id = 3
    actor3.name = "Robert De Niro"
    actor4 = Actor()
    actor4.id = 4
    actor4.name = "Robert Duvall"
    mocker.patch("movies_backend.models.Studio")
    studio = Studio()
    studio.id = 3
    studio.name = "Paramount Pictures"
    mocker.patch("movies_backend.models.Series")
    series = Series()
    series.id = 1
    series.name = "The Godfather"
    mocker.patch("movies_backend.models.Movie")
    movie = Movie()
    movie.id = 1
    movie.filename = "tgf2.mp4"
    movie.name = "The Godfather Part II"
    movie.series = series
    movie.series_number = 2
    movie.actors = [actor1, actor2, actor3, actor4]
    movie.studio = studio
    fn1 = (
        "[Paramount Pictures] {The Godfather 2} The Godfather Part II (Al"
        " Pacino, Diane Keaton, Robert De Niro, Robert Duvall).mp4"
    )
    fn2 = generate_movie_filename(movie=movie)
    assert fn1 == fn2


def test_list_files(mocker: MockerFixture) -> None:
    """
    Test list_files

    Parameters
    ----------
    mocker : MockerFixture
        Mocker
    """
    mocker.patch(
        "os.listdir", return_value=["file1.mp4", "file2.mp4", "file3.mp4"]
    )
    result = list_files("/some/path")
    assert result == ["file1.mp4", "file2.mp4", "file3.mp4"]
    mocker.patch("os.listdir", side_effect=FileNotFoundError)
    with pytest.raises(ListFilesException, match="does not exist"):
        list_files("/non/existent/path")
    mocker.patch("os.listdir", side_effect=PermissionError)
    with pytest.raises(ListFilesException, match="No permission"):
        list_files("/no/permission/path")
    mocker.patch("os.listdir", side_effect=NotADirectoryError)
    with pytest.raises(ListFilesException, match="is not a directory"):
        list_files("/not/a/directory/path")
    mocker.patch("os.listdir", side_effect=OSError)
    with pytest.raises(ListFilesException, match="An OS error occurred"):
        list_files("/some/path")


def test_get_movie_path() -> None:
    """
    Test get_movie_path

    Parameters
    ----------
    mocker : MockerFixture
        Mocker
    """
    db_path = get_db_path()
    expected_full_paths = {
        PathType.MOVIE: db_path + "/movies",
        PathType.SERIES: db_path + "/series",
        PathType.ACTOR: db_path + "/actors",
        PathType.CATEGORY: db_path + "/categories",
        PathType.STUDIO: db_path + "/studios",
        PathType.IMPORT: db_path + "/imports",
    }
    expected_relative_paths = {
        PathType.MOVIE: "../../movies",
        PathType.SERIES: "../../series",
        PathType.ACTOR: "../../actors",
        PathType.CATEGORY: "../../categories",
        PathType.STUDIO: "../../studios",
        PathType.IMPORT: "../../imports",
    }
    for path_type, expected in expected_full_paths.items():
        result = get_movie_path(path_type, full=True)
        assert result == expected
    for path_type, expected in expected_relative_paths.items():
        result = get_movie_path(path_type, full=False)
        assert result == expected
