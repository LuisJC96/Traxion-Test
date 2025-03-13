from app.v1.exceptions.handler import exception_handler
from fastapi import APIRouter, Depends, Request, Response
from tools.mongodb_singleton import MongoDBSingleton
from app.v1.flows.vehicle_flow import VehicleFlow

router = APIRouter()

@router.post("/vehicles")
@exception_handler()
async def create_vehicle(
        request: Request,
        response: Response,
        client = Depends(MongoDBSingleton.get_client)
):
    request_body = await request.json()
    flow = VehicleFlow(client)
    return flow.create_vehicle(request_body)

@router.get("/vehicles/{vehicle_id}")
@exception_handler()
async def get_vehicle(
        request: Request,
        response: Response,
        vehicle_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = VehicleFlow(client)
    return flow.read_vehicle(vehicle_id)

@router.patch("/vehicles/{vehicle_id}")
@exception_handler()
async def update_vehicle(
        request: Request,
        response: Response,
        vehicle_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    request_body = await request.json()
    flow = VehicleFlow(client)
    return flow.update_vehicle(vehicle_id, request_body)

@router.delete("/vehicles/{vehicle_id}")
@exception_handler()
async def delete_vehicle(
        request: Request,
        response: Response,
        vehicle_id: str,
        client=Depends(MongoDBSingleton.get_client)
):
    flow = VehicleFlow(client)
    return flow.delete_vehicle(vehicle_id)