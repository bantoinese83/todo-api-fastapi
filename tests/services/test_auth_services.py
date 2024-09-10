from app.core.security import create_user, authenticate_user
from app.schemas.auth_schema import UserCreate


def test_create_user(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    new_user = create_user(db, user_data)
    assert new_user.username == user_data.username
    assert new_user.email == user_data.email


def test_authenticate_user(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    create_user(db, user_data)
    authenticated_user = authenticate_user(db, user_data.username, user_data.password)
    assert authenticated_user is not False
    assert authenticated_user.username == user_data.username


def test_authenticate_user_invalid_credentials(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    create_user(db, user_data)
    authenticated_user = authenticate_user(db, user_data.username, "wrongpassword")
    assert authenticated_user is False
