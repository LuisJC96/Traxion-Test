from pymongo import MongoClient
from typing import Optional
import os


class MongoDBSingleton:
    _client: Optional[MongoClient] = None

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            connection_string = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            cls._client = MongoClient(connection_string)
        return cls._client

    @classmethod
    def close_client(cls):
        """Close the MongoDB client connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
