from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.core.services.user_service import (
    get_user,
    update_user,
    delete_user,
)
from app.schemas.user_schema import User, UserUpdate

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user_by_id(
    user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)
):
    user = update_user(db=db, user_id=user_id, user=user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}")
async def delete_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    delete_user(db=db, user_id=user_id)
    return {"message": "User deleted"}
