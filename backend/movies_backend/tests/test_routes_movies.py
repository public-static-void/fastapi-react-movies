#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Movies routes tests.

Author        : Vadim Titov
Created       : Mi Okt 29 15:24:53 2024 +0200
Last modified : Mi Okt 29 15:45:31 2024 +0200
"""


from fastapi.testclient import TestClient

from movies_backend.main import app

client = TestClient(app)


def test_get_all_movies():
    """Test get all movies"""
    response = client.get("/movies")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 13
    assert {"id": 13, "filename": "lotr.mp4"} in response.json()


def test_get_movie() -> None:
    """Test getting a movie."""
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Casino",
        "series": None,
        "series_number": None,
        "studio": {"id": 3, "name": "Universal Pictures"},
        "actors": [
            {"id": 10, "name": "Joe Pesci"},
            {"id": 8, "name": "Robert De Niro"},
            {"id": 14, "name": "Sharon Stone"},
        ],
        "categories": [{"id": 1, "name": "Crime"}, {"id": 3, "name": "Drama"}],
        "filename": (
            "[Universal Pictures] Casino (Joe Pesci, Robert De Niro, Sharon"
            " Stone).mp4"
        ),
    }
    response = client.get("/movies/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {"message": "Movie with ID 0 not found."}
    }
