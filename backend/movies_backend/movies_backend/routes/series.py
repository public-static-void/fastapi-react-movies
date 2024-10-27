#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Series endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:54:39 2024 +0200
Last modified : Di Okt 15 18:20:05 2024 +0200
"""

from typing import Dict, List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import (add_series, delete_series, get_all_series, get_series,
                    update_series)
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException,
                          IntegrityConstraintException, InvalidIDException,
                          PathException)
from ..models import Series
from ..schemas import (HTTPExceptionSchema, MessageSchema, MoviePropertySchema,
                       SeriesSchema)
from ..util import rename_movie_file

logger = get_logger()
router = APIRouter(prefix="/series")


@router.get(
    "",
    response_model=List[SeriesSchema],
    response_description="A list of series",
    summary="Get all series",
    tags=["series"],
)
def series_get_all(db: Session = Depends(get_db_session)) -> List[Series]:
    """
    Get all series.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Series]
        List of all series
    """
    return get_all_series(db=db)


@router.post(
    "",
    response_model=SeriesSchema,
    response_description="The created series",
    responses={
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Series",
        }
    },
    summary="Add series",
    tags=["series"],
)
def series_add(
    body: MoviePropertySchema, db: Session = Depends(get_db_session)
) -> Series:
    """
    Add a series to the database.

    Parameters
    ----------
    body : MoviePropertySchema
        The series data.
    db : Session
        Database session

    Returns
    -------
    Series
        The series, if it was added
    """
    try:
        series_name = body.name.strip()
        series = add_series(db=db, name=series_name)
        logger.debug("Added series %s", series_name)
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": (repr(e))},
        ) from e
    return series


@router.put(
    "/{series_id}",
    response_model=SeriesSchema,
    response_description="The updated series",
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Series",
        },
        500: {
            "model": HTTPExceptionSchema,
            "description": "Path Error",
        },
    },
    summary="Rename series",
    tags=["series"],
)
def series_update(
    series_id: int,
    body: MoviePropertySchema,
    db: Session = Depends(get_db_session),
) -> Series:
    """
    Update a series.

    Parameters
    ----------
    series_id : int
        The series ID.
    body : MoviePropertySchema
        The series data.
    db : Session
        Database session

    Returns
    -------
    Series
        The updated series
    """
    try:
        series = get_series(db=db, series_id=series_id)
        if series is not None:
            series_name = series.name
        else:
            series_name = ""
        new_series_name = body.name.strip()
        series = update_series(
            db=db, series_id=series_id, series_name=new_series_name
        )
        for movie in series.movies:
            rename_movie_file(movie=movie, series_current=series_name)
            db.commit()
        logger.debug("Updated series %s -> %s", series_name, new_series_name)
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
    return series


@router.delete(
    "/{series_id}",
    response_model=MessageSchema,
    responses={
        404: {
            "model": HTTPExceptionSchema,
            "description": "Invalid ID",
        },
        412: {
            "model": HTTPExceptionSchema,
            "description": "Precondition failed",
        },
    },
    summary="Delete series",
    tags=["series"],
)
def series_delete(
    series_id: int, db: Session = Depends(get_db_session)
) -> Dict[str, str]:
    """
    Delete a series.

    Parameters
    ----------
    series_id : int
        The series ID.
    db : Session
        Database session

    Returns
    -------
    Dict[str, str]
        Success message
    """
    try:
        series_name = delete_series(db=db, series_id=series_id)
        logger.debug("Deleted series %s", series_name)
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
    return {"message": f"Series with ID {series_id} deleted"}
