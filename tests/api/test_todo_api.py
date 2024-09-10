from fastapi.testclient import TestClient
from fastapi import status

from app.schemas.auth_schema import UserCreate
from app.schemas.todo_schema import TodoCreate


def test_create_todo(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    client.post("/auth/signup", json=user_data.dict())
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "password"}
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    response = client.post("/todos", json=todo_data.dict(), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == todo_data.title


def test_get_todos(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    client.post("/auth/signup", json=user_data.dict())
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "password"}
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    todo_data = TodoCreate(
        title="Test Todo 1", description="This is a test todo", completed=False
    )
    client.post("/todos", json=todo_data.dict(), headers=headers)
    todo_data = TodoCreate(
        title="Test Todo 2", description="This is another test todo", completed=True
    )
    client.post("/todos", json=todo_data.dict(), headers=headers)
    response = client.get("/todos", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


def test_get_todo_by_id(client: TestClient, db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    client.post("/auth/signup", json=user_data.dict())
    response = client.post(
        "/auth/login", data={"username": "testuser", "password": "password"}
    )
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    response = client.post("/todos", json=todo_data.dict(), headers=headers)
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == todo_id
