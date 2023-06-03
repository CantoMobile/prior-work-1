from flask import abort, request
from app.models.search_result_model import SearchResult
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class SearchResultRepository(AbstractRepository[SearchResult]):
    pass
