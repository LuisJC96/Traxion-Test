from app.v1.flows.service_order_flow import ServiceOrderFlow
from tests.mocks import SERVICE_ORDER
from app.v1.flows.vehicle_flow import VehicleFlow
from tests.mocks import VEHICLE
from app.v1.exceptions.entity_not_found import EntityNotFound
from app.v1.exceptions.invalid_state_change import InvalidStateChange


def test_get_service_order(client, mocker):
    mock_service_order = mocker.patch.object(ServiceOrderFlow, "read_service_order")
    mock_service_order.return_value = SERVICE_ORDER
    response = client.get("/v1/service-orders/123")
    assert response.status_code == 200

def test_get_service_order_not_found(client, mocker):
    mocker.patch.object(ServiceOrderFlow, "read_service_order", side_effect=EntityNotFound("","",""))
    response = client.get("/v1/service_orders/123")
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




