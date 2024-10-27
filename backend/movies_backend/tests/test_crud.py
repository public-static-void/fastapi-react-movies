#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : CRUD functionality tests.

Author        : Vadim Titov
Created       : Mi Okt 16 16:44:51 2024 +0200
Last modified : Mi Okt 16 18:13:08 2024 +0200
"""

import sqlite3
from pathlib import Path
from typing import Generator

import pytest
from pytest import FixtureRequest, TempPathFactory
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from movies_backend.crud import add_actor, get_actor, get_actor_by_name
from movies_backend.database import get_db_session, init_db
from movies_backend.exceptions import DuplicateEntryException


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
    actor2 = get_actor(db, actor1.id)
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
    actor = get_actor(db, 20)
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
    actor = get_actor_by_name(db, "")
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
