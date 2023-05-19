from flask import current_app
from models.role_model import Role
from models.user_model import User


class Authorization:
    def __init__(self, user_id, role_id, permission_id):
        self.user_id = user_id
        self.role_id = role_id
        self.permission_id = permission_id

    def save(self):
        with current_app.app_context():
            collection = current_app.mongo.db.authorizations
        result = collection.insert_one({
            'user_id': self.user_id,
            'role_id': self.role_id,
            'permission_id': self.permission_id
        })
        return result.inserted_id

    @staticmethod
    def check_permission(user, permission):
        with current_app.app_context():
            collection = current_app.mongo.db.authorizations
        authorization = collection.find_one({
            'user_id': user,
            'permission_id': permission
        })
        return authorization is not None

    @staticmethod
    def grant_permission(user, permission):
        new_authorization = Authorization(user, None, permission)
        new_authorization.save()

    @staticmethod
    def revoke_permission(user, permission):
        with current_app.app_context():
            collection = current_app.mongo.db.authorizations
        collection.delete_one({
            'user_id': user,
            'permission_id': permission
        })
