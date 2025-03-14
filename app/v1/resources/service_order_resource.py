from app.v1.exceptions.handler import exception_handler
from fastapi import APIRouter, Depends, Request, Response
from tools.mongodb_singleton import MongoDBSingleton
from app.v1.flows.service_order_flow import ServiceOrderFlow
from app.v1.schemas.service_orders_resource_schemas import ServiceOrderPostRequest, ServiceOrderPatchRequest

router = APIRouter()

@router.post("")
@exception_handler()
async def create_service_order(
        request: Request,
        response: Response,
        service_order: ServiceOrderPostRequest,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = ServiceOrderFlow(client)
    return flow.create_service_order(service_order.model_dump())



@router.get("/{service_order_id}")
@exception_handler()
async def get_service_order(
        request: Request,
        response: Response,
        service_order_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = ServiceOrderFlow(client)
    return flow.read_service_order(service_order_id)

@router.get("")
@exception_handler()
async def get_service_orders(
        request: Request,
        response: Response,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = ServiceOrderFlow(client)
    filters = dict(request.query_params)
    return flow.query_service_offers(filters)

@router.patch("/{service_order_id}")
@exception_handler()
async def update_service_order(
        request: Request,
        response: Response,
        service_order: ServiceOrderPatchRequest,
        service_order_id:str,
        client = Depends(MongoDBSingleton.get_client)
):
    flow = ServiceOrderFlow(client)
    return flow.update_service_order(service_order_id, service_order.model_dump())

