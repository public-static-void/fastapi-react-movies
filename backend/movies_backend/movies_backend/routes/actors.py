#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Actors endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:54:39 2024 +0200
Last modified : Di Okt 15 18:06:58 2024 +0200
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import (add_actor, delete_actor, get_actor, get_all_actors,
                    update_actor)
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException,
                          IntegrityConstraintException, InvalidIDException,
                          PathException)
from ..models import Actor
from ..schemas import (ActorSchema, HTTPExceptionSchema, MessageSchema,
                       MoviePropertySchema)
from ..util import rename_movie_file

logger = get_logger()
router = APIRouter(prefix="/actors")


@router.post(
    "",
    response_model=ActorSchema,
    responses={
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Actor",
        }
    },
    summary="Add actor",
    tags=["actors"],
)
def actors_add(
    body: MoviePropertySchema, db: Session = Depends(get_db_session)
) -> Actor:
    """
    Add an actor to the database.

    Parameters
    ----------
    body : MoviePropertySchema
        The actor data.
    db : Session
        Database session

    Returns
    -------
    Actor
        The actor, if it was added
    """
    try:
        actor_name = body.name.strip()
        actor = add_actor(db=db, name=actor_name)
        logger.debug("Added new actor %s", actor_name)
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": repr(e)},
        ) from e
    return actor


@router.delete(
    "/{actor_id}",
    response_model=MessageSchema,
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        412: {
            "model": HTTPExceptionSchema,
            "description": "Integrity Constraint Failed",
        },
    },
    summary="Delete actor",
    tags=["actors"],
)
def actors_delete(
    actor_id: int, db: Session = Depends(get_db_session)
) -> Dict[str, str]:
    """
    Delete an actor.

    Parameters
    ----------
    actor_id : int
        The actor ID.
    db : Session
        Database session

    Returns
    -------
    Dict[str, str]
        Success message
    """
    try:
        name = delete_actor(db=db, actor_id=actor_id)
        logger.debug("Deleted actor %s", name)
    except IntegrityConstraintException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={"message": repr(e)},
        ) from e
    except InvalidIDException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": repr(e)},
        ) from e
    return {"message": f"Actor with ID {actor_id} deleted"}


@router.get(
    "",
    response_model=List[ActorSchema],
    response_description="A list of actors",
    summary="Get all actors",
    tags=["actors"],
)
def actors_get_all(db: Session = Depends(get_db_session)) -> List[Actor]:
    """
    Get all actors.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Actor]
        List of all actors
    """
    return get_all_actors(db=db)


@router.put(
    "/{actor_id}",
    response_model=ActorSchema,
    response_description="The updated actor",
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
    summary="Rename actor",
    tags=["actors"],
)
def actors_update(
    actor_id: int,
    body: MoviePropertySchema,
    db: Session = Depends(get_db_session),
) -> Actor:
    """
    Update an actor.

    Parameters
    ----------
    actor_id : int
        The actor ID.
    body : MoviePropertySchema
        The actor data.
    db : Session
        Database session

    Returns
    -------
    Actor
        The updated actor
    """
    try:
        actor: Optional[Actor] = get_actor(db=db, actor_id=actor_id)
        if actor is not None:
            actor_name = actor.name
        else:
            actor_name = ""
        new_actor_name = body.name.strip()
        actor = update_actor(
            db=db, actor_id=actor_id, actor_name=new_actor_name
        )
        for movie in actor.movies:
            rename_movie_file(movie=movie, actor_current=actor_name)
            db.commit()
        logger.debug("Renamed actor %s -> %s", actor_name, new_actor_name)
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
    return actor
