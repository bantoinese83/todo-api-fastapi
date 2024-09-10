from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.auth_schema import UserCreate


def test_signup(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    response = client.post("/auth/signup", json=user_data.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == user_data.username


def test_login(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    client.post("/auth/signup", json=user_data.dict())
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_login_invalid_credentials(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    client.post("/auth/signup", json=user_data.dict())
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
