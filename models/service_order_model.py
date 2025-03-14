from models.vehicle_model import Vehicle
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal
import uuid

class ServiceOrder(BaseModel):
    id: str = Field(str(uuid.uuid4()), alias="_id")
    state: Literal['OPEN', 'ASSIGNED', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED'] = "OPEN"
    vehicle: Vehicle
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    millage: float
    notes: Optional[List[str]] = Field(
        [],
        description="Miscellaneous notes given by either the technician or either person updating the entity")
    technician: Optional[str] = None
    scheduled_date: str
    service_date: str
    completion_date: Optional[str] = None
    service_type: str
    service_description: str
    involved_parts: Optional[List[str]] = Field(
        [], description="List of involved parts on the given service")
    spare_parts: Optional[List[str]] = Field(
        [], description="List of used spare parts on the given service")