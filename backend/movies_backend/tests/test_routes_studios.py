#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Studios routes tests.

Author        : Vadim Titov
Created       : Mi Okt 29 15:20:15 2024 +0200
Last modified : Mi Okt 29 15:23:49 2024 +0200
"""


from fastapi.testclient import TestClient

from movies_backend.main import app

client = TestClient(app)


def test_add_studio() -> None:
    """Test adding a studios."""
    response = client.post("/studios", json={"name": "20th Century Fox"})
    assert response.status_code == 200
    assert response.json() == {"id": 7, "name": "20th Century Fox"}
    response = client.post("/studios", json={"name": "20th Century Fox"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "message": (
                "DuplicateEntryException('Studio 20th Century Fox already"
                " exists')"
            )
        }
    }


def test_delete_studio() -> None:
    """Test deleting a studios."""
    response = client.delete("/studios/7")
    assert response.status_code == 200
    assert response.json() == {"message": "Studio with ID 7 deleted"}
    response = client.delete("/studios/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "InvalidIDException('Studio ID 0 does not exist')"
        }
    }
    response = client.delete("/studios/1")
    assert response.status_code == 412
    assert response.json() == {
        "detail": {
            "message": (
                "IntegrityConstraintException('Studio Paramount Pictures (ID"
                " 1) has movies assigned to it')"
            )
        }
    }


def test_get_all_studios() -> None:
    """Test getting all studios."""
    response = client.get("/studios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 6
    assert {"id": 1, "name": "Paramount Pictures"} in response.json()
