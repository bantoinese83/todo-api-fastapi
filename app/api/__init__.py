from fastapi import APIRouter

from app.api.auth.auth_api import router as auth_router
from app.api.todo.todo_api import router as todo_router
from app.api.user.user_api import router as user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(todo_router, prefix="/todos", tags=["todos"])
router.include_router(user_router, prefix="/users", tags=["users"])
