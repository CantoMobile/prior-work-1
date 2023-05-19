from flask import abort, request
from models.auth_token_model import AuthToken
from bson.objectid import ObjectId
from repositories.abstract_repository import AbstractRepository
from main import db


class AuthenticationRepository(AbstractRepository[AuthToken]):
    def __init__(self):
        super().__init__()

    def find_by_token(self, token):
        laColeccion = db[self.coleccion]
        token_data = laColeccion.find_one({'token': token})
        token_data = self.getValuesDBRef(token_data)
        if token_data == None:
            token_data = {}
        else:
            token_data["_id"] = token_data["_id"].__str__()
        return token_data
    
    def delete_by_token(self, token):
        laColeccion = db[self.coleccion]
        cuenta = laColeccion.delete_one({"token":token}).deleted_count
        return {"deleted_count": cuenta}