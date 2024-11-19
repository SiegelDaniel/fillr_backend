import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = os.getenv('MONGO_URI', 'mongodb://root:fillr@mongodb:27017/')
    DATABASE_NAME: str = os.getenv('DATABASE_NAME', 'fillrdb')

    class Config:
        env_file = ".env"


settings = Settings()