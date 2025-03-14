from typing import Generator
from pytest import fixture
from starlette.testclient import TestClient
from unittest.mock import Mock
from unittest.mock import MagicMock
from tools.mongodb_singleton import MongoDBSingleton
from app.v1.router import api_router



@fixture
def client() -> Generator:
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(api_router, prefix='/v1')
    return TestClient(app)

@fixture
def mock_mongo_client(mocker):
    mock_client = MagicMock()
    mocker.patch.object(MongoDBSingleton, 'get_client', return_value=mock_client)
    return mock_client