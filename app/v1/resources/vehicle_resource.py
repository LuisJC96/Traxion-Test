from app.v1.exceptions.handler import exception_handler
from fastapi import APIRouter, Depends, Request, Response
from tools.mongodb_singleton import MongoDBSingleton
from app.v1.flows.vehicle_flow import VehicleFlow
from app.v1.schemas.vehicle_resource_schemas import VehiclePostRequest
from pymongo import MongoClient

router = APIRouter()

def get_mongo_client() -> MongoClient:
    return MongoDBSingleton.get_client()

def close_mongo_client() -> MongoClient:
    return MongoDBSingleton.get_client()

@router.post("")
@exception_handler()
async def create_vehicle(
        request: Request,
        response: Response,
        vehicle: VehiclePostRequest,
        client = Depends(get_mongo_client)
):
    flow = VehicleFlow(client)
    return flow.create_vehicle(vehicle.model_dump())

@router.get("/{vehicle_id}")
@exception_handler()
async def get_vehicle(
        request: Request,
        response: Response,
        vehicle_id:str,
        client = Depends(get_mongo_client)
):
    flow = VehicleFlow(client)
    return flow.read_vehicle(vehicle_id)

@router.delete("/{vehicle_id}")
@exception_handler()
async def delete_vehicle(
        request: Request,
        response: Response,
        vehicle_id: str,
        client=Depends(get_mongo_client)
):
    flow = VehicleFlow(client)
    return flow.delete_vehicle(vehicle_id)