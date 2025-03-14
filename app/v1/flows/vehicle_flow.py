from pymongo import MongoClient
from app.v1.exceptions.entity_not_found import EntityNotFound
from models.vehicle_model import Vehicle

class VehicleFlow:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client["vehicle_management"]
        self.collection = self.db["vehicles"]


    def create_vehicle(self, vehicle:dict):
        vehicle_model = Vehicle(**vehicle)
        return self.collection.insert_one(vehicle_model.model_dump())

    def update_vehicle(self, _id, data_to_update:dict):
        filter = {"_id": _id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        to_update = document.update(data_to_update)
        return self.collection.update_one(
            filter,
            {
                "$set":to_update
            }
        )

    def read_vehicle(self, _id):
        filter = {"_id":_id}
        document = self.collection.find_one(filter)
        if not document:
            raise EntityNotFound(self.db.name, self.collection.name, filter)
        return document

    def delete_vehicle(self, _id):
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
