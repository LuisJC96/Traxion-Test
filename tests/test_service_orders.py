from app.v1.flows.service_order_flow import ServiceOrderFlow
from tests.mocks import VEHICLE, SERVICE_ORDER
from unittest import mock


def test_get_service_order(client, mocker):
    mock_db = client.app.state.mongo_client.vehicle_management
    mock_collection = mock_db.service_orders
    mock_collection.find_one = mock.Mock(return_value=SERVICE_ORDER)

    response = client.get("/v1/service-orders/abc")
    assert response.status_code == 200

def test_get_service_order_not_found(client, mocker):
    mock_db = client.app.state.mongo_client.vehicle_management
    mock_collection = mock_db.service_orders
    mock_collection.find_one = mock.Mock(return_value=None)
    response = client.get("/v1/service-orders/def")
    assert response.status_code == 404

def test_create_service_order(client, mocker):
    mock_service_order = mocker.patch.object(ServiceOrderFlow, "create_service_order")
    mock_service_order.return_value = SERVICE_ORDER
    payload = {
        "millage": 1000,
        "vehicle_id":"c1c60720-51c4-5319-8924-ff4e0c9e0ae8",
        "service_date":"2025-03-15",
        "notes":["Urgent service required."],
        "scheduled_date":"2025-03-14",
        "service_type": "Oil change",
        "service_description": "Rutine oil change"
    }
    response = client.post(
        "/v1/service-orders",
        json=payload
    )
    assert response.status_code == 200

def test_update_service_order(client, mocker):
    mock_service_order = mocker.patch.object(ServiceOrderFlow, "update_service_order")
    mock_service_order.return_value = SERVICE_ORDER
    payload = {
        "state":"OPEN",
        "notes":["Se lo comio el perro"]
    }
    response = client.patch(
        "/v1/service-orders/123",
        json=payload
    )
    assert response.status_code == 200




