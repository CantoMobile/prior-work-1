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
        user_data = self.replaceDBRefsWithObjects(user_data)
        if user_data == None:
            user_data = {}
        else:
            user_data["_id"] = user_data["_id"].__str__()
        return user_data

