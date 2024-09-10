import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.services.todo_service import (
    get_todos,
    create_todo,
    get_todo,
    update_todo,
    delete_todo,
)
from app.db.database import get_db
from app.schemas.todo_schema import Todo, TodoCreate, TodoUpdate
from app.schemas.user_schema import User

router = APIRouter()


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=list[Todo])
async def get_all_todos(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_todos(db=db, user_id=current_user.id)


@router.get("/{todo_id}", response_model=Todo)
async def get_todo_by_id(
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = get_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=Todo)
async def update_todo_by_id(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = update_todo(db=db, todo_id=todo_id, todo=todo, user_id=current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.delete("/{todo_id}")
async def delete_todo_by_id(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    return {"message": "Todo deleted"}
