# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import app
from app.core.app_config import settings
from app.db.models import Base
from app.db.database import get_db

engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    # Drop all tables and recreate them before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Optionally, you can drop all tables after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    def override_get_db():
        try:
            yield TestingSessionLocal()
        finally:
            TestingSessionLocal.close_all()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
