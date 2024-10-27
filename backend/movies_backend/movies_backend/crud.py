#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : CRUD functionality.

Author        : Vadim Titov
Created       : Mo Sep 23 17:31:46 2024 +0200
Last modified : Do Okt 03 15:33:07 2024 +0200
"""

from typing import List, Optional, Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .exceptions import (DuplicateEntryException, IntegrityConstraintException,
                         InvalidIDException)
from .models import Actor, Category, Movie, Series, Studio
from .schemas import MovieUpdateSchema
from .util import (generate_sort_name, parse_filename, remove_movie,
                   rename_movie_file, update_actor_link, update_category_link,
                   update_series_link, update_studio_link)


def add_actor(
    db: Session,
    name: str,
) -> Actor:
    """
    Add an actor to the database.

    Parameters
    ----------
    db : Session
        Database session
    name : str
        Name of the actor

    Returns
    -------
    Actor
        The actor, if it was added
    """
    actor = Actor(name=name)
    try:
        db.add(actor)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"Actor {name} already exists") from e
    return actor


def add_category(
    db: Session,
    name: str,
) -> Category:
    """
    Add a category to the database.

    Parameters
    ----------
    db : Session
        Database session
    name : str
        Name of the category

    Returns
    -------
    Category
        The category, if it was added
    """
    category = Category(name=name)
    try:
        db.add(category)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"Category {name} already exists") from e
    return category


# pylint: disable=too-many-arguments
def add_movie(
    db: Session,
    filename: str,
    name: str,
    studio_id: Optional[int] = None,
    series_id: Optional[int] = None,
    series_number: Optional[int] = None,
    actors: Optional[List[Actor]] = None,
    categories: Optional[List[Category]] = None,
    processed: Optional[bool] = False,
) -> Movie:
    """
    Add a movie to the database.

    Parameters
    ----------
    db : Session
        Database session
    filename : str
        Name of the file
    name : str
        Name of the movie
    studio_id : Optional[int]
        Studio ID
    series_id : Optional[int]
        Series ID
    series_number : Optional[int]
        Series number
    actors : Optional[List[Actor]]
        Actors
    categories : Optional[List[Category]]
        Categories
    processed : Optional[bool] defaults to False
        Whether the movie has been processed

    Returns
    -------
    Movie
        The added movie, or None if the movie could not be added.
    """
    movie = Movie(
        filename=filename,
        name=name,
        sort_name=generate_sort_name(name),
        studio_id=studio_id,
        series_id=series_id,
        series_number=series_number,
        processed=processed,
    )
    if actors is not None:
        movie.actors = actors
    if categories is not None:
        movie.categories = categories
    try:
        db.add(movie)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"Movie {name} already exists") from e
    return movie


def add_series(
    db: Session,
    name: str,
) -> Series:
    """
    Add a series to the database.

    Parameters
    ----------
    db : Session
        Database session
    name : str
        Name of the series

    Returns
    -------
    Series
        The series, if it was added
    """
    series = Series(name=name, sort_name=generate_sort_name(name=name))
    try:
        db.add(series)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"Series {name} already exists") from e
    return series


def add_studio(
    db: Session,
    name: str,
) -> Studio:
    """
    Add a studio to the database.

    Parameters
    ----------
    db : Session
        Database session
    name : str
        Name of the studio

    Returns
    -------
    Studio
        The studio, if it was added
    """
    studio = Studio(name=name, sort_name=generate_sort_name(name=name))
    try:
        db.add(studio)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(f"Studio {name} already exists") from e
    return studio


def add_movie_category(
    db: Session, movie_id: int, category_id: int
) -> Tuple[Movie, Category]:
    """
    Add movie category.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    category_id : int
        The category ID.
    db : Session
        Database session

    Returns
    -------
    Tuple[Movie, Category]
        The updated movie and category
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    category = get_category(db=db, category_id=category_id)
    if category is None:
        raise InvalidIDException(f"Category ID {category_id} does not exist")
    movie_category: Category
    for movie_category in movie.categories:
        if category_id == movie_category.id:
            raise DuplicateEntryException(
                f"Category {category.name} (ID {category.id}) is already in"
                f" movie {movie.name} (ID {movie.id})"
            )
    movie.categories.append(category)
    db.commit()
    update_category_link(
        filename=movie.filename, category_name=category.name, selected=True
    )
    db.commit()
    return movie, category


def add_movie_actor(
    db: Session, movie_id: int, actor_id: int
) -> Tuple[Movie, Actor]:
    """
    Add movie actor.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    actor_id : int
        The actor ID.
    db : Session
        Database session

    Returns
    -------
    Tuple[Movie, Actor]
        The updated movie and actor
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    actor = get_actor(db=db, actor_id=actor_id)
    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")
    movie_actor: Actor
    for movie_actor in movie.actors:
        if actor_id == movie_actor.id:
            raise DuplicateEntryException(
                f"Actor {actor.name} (ID {actor.id}) is already in movie"
                f" {movie.name} (ID {movie.id})"
            )
    movie.actors.append(actor)
    db.commit()
    rename_movie_file(movie)
    update_actor_link(
        filename=movie.filename, actor_name=actor.name, selected=True
    )
    db.commit()
    return movie, actor


def get_all_actors(db: Session) -> List[Actor]:
    """
    Get all actors from the database.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Actor]
        List of all actors
    """
    return db.query(Actor).order_by(Actor.name).all()


def get_actor(db: Session, actor_id: int) -> Actor | None:
    """
    Get actor.

    Parameters
    ----------
    db : Session
        Database session
    actor_id : int
        The actor ID.

    Returns
    -------
    Actor | None
        The actor or None if it does not exist
    """
    return db.query(Actor).filter(Actor.id == actor_id).first()


def get_actor_by_name(db: Session, actor_name: str) -> Actor | None:
    """
    Get actor by name.

    Parameters
    ----------
    db : Session
        Database session
    actor_name : str
        The actor name

    Returns
    -------
    Actor | None
        The actor or None if it does not exist
    """
    return db.query(Actor).filter(Actor.name == actor_name).first()


def get_all_categories(db: Session) -> List[Category]:
    """
    Get all categories from the database.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Category]
        List of all categories
    """
    return db.query(Category).order_by(Category.name).all()


def get_category(db: Session, category_id: int) -> Category | None:
    """
    Get category.

    Parameters
    ----------
    db : Session
        Database session
    category_id : int
        The category ID.

    Returns
    -------
    Category | None
        The category or None if it does not exist
    """
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, category_name: str) -> Category | None:
    """
    Get category by name.

    Parameters
    ----------
    db : Session
        Database session
    category_name : str
        The category name

    Returns
    -------
    Category | None
        The category or None if it does not exist
    """
    return db.query(Category).filter(Category.name == category_name).first()


def get_all_movies(db: Session) -> List[Movie]:
    """
    Get all movies from the database.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Movie]
        List of all movies
    """
    return (
        db.query(Movie)
        .outerjoin(Studio)
        .outerjoin(Series)
        .order_by(
            Movie.processed,
            Studio.sort_name,
            Series.sort_name,
            Movie.sort_name,
        )
        .all()
    )


def get_movie(
    db: Session,
    movie_id: int,
) -> Movie | None:
    """
    Get movie.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    db : Session
        Database session

    Returns
    -------
    Movie | None
        The movie or None if it does not exist
    """
    return db.query(Movie).filter(Movie.id == movie_id).first()


def get_all_series(db: Session) -> List[Series]:
    """
    Get all series from the database.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Series]
        List of all series
    """
    return db.query(Series).order_by(Series.name).all()


def get_series(db: Session, series_id: int | None) -> Series | None:
    """
    Get series from the database.

    Parameters
    ----------
    db : Session
        Database session
    series_id : int | None
        The series ID

    Returns
    -------
    Series | None
        The series or None if it does not exist
    """
    return db.query(Series).filter(Series.id == series_id).first()


def get_series_by_name(db: Session, series_name: str) -> Series | None:
    """
    Get series by name.

    Parameters
    ----------
    db : Session
        Database session
    series_name : str
        The series name

    Returns
    -------
    Series | None
        The series or None if it does not exist
    """
    return db.query(Series).filter(Series.name == series_name).first()


def get_all_studios(db: Session) -> List[Studio]:
    """
    Get all studios from the database.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Studio]
        List of all studios
    """
    return db.query(Studio).order_by(Studio.name).all()


def get_studio(db: Session, studio_id: int | None) -> Studio | None:
    """
    Get studio from the database.

    Parameters
    ----------
    db : Session
        Database session
    studio_id : int | None
        The studio ID

    Returns
    -------
    Studio | None
        The studio or None if it does not exist
    """
    return db.query(Studio).filter(Studio.id == studio_id).first()


def get_studio_by_name(db: Session, studio_name: str) -> Studio | None:
    """
    Get studio by name.

    Parameters
    ----------
    db : Session
        Database session
    studio_name : str
        The studio name

    Returns
    -------
    Studio | None
        The studio or None if it does not exist
    """
    return db.query(Studio).filter(Studio.name == studio_name).first()


def update_actor(db: Session, actor_id: int, actor_name: str) -> Actor:
    """
    Update actor.

    Parameters
    ----------
    db : Session
        Database session
    actor_id : int
        The actor ID
    actor_name : str
        The new name

    Returns
    -------
    Actor
        The updated actor
    """
    actor = get_actor(db=db, actor_id=actor_id)
    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")
    actor_name_old = actor.name
    actor.name = actor_name
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(
            f"Renaming actor {actor_name_old} -> {actor_name} conflicts with"
            " existing"
        ) from e
    return actor


def update_category(
    db: Session, category_id: int, category_name: str
) -> Category:
    """
    Update category.

    Parameters
    ----------
    db : Session
        Database session
    category_id : int
        The category ID
    category_name : str
        The new name

    Returns
    -------
    Category
        The updated category
    """
    category = get_category(db=db, category_id=category_id)
    if category is None:
        raise InvalidIDException(f"Category ID {category_id} does not exist")
    category_name_old = category.name
    category.name = category_name
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(
            f"Renaming category {category_name_old} ->"
            f" {category_name} conflicts with existing"
        ) from e
    return category


def update_series(db: Session, series_id: int, series_name: str) -> Series:
    """
    Update series.

    Parameters
    ----------
    db : Session
        Database session
    series_id : int
        The series ID
    series_name : str
        The new name

    Returns
    -------
    Series
        The updated series
    """
    series = get_series(db=db, series_id=series_id)
    if series is None:
        raise InvalidIDException(f"Series ID {series_id} does not exist")
    series_name_old = series.name
    series.name = series_name
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(
            f"Renaming series {series_name_old} -> {series_name} conflicts"
            " with existing"
        ) from e
    return series


def update_studio(db: Session, studio_id: int, studio_name: str) -> Studio:
    """
    Update studio.

    Parameters
    ----------
    db : Session
        Database session
    studio_id : int
        The studio ID
    studio_name : str
        The new name

    Returns
    -------
    Studio
        The updated studio
    """
    studio = get_studio(db=db, studio_id=studio_id)
    if studio is None:
        raise InvalidIDException(f"Studio ID {studio_id} does not exist")
    studio_name_old = studio.name
    studio.name = studio_name
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise DuplicateEntryException(
            f"Renaming studio {studio_name_old} -> {studio_name} conflicts"
            " with existing"
        ) from e
    return studio


def update_movie(db: Session, movie_id: int, data: MovieUpdateSchema) -> Movie:
    """
    Update movie.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    data : MovieUpdateSchema
        The new data
    db : Session
        Database session

    Returns
    -------
    Movie
        The updated movie
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    movie.processed = True
    if (
        data.name == movie.name
        and data.series_id == movie.series_id
        and data.series_number == movie.series_number
        and data.studio_id == movie.studio_id
    ):
        db.commit()
        return movie
    if movie.name != data.name:
        movie.sort_name = generate_sort_name(name=data.name)
    series = get_series(db=db, series_id=movie.series_id)
    series_current = series.name if series is not None else None
    studio = get_studio(db=db, studio_id=movie.studio_id)
    studio_current = studio.name if studio is not None else None
    if movie.series_id != data.series_id and data.series_id is None:
        update_series_link(
            filename=movie.filename, series_name=series_current, selected=False
        )
    if movie.studio_id != data.studio_id and data.studio_id is None:
        update_studio_link(
            filename=movie.filename, studio_name=studio_current, selected=False
        )
    movie.name = data.name
    movie.studio_id = data.studio_id
    movie.series_id = data.series_id
    movie.series_number = data.series_number
    rename_movie_file(
        movie=movie,
        series_current=series_current,
        studio_current=studio_current,
    )
    db.commit()
    return movie


def delete_movie(db: Session, movie_id: int) -> str:
    """
    Delete a movie.

    Parameters
    ----------
    db : Session
        Database session
    movie_id : int
        The movie ID

    Returns
    -------
    str
        The movie name
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    remove_movie(movie=movie)
    db.delete(movie)
    db.commit()
    if movie.name is not None:
        movie_name = movie.name
    else:
        movie_name = ""
    return movie_name


def delete_movie_category(
    db: Session, movie_id: int, category_id: int
) -> Tuple[Movie, Category]:
    """
    Delete movie category.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    category_id : int
        The category ID.
    db : Session
        Database session

    Returns
    -------
    Tuple[Movie, Category]
        The updated movie and category
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    category = get_category(db=db, category_id=category_id)
    if category is None:
        raise InvalidIDException(f"Category ID {category_id} does not exist")
    try:
        movie.categories.remove(category)
    except ValueError as e:
        raise InvalidIDException(
            f"Movie {movie.name} (ID {movie_id}) does not have category"
            f" {category.name} (ID {category_id})"
        ) from e
    update_category_link(
        filename=movie.filename, category_name=category.name, selected=False
    )
    db.commit()
    return movie, category


def delete_movie_actor(
    db: Session, movie_id: int, actor_id: int
) -> Tuple[Movie, Actor]:
    """
    Delete movie actor.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    actor_id : int
        The actor ID.
    db : Session
        Database session

    Returns
    -------
    Tuple[Movie, Actor]
        The updated movie and actor
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        raise InvalidIDException(f"Movie ID {movie_id} does not exist")
    actor = get_actor(db=db, actor_id=actor_id)
    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")
    try:
        movie.actors.remove(actor)
    except ValueError as e:
        raise InvalidIDException(
            f"Actor {actor.name} (ID {actor.id}) is not in movie"
            f" {movie.name} (ID {movie.id})"
        ) from e
    update_actor_link(
        filename=movie.filename, actor_name=actor.name, selected=False
    )
    rename_movie_file(movie)
    db.commit()
    return movie, actor


def delete_actor(actor_id: int, db: Session) -> str:
    """
    Delete an actor.

    Parameters
    ----------
    actor_id : int
        The actor ID
    db : Session
        Database session

    Returns
    -------
    str
        The actor name
    """
    actor = get_actor(db=db, actor_id=actor_id)
    if actor is None:
        raise InvalidIDException(f"Actor ID {actor_id} does not exist")
    try:
        db.delete(actor)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityConstraintException(
            f"Actor {actor.name} (ID {actor.id}) has movies assigned to it"
        ) from e
    return actor.name


def delete_category(category_id: int, db: Session) -> str:
    """
    Delete a category.

    Parameters
    ----------
    category_id : int
        The category ID
    db : Session
        Database session

    Returns
    -------
    str
        The category name
    """
    category = get_category(db=db, category_id=category_id)
    if category is None:
        raise InvalidIDException(f"Category ID {category_id} does not exist")
    try:
        db.delete(category)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityConstraintException(
            f"Category {category.name} ({category.id}) has movies assigned"
            " to it"
        ) from e
    return category.name


def delete_series(series_id: int, db: Session) -> str:
    """
    Delete a series.

    Parameters
    ----------
    series_id : int
        The series ID
    db : Session
        Database session

    Returns
    -------
    str
        The series name
    """
    series = get_series(db=db, series_id=series_id)
    if series is None:
        raise InvalidIDException(f"Series ID {series_id} does not exist")
    try:
        db.delete(series)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityConstraintException(
            f"Series {series.name} (ID {series.id}) has movies assigned to it"
        ) from e
    if series.name is not None:
        series_name = series.name
    else:
        series_name = ""
    return series_name


def delete_studio(studio_id: int, db: Session) -> str:
    """
    Delete a studio.

    Parameters
    ----------
    studio_id : int
        The studio ID
    db : Session
        Database session

    Returns
    -------
    str
        The studio name
    """
    studio = get_studio(db=db, studio_id=studio_id)
    if studio is None:
        raise InvalidIDException(f"Studio ID {studio_id} does not exist")
    try:
        db.delete(studio)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise IntegrityConstraintException(
            f"Studio {studio.name} (ID {studio.id}) has movies assigned to it"
        ) from e
    if studio.name is not None:
        studio_name = studio.name
    else:
        studio_name = ""
    return studio_name


# pylint: disable=too-many-locals
def parse_file_info(
    db: Session, filename: str
) -> Tuple[str, Optional[int], Optional[int], Optional[int], List[Actor]]:
    """
    Parse a filename.

    Parameters
    ----------
    db : Session
        Database session
    filename : str
        The filename

    Returns
    -------
    Tuple[str, Optional[int], Optional[int], Optional[int], List[Actors]]
        Movie name, studio id, series id, series number, actors
    """
    studio_id: Optional[int] = None
    series_id: Optional[int] = None
    series_number: Optional[int] = None
    actors: List[Actor] = []

    series_number_str: Optional[str] = None

    name, studio_name, series_name, series_number_str, actor_names = (
        parse_filename(filename=filename)
    )

    if studio_name is not None:
        studio = get_studio_by_name(db=db, studio_name=studio_name)
        if studio is not None:
            studio_id = studio.id

    if series_name is not None:
        series = get_series_by_name(db=db, series_name=series_name)
        if series is not None:
            series_id = series.id

    if series_number_str is not None:
        series_number = int(series_number_str)

    if actor_names is not None:
        actors = [
            actor
            for actor in (
                get_actor_by_name(db=db, actor_name=actor_name)
                for actor_name in actor_names.split(", ")
            )
            if actor is not None
        ]

    return (name, studio_id, series_id, series_number, actors)
