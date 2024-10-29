#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summary       : Category routes tests.

Author        : Vadim Titov
Created       : Mi Okt 29 15:07:34 2024 +0200
Last modified : Mi Okt 29 15:15:34 2024 +0200
"""


from fastapi.testclient import TestClient

from movies_backend.main import app

client = TestClient(app)


def test_add_category() -> None:
    """Test adding a category."""
    response = client.post("/categories", json={"name": "Mystery"})
    assert response.status_code == 200
    assert response.json() == {"id": 6, "name": "Mystery"}
    response = client.post("/categories", json={"name": "Mystery"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "message": (
                "DuplicateEntryException('Category Mystery already exists')"
            )
        }
    }


def test_delete_category() -> None:
    """Test deleting a category."""
    response = client.delete("/categories/6")
    assert response.status_code == 200
    assert response.json() == {"message": "Category 6 deleted"}
    response = client.delete("/categories/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "message": "InvalidIDException('Category ID 0 does not exist')"
        }
    }
    response = client.delete("/categories/1")
    assert response.status_code == 412
    assert response.json() == {
        "detail": {
            "message": (
                "IntegrityConstraintException('Category Crime (1)"
                " has movies assigned to it')"
            )
        }
    }


def test_get_all_categories() -> None:
    """Test getting all categories."""
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5
    assert {"id": 1, "name": "Crime"} in response.json()
