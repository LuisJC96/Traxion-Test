from app.v1.exceptions.handler import exception_handler
from fastapi import APIRouter, Depends, Request, Response
from tools.mongodb_singleton import MongoDBSingleton
from app.v1.flows.service_order_flow import ServiceOrderFlow

router = APIRouter()

@router.post("/service-orders")
@exception_handler()
async def create_service_order(
        request: Request,
        response: Response,
        client = Depends(MongoDBSingleton.get_client)
):
    request_body = await request.json()
    flow = ServiceOrderFlow(client)
    return flow.create_service_order(request_body)

@router.get("/service-orders/{service_order_id}")
@exception_handler()
async def get_service_order(
        request: Request,
        response: Response,
        service_order_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = ServiceOrderFlow(client)
    return flow.read_service_order(service_order_id)

@router.patch("/service-orders/{service_order_id}")
@exception_handler()
async def update_service_order(
        request: Request,
        response: Response,
        service_order_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    request_body = await request.json()
    flow = ServiceOrderFlow(client)
    return flow.update_service_order(service_order_id, request_body)

