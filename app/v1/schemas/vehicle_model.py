from pydantic import BaseModel, Field
from typing import Optional, List



class ServiceSummary(BaseModel):
    date: str
    millage: int
    service_description: str
    technician: str

class Registration(BaseModel):
    country: str
    state: str
    plate_number: str

class Vehicle(BaseModel):
    id: str
    brand: str
    model: str
    year: int
    is_active: bool
    maintenance_history:Optional[List[ServiceSummary]] = Field(
        [], description="list of previous given services to the vehicle")
    registration: Registration
