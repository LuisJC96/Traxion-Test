from app.v1.flows.vehicle_flow import VehicleFlow
from tests.mocks import VEHICLE
from app.v1.exceptions.entity_not_found import EntityNotFound
from app.v1.exceptions.duplicated_enity import DuplicatedEntity
from tools.mongodb_singleton import MongoDBSingleton
from unittest.mock import MagicMock
from app.v1.flows.vehicle_flow import VehicleFlow
from pytest import mark
from unittest import mock
import mongomock


def test_get_vehicle(client):
    mock_db = client.app.state.mongo_client.vehicle_management
    mock_collection = mock_db.vehicles
    mock_collection.find_one = mock.Mock(return_value=VEHICLE)
    response = client.get("/v1/vehicles/123")
    assert response.status_code == 200


def test_get_vehicle_not_found(client):
    mock_db = client.app.state.mongo_client.vehicle_management
    mock_collection = mock_db.vehicles
    mock_collection.find_one = mock.Mock(return_value=None)
    response = client.get("/v1/vehicles/123")
    assert response.status_code == 404

def test_create_vehicle(client, mocker):
    mock_vehicle = mocker.patch.object(VehicleFlow, "create_vehicle")
    mock_vehicle.return_value = VEHICLE
    payload = {
    "brand":"Toyota",
    "model":"Corolla",
    "year":2025,
    "registration":{
        "country":"Mexico",
        "state":"Ciudad de México",
        "plate_number":"VPR-910"
    }
}
    response = client.post(
        "/v1/vehicles",
        json=payload
    )
    assert response.status_code == 200

def test_create_vehicle_duplicated(client, mocker):
    mocker.patch.object(VehicleFlow, "create_vehicle", side_effect=DuplicatedEntity("","",""))
    payload = {
    "brand":"Ford",
    "model":"Mustang",
    "year":2025,
    "registration":{
        "country":"Mexico",
        "state":"Ciudad de México",
        "plate_number":"VPR-910"
    }
}
    response = client.post(
        "/v1/vehicles",
        json=payload
    )
    assert response.status_code == 400

def test_delete_vehicle(client, mocker):
    mock_vehicle = mocker.patch.object(VehicleFlow, "delete_vehicle")
    mock_vehicle.return_value = VEHICLE
    response = client.delete(
        "/v1/vehicles/123"
    )
    assert response.status_code == 200



