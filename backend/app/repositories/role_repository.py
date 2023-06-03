from flask import abort, request
from app.models.role_model import Role
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class RoleRepository(AbstractRepository[Role]):
    pass
