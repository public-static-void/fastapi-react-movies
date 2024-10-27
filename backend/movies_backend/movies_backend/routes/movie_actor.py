#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Movie Actors endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:54:39 2024 +0200
Last modified : Di Okt 15 18:15:19 2024 +0200
"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import add_movie_actor, delete_movie_actor
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException, InvalidIDException,
                          PathException)
from ..models import Movie
from ..schemas import HTTPExceptionSchema, MovieSchema

logger = get_logger()
router = APIRouter(prefix="/movie_actor")


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
            "description": "Duplicate Actor",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path error",
        },
    },
    summary="Add actor to movie",
    tags=["movie_actor"],
)
def movie_actor_add(
    movie_id: int, actor_id: int, db: Session = Depends(get_db_session)
) -> Movie:
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
    Movie
        The updated movie
    """
    try:
        movie, actor = add_movie_actor(
            db=db, movie_id=movie_id, actor_id=actor_id
        )
        logger.debug("Added actor %s to movie %s", actor.name, movie.name)
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": repr(e)},
        ) from e
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
    summary="Remove actor from movie",
    tags=["movie_actor"],
)
def movie_actor_delete(
    movie_id: int, actor_id: int, db: Session = Depends(get_db_session)
) -> Movie:
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
    Movie
        The updated movie
    """
    try:
        movie, actor = delete_movie_actor(
            db=db, movie_id=movie_id, actor_id=actor_id
        )
        logger.debug("Removed actor %s from movie %s", actor.name, movie.name)
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
