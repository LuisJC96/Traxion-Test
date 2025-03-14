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
    state: str
    scheduled_date: Optional[str]
    completion_date: Optional[str]
    service_date: str
    notes: Optional[List[str]] = []
    technician: str
    involved_parts: Optional[List[str]]
    spare_parts: Optional[List[str]]

