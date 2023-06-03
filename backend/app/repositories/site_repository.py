from flask import abort, request
from app.models.site_model import Site
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class SiteRepository(AbstractRepository[Site]):
    pass
