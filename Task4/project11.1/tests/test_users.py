from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
for module_name in list(sys.modules):
    if module_name == "app" or module_name.startswith("app."):
        sys.modules.pop(module_name)

from app.main import app, reset_users_state  # noqa: E402


@pytest.fixture(autouse=True)
def clean_state():
    reset_users_state()
    yield
    reset_users_state()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_create_user(client):
    response = client.post("/users", json={"username": "alex", "age": 21})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "alex", "age": 21}


def test_get_existing_user(client):
    created = client.post("/users", json={"username": "maria", "age": 25})
    user_id = created.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"id": user_id, "username": "maria", "age": 25}


def test_get_missing_user(client):
    response = client.get("/users/404")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_existing_user(client):
    created = client.post("/users", json={"username": "ivan", "age": 30})
    user_id = created.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_user(client):
    response = client.delete("/users/404")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
