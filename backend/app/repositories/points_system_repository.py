from flask import abort, request
from app.models.points_system_model import PointsSystem
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class PointsSystemRepository(AbstractRepository[PointsSystem]):
    def __init__(self):
        super().__init__()

