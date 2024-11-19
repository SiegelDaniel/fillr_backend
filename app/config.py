import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
    DATABASE_NAME: str = os.getenv('DATABASE_NAME', 'pdf_management')

    class Config:
        env_file = ".env"


settings = Settings()