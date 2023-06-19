from flask import abort, request
from app.models.reviews_model import Review
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class ReviewsRepository(AbstractRepository[Review]):
    pass
    
