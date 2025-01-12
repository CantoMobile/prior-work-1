from bson import ObjectId
from flask import abort, request
from app.models.user_model import User
from app.repositories.abstract_repository import AbstractRepository


class UserRepository(AbstractRepository[User]):
    def __init__(self):
        super().__init__()

    def find_by_email(self, email):
        laColeccion = self.db[self.coleccion]
        user_data = laColeccion.find_one({'email': email})
        user_data = self.replaceDBRefsWithObjects(user_data)
        if user_data is None:
            user_data = {}
        else:
            user_data["_id"] = user_data["_id"].__str__()
        return user_data

    def verify_permissions(self, email_user, resource, method):
        laColeccion = self.db[self.coleccion]
        pipeline = [
            {
                '$match': {'email': email_user}
            },
            {
                '$lookup': {
                    'from': "role",
                    'localField': "roles._id",
                    'foreignField': "_id",
                    'as': "roles"
                }
            },
            {
                '$unwind': "$roles"
            },
            {
                '$lookup': {
                    'from': "permissions",
                    'localField': "roles.permissions._id",
                    'foreignField': "_id",
                    'as': "permissions"
                }
            },
            {
                '$match': {
                    "permissions.resource": resource,
                    "permissions.actions": method
                }
            }, {
                "$limit": 1
            }
        ]
        result = laColeccion.aggregate(pipeline)
        return bool(next(result, False))