from flask import abort, request
from models.site_model import Site
from bson.objectid import ObjectId
from repositories.abstract_repository import AbstractRepository
from main import db


class SiteRepository(AbstractRepository[Site]):
    pass
