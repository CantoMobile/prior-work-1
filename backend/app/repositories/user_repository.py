from bson import ObjectId
from flask import abort, request
from models.user_model import User
from repositories.abstract_repository import AbstractRepository
from main import db


class UserRepository(AbstractRepository[User]):
    def __init__(self):
        super().__init__()

    def find_by_email(self, email):
        laColeccion = db[self.coleccion]
        user_data = laColeccion.find_one({'email': email})
        user_data = self.getValuesDBRef(user_data)
        if user_data == None:
            user_data = {}
        else:
            user_data["_id"] = user_data["_id"].__str__()
        return user_data

    def update_role(self, user_id, role):
        laColeccion = db[self.coleccion]
        _id = ObjectId(user_id)
        print(role)
        x = laColeccion.update_one({"_id": _id}, {'$push': {'roles': role}})
        return {"updated_count": x.matched_count}
