#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Movies endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:56:25 2024 +0200
Last modified : Di Okt 15 17:56:22 2024 +0200
"""

from typing import Dict, List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import (add_movie, delete_movie, get_all_movies, get_movie,
                    parse_file_info, update_movie)
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException, InvalidIDException,
                          ListFilesException, PathException)
from ..models import Movie
from ..schemas import (HTTPExceptionSchema, MessageSchema, MovieFileSchema,
                       MovieSchema, MovieUpdateSchema)
from ..util import PathType, get_movie_path, list_files, migrate_file

logger = get_logger()
router = APIRouter(prefix="/movies")


@router.get(
    "",
    response_model=List[MovieFileSchema],
    response_description="A list of movie IDs and filenames",
    summary="Get all movies",
    tags=["movies"],
)
def movies_get_all(db: Session = Depends(get_db_session)) -> List[Movie]:
    """
    Get all movies.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Movie]
        List of all movies
    """
    return get_all_movies(db=db)


@router.get(
    "/{movie_id}",
    response_model=MovieSchema,
    response_description="Movie data",
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        }
    },
    summary="Get movie by ID",
    tags=["movies"],
)
def movies_get_one(
    movie_id: int, db: Session = Depends(get_db_session)
) -> Movie:
    """
    Get movie by ID.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    db : Session
        Database session

    Returns
    -------
    Movie
        The movie
    """
    movie = get_movie(db=db, movie_id=movie_id)
    if movie is None:
        message = f"Movie with ID {movie_id} not found."
        logger.warning(message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": message},
        )
    return movie


@router.post(
    "",
    response_model=List[MovieSchema],
    response_description="List of imported movie filenames and IDs",
    responses={
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate entry",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path error",
        },
    },
    summary="Import movies from imports directory",
    tags=["movies"],
)
def movies_import(db: Session = Depends(get_db_session)) -> List[Movie]:
    """
    Import movies from the given directory.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Movie]
        The list of imported movies.
    """
    try:
        files = list_files(get_movie_path(PathType.IMPORT))
    except ListFilesException as e:
        logger.error(repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": repr(e)},
        ) from e
    movies = []
    for file in files:
        if file == ".keep":
            continue
        name, studio_id, series_id, series_number, actors = parse_file_info(
            db=db, filename=file
        )
        try:
            migrate_file(filename=file)
            movie = add_movie(
                db=db,
                filename=file,
                name=name,
                studio_id=studio_id,
                series_id=series_id,
                series_number=series_number,
                actors=actors,
            )
            movies.append(movie)
            logger.debug("Imported movie %s", movie.filename)
        except DuplicateEntryException as e:
            logger.warning(repr(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": repr(e)},
            ) from e
        except PathException as e:
            logger.error(repr(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": repr(e)},
            ) from e
    return movies


@router.put(
    "/{movie_id}",
    response_model=MovieSchema,
    response_description="Updated movie data",
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path error",
        },
    },
    summary="Update movie",
    tags=["movies"],
)
def movies_update(
    movie_id: int,
    body: MovieUpdateSchema,
    db: Session = Depends(get_db_session),
) -> Movie:
    """
    Update movie.

    Parameters
    ----------
    movie_id : int
        The movie ID.
    body : MovieUpdateSchema
        The movie data.
    db : Session
        Database session

    Returns
    -------
    Movie
        The updated movie, if it was updated
    """
    try:
        movie = update_movie(db=db, movie_id=movie_id, data=body)
        logger.debug("Updated movie %s", movie.filename)
    except InvalidIDException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": repr(e)},
        ) from e
    except PathException as e:
        logger.error(repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": repr(e)},
        ) from e
    return movie


@router.delete(
    "/{movie_id}",
    response_model=MessageSchema,
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path error",
        },
    },
    summary="Delete movie and move file back to imports folder",
    tags=["movies"],
)
def movies_delete(
    movie_id: int,
    db: Session = Depends(get_db_session),
) -> Dict[str, str]:
    """
    Delete movie.

    Parameters
    ----------
    db : Session
        Database session
    movie_id : int
        The movie ID

    Returns
    -------
    Dict[str, str]
        A success message
    """
    try:
        movie_name = delete_movie(db=db, movie_id=movie_id)
        logger.debug("Deleted movie %s", movie_name)
    except InvalidIDException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail={"message": str(e)}
        ) from e
    except PathException as e:
        logger.error(repr(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e)}
        ) from e
    return {"message": f"Deleted movie with ID {movie_id}"}
