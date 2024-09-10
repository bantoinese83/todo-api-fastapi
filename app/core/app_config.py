from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    APP_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://root:letmeinnow@localhost:5432/todo_test_db"
    SECRET_KEY: str = "your_secret_key" or secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"


settings = Settings()
