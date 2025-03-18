from typing import Generator
from unittest import mock
from pytest import fixture
from starlette.testclient import TestClient
from pymongo import MongoClient
from tests.mocks import VEHICLE, SERVICE_ORDER
import mongomock
from main import app, MongoDBSingleton


@fixture
def mock_mongo_client():
    mock_client = mongomock.MongoClient()
    mock_db = mock_client.vehicle_management
    mock_collection_vehicles = mock_db.vehicles
    mock_collection_vehicles.insert_one(VEHICLE)
    mock_collection_service_orders = mock_db.service_orders
    mock_collection_service_orders.insert_one(SERVICE_ORDER)
    return mock_client


@fixture
def client(mock_mongo_client):
    app.state.mongo_client = mock_mongo_client
    with mock.patch.object(MongoDBSingleton, 'get_client', return_value=mock_mongo_client):
        with TestClient(app) as client:
            yield client