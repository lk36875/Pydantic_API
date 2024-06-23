"""Tests for Opinions API"""
from async_asgi_testclient import TestClient


async def test_get_opinions(client: TestClient):
    response = await client.get("/opinions/")
    assert response.status_code == 200
    assert response.json() != []
    assert len(response.json()) == 5


async def test_create_opinion(client: TestClient):
    co = {
        "place_id": 1,
        "username": "test_user6",
        "opinion": "test_opinion6",
        "vote": 5,
        "date_of_visit": "2024-01-01",
    }
    response = await client.post("/opinions/", json=co)
    assert response.status_code == 201
    assert response.json()["username"] == "test_user6"


async def test_get_opinion(client: TestClient):
    response = await client.get("/opinions/1")
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


async def test_update_opinion(client: TestClient):
    co = {
        "place_id": 1,
        "username": "test_user",
        "opinion": "test_opinion",
        "vote": 1,
        "date_of_visit": "2024-01-01",
    }
    response = await client.put("/opinions/1", json=co)
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


async def test_delete_opinion(client: TestClient):
    response = await client.delete("/opinions/1")
    assert response.status_code == 202
    assert response.json() == {"status": "ok"}


"""Tests for Places API"""


async def test_get_places(client: TestClient):
    response = await client.get("/places/")
    assert response.status_code == 200
    assert response.json() != []
    assert len(response.json()) == 5


async def test_create_place(client: TestClient):
    cp = {
        "name": "test_place6",
        "description": "test_description6",
        "location": "test_location6",
        "country": "test_country6",
        "city": "test_city6",
        "address": "test_address6",
    }
    response = await client.post("/places/", json=cp)
    assert response.status_code == 201
    assert response.json()["name"] == "test_place6"


async def test_get_place(client: TestClient):
    response = await client.get("/places/1")
    assert response.status_code == 200
    assert response.json()["name"] == "test_name"


async def test_update_place(client: TestClient):
    cp = {
        "name": "test_place",
        "description": "test_description",
        "location": "test_location",
    }
    response = await client.put("/places/1", json=cp)
    assert response.status_code == 200
    assert response.json()["name"] == "test_place"


async def test_delete_place(client: TestClient):
    response = await client.delete("/places/1")
    assert response.status_code == 202
    assert response.json() == {"status": "ok"}


async def test_get_opinions_for_place(client: TestClient):
    response = await client.get("/places/1/opinions")
    assert response.status_code == 200
    assert len(response.json()) == 3
