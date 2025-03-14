from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
import uuid


class Registration(BaseModel):
    country: str
    state: str
    plate_number: str

class Vehicle(BaseModel):
    brand: str
    model: str
    year: int
    is_active: bool = True
    registration: Registration

    @model_validator(mode='before')
    def generate_id(cls, values):
        #generates id based on fields to avoid duplication of vehicles
        build_str = (
                values.get("registration").get("country")+
               values.get("registration").get("plate_number")+
                values.get("registration").get("state")+
                values.get("brand")+
                values.get("model")+
                values.get("year")
        )
        values["_id"] = uuid.uuid5(uuid.NAMESPACE_OID, build_str)
        return values

