#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Movie Category endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:56:31 2024 +0200
Last modified : Di Okt 15 18:16:54 2024 +0200
"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import add_movie_category, delete_movie_category
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException, InvalidIDException,
                          PathException)
from ..models import Movie
from ..schemas import HTTPExceptionSchema, MovieSchema

logger = get_logger()
router = APIRouter(prefix="/movie_category")


@router.post(
    "",
    response_model=MovieSchema,
    response_description="The updated movie",
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Category",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path error",
        },
    },
    summary="Add category to movie",
    tags=["movie_category"],
)
def movie_category_add(
    movie_id: int, category_id: int, db: Session = Depends(get_db_session)
) -> Movie:
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
    Movie
        The updated movie, if it was updated
    """
    try:
        movie, category = add_movie_category(
            db=db, movie_id=movie_id, category_id=category_id
        )
        logger.debug(
            "Added category %s to movie %s", category.name, movie.name
        )
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": (repr(e))},
        ) from e
    except InvalidIDException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": (repr(e))},
        ) from e
    except PathException as e:
        logger.error(repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": (repr(e))},
        ) from e
    return movie


@router.delete(
    "",
    response_model=MovieSchema,
    response_description="The updated movie",
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
    summary="Delete movie category",
    tags=["movie_category"],
)
def movie_category_delete(
    movie_id: int, category_id: int, db: Session = Depends(get_db_session)
) -> Movie:
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
    Movie
        The deleted movie, if it was deleted
    """
    try:
        movie, category = delete_movie_category(
            db=db, movie_id=movie_id, category_id=category_id
        )
        logger.debug(
            "Deleted category %s from movie %s", category.name, movie.name
        )
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
