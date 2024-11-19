from pymongo import MongoClient
from .config import settings

class DatabaseConnection:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = MongoClient(settings.MONGO_URI)
        return cls._instance

    @classmethod
    def get_database(cls):
        client = cls.get_instance()
        return client[settings.DATABASE_NAME]