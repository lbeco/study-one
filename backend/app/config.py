from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "study-one"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./data/study_one.db"

    DATA_DIR: str = "./data"
    UPLOAD_DIR: str = "./data/uploads"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
