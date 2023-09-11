import math
from app.models.site_model import Site
from bson.objectid import ObjectId
from app.repositories.abstract_repository import AbstractRepository


class SiteRepository(AbstractRepository[Site]):
    def __init__(self):
        super().__init__()

    def getNotReferenced(self, referenceds_id, page=None, limit=None):
        laColeccion = self.db[self.coleccion]
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        total_documents = laColeccion.count_documents(
            {'_id': {'$nin': object_ids}})
        total_pages = None
        data = []
        if page is not None and limit is not None:
            skip = (page - 1) * limit
            cursor = laColeccion.find(
                {'_id': {'$nin': object_ids}}).skip(skip).limit(limit)
            total_pages = int(math.ceil(total_documents / limit))
        else:
            cursor = laColeccion.find({'_id': {'$nin': object_ids}})
        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)

            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        if total_pages != None:
            return {"data": data, "totalPages": total_pages}
        else:
            return data

    def getReferenced(self, referenceds_id, page=None, limit=None):
        laColeccion = self.db[self.coleccion]
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        total_documents = laColeccion.count_documents(
            {'_id': {'$in': object_ids}})
        total_pages = None
        result = []
        if page is not None and limit is not None:
            skip = (page - 1) * limit
            cursor = laColeccion.find({'_id': {'$in': object_ids}}
                             ).skip(skip).limit(limit)
            total_pages = int(math.ceil(total_documents / limit))
        else:
            cursor = laColeccion.find({'_id': {'$in': object_ids}})

        for x in cursor:
            x['_id'] = x['_id'].__str__()
            x = self.replaceDBRefsWithObjects(x)
            result.append(x)
        if total_pages != None:
            return {"data": result, "totalPages": total_pages}
        else:
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

    def queryRefereced(self, referenceds_id, theQuery):
        object_ids = [ObjectId(oid) for oid in referenceds_id]
        search = {
            '$and': [
                {'_id': {'$in': object_ids}},
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

    def queryTopSixLogged(self, referenced_ids):
        laColeccion = self.db[self.coleccion]
        object_ids = [ObjectId(oid) for oid in referenced_ids]
        query = {"_id": {"$nin": object_ids}}
        cursor = laColeccion.find(query).limit(6)
        data = []
        for x in cursor:
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)

            x = self.replaceDBRefsWithObjects(x)
            data.append(x)
        return data
