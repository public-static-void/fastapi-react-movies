#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Series routes tests.

Author        : Vadim Titov
Created       : Mi Okt 29 15:16:08 2024 +0200
Last modified : Mi Okt 29 15:19:08 2024 +0200
"""


from fastapi.testclient import TestClient

from movies_backend.main import app

client = TestClient(app)


def test_add_series() -> None:
    """Test adding a series."""
    response = client.post("/series", json={"name": "Star Wars"})
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "Star Wars"}
    response = client.post("/series", json={"name": "Star Wars"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "message": (
                "DuplicateEntryException('Series Star Wars already exists')"
            )
        }
    }


def test_delete_series() -> None:
    """Test deleting a series."""
    response = client.delete("/series/3")
    assert response.status_code == 200
    assert response.json() == {"message": "Series with ID 3 deleted"}
    response = client.delete("/series/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "InvalidIDException('Series ID 0 does not exist')"
        }
    }
    response = client.delete("/series/1")
    assert response.status_code == 412
    assert response.json() == {
        "detail": {
            "message": (
                "IntegrityConstraintException('Series Saw (ID 1)"
                " has movies assigned to it')"
            )
        }
    }


def test_get_all_series() -> None:
    """Test getting all series."""
    response = client.get("/series")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    assert {"id": 1, "name": "Saw"} in response.json()
