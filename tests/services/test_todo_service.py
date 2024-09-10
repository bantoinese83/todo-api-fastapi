from app.core.services import create_todo, get_todos, get_todo, delete_todo, update_todo
from app.db.models import User
from app.schemas.todo_schema import TodoCreate, TodoUpdate


def test_create_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    new_todo = create_todo(db, todo_data, user_id=user.id)
    assert new_todo.title == todo_data.title
    assert new_todo.description == todo_data.description
    assert new_todo.completed == todo_data.completed
    assert new_todo.owner_id == user.id


def test_get_todos(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo_data = TodoCreate(
        title="Test Todo 1", description="This is a test todo", completed=False
    )
    create_todo(db, todo_data, user_id=user.id)
    todo_data = TodoCreate(
        title="Test Todo 2", description="This is another test todo", completed=True
    )
    create_todo(db, todo_data, user_id=user.id)
    todos = get_todos(db, user_id=user.id)
    assert len(todos) == 2


def test_get_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    new_todo = create_todo(db, todo_data, user_id=user.id)
    retrieved_todo = get_todo(db, todo_id=new_todo.id, user_id=user.id)
    assert retrieved_todo == new_todo


def test_update_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    new_todo = create_todo(db, todo_data, user_id=user.id)
    update_data = TodoUpdate(
        title="Updated Title", description="Updated Description", completed=True
    )
    updated_todo = update_todo(
        db, todo_id=new_todo.id, todo=update_data, user_id=user.id
    )
    assert updated_todo.title == update_data.title
    assert updated_todo.description == update_data.description
    assert updated_todo.completed == update_data.completed


def test_delete_todo(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    todo_data = TodoCreate(
        title="Test Todo", description="This is a test todo", completed=False
    )
    new_todo = create_todo(db, todo_data, user_id=user.id)
    delete_todo(db, todo_id=new_todo.id, user_id=user.id)
    retrieved_todo = get_todo(db, todo_id=new_todo.id, user_id=user.id)
    assert retrieved_todo is None
