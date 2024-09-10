from app.core.security import create_user
from app.core.services import get_user, update_user, delete_user
from app.schemas import UserCreate
from app.schemas.user_schema import UserUpdate


def test_get_user(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    new_user = create_user(db, user_data)
    retrieved_user = get_user(db, user_id=new_user.id)
    assert retrieved_user == new_user


def test_update_user(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    new_user = create_user(db, user_data)
    update_data = UserUpdate(username="updateduser", email="updateduser@example.com")
    updated_user = update_user(db, user_id=new_user.id, user=update_data)
    assert updated_user.username == update_data.username
    assert updated_user.email == update_data.email


def test_delete_user(db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="password"
    )
    new_user = create_user(db, user_data)
    delete_user(db, user_id=new_user.id)
    retrieved_user = get_user(db, user_id=new_user.id)
    assert retrieved_user is None
