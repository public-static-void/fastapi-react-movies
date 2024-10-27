#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Data Schemas.

Author        : Vadim Titov
Created       : Mo Sep 23 17:50:06 2024 +0200
Last modified : Mi Okt 16 17:02:17 2024 +0200
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BaseMovieSchema(BaseModel):
    """
    Base schema for movie data.

    Attributes
    ----------
    id : int
        ID
    filename : str
        Filename
    """

    id: int
    filename: str
    model_config = ConfigDict(from_attributes=True)


class BasePropertySchema(BaseModel):
    """
    Base schema for movie data.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class MovieData(BaseModel):
    """
    Base schema for movie data.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class MovieUpdateSchema(BaseModel):
    """
    Schema for updating a movie.

    Attributes
    ----------
    name : str
        Name
    series_id : int
        Series ID
    series_number : int
        Series number
    studio_id : int
        Studio ID
    """

    name: Optional[str] = None
    series_id: Optional[int] = None
    series_number: Optional[int] = None
    studio_id: Optional[int] = None


class MoviePropertySchema(BaseModel):
    """
    Movie property schema.

    Attributes
    ----------
    name : str
        Name
    """

    name: str


class ActorSchema(MovieData):
    """
    Actor schema.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    # pylint: disable=unnecessary-ellipsis
    ...


class CategorySchema(MovieData):
    """
    Category schema.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    # pylint: disable=unnecessary-ellipsis
    ...


class SeriesSchema(MovieData):
    """
    Series schema.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    # pylint: disable=unnecessary-ellipsis
    ...


class StudioSchema(MovieData):
    """
    Studio schema.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    # pylint: disable=unnecessary-ellipsis
    ...


class MovieFileSchema(BaseMovieSchema):
    """
    Movie file schema.

    Attributes
    ----------
    id : int
        ID
    name : str
        Name
    """

    # pylint: disable=unnecessary-ellipsis
    ...


class MovieSchema(BaseMovieSchema):
    """
    Movie schema.

    Attributes
    ----------
    name : Optional[str] defaults to None
        Name of the movie
    actors : Optional[List[ActorSchema]] defaults to None
        List of actors
    categories : Optional[List[Category]] defaults to None
        List of categories
    series : Optional[Series] defaults to None
        Series
    series_number : Optional[int] defaults to None
        Series number
    studio : Optional[Studio] defaults to None
        Studio
    """

    name: Optional[str] = None
    actors: Optional[List[ActorSchema]] = None
    categories: Optional[List[CategorySchema]] = None
    series: Optional[SeriesSchema] = None
    series_number: Optional[int] = None
    studio: Optional[StudioSchema] = None
    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    """
    HTTP exception model.

    Attributes
    ----------
    message : str
        Message
    """

    message: str


class HTTPExceptionSchema(BaseModel):
    """
    HTTP exception schema.

    Attributes
    ----------
    detail : MessageSchema
        Detail
    """

    detail: MessageSchema
