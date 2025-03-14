from models.vehicle_model import Vehicle
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehiclePost(BaseModel):
    id: str


class VehiclePatch(BaseModel):
    id: str