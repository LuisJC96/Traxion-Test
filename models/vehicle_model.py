from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime
import uuid


class Registration(BaseModel):
    country: str
    state: str
    plate_number: str

class Vehicle(BaseModel):
    id: str = Field(None,alias="_id")
    brand: str
    model: str
    year: int
    is_active: bool = True
    registration: Registration
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @model_validator(mode='before')
    def generate_id(cls, values):
        registration = values.get("registration", {})
        build_str = (
                registration.get("country", "") +
                registration.get("plate_number", "") +
                registration.get("state", "") +
                values.get("brand", "") +
                values.get("model", "") +
                str(values.get("year", ""))
        )
        values["_id"] = str(uuid.uuid5(uuid.NAMESPACE_OID, build_str))
        return values

