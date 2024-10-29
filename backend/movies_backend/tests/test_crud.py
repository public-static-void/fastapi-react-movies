#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : CRUD functionality tests.

Author        : Vadim Titov
Created       : Mi Okt 16 16:44:51 2024 +0200
Last modified : Mi Okt 29 13:11:16 2024 +0200
"""

import sqlite3
from pathlib import Path
from typing import Generator

import pytest
from pytest import FixtureRequest, TempPathFactory
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from movies_backend.crud import (add_actor, add_category, add_movie,
                                 add_series, add_studio, delete_actor,
                                 delete_category, delete_series, delete_studio,
                                 get_actor, get_actor_by_name, get_all_actors,
                                 get_all_categories, get_all_movies,
                                 get_all_series, get_all_studios, get_category,
                                 get_category_by_name, get_movie, get_series,
                                 get_series_by_name, get_studio,
                                 get_studio_by_name, parse_file_info,
                                 update_actor, update_category, update_series,
                                 update_studio)
from movies_backend.database import get_db_session, init_db
from movies_backend.exceptions import (DuplicateEntryException,
                                       IntegrityConstraintException,
                                       InvalidIDException)


@pytest.fixture(scope="module", autouse=True)
def setup_database(
    tmp_path_factory: TempPathFactory,
    module_mocker: MockerFixture,
    request: FixtureRequest,
) -> None:
    """
    Setup database for tests.

    Parameters
    ----------
    tmp_path_factory : TempPathFactory
        Temporary path factory
    request : FixtureRequest
        Fixture request
    module_mocker : MockerFixture
        Module mocker
    """
    path: Path = tmp_path_factory.mktemp("database") / "db.sqlite3"
    module_mocker.patch(
        "movies_backend.database.get_sqlite_path", return_value=path.as_posix()
    )
    connection = sqlite3.connect(path.as_posix())
    filename = Path(request.path).parent / "data" / "init.sql"
    with open(filename, "r", encoding="utf-8") as f:
        connection.executescript(f.read())
    init_db()


@pytest.fixture(name="db")
def db_fixture() -> Generator[Session, None, None]:
    """
    Get database session.

    Yields
    ------
    Session
        The database session.
    """
    yield from get_db_session()


def test_add_actor(db: Session) -> None:
    """
    Test add_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    actor1 = add_actor(db=db, name="Silvester Stallone")
    assert actor1 is not None
    assert actor1.id == 20
    assert actor1.name == "Silvester Stallone"
    actor2 = get_actor(db=db, actor_id=actor1.id)
    assert actor2 is not None
    assert actor2.name == "Silvester Stallone"


def test_add_actor_duplicate(db: Session) -> None:
    """
    Test add_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    with pytest.raises(DuplicateEntryException):
        add_actor(db=db, name="Al Pacino")


def test_get_actor(db: Session) -> None:
    """
    Test get_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    actor = get_actor(db=db, actor_id=20)
    assert actor is not None
    assert actor.name == "Silvester Stallone"


def test_actor_not_found(db: Session) -> None:
    """
    Test get_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    actor = get_actor_by_name(db=db, actor_name="")
    assert actor is None


def test_get_actor_by_name(db: Session) -> None:
    """
    Test get_actor_by_name

    Parameters
    ----------
    db : Session
        Database session
    """
    name = "Brad Pitt"
    actor = get_actor_by_name(db=db, actor_name=name)
    assert actor is not None
    assert actor.name == name
    assert actor.id == 2


def test_get_all_actors(db: Session) -> None:
    """
    Test get_all_actors

    Parameters
    ----------
    db : Session
        Database session
    """
    actors = get_all_actors(db=db)
    assert actors is not None
    assert len(actors) == 20


def test_update_actor(db: Session) -> None:
    """
    Test update_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    actor_id = 20
    actor_name = "Silvester Stallone"
    actor_name_new = "Mark Hamil"
    actor = get_actor(db=db, actor_id=actor_id)
    assert actor is not None
    assert actor.name == actor_name
    updated_actor = update_actor(
        db=db, actor_id=actor.id, actor_name=actor_name_new
    )
    actor = get_actor(db=db, actor_id=actor_id)
    assert actor is not None
    assert actor == updated_actor
    assert actor.name == actor_name_new
    with pytest.raises(InvalidIDException):
        _ = update_actor(db=db, actor_id=-1, actor_name="")
    with pytest.raises(DuplicateEntryException):
        _ = update_actor(db=db, actor_id=20, actor_name="Al Pacino")


def test_delete_actor(db: Session) -> None:
    """
    Test delete_actor

    Parameters
    ----------
    db : Session
        Database session
    """
    delete_actor(db=db, actor_id=20)
    actor = get_actor(db=db, actor_id=20)
    assert actor is None
    with pytest.raises(InvalidIDException):
        _ = delete_actor(db=db, actor_id=-1)
    with pytest.raises(IntegrityConstraintException):
        _ = delete_actor(db=db, actor_id=1)


def test_add_category(db: Session) -> None:
    """
    Test add_category

    Parameters
    ----------
    db : Session
        Database session
    """
    category1 = add_category(db=db, name="Mystery")
    assert category1 is not None
    assert category1.id == 5
    assert category1.name == "Mystery"
    category2 = get_category(db=db, category_id=category1.id)
    assert category2 is not None
    assert category2.name == "Mystery"


def test_add_category_duplicate(db: Session) -> None:
    """
    Test add_category

    Parameters
    ----------
    db : Session
        Database session
    """
    with pytest.raises(DuplicateEntryException):
        add_category(db=db, name="Drama")


def test_get_category(db: Session) -> None:
    """
    Test get_category

    Parameters
    ----------
    db : Session
        Database session
    """
    category = get_category(db=db, category_id=5)
    assert category is not None
    assert category.name == "Mystery"


def test_category_not_found(db: Session) -> None:
    """
    Test get_category

    Parameters
    ----------
    db : Session
        Database session
    """
    category = get_category(db=db, category_id=0)
    assert category is None


def test_get_category_by_name(db: Session) -> None:
    """
    Test get_category_by_name

    Parameters
    ----------
    db : Session
        Database session
    """
    name = "Drama"
    category = get_category_by_name(db=db, category_name=name)
    assert category is not None
    assert category.name == name
    assert category.id == 3


def test_get_all_categories(db: Session) -> None:
    """
    Test get_all_categories

    Parameters
    ----------
    db : Session
        Database session
    """
    categories = get_all_categories(db=db)
    assert categories is not None
    assert len(categories) == 5


def test_update_category(db: Session) -> None:
    """
    Test update_category

    Parameters
    ----------
    db : Session
        Database session
    """
    category_id = 5
    category_name_new = "Sci-Fi"
    category = get_category(db=db, category_id=category_id)
    assert category is not None
    assert category.name == "Mystery"
    updated_category = update_category(
        db=db, category_id=category.id, category_name=category_name_new
    )
    category = get_category(db=db, category_id=category_id)
    assert category is not None
    assert category == updated_category
    assert category.name == category_name_new
    with pytest.raises(InvalidIDException):
        _ = update_category(db=db, category_id=-1, category_name="")
    with pytest.raises(DuplicateEntryException):
        _ = update_category(db=db, category_id=5, category_name="Drama")


def test_delete_category(db: Session) -> None:
    """
    Test delete_category

    Parameters
    ----------
    db : Session
        Database session
    """
    delete_category(db=db, category_id=5)
    category = get_category(db=db, category_id=5)
    assert category is None
    with pytest.raises(InvalidIDException):
        _ = delete_category(db=db, category_id=-1)
    with pytest.raises(IntegrityConstraintException):
        _ = delete_category(db=db, category_id=1)


def test_add_series(db: Session) -> None:
    """
    Test add_series

    Parameters
    ----------
    db : Session
        Database session
    """
    series = add_series(db=db, name="The Lord Of The Rings")
    assert series is not None
    assert series.id == 3
    assert series.name == "The Lord Of The Rings"


def test_add_series_duplicate(db: Session) -> None:
    """
    Test add_series

    Parameters
    ----------
    db : Session
        Database session
    """
    with pytest.raises(DuplicateEntryException):
        add_series(db=db, name="The Lord Of The Rings")


def test_get_series(db: Session) -> None:
    """
    Test get_series

    Parameters
    ----------
    db : Session
        Database session
    """
    series = get_series(db=db, series_id=3)
    assert series is not None
    assert series.name == "The Lord Of The Rings"


def test_series_not_found(db: Session) -> None:
    """
    Test get_series

    Parameters
    ----------
    db : Session
        Database session
    """
    series = get_series(db=db, series_id=0)
    assert series is None


def test_get_series_by_name(db: Session) -> None:
    """
    Test get_series_by_name

    Parameters
    ----------
    db : Session
        Database session
    """
    name = "The Lord Of The Rings"
    series = get_series_by_name(db=db, series_name=name)
    assert series is not None
    assert series.name == name
    assert series.id == 3


def test_get_all_series(db: Session) -> None:
    """
    Test get_all_series

    Parameters
    ----------
    db : Session
        Database session
    """
    series = get_all_series(db=db)
    assert series is not None
    assert len(series) == 3


def test_update_series(db: Session) -> None:
    """
    Test update_series

    Parameters
    ----------
    db : Session
        Database session
    """
    series_id = 3
    series_name_new = "Star Wars"
    series = get_series(db=db, series_id=series_id)
    assert series is not None
    assert series.name == "The Lord Of The Rings"
    updated_series = update_series(
        db=db, series_id=series.id, series_name=series_name_new
    )
    series = get_series(db=db, series_id=series_id)
    assert series is not None
    assert series == updated_series
    assert series.name == series_name_new
    with pytest.raises(InvalidIDException):
        _ = update_series(db=db, series_id=-1, series_name="")
    with pytest.raises(DuplicateEntryException):
        _ = update_series(db=db, series_id=3, series_name="Saw")


def test_delete_series(db: Session) -> None:
    """
    Test delete_series

    Parameters
    ----------
    db : Session
        Database session
    """
    delete_series(db=db, series_id=3)
    series = get_series(db=db, series_id=3)
    assert series is None
    with pytest.raises(InvalidIDException):
        _ = delete_series(db=db, series_id=-1)
    with pytest.raises(IntegrityConstraintException):
        _ = delete_series(db=db, series_id=1)


def test_add_studio(db: Session) -> None:
    """
    Test add_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    studio = add_studio(db=db, name="20th Century Studios")
    assert studio is not None
    assert studio.id == 7
    assert studio.name == "20th Century Studios"


def test_add_studio_duplicate(db: Session) -> None:
    """
    Test add_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    with pytest.raises(DuplicateEntryException):
        add_studio(db=db, name="20th Century Studios")


def test_get_studio(db: Session) -> None:
    """
    Test get_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    studio = get_studio(db=db, studio_id=7)
    assert studio is not None
    assert studio.name == "20th Century Studios"


def test_studio_not_found(db: Session) -> None:
    """
    Test get_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    studio = get_studio(db=db, studio_id=0)
    assert studio is None


def test_get_studio_by_name(db: Session) -> None:
    """
    Test get_studio_by_name

    Parameters
    ----------
    db : Session
        Database session
    """
    name = "20th Century Studios"
    studio = get_studio_by_name(db=db, studio_name=name)
    assert studio is not None
    assert studio.name == name
    assert studio.id == 7


def test_get_all_studios(db: Session) -> None:
    """
    Test get_all_studios

    Parameters
    ----------
    db : Session
        Database session
    """
    studios = get_all_studios(db=db)
    assert studios is not None
    assert len(studios) == 7


def test_update_studio(db: Session) -> None:
    """
    Test update_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    studio_id = 7
    studio_name_new = "20th Century Fox"
    studio = get_studio(db=db, studio_id=studio_id)
    assert studio is not None
    updated_studio = update_studio(
        db=db, studio_id=studio.id, studio_name=studio_name_new
    )
    studio = get_studio(db=db, studio_id=studio_id)
    assert studio is not None
    assert studio == updated_studio
    assert studio.name == studio_name_new
    with pytest.raises(InvalidIDException):
        _ = update_studio(db=db, studio_id=-1, studio_name="")
    with pytest.raises(DuplicateEntryException):
        _ = update_studio(db=db, studio_id=7, studio_name="Warner Bros.")


def test_delete_studio(db: Session) -> None:
    """
    Test delete_studio

    Parameters
    ----------
    db : Session
        Database session
    """
    delete_studio(db=db, studio_id=7)
    studio = get_studio(db=db, studio_id=7)
    assert studio is None
    with pytest.raises(InvalidIDException):
        _ = delete_studio(db=db, studio_id=-1)
    with pytest.raises(IntegrityConstraintException):
        _ = delete_studio(db=db, studio_id=1)


def test_add_movie(db: Session) -> None:
    """
    Test add_movie

    Parameters
    ----------
    db : Session
        Database session
    """
    actor1 = add_actor(db=db, name="Elijah Wood")
    actor2 = add_actor(db=db, name="Ian McKellen")
    actor3 = add_actor(db=db, name="Liv Tyler")
    actor4 = add_actor(db=db, name="Viggo Mortensen")
    category1 = add_category(db=db, name="Fantasy")
    movie = add_movie(
        db=db,
        filename="lotr.mp4",
        name="The Lord of the Rings: The Fellowship of the Ring",
        actors=[actor1, actor2, actor3, actor4],
        categories=[category1],
    )
    assert movie is not None
    assert movie.id == 13
    assert movie.name == "The Lord of the Rings: The Fellowship of the Ring"
    assert movie.filename == "lotr.mp4"
    assert movie.actors == [actor1, actor2, actor3, actor4]
    assert movie.categories == [category1]
    assert movie.processed is False


def test_add_movie_duplicate(db: Session) -> None:
    """
    Test add_movie

    Parameters
    ----------
    db : Session
        Database session
    """
    with pytest.raises(DuplicateEntryException):
        add_movie(
            db=db,
            filename="lotr.mp4",
            name="The Lord of the Rings: The Fellowship of the Ring",
        )


def test_get_movie(db: Session) -> None:
    """
    Test get_movie

    Parameters
    ----------
    db : Session
        Database session
    """
    movie = get_movie(db=db, movie_id=13)
    assert movie is not None
    assert movie.name == "The Lord of the Rings: The Fellowship of the Ring"
    assert movie.filename == "lotr.mp4"
    assert movie.processed is False


def test_movie_not_found(db: Session) -> None:
    """
    Test get_movie

    Parameters
    ----------
    db : Session
        Database session
    """
    movie = get_movie(db=db, movie_id=0)
    assert movie is None


def test_get_all_movies(db: Session) -> None:
    """
    Test get_all_movies

    Parameters
    ----------
    db : Session
        Database session
    """
    movies = get_all_movies(db=db)
    assert movies is not None
    assert len(movies) == 13


def test_parse_file_info(db: Session) -> None:
    """
    Test parse_file_info

    Parameters
    ----------
    db : Session
        Database session
    """
    filename = (
        "[Paramount Pictures] {The Godfather 2} The Godfather Part II (Al"
        " Pacino, Diane Keaton, Robert De Niro, Robert Duvall)"
    )
    name, studio_id, series_id, series_number, actors = parse_file_info(
        db=db, filename=filename
    )
    assert name == "The Godfather Part II"
    studio = get_studio_by_name(db=db, studio_name="Paramount Pictures")
    assert studio is not None
    assert studio.id == studio_id
    series = get_series_by_name(db=db, series_name="The Godfather")
    assert series is not None
    assert series.id == series_id
    assert series_number == 2
    assert len(actors) == 4
