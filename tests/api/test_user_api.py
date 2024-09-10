from fastapi import status
from fastapi.testclient import TestClient

from app.schemas import UserUpdate
from app.schemas.auth_schema import UserCreate


def test_get_user_by_id(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    response = client.post("/auth/signup", json=user_data.dict())
    user_id = response.json()["id"]

    # Log in to get the access token
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "password"}
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Use the access token in the headers for the GET request
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id


def test_update_user_by_id(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    response = client.post("/auth/signup", json=user_data.dict())
    user_id = response.json()["id"]
    update_data = UserUpdate(username="updateduser", email="updateduser@example.com")
    response = client.put(f"/users/{user_id}", json=update_data.dict())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == update_data.username
    assert response.json()["email"] == update_data.email


def test_delete_user_by_id(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    response = client.post("/auth/signup", json=user_data.dict())
    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
