from models.vehicle_model import Vehicle
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ServiceOrderPost(BaseModel):
    id: str

class ServiceOrderPatch(BaseModel):
    id: str

