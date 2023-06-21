from flask import abort, jsonify, request
from app.models.site_model import Site
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class SiteRepository(AbstractRepository[Site]):
    def __init__(self):
        super().__init__()

    def getNotReferenced(self, referenceds_id):
        laColeccion = self.db[self.coleccion]
        print(referenceds_id)
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        cursor = laColeccion.find({'_id': {'$nin': object_ids}})
        data = []
        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)

            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        return data

    def getReferenced(self, referenceds_id):
        laColeccion = self.db[self.coleccion]
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        cursor = laColeccion.find({'_id': {'$in': object_ids}})

        result = []
        for x in cursor:
            x['_id'] = x['_id'].__str__()
            x = self.replaceDBRefsWithObjects(x)
            result.append(x)

        return result

    def queryNotRefereced(self, referenceds_id, theQuery):
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        search = {
            '$and': [
                {'_id': {'$nin': object_ids}},
                {
                    '$or': [
                        {'url': {'$regex': theQuery, '$options': 'i'}},
                        {'name': {'$regex': theQuery, '$options': 'i'}},
                        {'description': {'$regex': theQuery, '$options': 'i'}},
                        {'keywords': {'$regex': theQuery, '$options': 'i'}}
                    ]
                }
            ]
        }
        return search