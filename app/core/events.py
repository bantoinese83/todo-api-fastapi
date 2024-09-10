from fastapi import FastAPI
from app.core.log_config import configure_logging
from app.db.database import Base, engine


def create_startup_app_handler(app: FastAPI):
    """
    Creates a startup event handler for the FastAPI app.
    This handler configures logging and creates all database tables.
    """

    @app.on_event("startup")
    async def startup_event():
        configure_logging()
        Base.metadata.create_all(bind=engine)


def create_shutdown_app_handler(app: FastAPI):
    """
    Creates a shutdown event handler for the FastAPI app.
    This handler disposes of the engine and drops all database tables.
    """

    @app.on_event("shutdown")
    async def shutdown_event():
        engine.dispose()
        Base.metadata.drop_all(bind=engine)
