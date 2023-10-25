from flask import abort, request
from app.models.user_action_model import UserAction
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class UserActionRepository(AbstractRepository[UserAction]):
    def __init__(self):
        super().__init__()

    # def deleteAllUserReferences(self, user_id):
    #     laColeccion = self.db[self.coleccion]
    #     query = {'user._id': ObjectId(user_id)}
    #     update_query = {'$pull': {'user': {'_id': ObjectId(user_id)}}}
    #     result = laColeccion.update_many(query, update_query)
    #     print(result)
    #     print(result.modified_count)
    #     if result.modified_count > 0:
    #         return True
    #     else:
    #         return False
