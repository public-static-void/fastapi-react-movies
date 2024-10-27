#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Studios endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:54:39 2024 +0200
Last modified : Di Okt 15 18:22:16 2024 +0200
"""

from typing import Dict, List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import (add_studio, delete_studio, get_all_studios, get_studio,
                    update_studio)
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException,
                          IntegrityConstraintException, InvalidIDException,
                          PathException)
from ..models import Studio
from ..schemas import HTTPExceptionSchema, MoviePropertySchema, StudioSchema
from ..util import rename_movie_file

logger = get_logger()
router = APIRouter(prefix="/studios")


@router.get(
    "",
    response_model=List[StudioSchema],
    response_description="A list of studios",
    summary="Get all studios",
    tags=["studios"],
)
def studios_get_all(db: Session = Depends(get_db_session)) -> List[Studio]:
    """
    Get all studios.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Studio]
        List of all studios
    """
    return get_all_studios(db=db)


@router.post(
    "",
    response_model=StudioSchema,
    response_description="The added studio",
    responses={
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Studio",
        }
    },
    summary="Add studio",
    tags=["studios"],
)
def studios_add(
    body: MoviePropertySchema, db: Session = Depends(get_db_session)
) -> Studio:
    """
    Add a studio to the database.

    Parameters
    ----------
    body : MoviePropertySchema
        The studio data.
    db : Session
        Database session

    Returns
    -------
    Studio
        The studio, if it was added
    """
    try:
        studio_name = body.name.strip()
        studio = add_studio(db=db, name=studio_name)
        logger.debug("Added studio %s", studio_name)
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": (repr(e))},
        ) from e
    return studio


@router.put(
    "/{studio_id}",
    response_model=StudioSchema,
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Studio",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path Error",
        },
    },
    summary="Update studio",
    tags=["studios"],
)
def studios_update(
    studio_id: int,
    body: MoviePropertySchema,
    db: Session = Depends(get_db_session),
) -> Studio:
    """
    Update a studio.

    Parameters
    ----------
    studio_id : int
        The studio ID.
    body : MoviePropertySchema
        The studio data.
    db : Session
        Database session

    Returns
    -------
    Studio
        The updated studio
    """
    try:
        studio = get_studio(db=db, studio_id=studio_id)
        if studio is not None:
            studio_name = studio.name
        else:
            studio_name = ""
        new_studio_name = body.name.strip()
        studio = update_studio(
            db=db, studio_id=studio_id, studio_name=new_studio_name
        )
        for movie in studio.movies:
            rename_movie_file(movie=movie, studio_current=studio_name)
            db.commit()
        logger.debug("Updated studio %s -> %s", studio_name, new_studio_name)
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
    return studio


@router.delete(
    "/{studio_id}",
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
    summary="Delete studio",
    tags=["studios"],
)
def studios_delete(
    studio_id: int, db: Session = Depends(get_db_session)
) -> Dict[str, str]:
    """
    Delete a studio.

    Parameters
    ----------
    studio_id : int
        The studio ID.
    db : Session
        Database session

    Returns
    -------
    Dict[str, str]
        Success message
    """
    try:
        studio_name = delete_studio(db=db, studio_id=studio_id)
        logger.debug("Deleted studio %s", studio_name)
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
    return {"message": f"Studio with ID {studio_id} deleted"}
