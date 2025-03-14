from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from app.v1.exceptions.entity_not_found import EntityNotFound
from app.v1.exceptions.duplicated_enity import DuplicatedEntity
from models.vehicle_model import Vehicle
from datetime import datetime

class VehicleFlow:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client.vehicle_management
        self.collection = self.db.vehicles


    def create_vehicle(self, vehicle:dict):
        data_to_insert = Vehicle(**vehicle)
        try:
            self.collection.insert_one(data_to_insert.model_dump(by_alias=True))
        except DuplicateKeyError:
            raise DuplicatedEntity(self.db.name, self.collection.name, data_to_insert.model_dump(by_alias=True))
        return data_to_insert.model_dump(by_alias=True)

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
        self.collection.update_one(
            filter,
            {
                "$set": {
                    "is_active": False,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        )
        return document
