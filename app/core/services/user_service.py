from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user_schema import UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieve a user by their ID.

    :param db: Database session
    :param user_id: ID of the user to retrieve
    :return: User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """
    Update a user's information.

    :param db: Database session
    :param user_id: ID of the user to update
    :param user: UserUpdate object containing updated information
    :return: Updated User object or None if not found
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """
    Delete a user by their ID.

    :param db: Database session
    :param user_id: ID of the user to delete
    :return: None
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
