from pydantic import BaseModel
from typing import Optional, List



class ServiceOrderPostRequest(BaseModel):
    vehicle_id: str
    service_date: str
    notes: Optional[List[str]] = []
    technician: Optional[str] = None
    scheduled_date: str
    millage: float
    service_type: str
    service_description: str

class ServiceOrderPatchRequest(BaseModel):
    state: Optional[str]
    scheduled_date: Optional[str] = None
    service_date: Optional[str] = None
    notes: Optional[List[str]] = []
    technician: Optional[str] = None
    involved_parts: Optional[List[str]] = []
    spare_parts: Optional[List[str]] = []

