from pymongo import MongoClient
from app.v1.exceptions.entity_not_found import EntityNotFound
from app.v1.schemas.service_order_model import ServiceOrder
from tools.service_orders_states_machine import ServiceOrderStatesMachine

class ServiceOrderFlow:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client["vehicle_management"]
        self.collection = self.db["service_orders"]


    def create_service_order(self, service_order:dict):
        service_order_model = ServiceOrder(**service_order)
        return self.collection.insert_one(service_order_model.model_dump())

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
