#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Database module.

Author        : Vadim Titov
Created       : Mo Sep 23 16:20:14 2024 +0200
Last modified : Di Okt 15 17:30:44 2024 +0200
"""

from sqlite3 import Connection as SQLite3Connection
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_sqlite_path
from .models import TableBase

__FACTORY = None


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session.

    Yields
    ------
    Session
        The database session.
    """
    if __FACTORY is None:
        raise RuntimeError("Must call init_db first!")
    with __FACTORY() as db:
        yield db


def init_db() -> None:
    """Init database."""
    global __FACTORY
    engine = create_engine(
        f"sqlite:///{get_sqlite_path()}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    __FACTORY = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    TableBase.metadata.create_all(bind=engine)
