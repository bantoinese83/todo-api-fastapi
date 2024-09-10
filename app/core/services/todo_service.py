from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import Todo
from app.schemas.todo_schema import TodoUpdate, TodoCreate


def create_todo(db: Session, todo: TodoCreate, user_id: int) -> Todo:
    """
    Create a new todo item.

    :param db: Database session
    :param todo: TodoCreate object containing todo details
    :param user_id: ID of the user creating the todo
    :return: Created Todo object
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        owner_id=user_id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int) -> list[Todo]:
    """
    Retrieve all todos for a specific user.

    :param db: Database session
    :param user_id: ID of the user
    :return: List of Todo objects
    """
    return db.query(Todo).filter(Todo.owner_id == user_id).all()


def get_todo(db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """
    Retrieve a specific todo by its ID and user ID.

    :param db: Database session
    :param todo_id: ID of the todo
    :param user_id: ID of the user
    :return: Todo object or None if not found
    """
    return db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_id).first()


def update_todo(
    db: Session, todo_id: int, todo: TodoUpdate, user_id: int
) -> Optional[Todo]:
    """
    Update a specific todo by its ID and user ID.

    :param db: Database session
    :param todo_id: ID of the todo to update
    :param todo: TodoUpdate object containing updated details
    :param user_id: ID of the user
    :return: Updated Todo object or None if not found
    """
    db_todo = (
        db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_id).first()
    )
    if not db_todo:
        return None
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """
    Delete a specific todo by its ID and user ID.

    :param db: Database session
    :param todo_id: ID of the todo to delete
    :param user_id: ID of the user
    :return: None
    """
    db_todo = (
        db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user_id).first()
    )
    if not db_todo:
        return None
    db.delete(db_todo)
    db.commit()
