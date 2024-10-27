#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Categories endpoints.

Author        : Vadim Titov
Created       : Di Okt 15 17:54:39 2024 +0200
Last modified : Di Okt 15 18:12:22 2024 +0200
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..config import get_logger
from ..crud import (add_category, delete_category, get_all_categories,
                    get_category, update_category)
from ..database import get_db_session
from ..exceptions import (DuplicateEntryException,
                          IntegrityConstraintException, InvalidIDException,
                          PathException)
from ..models import Category, Movie
from ..schemas import (CategorySchema, HTTPExceptionSchema, MessageSchema,
                       MoviePropertySchema)
from ..util import update_category_link

logger = get_logger()
router = APIRouter(prefix="/categories")


@router.get(
    "",
    response_model=List[CategorySchema],
    response_description="List of all categories",
    summary="Get all categories",
    tags=["categories"],
)
def categories_get_all(
    db: Session = Depends(get_db_session),
) -> List[Category]:
    """
    Get all categories.

    Parameters
    ----------
    db : Session
        Database session

    Returns
    -------
    List[Category]
        List of all categories
    """
    return get_all_categories(db=db)


@router.post(
    "",
    response_model=CategorySchema,
    response_description="The created category",
    responses={
        409: {
            "model": HTTPExceptionSchema,
            "description": "Duplicate Category",
        }
    },
    summary="Add category",
    tags=["categories"],
)
def categories_add(
    body: MoviePropertySchema, db: Session = Depends(get_db_session)
) -> Category:
    """
    Add a category to the database.

    Parameters
    ----------
    body : MoviePropertySchema
        The category data.
    db : Session
        Database session

    Returns
    -------
    Category
        The category, if it was added
    """
    try:
        category_name = body.name.strip()
        category = add_category(db=db, name=category_name)
        logger.debug("Added category %s", category_name)
    except DuplicateEntryException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": (repr(e))},
        ) from e
    return category


@router.put(
    "/{category_id}",
    response_model=CategorySchema,
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
            "description": "Path Error",
        },
    },
    summary="Update category",
    tags=["categories"],
)
def categories_update(
    category_id: int,
    body: MoviePropertySchema,
    db: Session = Depends(get_db_session),
) -> Category:
    """
    Update a category.

    Parameters
    ----------
    category_id : int
        The category ID.
    body : MoviePropertySchema
        The category data.
    db : Session
        Database session

    Returns
    -------
    Category
        The updated category
    """
    try:
        category: Optional[Category] = get_category(
            db=db, category_id=category_id
        )
        if category is not None:
            category_name = category.name
        else:
            category_name = ""
        new_category_name = body.name.strip()
        category = update_category(
            db=db, category_id=category_id, category_name=new_category_name
        )
        movie: Movie
        for movie in category.movies:
            update_category_link(
                filename=movie.filename,
                category_name=category_name,
                selected=False,
            )
            update_category_link(
                filename=movie.filename,
                category_name=new_category_name,
                selected=True,
            )
        logger.debug(
            "Renamed category %s -> %s", category_name, new_category_name
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
            detail={"message": repr(e)},
        ) from e
    return category


@router.delete(
    "/{category_id}",
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
    summary="Delete category",
    tags=["categories"],
)
def categories_delete(
    category_id: int, db: Session = Depends(get_db_session)
) -> Dict[str, str]:
    """
    Delete a category.

    Parameters
    ----------
    category_id : int
        The category ID.
    db : Session
        Database session

    Returns
    -------
    Dict[str, str]
        A message
    """
    try:
        category_name = delete_category(db=db, category_id=category_id)
        logger.debug("Deleted category %s", category_name)
    except IntegrityConstraintException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={"message": (repr(e))},
        ) from e
    except InvalidIDException as e:
        logger.warning(repr(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": (repr(e))},
        ) from e
    return {"message": f"Category {category_id} deleted"}
