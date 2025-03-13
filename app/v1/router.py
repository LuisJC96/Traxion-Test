from fastapi import  APIRouter, FastAPI
from app.v1.resources import service_order_resource, vehicle_resource

api_router = APIRouter(redirect_slashes=False)
api_router.include_router(
    vehicle_resource.router,
    prefix="/vehicle"
)
api_router.include_router(
    service_order_resource.router,
    prefix="/service-order"
)

app = FastAPI()
app.include_router(api_router)