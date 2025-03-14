from models.vehicle_model import Vehicle
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Payment(BaseModel):
    amount: float
    payment_status: str
    payment_method: str

class Customer(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

class ServiceDetails(BaseModel):
    service_type: str
    service_description: str
    replaced_parts: str

class ServiceOrder(BaseModel):
    id: str
    state: str
    vehicle: Vehicle
    service_date: str
    customer: Customer
    notes: Optional[str]
    technician: Optional[str]
    scheduled_date: datetime
    completion_date: Optional[datetime]