from __future__ import annotations

import pytest


pytestmark = pytest.mark.asyncio


def user_payload(faker, age: int | None = None) -> dict[str, int | str]:
    return {
        "username": faker.user_name(),
        "age": age if age is not None else faker.random_int(min=19, max=80),
    }


async def test_create_user_returns_201_and_response_shape(client, faker):
    payload = user_payload(faker)

    response = await client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == payload["username"]
    assert data["age"] == payload["age"]
    assert set(data) == {"id", "username", "age"}


async def test_get_existing_user_returns_200(client, faker):
    payload = user_payload(faker)
    created = await client.post("/users", json=payload)
    user_id = created.json()["id"]

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"id": user_id, **payload}


async def test_get_missing_user_returns_404(client):
    response = await client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_delete_existing_user_returns_204(client, faker):
    created = await client.post("/users", json=user_payload(faker))
    user_id = created.json()["id"]

    response = await client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""


async def test_delete_same_user_twice_returns_404(client, faker):
    created = await client.post("/users", json=user_payload(faker))
    user_id = created.json()["id"]

    first_response = await client.delete(f"/users/{user_id}")
    second_response = await client.delete(f"/users/{user_id}")

    assert first_response.status_code == 204
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "User not found"


async def test_user_state_is_isolated_between_tests(client, faker):
    response = await client.post("/users", json=user_payload(faker))

    assert response.status_code == 201
    assert response.json()["id"] == 1
