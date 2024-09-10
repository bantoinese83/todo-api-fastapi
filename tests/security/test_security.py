import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    create_user,
    authenticate_user,
    get_current_user,
)
from app.schemas import UserCreate


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert token is not None


def test_get_password_hash():
    password = "password"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert verify_password(password, hashed_password)


def test_create_user(db: Session):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    user = create_user(db, user_data)
    assert user.username == user_data.username
    assert user.email == user_data.email
    assert verify_password(user_data.password, user.hashed_password)


def test_authenticate_user(db: Session):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    create_user(db, user_data)
    user = authenticate_user(db, user_data.username, user_data.password)
    assert user is not False
    assert user.username == user_data.username


def test_authenticate_user_invalid_credentials(db: Session):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    create_user(db, user_data)
    user = authenticate_user(db, user_data.username, "wrongpassword")
    assert user is False


def test_get_current_user(db: Session):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    user = create_user(db, user_data)
    token = create_access_token({"sub": user.username})
    current_user = get_current_user(db, token)
    assert current_user.username == user.username


def test_get_current_user_invalid_token(db: Session):
    with pytest.raises(HTTPException):
        get_current_user(db, "invalid_token")
