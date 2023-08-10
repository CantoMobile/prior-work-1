from flask import abort, request
from app.models.user_site_model import UserSite
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class UserSiteRepository(AbstractRepository[UserSite]):
    def __init__(self):
        super().__init__()

    def deleteAllSitesReferenceds(self, site_id):
        laColeccion = self.db[self.coleccion]
        query = {'site._id': ObjectId(site_id)}
        update_query = {'$pull': {'site': {'_id': ObjectId(site_id)}}}
        result = laColeccion.update_many(query, update_query)
        print(result)
        print(result.modified_count)
        if result.modified_count > 0:
            return True
        else:
            return False
