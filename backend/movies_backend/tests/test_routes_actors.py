#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Actor routes tests.

Author        : Vadim Titov
Created       : Mi Okt 29 14:42:33 2024 +0200
Last modified : Mi Okt 29 15:02:33 2024 +0200
"""


from fastapi.testclient import TestClient

from movies_backend.main import app

client = TestClient(app)


def test_add_actor() -> None:
    """Test adding an actor."""
    response = client.post("/actors", json={"name": "Silvester Stallone"})
    assert response.status_code == 200
    assert response.json() == {"id": 24, "name": "Silvester Stallone"}
    response = client.post("/actors", json={"name": "Silvester Stallone"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "message": (
                "DuplicateEntryException('Actor Silvester Stallone already"
                " exists')"
            )
        }
    }


def test_delete_actor() -> None:
    """Test deleting an actor."""
    response = client.delete("/actors/24")
    assert response.status_code == 200
    assert response.json() == {"message": "Actor with ID 24 deleted"}
    response = client.delete("/actors/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "InvalidIDException('Actor ID 0 does not exist')"
        }
    }
    response = client.delete("/actors/1")
    assert response.status_code == 412
    assert response.json() == {
        "detail": {
            "message": (
                "IntegrityConstraintException('Actor Benicio del Toro (ID 1)"
                " has movies assigned to it')"
            )
        }
    }


def test_get_all_actors() -> None:
    """Test getting all actors."""
    response = client.get("/actors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 23
    assert {"id": 1, "name": "Benicio del Toro"} in response.json()
