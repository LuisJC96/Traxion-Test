from pymongo import MongoClient
from app.v1.exceptions.entity_not_found import EntityNotFound
from models.service_order_model import ServiceOrder
from tools.service_orders_states_machine import ServiceOrderStatesMachine
from app.v1.flows.vehicle_flow import VehicleFlow

class ServiceOrderFlow:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client["vehicle_management"]
        self.collection = self.db["service_orders"]


    def __create_order_dict(self, service_order, vehicle_info):
        return ServiceOrder(**{
            "vehicle": vehicle_info,
            "millage": service_order.get("millage"),
            "notes": service_order.get("notes", []),
            "technician": service_order.get("technician"),
            "scheduled_date": service_order.get("scheduled_date"),
            "service_date": service_order.get("service_date"),
            "service_type": service_order.get("service_type"),
            "service_description": service_order.get("service_description")
        }).model_dump(by_alias=True)

    def create_service_order(self, service_order:dict):
        vehicle_flow = VehicleFlow(self.client)
        vehicle_info = vehicle_flow.read_vehicle(service_order.get("vehicle_id"))
        data_to_upload = self.__create_order_dict(service_order, vehicle_info)
        self.collection.insert_one(data_to_upload)
        return data_to_upload

    def update_service_order(self, _id, data_to_update:dict):
        filter = {"_id": _id}
        document = self.collection.find_one(filter)
        if "state" in data_to_update:
            if not ServiceOrderStatesMachine().validate_transition(document.get("state"), data_to_update.get("state")):
                raise

        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        to_update = document.update(data_to_update)
        return self.collection.update_one(
            filter,
            {
                "$set":to_update
            }
        )

    def read_service_order(self, _id):
        filter = {"_id":_id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        return document

    def delete_service_order(self, _id):
        filter = {"_id": _id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        return self.collection.update_one(
            filter,
            {
                "$set": {
                    "is_active":False
                }
            }
        )
