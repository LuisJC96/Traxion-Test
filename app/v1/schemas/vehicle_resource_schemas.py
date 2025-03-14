from models.vehicle_model import Registration, Vehicle
from pydantic import BaseModel, Field


class VehiclePostRequest(BaseModel):
    brand: str
    model: str
    year: int
    registration: Registration
