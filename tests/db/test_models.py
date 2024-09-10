import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, Todo
from app.core.app_config import settings

# Create a new engine and session for testing
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"


def test_create_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo = Todo(title="Test Todo", description="This is a test todo", owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.owner_id == user.id


def test_update_user(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user.username = "updateduser"
    db.commit()
    db.refresh(user)
    assert user.username == "updateduser"


def test_update_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo = Todo(title="Test Todo", description="This is a test todo", owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    todo.title = "Updated Todo"
    db.commit()
    db.refresh(todo)
    assert todo.title == "Updated Todo"


def test_delete_user(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.delete(user)
    db.commit()
    deleted_user = db.query(User).filter(User.id == user.id).first()
    assert deleted_user is None


def test_delete_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo = Todo(title="Test Todo", description="This is a test todo", owner_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    db.delete(todo)
    db.commit()
    deleted_todo = db.query(Todo).filter(Todo.id == todo.id).first()
    assert deleted_todo is None
