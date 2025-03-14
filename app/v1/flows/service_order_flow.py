from pymongo import MongoClient
from datetime import datetime
from app.v1.exceptions.entity_not_found import EntityNotFound
from app.v1.exceptions.invalid_state_change import InvalidStateChange
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

    def __state_change_valid(self, actual_state, wished_state):
        return  ServiceOrderStatesMachine().validate_transition(actual_state, wished_state)

    def __manage_listed_values(self, document, field:str, new_list):
        document[field] += new_list

    def update_service_order(self, _id, data_to_update:dict):
        filter = {"_id": _id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_to_update["updated_at"] = now
        if "state" in data_to_update:
            if not self.__state_change_valid(document.get("state"), data_to_update.get("state")):
                raise InvalidStateChange(document.get("state"), data_to_update.get("state"))
            if data_to_update.get("state") in ["COMPLETED", "CANCELLED"]:
                data_to_update["completion_date"] = now
        self.__manage_listed_values(document, "notes", data_to_update.pop("notes", []))
        self.__manage_listed_values(document, "involved_parts", data_to_update.pop("involved_parts", []))
        self.__manage_listed_values(document, "spare_parts", data_to_update.pop("spare_parts", []))
        to_update = dict(document)
        to_update.update(data_to_update)
        self.collection.update_one(
            filter,
            {
                "$set": to_update
            }
        )
        return document

    def read_service_order(self, _id):
        filter = {"_id":_id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        return document

    def query_service_offers(self, filters):
        limit = filters.pop("limit", 20)
        page = filters.pop("page", 1)
        skip_documents = (page-1)*limit
        response = [value for value in self.collection.find(filters).skip(skip_documents).limit(limit)]
        return response

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
