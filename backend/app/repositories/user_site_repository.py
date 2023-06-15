from flask import abort, request
from app.models.user_site_model import UserSite
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository




class UserSiteRepository(AbstractRepository[UserSite]):
    pass

