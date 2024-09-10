from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.api.auth.auth_api import router as auth_router
from app.api.todo.todo_api import router as todo_router
from app.api.user.user_api import router as user_router
from app.core.app_config import settings
from app.core.events import create_startup_app_handler, create_shutdown_app_handler
from app.core.exceptions import (
    NotFoundError,
    UnauthorizedError,
    BadRequestError,
    InternalServerError,
)
from app.core.log_config import configure_logging
from app.core.middlewares import configure_middlewares

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

configure_middlewares(app)
create_startup_app_handler(app)
create_shutdown_app_handler(app)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(todo_router, prefix="/todos", tags=["todos"])
app.include_router(user_router, prefix="/users", tags=["users"])

app.add_exception_handler(NotFoundError, NotFoundError.handle)
app.add_exception_handler(UnauthorizedError, UnauthorizedError.handle)
app.add_exception_handler(BadRequestError, BadRequestError.handle)
app.add_exception_handler(InternalServerError, InternalServerError.handle)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
