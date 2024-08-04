from typing import Optional

from pydantic import BaseSettings, EmailStr

from app.service import AppMessages


class Settings(BaseSettings):
    app_title: str = AppMessages.APP_TITLE
    app_description = AppMessages.APP_DESCRIPTION
    database_url: str = AppMessages.DATABASE_URL
    secret: str = AppMessages.SECRET_KEY
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
