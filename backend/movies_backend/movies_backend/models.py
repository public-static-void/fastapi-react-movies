#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Data Models.

Author        : Vadim Titov
Created       : Mo Sep 23 14:40:13 2024 +0200
Last modified : Di Okt 15 17:37:42 2024 +0200
"""

from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# pylint: disable=too-few-public-methods
class TableBase(DeclarativeBase):
    """Base class for the models."""

    # pylint: disable=unnecessary-ellipsis
    ...


movie_actors = Table(
    "movie_actors",
    TableBase.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
)

movie_categories = Table(
    "movie_categories",
    TableBase.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


# pylint: disable=too-few-public-methods
class Actor(TableBase):
    """
    Actor model.

    Attributes
    ----------
    __tablename__ : str
        Name of the table
    id : int
        ID
    name : str
        Name
    movies : List[Movie]
        List of movies
    """

    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    movies = relationship(
        "Movie",
        secondary=movie_actors,
        back_populates="actors",
        order_by="Movie.sort_name",
        passive_deletes="all",
    )


# pylint: disable=too-few-public-methods
class Category(TableBase):
    """
    Category model.

    Attributes
    ----------
    __tablename__ : str
        Name of the table
    id : int
        ID
    name : str
        Name
    movies : List[Movie]
        List of movies
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    movies = relationship(
        "Movie",
        secondary=movie_categories,
        back_populates="categories",
        order_by="Movie.sort_name",
        passive_deletes="all",
    )


# pylint: disable=too-few-public-methods
class Series(TableBase):
    """
    Series model.

    Attributes
    ----------
    __tablename__ : str
        Name of the table
    id : int
        ID
    name : str | None
        Name
    sort_name : str | None
        Sort name
    movies : List[Movie]
        List of movies
    """

    __tablename__ = "series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=False, unique=True
    )
    sort_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=False, unique=True
    )

    movies = relationship(
        "Movie",
        back_populates="series",
        order_by="Movie.sort_name",
        passive_deletes="all",
    )


# pylint: disable=too-few-public-methods
class Studio(TableBase):
    """
    Studio model.

    Attributes
    ----------
    __tablename__ : str
        Name of the table
    id : int
        ID
    name : str | None
        Name
    sort_name : str | None
        Sort name
    movies : List[Movie]
        List of movies
    """

    __tablename__ = "studios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=False, unique=True
    )
    sort_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=False, unique=True
    )

    movies = relationship(
        "Movie",
        back_populates="studio",
        order_by="Movie.sort_name",
        passive_deletes="all",
    )


# pylint: disable=too-few-public-methods
class Movie(TableBase):
    """
    Movie model.

    Attributes
    ----------
    __tablename__ : str
        Name of the table
    id : int
        ID
    filename : str
        Filename
    name : str | None
        Name
    sort_name : str | None
        Sort name
    series_id : int
        Series ID
    series_number : int
        Series number
    studio_id : int
        Studio ID
    processed : bool
        Whether the movie has been processed
    """

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sort_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    series_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("series.id"), nullable=True
    )
    series_number: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    studio_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("studios.id"), nullable=True
    )
    processed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    actors = relationship(
        "Actor",
        secondary=movie_actors,
        back_populates="movies",
        order_by="Actor.name",
    )

    categories = relationship(
        "Category",
        secondary=movie_categories,
        back_populates="movies",
        order_by="Category.name",
    )

    series = relationship(
        "Series",
        back_populates="movies",
        uselist=False,
    )

    studio = relationship(
        "Studio",
        back_populates="movies",
        uselist=False,
    )
