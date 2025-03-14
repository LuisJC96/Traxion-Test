from models.vehicle_model import Vehicle
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class Payment(BaseModel):
    amount: float
    payment_status: str
    payment_method: str

class Customer(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

class ServiceOrder(BaseModel):
    id: str
    state: str
    vehicle: Vehicle

    customer: Customer
    millage: float
    notes: Optional[str] = Field(
        [],
        description="Miscellaneous notes given by either the technician or either person updating the entity")
    technician: Optional[str] = None
    scheduled_date: datetime
    service_date: str
    completion_date: Optional[datetime] = None
    service_type: str
    service_description: str
    involved_parts: Optional[List[str]] = Field(
        [], description="List of involved parts on the given service")
    spare_parts: Optional[List[str]] = Field(
        [], description="List of used spare parts on the given service")